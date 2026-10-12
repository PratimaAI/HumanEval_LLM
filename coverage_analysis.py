import json
import re
import os
import subprocess
import tempfile
import pandas as pd

TASKS_FILE = "data/selected_tasks.json"
GENERATED_FILE = "outputs/generated_tests.json"
OUTPUT_FILE = "outputs/coverage_results.csv"


def count_asserts(text):
    return len(re.findall(r"assert\s+", text))


def extract_coverage(report_text):

    lines = report_text.splitlines()

    for line in lines:

        if "solution.py" in line:

            parts = line.split()

            try:
                return float(parts[-1].replace("%", ""))
            except:
                return 0.0

    return 0.0


def get_coverage(solution_code, test_code, function_name):

    with tempfile.TemporaryDirectory() as temp_dir:

        solution_file = os.path.join(
            temp_dir,
            "solution.py"
        )

        test_file = os.path.join(
            temp_dir,
            "test_generated.py"
        )

        with open(solution_file, "w") as f:
            f.write(solution_code)

        with open(test_file, "w") as f:
            f.write(test_code)

        subprocess.run(
            ["coverage", "erase"],
            capture_output=True
        )

        subprocess.run(
            [
                "coverage",
                "run",
                test_file
            ],
            cwd=temp_dir,
            capture_output=True,
            text=True
        )

        report = subprocess.run(
            [
                "coverage",
                "report"
            ],
            cwd=temp_dir,
            capture_output=True,
            text=True
        )

        return extract_coverage(
            report.stdout
        )


# --------------------------------------------------
# Load files
# --------------------------------------------------

with open(TASKS_FILE, "r") as f:
    tasks = json.load(f)

with open(GENERATED_FILE, "r") as f:
    generated = json.load(f)

task_lookup = {}

for task in tasks:
    task_lookup[task["task_id"]] = task

results = []

# --------------------------------------------------
# Process all 20 tasks
# --------------------------------------------------

for item in generated:

    task = task_lookup[item["task_id"]]

    function_name = task["entry_point"]

    print(
        f"Processing {function_name}..."
    )

    solution_code = (
        task["prompt"]
        + task["canonical_solution"]
    )

    # ----------------------
    # LLM tests
    # ----------------------

    llm_tests_raw = item["generated_tests"]

    llm_test_code = (
        f"from solution import {function_name}\n\n"
        + llm_tests_raw
    )

    llm_coverage = get_coverage(
        solution_code,
        llm_test_code,
        function_name
    )

    # ----------------------
    # HumanEval tests
    # ----------------------

    humaneval_test_text = task["test"]

    humaneval_lines = []

    for line in humaneval_test_text.splitlines():

        line = line.strip()

        if line.startswith("assert"):

            line = line.replace(
                "candidate(",
                f"{function_name}("
            )

            humaneval_lines.append(line)

    humaneval_test_code = (
        f"from solution import {function_name}\n\n"
        + "\n".join(humaneval_lines)
    )

    humaneval_coverage = get_coverage(
        solution_code,
        humaneval_test_code,
        function_name
    )

    results.append({

        "task_id":
            item["task_id"],

        "function":
            function_name,

        "humaneval_test_count":
            count_asserts(
                humaneval_test_text
            ),

        "llm_test_count":
            count_asserts(
                llm_tests_raw
            ),

        "humaneval_coverage":
            humaneval_coverage,

        "llm_coverage":
            llm_coverage
    })

# --------------------------------------------------
# Save CSV
# --------------------------------------------------

df = pd.DataFrame(results)

os.makedirs(
    "outputs",
    exist_ok=True
)

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\nCoverage Results\n")
print(df)

print(
    f"\nSaved to {OUTPUT_FILE}"
)
