select CONCAT(k."Nachname",  ', ', k."Vorname"), k."ParteiID"  from   abgeordnete a, kandidaten k where a."KandidatID" = k."KandidatID";
