import json

print(json.dumps(json.loads("transactions.json"), indent=4, sort_keys=False))
