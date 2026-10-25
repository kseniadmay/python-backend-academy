import json
import re
from pathlib import Path

base_dir = Path(r"C:\Users\fury6\OneDrive\Python_Backend_Academy")

# Load tier 1 summary
with open(base_dir / "scripts" / "tier1_tasks_summary.json", "r", encoding="utf-8") as f:
    tier1_tasks = json.load(f)

print(f"Total Tier 1 tasks to enrich: {len(tier1_tasks)}")

# Let's inspect titles and solutions to generate mappings
# We can create a comprehensive dictionary of (hint, io_in, io_out) for each task id in tier 1!
