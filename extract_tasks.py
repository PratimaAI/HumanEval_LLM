from datasets import load_dataset
import os

# Load HumanEval dataset
dataset = load_dataset("openai/openai_humaneval")

# Create main directory
os.makedirs("tasks", exist_ok=True)

for task in dataset["test"]:
    task_id = task["task_id"].replace("/", "_")

    # Create a folder for each task
    task_dir = os.path.join("tasks", task_id)
    os.makedirs(task_dir, exist_ok=True)

    # Save prompt
    with open(os.path.join(task_dir, "prompt.py"), "w") as f:
        f.write(task["prompt"])

    # Save canonical solution
    with open(os.path.join(task_dir, "solution.py"), "w") as f:
        f.write(task["canonical_solution"])

    # Save official tests
    with open(os.path.join(task_dir, "tests.py"), "w") as f:
        f.write(task["test"])

print("All HumanEval tasks extracted successfully!")
