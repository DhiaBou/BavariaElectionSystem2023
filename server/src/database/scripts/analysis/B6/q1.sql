select p."kurzbezeichnung", count(*) from   abgeordnete a, kandidaten k, parteien p where a."KandidatID" = k."KandidatID" and p."ParteiID"=k."ParteiID" group by p."kurzbezeichnung";
