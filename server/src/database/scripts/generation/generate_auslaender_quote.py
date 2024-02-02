import pandas as pd


from database.database import get_db, engine
from src.database.models.models import Auslaender_Quote, Base

# Define the path to your CSV file
csv_file_path = '/Users/omarbouattour/PycharmProjects/Bayern_Wahl_dbs/server/src/database/scripts/csv/Auslaender_quote/auslaenderquote.csv'


df = pd.read_csv(csv_file_path)
quote_entries = []
Base.metadata.create_all(bind=engine)
with get_db() as db:
    for index, row in df.iterrows():
        quote_entries.append(Auslaender_Quote(
            kreis =row['kreis'],
            Quote=row['quote']
        ))
    db.add_all(quote_entries)
    db.commit()

print("Data from 'auslaenderquote.csv' has been successfully inserted into the database.")