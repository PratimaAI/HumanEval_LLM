import pandas as pd

df = pd.read_csv("outputs/final_results.csv")

avg_pass_rate = round(
    df["pass_rate"].mean(),
    2
)

avg_he_cov = round(
    df["humaneval_coverage"].mean(),
    2
)

avg_llm_cov = round(
    df["llm_coverage"].mean(),
    2
)

print(f"Average Pass Rate: {avg_pass_rate}%")
print(f"Average HumanEval Coverage: {avg_he_cov}%")
print(f"Average LLM Coverage: {avg_llm_cov}%")

with open(
    "outputs/summary.txt",
    "w"
) as f:

    f.write(
        f"Average Pass Rate: {avg_pass_rate}%\n"
    )

    f.write(
        f"Average HumanEval Coverage: {avg_he_cov}%\n"
    )

    f.write(
        f"Average LLM Coverage: {avg_llm_cov}%\n"
    )
