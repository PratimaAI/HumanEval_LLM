from datasets import load_dataset
import json
import os

dataset = load_dataset("openai/openai_humaneval")

selected_ids = [
    13,31,45,55,139,
    10,48,51,64,140,
    26,35,47,57,127,
    0,3,20,69,124
]

selected_tasks = []

for idx in selected_ids:
    task = dataset["test"][idx]

    selected_tasks.append({
        "task_index": idx,
        "task_id": task["task_id"],
        "entry_point": task["entry_point"],
        "prompt": task["prompt"],
        "canonical_solution": task["canonical_solution"],
        "test": task["test"]
    })

os.makedirs("data", exist_ok=True)

with open("data/selected_tasks.json", "w") as f:
    json.dump(selected_tasks, f, indent=4)

print(f"Saved {len(selected_tasks)} tasks.")
