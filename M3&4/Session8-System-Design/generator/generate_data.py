import os
import sys
import argparse
import json
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from datetime import datetime, timedelta

# Load sensor limits from json
script_dir = os.path.dirname(os.path.abspath(__file__))
limits_path = os.path.join(script_dir, "sensor_limits.json")
try:
    with open(limits_path, "r", encoding="utf-8") as f:
        SENSOR_LIMITS = json.load(f)
except Exception as e:
    print(f"Warning: Could not load sensor_limits.json: {e}")
    SENSOR_LIMITS = {}

# Helper to construct fields with metadata
def make_field(name, pa_type, description, brief=None, unit=None, limits=None):
    meta = {b'description': description.encode('utf-8')}
    if brief:
        meta[b'brief'] = brief.encode('utf-8')
    if unit:
        meta[b'unit'] = unit.encode('utf-8')
    if limits:
        meta[b'limits_normal'] = str(limits.get('normal', [])).encode('utf-8')
        meta[b'limits_warning'] = str(limits.get('warning', [])).encode('utf-8')
        meta[b'limits_critical'] = str(limits.get('critical', [])).encode('utf-8')
    return pa.field(name, pa_type, metadata=meta)

# Helper to extract limits and construct station telemetry fields
def get_sensor_field(station_id, sensor_name, pa_type=pa.float64()):
    station_data = SENSOR_LIMITS.get(station_id, {})
    sensor_data = station_data.get('sensors', {}).get(sensor_name, {})
    return make_field(
        name=sensor_name,
        pa_type=pa_type,
        description=sensor_data.get('description', f"Sensor {sensor_name}"),
        brief=sensor_data.get('brief'),
        unit=sensor_data.get('unit'),
        limits=sensor_data.get('limits')
    )

# Define schemas for all tables with metadata
production_log_schema = pa.schema([
    make_field('part_id', pa.string(), "Unique part tracking identifier"),
    make_field('start_time', pa.timestamp('ns'), "Timestamp when the part was initialized at Station 1"),
    make_field('end_time', pa.timestamp('ns'), "Timestamp when the part exited the production line (pass or scrap)"),
    make_field('final_status', pa.string(), "Final status of the steering wheel: Pass or Scrap"),
    make_field('scrap_reason', pa.string(), "Defect description if the part was scrapped; empty otherwise"),
    make_field('material_batch_id', pa.string(), "Links part to raw material supplier batches"),
], metadata={b'table_description': b'High-level log tracking the production lifecycle and final status of each steering wheel.'})

casting_telemetry_schema = pa.schema([
    make_field('part_id', pa.string(), "Unique part tracking identifier"),
    make_field('machine_id', pa.string(), "Casting machine identifier"),
    get_sensor_field('ST-100', 'clamp_force'),
    get_sensor_field('ST-100', 'melt_temp'),
    get_sensor_field('ST-100', 'injection_pressure'),
    get_sensor_field('ST-100', 'die_temp'),
    get_sensor_field('ST-100', 'vacuum_level'),
    make_field('cooling_time', pa.float64(), "Cooling duration inside the mold", "seconds"),
    make_field('cycle_time', pa.float64(), "Total machine cycle duration", "seconds"),
], metadata={b'table_description': b'Process telemetry parameters collected during Magnesium skeleton die-casting.'})

foaming_telemetry_schema = pa.schema([
    make_field('part_id', pa.string(), "Unique part tracking identifier"),
    make_field('machine_id', pa.string(), "Foaming machine identifier"),
    get_sensor_field('ST-200', 'mold_temp'),
    get_sensor_field('ST-200', 'polyol_temp'),
    get_sensor_field('ST-200', 'iso_temp'),
    get_sensor_field('ST-200', 'polyol_flow_rate'),
    get_sensor_field('ST-200', 'iso_flow_rate'),
    get_sensor_field('ST-200', 'mixing_ratio'),
    get_sensor_field('ST-200', 'injection_pressure'),
    make_field('demold_time', pa.float64(), "Duration before part demolding", "seconds"),
], metadata={b'table_description': b'Process parameters and flow rates monitored during Polyurethane cushion foaming.'})

conductor_telemetry_schema = pa.schema([
    make_field('part_id', pa.string(), "Unique part tracking identifier"),
    make_field('machine_id', pa.string(), "Conductor winding machine identifier"),
    get_sensor_field('ST-300', 'winding_tension'),
    get_sensor_field('ST-300', 'pressing_force'),
    get_sensor_field('ST-300', 'crimp_force'),
], metadata={b'table_description': b'Process telemetry parameters for heater winding and sensor press-embedding.'})

laser_telemetry_schema = pa.schema([
    make_field('part_id', pa.string(), "Unique part tracking identifier"),
    make_field('machine_id', pa.string(), "Laser texturing machine identifier"),
    get_sensor_field('ST-400', 'laser_power'),
    get_sensor_field('ST-400', 'laser_scan_speed'),
    get_sensor_field('ST-400', 'pulse_freq'),
    get_sensor_field('ST-400', 'robot_offset'),
    get_sensor_field('ST-400', 'focal_distance'),
], metadata={b'table_description': b'Process parameters collected during robotic laser surface activation and texturing.'})

finishing_telemetry_schema = pa.schema([
    make_field('part_id', pa.string(), "Unique part tracking identifier"),
    make_field('machine_id', pa.string(), "Final assembly station identifier"),
    get_sensor_field('ST-500', 'wrapping_tension'),
    get_sensor_field('ST-500', 'glue_weight'),
    get_sensor_field('ST-500', 'glue_temp'),
    get_sensor_field('ST-500', 'screw_torque'),
], metadata={b'table_description': b'Assembly parameters logged during leather wrapping, stitching, and switch screw tightening.'})

quality_inspections_schema = pa.schema([
    make_field('part_id', pa.string(), "Unique part tracking identifier"),
    make_field('station_id', pa.string(), "Identifier of the station performing the inspection check"),
    make_field('gate_id', pa.string(), "Identifier of the quality checkpoint gate (QC-100 to QC-500)"),
    make_field('timestamp', pa.timestamp('ns'), "Time when inspection occurred"),
    make_field('parameter_name', pa.string(), "Name of the quality parameter checked"),
    make_field('measured_value', pa.float64(), "Numeric value measured by quality equipment"),
    make_field('lsl', pa.float64(), "Lower Specification Limit"),
    make_field('usl', pa.float64(), "Upper Specification Limit"),
    make_field('result', pa.string(), "Outcome of check: PASS or FAIL"),
], metadata={b'table_description': b'Log of structured quality control checks and specification tolerances across all inspection gates.'})

material_batches_schema = pa.schema([
    make_field('material_batch_id', pa.string(), "Unique raw material batch ID"),
    make_field('supplier_name', pa.string(), "Raw material supplier"),
    make_field('raw_magnesium_purity', pa.float64(), "Chemical purity percentage of magnesium alloy", "%"),
    make_field('polyol_batch_no', pa.string(), "Batch identifier for Polyol chemicals"),
    make_field('iso_batch_no', pa.string(), "Batch identifier for Isocyanate chemicals"),
    make_field('leather_grade', pa.string(), "Supplier grade classification for wrapping leather"),
], metadata={b'table_description': b'Lookup table tracing material batch numbers to chemical purities, grades, and supplier names.'})

operator_logs_schema = pa.schema([
    make_field('part_id', pa.string(), "Unique part tracking identifier"),
    make_field('station_id', pa.string(), "Station where note was logged"),
    make_field('operator_id', pa.string(), "Technician operator identifier"),
    make_field('timestamp', pa.timestamp('ns'), "Logging timestamp"),
    make_field('operator_notes', pa.string(), "Free-text observations, notes, or warning comments from the operator"),
], metadata={b'table_description': b'Unstructured technician and operator logs containing process notes, errors, and shift comments.'})

def generate_static_material_batches(output_dir):
    print("Generating material_batches.parquet...")
    batches = []
    suppliers = ["AluMag Corp", "Magnesium Alloys Ltd", "Global Light Metals"]
    leather_grades = ["Premium Nappa", "Standard Dakota", "Synthetic Alcantara"]
    
    # 20 batches
    for i in range(1, 21):
        batch_id = f"MB-2026-B{i}"
        
        # Anomaly 1: Batch 3 is low purity from AluMag Corp
        if i == 3:
            supplier = "AluMag Corp"
            purity = 92.5
        else:
            supplier = np.random.choice(suppliers)
            purity = float(np.random.normal(98.5, 0.3))
            
        batches.append({
            'material_batch_id': batch_id,
            'supplier_name': supplier,
            'raw_magnesium_purity': purity,
            'polyol_batch_no': f"POL-{1000 + i}",
            'iso_batch_no': f"ISO-{2000 + i}",
            'leather_grade': np.random.choice(leather_grades)
        })
        
    df = pd.DataFrame(batches)
    table = pa.Table.from_pandas(df, schema=material_batches_schema)
    pq.write_table(table, os.path.join(output_dir, "material_batches.parquet"))

def generate_data(num_wheels, output_dir, chunk_size=50000):
    print(f"Starting data generation for {num_wheels} unique steering wheels in chunks of {chunk_size}...")
    
    # Initialize Parquet writers
    writers = {
        'production_log': pq.ParquetWriter(os.path.join(output_dir, "production_log.parquet"), production_log_schema),
        'casting_telemetry': pq.ParquetWriter(os.path.join(output_dir, "casting_telemetry.parquet"), casting_telemetry_schema),
        'foaming_telemetry': pq.ParquetWriter(os.path.join(output_dir, "foaming_telemetry.parquet"), foaming_telemetry_schema),
        'conductor_telemetry': pq.ParquetWriter(os.path.join(output_dir, "conductor_telemetry.parquet"), conductor_telemetry_schema),
        'laser_telemetry': pq.ParquetWriter(os.path.join(output_dir, "laser_telemetry.parquet"), laser_telemetry_schema),
        'finishing_telemetry': pq.ParquetWriter(os.path.join(output_dir, "finishing_telemetry.parquet"), finishing_telemetry_schema),
        'quality_inspections': pq.ParquetWriter(os.path.join(output_dir, "quality_inspections.parquet"), quality_inspections_schema),
        'operator_logs': pq.ParquetWriter(os.path.join(output_dir, "operator_logs.parquet"), operator_logs_schema)
    }

    # Setup config
    base_date = datetime(2026, 7, 1, 6, 0, 0)
    
    # Pre-define arrays for performance
    operators = {
        'ST-100': [f"OP-C{i:02d}" for i in range(1, 6)],
        'ST-200': [f"OP-F{i:02d}" for i in range(1, 6)],
        'ST-300': [f"OP-E{i:02d}" for i in range(1, 6)],
        'ST-400': [f"OP-L{i:02d}" for i in range(1, 4)],
        'ST-500': [f"OP-A{i:02d}" for i in range(1, 8)] + ["OP-098"]  # OP-098 is the fatigued operator
    }
    
    machines = {
        'ST-100': ["CAST-01", "CAST-02", "CAST-03"],
        'ST-200': ["FOAM-01", "FOAM-02", "FOAM-03", "FOAM-04"], # FOAM-04 drifts
        'ST-300': ["COND-01", "COND-02"],
        'ST-400': ["LASR-01", "LASR-02"],  # LASR-02 sometimes overpowers
        'ST-500': ["FIN-01", "FIN-02", "FIN-03"] # FIN-03 has cold glue temp
    }
    
    total_chunks = (num_wheels + chunk_size - 1) // chunk_size
    parts_generated = 0
    
    # Use deterministic seeds for reproducibility but allow randomness
    np.random.seed(42)
    
    for chunk_idx in range(total_chunks):
        current_chunk_size = min(chunk_size, num_wheels - parts_generated)
        print(f"Generating chunk {chunk_idx + 1}/{total_chunks} ({current_chunk_size} parts)...")
        
        # Buffer containers for this chunk
        buf = {k: [] for k in writers.keys()}
        
        for idx in range(current_chunk_size):
            part_num = parts_generated + idx + 1
            part_id = f"SW-202607-{part_num:07d}"
            
            # Base timestamp for this wheel's production cycle
            day_offset = part_num / 50000.0
            t_base = base_date + timedelta(days=day_offset)
            
            # Choose batch
            if np.random.random() < 0.05:
                batch_id = "MB-2026-B3"
            else:
                batch_id = f"MB-2026-B{np.random.randint(1, 21)}"
                if batch_id == "MB-2026-B3":
                    batch_id = "MB-2026-B1"  # redirect normal parts away from bad batch
                    
            # ----------------------------------------------------
            # STATION 1: Magnesium Skeleton Casting (ST-100)
            # ----------------------------------------------------
            t1_start = t_base + timedelta(seconds=float(np.random.uniform(0, 10)))
            t1_end = t1_start + timedelta(seconds=float(np.random.normal(40, 2)))
            op_1 = np.random.choice(operators['ST-100'])
            m_1 = np.random.choice(machines['ST-100'])
            
            # Base casting parameters
            melt_t = float(np.random.normal(660.0, 5.0))
            clamp_f = float(np.random.normal(600.0, 5.0))
            inj_p = float(np.random.normal(710.0, 10.0))
            die_t = float(np.random.normal(215.0, 4.0))
            vac_l = float(np.random.normal(40.0, 3.0))
            cool_t = float(np.random.normal(10.0, 0.5))
            cycle_t1 = (t1_end - t1_start).total_seconds()
            
            # QC check parameters
            porosity = float(np.random.exponential(0.3))
            weight_cast = float(np.random.normal(1000.0, 12.0))
            
            # Anomaly 1: Batch 3 is low purity, causing high porosity
            is_anomaly_1 = False
            if batch_id == "MB-2026-B3":
                if np.random.random() < 0.15: # 15% probability
                    porosity = float(np.random.uniform(2.1, 4.8))
                    is_anomaly_1 = True
            
            # Let's assess QC-100
            failed_qc100 = False
            qc100_results = []
            
            # Porosity check USL=2.0
            p_res = "PASS"
            if porosity > 2.0:
                p_res = "FAIL"
                failed_qc100 = True
            qc100_results.append(('porosity_pct', porosity, 0.0, 2.0, p_res))
            
            # Casting Weight LSL=950, USL=1050
            w_res = "PASS"
            if weight_cast < 950.0 or weight_cast > 1050.0:
                w_res = "FAIL"
                failed_qc100 = True
            qc100_results.append(('casting_weight', weight_cast, 950.0, 1050.0, w_res))
            
            # Append telemetry
            buf['casting_telemetry'].append({
                'part_id': part_id, 'machine_id': m_1, 'clamp_force': clamp_f,
                'melt_temp': melt_t, 'injection_pressure': inj_p, 'die_temp': die_t,
                'vacuum_level': vac_l, 'cooling_time': cool_t, 'cycle_time': cycle_t1
            })
            
            # Append QC checks
            for p_name, val, lsl, usl, res in qc100_results:
                buf['quality_inspections'].append({
                    'part_id': part_id, 'station_id': 'ST-100', 'gate_id': 'QC-100',
                    'timestamp': t1_end, 'parameter_name': p_name, 'measured_value': val,
                    'lsl': lsl, 'usl': usl, 'result': res
                })
                
            # Append Operator logs
            op1_note = ""
            if is_anomaly_1:
                op1_note = "X-ray detected structural voids. Possible raw material impurity issue."
            elif failed_qc100:
                op1_note = "Part weight out of range, surface defects visible."
                
            buf['operator_logs'].append({
                'part_id': part_id, 'station_id': 'ST-100', 'operator_id': op_1,
                'timestamp': t1_end, 'operator_notes': op1_note
            })
            
            if failed_qc100:
                # Part is scrapped at Station 1. Do not proceed.
                buf['production_log'].append({
                    'part_id': part_id, 'start_time': t1_start, 'end_time': t1_end,
                    'final_status': 'Scrap', 'scrap_reason': 'Casting Porosity' if porosity > 2.0 else 'Casting Weight OOS',
                    'material_batch_id': batch_id
                })
                continue
                
            # ----------------------------------------------------
            # STATION 2: Polyurethane Foaming (ST-200)
            # ----------------------------------------------------
            t2_start = t1_end + timedelta(minutes=float(np.random.uniform(2, 5)))
            t2_end = t2_start + timedelta(seconds=float(np.random.normal(120, 5)))
            op_2 = np.random.choice(operators['ST-200'])
            m_2 = np.random.choice(machines['ST-200'])
            
            # Base foaming parameters
            mold_t = float(np.random.normal(50.0, 1.5))
            poly_t = float(np.random.normal(23.5, 0.5))
            iso_t = float(np.random.normal(23.5, 0.5))
            poly_flow = float(np.random.normal(100.0, 1.0))
            
            # Anomaly 2: FOAM-04 drifts between Day 10 and Day 15
            is_anomaly_2 = False
            is_drift_time = (10 <= day_offset <= 15)
            
            if m_2 == "FOAM-04" and is_drift_time:
                drift_factor = (day_offset - 10) / 5.0
                iso_flow = float(np.random.normal(106.0 - (10.0 * drift_factor), 1.0))
                is_anomaly_2 = True
            else:
                iso_flow = float(np.random.normal(106.0, 1.0))
                
            mixing_ratio = (iso_flow / poly_flow) * 100.0
            inj_p2 = float(np.random.normal(150.0, 4.0))
            demold = (t2_end - t2_start).total_seconds()
            
            # QC check parameters
            hardness = float(np.random.normal(50.0, 3.0))
            weight_foam = float(np.random.normal(325.0, 8.0))
            
            if is_anomaly_2 and mixing_ratio < 104.0:
                if np.random.random() < 0.75:
                    hardness = float(np.random.uniform(30.0, 39.0))
                    
            # Assess QC-200
            failed_qc200 = False
            qc200_results = []
            
            # Hardness check LSL=40, USL=60
            h_res = "PASS"
            if hardness < 40.0 or hardness > 60.0:
                h_res = "FAIL"
                failed_qc200 = True
            qc200_results.append(('foam_hardness_shore_a', hardness, 40.0, 60.0, h_res))
            
            # Foam Weight LSL=300, USL=350
            f_res = "PASS"
            if weight_foam < 300.0 or weight_foam > 350.0:
                f_res = "FAIL"
                failed_qc200 = True
            qc200_results.append(('foam_weight', weight_foam, 300.0, 350.0, f_res))
            
            # Append telemetry
            buf['foaming_telemetry'].append({
                'part_id': part_id, 'machine_id': m_2, 'polyol_temp': poly_t,
                'iso_temp': iso_t, 'polyol_flow_rate': poly_flow, 'iso_flow_rate': iso_flow,
                'mixing_ratio': mixing_ratio, 'injection_pressure': inj_p2, 'mold_temp': mold_t,
                'demold_time': demold
            })
            
            # Append QC
            for p_name, val, lsl, usl, res in qc200_results:
                buf['quality_inspections'].append({
                    'part_id': part_id, 'station_id': 'ST-200', 'gate_id': 'QC-200',
                    'timestamp': t2_end, 'parameter_name': p_name, 'measured_value': val,
                    'lsl': lsl, 'usl': usl, 'result': res
                })
                
            # Append Operator logs
            op2_note = ""
            if is_anomaly_2 and failed_qc200:
                op2_note = f"Foam tactile check failed. Material feels soft. Mixing ratio registered low: {mixing_ratio:.2f}."
            elif failed_qc200:
                op2_note = "Short fill or bubbling on skin."
                
            buf['operator_logs'].append({
                'part_id': part_id, 'station_id': 'ST-200', 'operator_id': op_2,
                'timestamp': t2_end, 'operator_notes': op2_note
            })
            
            if failed_qc200:
                # Part is scrapped at Station 2. Do not proceed.
                buf['production_log'].append({
                    'part_id': part_id, 'start_time': t1_start, 'end_time': t2_end,
                    'final_status': 'Scrap', 'scrap_reason': 'Soft Foam' if hardness < 40.0 else 'Foam Weight OOS',
                    'material_batch_id': batch_id
                })
                continue
                
            # ----------------------------------------------------
            # STATION 3: Conductor Insertion (ST-300)
            # ----------------------------------------------------
            t3_start = t2_end + timedelta(minutes=float(np.random.uniform(5, 10)))
            t3_end = t3_start + timedelta(seconds=float(np.random.normal(85, 3)))
            op_3 = np.random.choice(operators['ST-300'])
            m_3 = np.random.choice(machines['ST-300'])
            
            # Telemetry
            wind_t = float(np.random.normal(14.0, 0.8))
            press_f = float(np.random.normal(90.0, 3.0))
            crimp_f = float(np.random.normal(1.35, 0.05))
            
            # QC Check Parameters
            heater_res = float(np.random.normal(2.3, 0.05))
            therm_res = float(np.random.normal(10.0, 0.2))
            
            # Anomaly 4 (Supplier Thermistor Issue)
            is_anomaly_tc_batch = False
            if np.random.random() < 0.01:
                is_anomaly_tc_batch = True
                therm_res = float(np.random.normal(14.0, 0.5))
                
            # Assess QC-300
            failed_qc300 = False
            qc300_results = []
            
            # Heater resistance check LSL=2.1, USL=2.5
            hr_res = "PASS"
            if heater_res < 2.1 or heater_res > 2.5:
                hr_res = "FAIL"
                failed_qc300 = True
            qc300_results.append(('heater_resistance_ohms', heater_res, 2.1, 2.5, hr_res))
            
            # Thermistor LSL=9.5, USL=10.5
            tc_res = "PASS"
            if therm_res < 9.5 or therm_res > 10.5:
                tc_res = "FAIL"
                failed_qc300 = True
            qc300_results.append(('thermistor_resistance_kohm', therm_res, 9.5, 10.5, tc_res))
            
            # Append Telemetry
            buf['conductor_telemetry'].append({
                'part_id': part_id, 'machine_id': m_3, 'winding_tension': wind_t,
                'pressing_force': press_f, 'crimp_force': crimp_f
            })
            
            # Append QC
            for p_name, val, lsl, usl, res in qc300_results:
                buf['quality_inspections'].append({
                    'part_id': part_id, 'station_id': 'ST-300', 'gate_id': 'QC-300',
                    'timestamp': t3_end, 'parameter_name': p_name, 'measured_value': val,
                    'lsl': lsl, 'usl': usl, 'result': res
                })
                
            # Append Operator logs
            op3_note = ""
            if is_anomaly_tc_batch:
                op3_note = f"Thermistor resistance measured high ({therm_res:.2f} kOhm). Bad component lot TC-BATCH-99 suspected."
            elif failed_qc300:
                op3_note = "Electrical check failed. Retested and rejected."
                
            buf['operator_logs'].append({
                'part_id': part_id, 'station_id': 'ST-300', 'operator_id': op_3,
                'timestamp': t3_end, 'operator_notes': op3_note
            })
            
            if failed_qc300:
                buf['production_log'].append({
                    'part_id': part_id, 'start_time': t1_start, 'end_time': t3_end,
                    'final_status': 'Scrap', 'scrap_reason': 'Electrical resistance OOS' if heater_res > 2.5 else 'Thermistor OOS',
                    'material_batch_id': batch_id
                })
                continue
                
            # ----------------------------------------------------
            # STATION 4: Laser Surface Texturing (ST-400)
            # ----------------------------------------------------
            t4_start = t3_end + timedelta(minutes=float(np.random.uniform(3, 8)))
            t4_end = t4_start + timedelta(seconds=float(np.random.normal(50, 2)))
            op_4 = np.random.choice(operators['ST-400'])
            m_4 = np.random.choice(machines['ST-400'])
            
            # Telemetry
            laser_p = float(np.random.normal(100.0, 5.0))
            scan_s = float(np.random.normal(900.0, 20.0))
            pulse_f = float(np.random.normal(40.0, 2.0))
            robot_off = float(np.random.exponential(0.04))
            focal_d = float(np.random.normal(150.0, 0.5))
            
            # Anomaly 3 (Laser over-power on LASR-02)
            is_anomaly_3 = False
            is_laser_fault_day = (5 <= day_offset <= 6)
            if m_4 == "LASR-02" and is_laser_fault_day:
                if np.random.random() < 0.35:
                    laser_p = float(np.random.normal(126.0, 2.0))
                    robot_off = float(np.random.normal(0.24, 0.02))
                    is_anomaly_3 = True
                    
            # QC Check Parameters
            depth = float(np.random.normal(100.0, 6.0))
            roughness = float(np.random.normal(8.0, 0.6))
            
            if is_anomaly_3:
                depth = float(np.random.normal(124.0, 5.0))
                roughness = float(np.random.normal(10.8, 0.5))
                
            # Assess QC-400
            failed_qc400 = False
            qc400_results = []
            
            # Depth check LSL=80, USL=120
            d_res = "PASS"
            if depth < 80.0 or depth > 120.0:
                d_res = "FAIL"
                failed_qc400 = True
            qc400_results.append(('texture_depth_microns', depth, 80.0, 120.0, d_res))
            
            # Roughness LSL=6.0, USL=10.0
            r_res = "PASS"
            if roughness < 6.0 or roughness > 10.0:
                r_res = "FAIL"
                failed_qc400 = True
            qc400_results.append(('surface_roughness_ra', roughness, 6.0, 10.0, r_res))
            
            # Append Telemetry
            buf['laser_telemetry'].append({
                'part_id': part_id, 'machine_id': m_4, 'laser_power': laser_p,
                'laser_scan_speed': scan_s, 'pulse_freq': pulse_f, 'robot_offset': robot_off,
                'focal_distance': focal_d
            })
            
            # Append QC
            for p_name, val, lsl, usl, res in qc400_results:
                buf['quality_inspections'].append({
                    'part_id': part_id, 'station_id': 'ST-400', 'gate_id': 'QC-400',
                    'timestamp': t4_end, 'parameter_name': p_name, 'measured_value': val,
                    'lsl': lsl, 'usl': usl, 'result': res
                })
                
            # Append Operator logs
            op4_note = ""
            if is_anomaly_3:
                op4_note = f"Laser scanning completed. Noticed slight scorching on foam surface. Laser power: {laser_p:.1f}W, Offset: {robot_off:.3f}mm."
            elif failed_qc400:
                op4_note = "Laser depth check out of specification."
                
            buf['operator_logs'].append({
                'part_id': part_id, 'station_id': 'ST-400', 'operator_id': op_4,
                'timestamp': t4_end, 'operator_notes': op4_note
            })
            
            is_wire_damaged_by_laser = False
            if is_anomaly_3 and not failed_qc400:
                if np.random.random() < 0.90:
                    is_wire_damaged_by_laser = True
                    
            if failed_qc400:
                buf['production_log'].append({
                    'part_id': part_id, 'start_time': t1_start, 'end_time': t4_end,
                    'final_status': 'Scrap', 'scrap_reason': 'Laser Depth OOS' if depth > 120.0 else 'Laser Roughness OOS',
                    'material_batch_id': batch_id
                })
                continue
                
            # ----------------------------------------------------
            # STATION 5: Leather Wrapping & Final Assembly (ST-500)
            # ----------------------------------------------------
            t5_start = t4_end + timedelta(minutes=float(np.random.uniform(10, 20)))
            t5_end = t5_start + timedelta(seconds=float(np.random.normal(300, 15)))
            op_5 = np.random.choice(operators['ST-500'])
            m_5 = np.random.choice(machines['ST-500'])
            
            # Telemetry
            wrap_t = float(np.random.normal(22.5, 1.2))
            glue_w = float(np.random.normal(20.0, 1.5))
            
            # Anomaly 5: Cold glue on FIN-03
            is_anomaly_5 = False
            if m_5 == "FIN-03" and np.random.random() < 0.04:
                glue_t = float(np.random.normal(105.0, 2.0))
                is_anomaly_5 = True
            else:
                glue_t = float(np.random.normal(130.0, 3.0))
                
            screw_t = float(np.random.normal(2.6, 0.1))
            
            # Anomaly 4: OP-098 night shift fatigue
            is_night_fatigue = (t5_end.hour in [3, 4, 5])
            is_anomaly_4 = False
            if op_5 == "OP-098" and is_night_fatigue:
                wrap_t = float(np.random.normal(34.0, 2.5))
                is_anomaly_4 = True
                
            # QC Check Parameters
            final_heater_res = heater_res
            airbag_res = float(np.random.normal(2.0, 0.08))
            switch_res = float(np.random.normal(0.25, 0.05))
            peel_force = float(np.random.normal(22.0, 2.0))
            
            # Apply wire break logic
            is_wire_broken = False
            if is_wire_damaged_by_laser:
                final_heater_res = 999.9
                is_wire_broken = True
            elif is_anomaly_4:
                if np.random.random() < 0.85:
                    final_heater_res = 999.9
                    is_wire_broken = True
                    
            # Apply cold glue adhesion failure
            if is_anomaly_5:
                peel_force = float(np.random.normal(9.5, 1.5))
                
            # Assess QC-500
            failed_qc500 = False
            qc500_results = []
            
            # Final Heater resistance check LSL=2.1, USL=2.5
            fhr_res = "PASS"
            if final_heater_res < 2.1 or final_heater_res > 2.5:
                fhr_res = "FAIL"
                failed_qc500 = True
            qc500_results.append(('final_heater_resistance_ohms', final_heater_res, 2.1, 2.5, fhr_res))
            
            # Airbag LSL=1.8, USL=2.2
            ab_res = "PASS"
            if airbag_res < 1.8 or airbag_res > 2.2:
                ab_res = "FAIL"
                failed_qc500 = True
            qc500_results.append(('airbag_resistance_ohms', airbag_res, 1.8, 2.2, ab_res))
            
            # Switch LSL=0.0, USL=0.5
            sw_res = "PASS"
            if switch_res < 0.0 or switch_res > 0.5:
                sw_res = "FAIL"
                failed_qc500 = True
            qc500_results.append(('switch_continuity_resistance_ohms', switch_res, 0.0, 0.5, sw_res))
            
            # Adhesion LSL=15.0
            pf_res = "PASS"
            if peel_force < 15.0:
                pf_res = "FAIL"
                failed_qc500 = True
            qc500_results.append(('adhesion_peel_force_n', peel_force, 15.0, 30.0, pf_res))
            
            # Append Telemetry
            buf['finishing_telemetry'].append({
                'part_id': part_id, 'machine_id': m_5, 'wrapping_tension': wrap_t,
                'glue_weight': glue_w, 'glue_temp': glue_t, 'screw_torque': screw_t
            })
            
            # Append QC
            for p_name, val, lsl, usl, res in qc500_results:
                buf['quality_inspections'].append({
                    'part_id': part_id, 'station_id': 'ST-500', 'gate_id': 'QC-500',
                    'timestamp': t5_end, 'parameter_name': p_name, 'measured_value': val,
                    'lsl': lsl, 'usl': usl, 'result': res
                })
                
            # Append Operator logs
            op5_note = ""
            if is_anomaly_4:
                op5_note = f"Stitching leather. Leather required heavy pulling to close seams. Wrapping tension measured: {wrap_t:.1f}N."
            elif is_anomaly_5:
                op5_note = "Adhesive dispensing nozzle temp feels cold. Adhesion bonding seems weak."
            elif is_wire_broken and is_wire_damaged_by_laser:
                op5_note = "Standard assembly and stitching. Electrical test failed with open circuit."
                
            buf['operator_logs'].append({
                'part_id': part_id, 'station_id': 'ST-500', 'operator_id': op_5,
                'timestamp': t5_end, 'operator_notes': op5_note
            })
            
            if failed_qc500:
                reason = "Heater Circuit Open"
                if peel_force < 15.0:
                    reason = "Leather Adhesion Fail"
                elif airbag_res < 1.8 or airbag_res > 2.2:
                    reason = "Airbag Loop Fault"
                elif switch_res > 0.5:
                    reason = "Switch Contact Fault"
                    
                buf['production_log'].append({
                    'part_id': part_id, 'start_time': t1_start, 'end_time': t5_end,
                    'final_status': 'Scrap', 'scrap_reason': reason,
                    'material_batch_id': batch_id
                })
            else:
                buf['production_log'].append({
                    'part_id': part_id, 'start_time': t1_start, 'end_time': t5_end,
                    'final_status': 'Pass', 'scrap_reason': '',
                    'material_batch_id': batch_id
                })
                
        # Write chunk
        for k, writer in writers.items():
            if buf[k]:
                df_chunk = pd.DataFrame(buf[k])
                if k == 'production_log':
                    df_chunk['start_time'] = pd.to_datetime(df_chunk['start_time'])
                    df_chunk['end_time'] = pd.to_datetime(df_chunk['end_time'])
                elif k == 'quality_inspections':
                    df_chunk['timestamp'] = pd.to_datetime(df_chunk['timestamp'])
                elif k == 'operator_logs':
                    df_chunk['timestamp'] = pd.to_datetime(df_chunk['timestamp'])
                    
                table = pa.Table.from_pandas(df_chunk, schema=globals()[f"{k}_schema"])
                writer.write_table(table)
                
        parts_generated += current_chunk_size
        
    for writer in writers.values():
        writer.close()
        
    print(f"Data generation complete! Saved files to {output_dir}")

def main():
    parser = argparse.ArgumentParser(description="Manufacturing Data Generator for Savnet Session 8")
    parser.add_argument('--num-wheels', '-n', type=int, default=1000000, help="Number of steering wheels to generate")
    parser.add_argument('--output-dir', '-o', type=str, default="data", help="Output directory to save Parquet files")
    parser.add_argument('--chunk-size', type=int, default=50000, help="Generator chunk size for batch writing")
    
    args = parser.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    
    generate_static_material_batches(args.output_dir)
    generate_data(args.num_wheels, args.output_dir, args.chunk_size)

if __name__ == "__main__":
    main()
