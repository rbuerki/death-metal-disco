import pandas as pd

collection = pd.read_excel("data/dm_records_20-02-17.xlsx", 
                           encoding='utf-8')

albums = list(zip(collection["Artist"], collection['Titel']))
