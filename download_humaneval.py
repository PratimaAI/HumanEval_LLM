from datasets import load_dataset

dataset = load_dataset("openai/openai_humaneval")

print(dataset["test"][0])
