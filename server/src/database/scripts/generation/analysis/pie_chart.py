from database.database import get_db
from database.models.models import Parteien
from database.scripts.generation.analysis.votes_pro_party_pro_wahlkreis import wahlkreise_dict

def pie_chart(wahlkreise_dict, wahlkreis):
    votes = wahlkreise_dict[wahlkreis]["parties"]
    new_votes = {}
    import matplotlib.pyplot as plt
    with get_db() as db:
     parteien: list[Parteien] = db.query(Parteien
     ).all()
     for party in parteien:
         if party.ParteiID in votes:
             new_votes[party.kurzbezeichnung] = votes[party.ParteiID]

    # Your dictionary with keys and values

    # Extract keys and values from the dictionary
    categories = list(new_votes.keys())
    values = list(new_votes.values())

    # Create a pie chart
    plt.figure(figsize=(8, 6))
    plt.pie(values, labels=categories, autopct='%1.1f%%', colors=['royalblue', 'forestgreen', 'gold', 'tomato', 'purple'], startangle=140)

    # Add a title
    plt.title(f'Gesamtstimmen in Wahlkreis {wahlkreis}')

    # Display the plot
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()


pie_chart(wahlkreise_dict, 907)