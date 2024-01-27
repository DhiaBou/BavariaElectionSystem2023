select w.parteiid, w.parteiname, w.erststimmen, w.zweitestimmen, w.gesamt_stimmen , w.vote_percentage, (w.vote_percentage - w_old.stimmen_prozent)as Veränderung_gesamt_stimmen,w.seats as Anzahl_Sitze, (w.seats - w_old.sitze)as Veränderung_Anzahl_sitze
from wahlergebnisse2023 w left outer join wahlergebnisse2018 w_old on w.parteiid = w_old.parteiid
