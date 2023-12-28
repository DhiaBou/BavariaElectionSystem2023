select CONCAT(k."Nachname",  ', ', k."Vorname") as Kandidat, p.kurzbezeichnung  from   abgeordnete a, kandidaten k, parteien p where a."KandidatID" = k."KandidatID" and p."ParteiID" = k."ParteiID";
