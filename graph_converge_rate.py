import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("outputs/final_results.csv")

x = np.arange(len(df))
width = 0.4

plt.figure(figsize=(12,6))

plt.bar(
    x - width/2,
    df["humaneval_coverage"],
    width,
    label="HumanEval Coverage"
)

plt.bar(
    x + width/2,
    df["llm_coverage"],
    width,
    label="LLM Coverage"
)

# Average coverage lines
plt.axhline(
    y=df["humaneval_coverage"].mean(),
    color="blue",
    linestyle="--",
    alpha=0.7,
    label=f'HumanEval Avg ({df["humaneval_coverage"].mean():.1f}%)'
)

plt.axhline(
    y=df["llm_coverage"].mean(),
    color="orange",
    linestyle="--",
    alpha=0.7,
    label=f'LLM Avg ({df["llm_coverage"].mean():.1f}%)'
)

plt.xticks(x, df["function"], rotation=90)
plt.ylabel("Coverage (%)")
plt.xlabel("Function")
plt.title("HumanEval vs LLM Statement Coverage")
plt.legend()

plt.tight_layout()

plt.savefig("outputs/coverage_comparison.png", dpi=300)
plt.show()
