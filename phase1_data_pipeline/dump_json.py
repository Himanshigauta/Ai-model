import json
from datasets import load_dataset
ds = load_dataset('ManikaSaini/zomato-restaurant-recommendation', split='train')
row = ds.to_pandas().head(1).to_dict('records')[0]
with open('sample.json', 'w') as f:
    json.dump(row, f, indent=2)
