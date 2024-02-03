import pandas as pd
from sqlalchemy.orm import sessionmaker
from database.database import engine
from src.database.models.models import Einkommen_pro_wahlkreis, Base

# Define the path to your CSV file
csv_file_path = '/Users/omarbouattour/PycharmProjects/Bayern_Wahl_dbs/server/src/database/scripts/csv/Einkommen_bayern/einkommen_wahlkreis.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file_path)

# Create the database tables if they don't exist
Base.metadata.create_all(bind=engine)

# Create a Session
SessionLocal = sessionmaker(bind=engine)

with SessionLocal() as db:
    for index, row in df.iterrows():
        entry = Einkommen_pro_wahlkreis(
            WahlkreisID=int(row['BezirkID']),
            Einkommen=int(row['Einkommen'])
        )

        db.add(entry)

    db.commit()

print("Data from 'Einkommen_pro_wahlkreis.csv' has been successfully inserted into the database.")
