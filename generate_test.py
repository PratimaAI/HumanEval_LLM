import json
import os
import ollama

# Input and output files
INPUT_FILE = "data/selected_tasks.json"
OUTPUT_FILE = "outputs/generated_tests.json"

# Create output directory
os.makedirs("outputs", exist_ok=True)

# Load selected tasks
with open(INPUT_FILE, "r") as f:
    tasks = json.load(f)

results = []

for task in tasks:

    function_name = task["entry_point"]
    prompt = task["prompt"]

    print(f"Generating tests for: {function_name}")

    llm_prompt = f"""
You are a software testing expert.

Generate 10 Python assert statements for the following function.

Requirements:
- Include normal cases
- Include boundary cases
- Include edge cases when appropriate
- Return ONLY Python assert statements
- Do not include explanations
- Do not use markdown

Function:

{prompt}
"""

    response = ollama.chat(
        model="qwen2.5-coder:7b",
        messages=[
            {
                "role": "user",
                "content": llm_prompt
            }
        ]
    )

    generated_tests = response["message"]["content"]

    results.append({
        "task_id": task["task_id"],
        "entry_point": function_name,
        "generated_tests": generated_tests
    })

# Save results
with open(OUTPUT_FILE, "w") as f:
    json.dump(results, f, indent=4)

print(f"\nSaved generated tests to {OUTPUT_FILE}")
