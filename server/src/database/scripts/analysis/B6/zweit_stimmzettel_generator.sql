select CONCAT(k."Nachname", ', ', k."Vorname") AS Kandidat,
       p.kurzbezeichnung,
       k."KandidatID",
       p."ParteiID"
from kandidaten k,
     parteien p
where p."ParteiID" = k."ParteiID"