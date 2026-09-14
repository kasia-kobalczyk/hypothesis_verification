import pandas as pd

df = pd.read_json("hf://datasets/ankilok/ResearchBench/ranking/ranking.jsonl", lines=True)

# save to jsonl
df.to_json("./ranking.jsonl", orient="records", lines=True)
