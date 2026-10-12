import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("outputs/final_results.csv")

plt.figure(figsize=(12,6))

plt.bar(
    df["function"],
    df["pass_rate"]
)

plt.xticks(rotation=90)

plt.ylabel("Pass Rate (%)")
plt.xlabel("Function")
plt.title("LLM Test Pass Rate per HumanEval Task")

plt.tight_layout()

plt.savefig("outputs/pass_rate.png")

plt.show()
