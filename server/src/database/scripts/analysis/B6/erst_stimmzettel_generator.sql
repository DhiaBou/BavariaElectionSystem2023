SELECT CONCAT(k."Nachname", ', ', k."Vorname") AS Kandidat,
       p.kurzbezeichnung                       AS parteiname,
       e."StimmkreisId",
       k."KandidatID"
FROM erst_stimmzettel e
         JOIN kandidaten k ON k."KandidatID" = e."KandidatID"
         JOIN parteien p ON p."ParteiID" = k."ParteiID"
order by p.kurzbezeichnung
