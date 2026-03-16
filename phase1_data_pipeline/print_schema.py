from datasets import load_dataset
ds = load_dataset('ManikaSaini/zomato-restaurant-recommendation', split='train')
print(ds.column_names)
print(ds.features)
df = ds.to_pandas()
print(df.head(1).to_dict('records')[0])
