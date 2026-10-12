import pandas as pd

results = pd.read_csv(
    "outputs/results.csv"
)

coverage = pd.read_csv(
    "outputs/coverage_results.csv"
)

merged = results.merge(
    coverage[
        [
            "task_id",
            "humaneval_test_count",
            "humaneval_coverage",
            "llm_coverage"
        ]
    ],
    on="task_id",
    how="left"
)

merged.to_csv(
    "outputs/final_results.csv",
    index=False
)

print(merged)
