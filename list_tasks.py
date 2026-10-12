from datasets import load_dataset

dataset = load_dataset("openai/openai_humaneval")

for i in range(len(dataset["test"])):
    print(i, dataset["test"][i]["entry_point"])
