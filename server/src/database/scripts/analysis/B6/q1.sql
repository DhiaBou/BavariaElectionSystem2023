select k."ParteiID", count(*) from   abgeordnete a, kandidaten k where a."KandidatID" = k."KandidatID" group by k."ParteiID";
