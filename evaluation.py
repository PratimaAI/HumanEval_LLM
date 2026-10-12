import json
import re
import pandas as pd
import os

TASKS_FILE = "data/selected_tasks.json"
TESTS_FILE = "outputs/generated_tests.json"
RESULTS_FILE = "outputs/results.csv"


def count_asserts(text):
    return len(re.findall(r"assert\s+", text))


with open(TASKS_FILE, "r") as f:
    tasks = json.load(f)

with open(TESTS_FILE, "r") as f:
    generated = json.load(f)

task_lookup = {}

for task in tasks:
    task_lookup[task["task_id"]] = task

results = []

for item in generated:

    task_id = item["task_id"]

    function_name = item["entry_point"]

    task = task_lookup[task_id]

    solution_code = (
        task["prompt"]
        + task["canonical_solution"]
    )

    generated_tests = item["generated_tests"]

    assertions = []

    for line in generated_tests.splitlines():

        line = line.strip()

        if line.startswith("assert"):
            assertions.append(line)

    total_tests = len(assertions)

    passed_tests = 0
    failed_tests = 0

    for assertion in assertions:

        try:

            code = (
                solution_code
                + "\n\n"
                + assertion
            )

            namespace = {}

            exec(code, namespace)

            passed_tests += 1

        except Exception:

            failed_tests += 1

    pass_rate = 0

    if total_tests > 0:

        pass_rate = round(
            (passed_tests / total_tests) * 100,
            2
        )

    results.append({
        "task_id": task_id,
        "function": function_name,
        "llm_test_count": total_tests,
        "passed_tests": passed_tests,
        "failed_tests": failed_tests,
        "pass_rate": pass_rate
    })

df = pd.DataFrame(results)

os.makedirs("outputs", exist_ok=True)

df.to_csv(
    RESULTS_FILE,
    index=False
)

print(df)

print("\nSaved:", RESULTS_FILE)
