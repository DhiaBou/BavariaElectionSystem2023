import pandas as pd
from sqlalchemy.orm import sessionmaker
from database.database import engine
from src.database.models.models import Einkommen_pro_stimmkreis, Base

# Define the path to your CSV file
csv_file_path = '/database/scripts/csv/Einkommen_bayern/einkommen_kreis.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file_path)

# Create the database tables if they don't exist
Base.metadata.create_all(bind=engine)

# Create a Session
SessionLocal = sessionmaker(bind=engine)

# Instantiate a session
with SessionLocal() as db:
    # Iterate over the DataFrame rows
    for index, row in df.iterrows():
        entry = Einkommen_pro_stimmkreis(
            Kreis=int(row['kreis']),
            Einkommen=int(row['einkommen'])
        )
        # Add the entry to the session
        db.add(entry)
    # Commit the session to insert the data
    db.commit()

print("Data from 'einkommen_pro_stimmkreis.csv' has been successfully inserted into the database.")
