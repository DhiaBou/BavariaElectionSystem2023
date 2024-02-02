import pandas as pd
from sqlalchemy.orm import sessionmaker
from database.database import engine
from src.database.models.models import gemeinde, Base

# Define the path to your CSV file
csv_file_path = '/Users/omarbouattour/PycharmProjects/Bayern_Wahl_dbs/server/src/database/scripts/csv/gemeinde_.csv'
# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file_path, delimiter=';')

# Create the database tables if they don't exist
Base.metadata.create_all(bind=engine)

# Create a Session
SessionLocal = sessionmaker(bind=engine)

with SessionLocal() as db:
    for index, row in df.iterrows():
        entry = gemeinde(
            Gemeineschluessel = int(row['Gemeineschluessel']),
            Kreisschluessel=int(row['Kreisschluessel']),
            StimmkreisID=int(row['Stimmkreis']),
            Name=row['Name']
        )

        db.add(entry)

    db.commit()

print("Data from 'gemeinde_.csv' has been successfully inserted into the database.")
