
from pprint import pprint
import random


def generate_data():
    fleet = []
    for t_id in range(100, 150):
        # Planned vs Actual
        truck = {
            "id": f"TRUCK-{t_id}",
            "plan": {"dist_km": 2500, "eta_hrs": 120, "consumption_rate": 16},
            "logs": [],  # Hourly data
        }
        fuel = 400
        for h in range(168):
            dist_moved = random.uniform(15, 25)
            # Simulate Fuel Theft (Anomaly)
            fuel_loss = (dist_moved / 100) * truck["plan"]["consumption_rate"]
            if t_id == 105 and h == 20:
                fuel -= 50  # Theft event
            fuel -= fuel_loss

            truck["logs"].append(
                {
                    "hour": h,
                    "gps_deviation": (
                        random.uniform(0, 15) if t_id != 110 else random.uniform(0, 60)
                    ),
                    "fuel_level": fuel,
                    "dist_covered": dist_moved,
                    "road_block": (
                        random.choice([True, False])
                        if random.random() > 0.95
                        else False
                    ),
                }
            )
        fleet.append(truck)
    return fleet


fleet_data = generate_data()


pprint(fleet_data)
