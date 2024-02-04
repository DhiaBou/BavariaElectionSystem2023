WITH gesamt_erststimmen_pro_partei_pro_stimmkreis AS (SELECT s."StimmkreisId"      AS stimmkreisid,
                                                             s."Name"              AS stimmkreisname,
                                                             p."ParteiID"          AS parteiid,
                                                             p."Name"              AS parteiname,
                                                             count(e."KandidatID") AS erststimmen
                                                      FROM stimmkreis s
                                                               CROSS JOIN parteien p
                                                               LEFT JOIN kandidaten k ON p."ParteiID" = k."ParteiID"
                                                               LEFT JOIN erste_stimmzettel e
                                                                         ON e."KandidatID" = k."KandidatID" AND e."StimmkreisId" = s."StimmkreisId"
                                                      where s."StimmkreisId" = :StimmkreisId
                                                      GROUP BY s."StimmkreisId", s."Name", p."ParteiID", p."Name"),
     gesamt_zweitstimmen_pro_partei_pro_stimmkreis AS (SELECT s."StimmkreisId"      AS stimmkreisid,
                                                              s."Name"              AS stimmkreisname,
                                                              p."ParteiID"          AS parteiid,
                                                              p."Name"              AS parteiname,
                                                              count(e."KandidatID") AS zweitstimmen
                                                       FROM stimmkreis s
                                                                CROSS JOIN parteien p
                                                                LEFT JOIN kandidaten k ON p."ParteiID" = k."ParteiID"
                                                                LEFT JOIN zweite_stimmzettel e
                                                                          ON e."KandidatID" = k."KandidatID" AND e."StimmkreisId" = s."StimmkreisId"
                                                       where s."StimmkreisId" = :StimmkreisId
                                                       GROUP BY s."StimmkreisId", s."Name", p."ParteiID", p."Name"),
     gesamt_zweitstimmen_ohne_kandidaten_pro_partei_pro_stimmkreis AS (SELECT s."StimmkreisId"    AS stimmkreisid,
                                                                              s."Name"            AS stimmkreisname,
                                                                              p."ParteiID"        AS parteiid,
                                                                              p."Name"            AS parteiname,
                                                                              count(e."ParteiID") AS zweitstimmen_ohne_kandidaten
                                                                       FROM stimmkreis s
                                                                                CROSS JOIN parteien p
                                                                                LEFT JOIN zweite_stimme_ohne_kandidaten e
                                                                                          ON e."ParteiID" = p."ParteiID" AND e."StimmkreisId" = s."StimmkreisId"
                                                                       where s."StimmkreisId" = :StimmkreisId
                                                                       GROUP BY s."StimmkreisId", s."Name", p."ParteiID", p."Name"),
     gesamt_stimmen_pro_partei_pro_stimmkreis_ AS (SELECT g1.stimmkreisid,
                                                          g1.stimmkreisname,
                                                          g1.parteiid,
                                                          g1.parteiname,
                                                          g1.erststimmen + g2.zweitstimmen + g3.zweitstimmen_ohne_kandidaten AS gesamt_stimmen,
                                                          g1.erststimmen,
                                                          g2.zweitstimmen + g3.zweitstimmen_ohne_kandidaten                  AS zweite_stimme
                                                   FROM gesamt_erststimmen_pro_partei_pro_stimmkreis g1
                                                            JOIN gesamt_zweitstimmen_pro_partei_pro_stimmkreis g2
                                                                 ON g1.stimmkreisid = g2.stimmkreisid AND g1.parteiid = g2.parteiid
                                                            JOIN gesamt_zweitstimmen_ohne_kandidaten_pro_partei_pro_stimmkreis g3
                                                                 ON g2.stimmkreisid = g3.stimmkreisid AND g2.parteiid = g3.parteiid),
     anzahl_stimmen_pro_stimmkreis as (select g.stimmkreisid,
                                              sum(g.gesamt_stimmen) as sum
                                       from gesamt_stimmen_pro_partei_pro_stimmkreis_ g
                                       group by g.stimmkreisid),
     voters_pro_stimmkreis as (select "StimmkreisId", count(*) as Count_Voters
                               from erste_stimmzettel
                               group by "StimmkreisId"),
     wahlbeteiligung as (select s."StimmkreisId",
                                v.count_voters,
                                s."Stimmberechtigte",
                                ROUND(v.Count_Voters * 100.0 / s."Stimmberechtigte", 2) as Wahlbeteiligung
                         from voters_pro_stimmkreis v,
                              stimmkreis s
                         where s."StimmkreisId" = v."StimmkreisId")


--q3

select g.stimmkreisid,
       g.parteiname,
       w.wahlbeteiligung,
       g.gesamt_stimmen,
       g.erststimmen,
       g.zweite_stimme,
       ROUND(g.gesamt_stimmen * 100.00 / a.sum, 2)      AS percentage,
       COALESCE((SELECT CONCAT(d."Nachname", ', ', d."Vorname")
                 FROM direct_candidates d
                 WHERE d."StimmkreisId" = a.stimmkreisid
                   AND d."ParteiID" = g.parteiid), '-') AS gewaehlte_kandidaten
from gesamt_stimmen_pro_partei_pro_stimmkreis_view g,
     anzahl_stimmen_pro_stimmkreis a,
     wahlbeteiligung w
where a.stimmkreisid = g.stimmkreisid
  and w."StimmkreisId" = a.stimmkreisid
order by g.stimmkreisid, g.erststimmen DESC;
