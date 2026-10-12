from datasets import load_dataset

dataset = load_dataset("openai/openai_humaneval")

selected_ids = [
    13,31,45,55,139,
    10,48,51,64,140,
    26,35,47,57,127,
    0,3,20,69,124
]

for idx in selected_ids:
    task = dataset["test"][idx]

    print("="*60)
    print("TASK:", idx)
    print("FUNCTION:", task["entry_point"])
    print("="*60)
    print(task["prompt"])
