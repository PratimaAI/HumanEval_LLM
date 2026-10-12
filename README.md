# Evaluating LLM-Generated Unit Tests with HumanEval

This project explores how useful LLM-generated tests are for Python functions in the HumanEval dataset. It uses Ollama to generate tests for 20 selected tasks, then compares their pass rate and statement coverage with HumanEval's tests.

## Getting started

You'll need Python, [Ollama](https://ollama.com/), and the `qwen2.5-coder:7b` model:

```bash
python -m venv .venv
source .venv/bin/activate  
python -m pip install datasets ollama pandas matplotlib numpy coverage
ollama pull qwen2.5-coder:7b
```

From the project folder, run:

```bash
python generate_test.py
python evaluation.py
python coverage_analysis.py
python merge_results.py
python summary_stats.py
python graph_pass_rate.py
python graph_converge_rate.py
```

The scripts save generated tests, CSV results, a summary, and plots in `outputs/`. The selected inputs are in `data/selected_tasks.json`; run `python save_selected_tasks.py` to fetch and recreate them from Hugging Face.

## A note on the results

The pass rate is the share of generated assertions that pass against the reference solutions; it is not HumanEval's `pass@k` metric. The results cover only the 20 selected tasks. 
