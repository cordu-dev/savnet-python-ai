"""
Step 03 — Structured output (reliable JSON)
===========================================

Problem:
    Free-text answers are great for humans but terrible for code. If your
    program needs "the defect type and severity", you don't want a paragraph —
    you want a predictable object with exact fields.

Old, fragile way:
    "Please reply in JSON" ... then cross your fingers and hope it doesn't add
    a chatty "Sure! Here's your JSON:" that breaks json.loads().

Reliable way (what we use):
    Define a SCHEMA with Pydantic (a class describing the fields + types), then
    call `model.with_structured_output(Schema)`. LangChain forces the model to
    return data that matches your schema and hands you a real Python object.

Why builders love this:
    Every downstream agent in this course passes STRUCTURED data to the next.
    Reliable JSON is the glue of the whole system.

Run it:
    python 03_structured_output.py
"""

from pydantic import BaseModel, Field

import llm_utils as llm


# --- 1. Describe the shape we want ---------------------------------------
# Each field has a type and a short description. The description is not just a
# comment — the model reads it to understand what to put there.
class DefectRecord(BaseModel):
    """A single defect extracted from an operator's note."""

    station: str = Field(description="Which station the defect happened at")
    defect_type: str = Field(description="Short label, e.g. 'surface scratch'")
    severity: str = Field(description="One of: low, medium, high")
    scrap: bool = Field(description="True if the part was scrapped")


# --- 2. Ask the model to fill that shape ---------------------------------
# temperature=0 because for extraction we want the most faithful, repeatable
# reading of the text — not creativity.
model = llm.get_llm(temperature=0)
extractor = model.with_structured_output(DefectRecord)

operator_note = (
    "Foaming line again — big overfill on a premium wheel, foam everywhere. "
    "Surface looked bad so we scrapped it. Third time this shift."
)

print("Operator note:\n ", operator_note, "\n")

result = extractor.invoke(f"Extract the defect from this note:\n{operator_note}")

# `result` is a DefectRecord object — real attributes, not a string to parse!
print("Parsed as structured data:")
print("  station     =", result.station)
print("  defect_type =", result.defect_type)
print("  severity    =", result.severity)
print("  scrap       =", result.scrap)

print("\nBecause it's a Python object, code can use it directly:")
if result.scrap and result.severity == "high":
    print("  -> ALERT: high-severity scrap, flag for review.")

# =========================================================================
# YOUR CHALLENGE (15 min)
# -------------------------------------------------------------------------
# 1. Add a field `quantity: int` (how many parts affected) with a sensible
#    description. Re-run — did the model infer it correctly from the note?
# 2. Feed it a VAGUE note ("something felt off today"). What does it put in
#    the fields? Is that safe? (Preview of hallucinations — step 05.)
# 3. Change severity to a proper enum using Python's Literal type:
#       from typing import Literal
#       severity: Literal["low", "medium", "high"]
#    Why is constraining the allowed values safer than a free-text string?
# =========================================================================
