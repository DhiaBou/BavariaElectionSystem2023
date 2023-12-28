create MATERIALIZED  view gesamt_stimmen_pro_partei_pro_wahlkreis_view as (WITH gesamt_erststimmen_pro_partei_pro_wahlkreis AS (SELECT w."WahlkreisId"       AS wahlkreisid,
                                                            w."Name"              AS wahlkreisname,
                                                            p."ParteiID"          AS parteiid,
                                                            p."Name"              AS parteiname,
                                                            count(e."KandidatID") AS erststimmen
                                                     FROM stimmkreis s
                                                              JOIN wahlkreis w ON s."WahlkreisId" = w."WahlkreisId"
                                                              CROSS JOIN parteien p
                                                              LEFT JOIN kandidaten k ON p."ParteiID" = k."ParteiID"
                                                              LEFT JOIN erste_stimmzettel e
                                                                        ON e."KandidatID" = k."KandidatID" AND e."StimmkreisId" = s."StimmkreisId"
                                                     GROUP BY w."WahlkreisId", w."Name", p."ParteiID", p."Name"),
     gesamt_zweitstimmen_pro_partei_pro_wahlkreis AS (SELECT w."WahlkreisId"       AS wahlkreisid,
                                                             w."Name"              AS wahlkreisname,
                                                             p."ParteiID"          AS parteiid,
                                                             p."Name"              AS parteiname,
                                                             count(e."KandidatID") AS zweitstimmen
                                                      FROM stimmkreis s
                                                               JOIN wahlkreis w ON s."WahlkreisId" = w."WahlkreisId"
                                                               CROSS JOIN parteien p
                                                               LEFT JOIN kandidaten k ON p."ParteiID" = k."ParteiID"
                                                               LEFT JOIN zweite_stimmzettel e
                                                                         ON e."KandidatID" = k."KandidatID" AND e."StimmkreisId" = s."StimmkreisId"
                                                      GROUP BY w."WahlkreisId", w."Name", p."ParteiID", p."Name"),
     gesamt_zweitstimmen_ohne_kandidaten_pro_partei_pro_wahlkreis AS (SELECT w."WahlkreisId"     AS wahlkreisid,
                                                                             w."Name"            AS wahlkreisname,
                                                                             p."ParteiID"        AS parteiid,
                                                                             p."Name"            AS parteiname,
                                                                             count(e."ParteiID") AS zweitstimmen_ohne_kandidaten
                                                                      FROM stimmkreis s
                                                                               JOIN wahlkreis w ON s."WahlkreisId" = w."WahlkreisId"
                                                                               CROSS JOIN parteien p
                                                                               LEFT JOIN zweite_stimme_ohne_kandidaten e
                                                                                         ON e."ParteiID" = p."ParteiID" AND e."StimmkreisId" = s."StimmkreisId"
                                                                      GROUP BY w."WahlkreisId", w."Name", p."ParteiID", p."Name"),
     gesamt_stimmen_pro_partei_pro_wahlkreis AS (SELECT g1.wahlkreisid,
                                                        g1.wahlkreisname,
                                                        g1.parteiid,
                                                        g1.parteiname,
                                                        g1.erststimmen + g2.zweitstimmen + g3.zweitstimmen_ohne_kandidaten AS gesamt_stimmen
                                                 FROM gesamt_erststimmen_pro_partei_pro_wahlkreis g1
                                                          JOIN gesamt_zweitstimmen_pro_partei_pro_wahlkreis g2
                                                               ON g1.wahlkreisid = g2.wahlkreisid AND g1.parteiid = g2.parteiid
                                                          JOIN gesamt_zweitstimmen_ohne_kandidaten_pro_partei_pro_wahlkreis g3
                                                               ON g2.wahlkreisid = g3.wahlkreisid AND g2.parteiid = g3.parteiid)
SELECT wahlkreisid,
       wahlkreisname,
       parteiid,
       parteiname,
       gesamt_stimmen
FROM gesamt_stimmen_pro_partei_pro_wahlkreis);
create MATERIALIZED  view anteil_over_five_percent as (WITH
     totalvotes AS (SELECT g.wahlkreisid,
                           sum(g.gesamt_stimmen) AS sum
                    FROM gesamt_stimmen_pro_partei_pro_wahlkreis_view g
                    GROUP BY g.wahlkreisid),
     anteil AS (SELECT g.wahlkreisid,
                       g.parteiid,
                       sum(g.gesamt_stimmen) * 100.000 / t.sum AS anteil
                FROM gesamt_stimmen_pro_partei_pro_wahlkreis_view g,
                     totalvotes t
                WHERE g.wahlkreisid = t.wahlkreisid
                GROUP BY g.wahlkreisid, g.parteiid, t.sum
                HAVING (sum(g.gesamt_stimmen) * 100.000 / t.sum) >= 5.00
                ORDER BY g.wahlkreisid, (sum(g.gesamt_stimmen) * 100.000 / t.sum) DESC)


SELECT wahlkreisid,
       parteiid,
       anteil
FROM anteil);


create MATERIALIZED view direct_candidates as ( with
     candidatevotes AS (SELECT erste_stimmzettel."StimmkreisId",
                               kandidaten."KandidatID",
                               kandidaten."Vorname",
                               kandidaten."Nachname",
                               kandidaten."ParteiID",
                               count(erste_stimmzettel."KandidatID") AS stimmenzahl
                        FROM erste_stimmzettel
                                 JOIN kandidaten ON erste_stimmzettel."KandidatID" = kandidaten."KandidatID"
                        GROUP BY erste_stimmzettel."StimmkreisId", kandidaten."KandidatID"),
     rankedcandidates AS (SELECT cv."StimmkreisId",
                                 cv."KandidatID",
                                 cv."Vorname",
                                 cv."Nachname",
                                 cv."ParteiID",
                                 cv.stimmenzahl,
                                 rank() OVER (PARTITION BY cv."StimmkreisId" ORDER BY cv.stimmenzahl DESC) AS rank
                          FROM candidatevotes cv),
     direct_candidates AS (SELECT rc."StimmkreisId",
                                  sk."Name" AS stimmkreisname,
                                  rc."KandidatID",
                                  rc."Vorname",
                                  rc."Nachname",
                                  rc."ParteiID",
                                  sk."WahlkreisId",
                                  rc.stimmenzahl
                           FROM rankedcandidates rc
                                    JOIN stimmkreis sk ON rc."StimmkreisId" = sk."StimmkreisId"
                           WHERE NOT (EXISTS (SELECT rc2."StimmkreisId",
                                                     rc2."KandidatID",
                                                     rc2."Vorname",
                                                     rc2."Nachname",
                                                     rc2."ParteiID",
                                                     rc2.stimmenzahl,
                                                     rc2.rank
                                              FROM rankedcandidates rc2
                                              WHERE rc2.rank < rc.rank
                                                AND rc2."StimmkreisId" = rc."StimmkreisId"))
                             AND (rc."ParteiID" IN (SELECT an.parteiid
                                                    FROM anteil_over_five_percent an,
                                                         stimmkreis s
                                                    WHERE s."StimmkreisId" = rc."StimmkreisId"
                                                      AND s."WahlkreisId" = an.wahlkreisid)))
SELECT "WahlkreisId",
    "StimmkreisId",
       stimmkreisname,
       "KandidatID",
       "Vorname",
       "Nachname",
       "ParteiID",
       stimmenzahl
FROM direct_candidates);
create MATERIALIZED view gesamt_stimmen_pro_partei_pro_stimmkreis_view as (WITH gesamt_erststimmen_pro_partei_pro_stimmkreis AS (SELECT s."StimmkreisId"       AS stimmkreisid,
                                                            s."Name"              AS stimmkreisname,
                                                            p."ParteiID"          AS parteiid,
                                                            p."Name"              AS parteiname,
                                                            count(e."KandidatID") AS erststimmen
                                                     FROM stimmkreis s
                                                              CROSS JOIN parteien p
                                                              LEFT JOIN kandidaten k ON p."ParteiID" = k."ParteiID"
                                                              LEFT JOIN erste_stimmzettel e
                                                                        ON e."KandidatID" = k."KandidatID" AND e."StimmkreisId" = s."StimmkreisId"
                                                     GROUP BY s."StimmkreisId", s."Name", p."ParteiID", p."Name"),
     gesamt_zweitstimmen_pro_partei_pro_stimmkreis AS (SELECT s."StimmkreisId"       AS stimmkreisid,
                                                             s."Name"              AS stimmkreisname,
                                                             p."ParteiID"          AS parteiid,
                                                             p."Name"              AS parteiname,
                                                             count(e."KandidatID") AS zweitstimmen
                                                      FROM stimmkreis s
                                                               CROSS JOIN parteien p
                                                               LEFT JOIN kandidaten k ON p."ParteiID" = k."ParteiID"
                                                               LEFT JOIN zweite_stimmzettel e
                                                                         ON e."KandidatID" = k."KandidatID" AND e."StimmkreisId" = s."StimmkreisId"
                                                      GROUP BY s."StimmkreisId", s."Name", p."ParteiID", p."Name"),
     gesamt_zweitstimmen_ohne_kandidaten_pro_partei_pro_stimmkreis AS (SELECT s."StimmkreisId"     AS stimmkreisid,
                                                                             s."Name"            AS stimmkreisname,
                                                                             p."ParteiID"        AS parteiid,
                                                                             p."Name"            AS parteiname,
                                                                             count(e."ParteiID") AS zweitstimmen_ohne_kandidaten
                                                                      FROM stimmkreis s
                                                                               CROSS JOIN parteien p
                                                                               LEFT JOIN zweite_stimme_ohne_kandidaten e
                                                                                         ON e."ParteiID" = p."ParteiID" AND e."StimmkreisId" = s."StimmkreisId"
                                                                      GROUP BY s."StimmkreisId", s."Name", p."ParteiID", p."Name"),
     gesamt_stimmen_pro_partei_pro_stimmkreis AS (SELECT g1.stimmkreisid,
                                                        g1.stimmkreisname,
                                                        g1.parteiid,
                                                        g1.parteiname,
                                                        g1.erststimmen + g2.zweitstimmen + g3.zweitstimmen_ohne_kandidaten AS gesamt_stimmen,
                                                        g1.erststimmen,
                                                        g2.zweitstimmen + g3.zweitstimmen_ohne_kandidaten as zweite_stimme
                                                 FROM gesamt_erststimmen_pro_partei_pro_stimmkreis g1
                                                          JOIN gesamt_zweitstimmen_pro_partei_pro_stimmkreis g2
                                                               ON g1.stimmkreisid = g2.stimmkreisid AND g1.parteiid = g2.parteiid
                                                          JOIN gesamt_zweitstimmen_ohne_kandidaten_pro_partei_pro_stimmkreis g3
                                                               ON g2.stimmkreisid = g3.stimmkreisid AND g2.parteiid = g3.parteiid)
SELECT stimmkreisid,
       stimmkreisname,
       parteiid,
       parteiname,
       gesamt_stimmen,
       erststimmen,
       zweite_stimme
FROM gesamt_stimmen_pro_partei_pro_stimmkreis);
create MATERIALIZED  view kandidat_gasammt_stimmen as (
with erste_stimme as (
select k."KandidatID", count(*) as count from kandidaten k ,erste_stimmzettel e where e."KandidatID" = k."KandidatID" group by k."KandidatID"
       )    ,
     zweite_stimme as (
select k."KandidatID", count(*) as count from kandidaten k ,zweite_stimmzettel e where e."KandidatID" = k."KandidatID" group by k."KandidatID"
       )
select k.*, e2.count + e2.count as gesammt_stimmen from kandidaten k ,erste_stimme e1, zweite_stimme e2 where e1."KandidatID" = k."KandidatID" and e2."KandidatID" = k."KandidatID" order by gesammt_stimmen desc , "Nachname" asc
       );
                                                                                                             
create MATERIALIZED  view erst_stimmzettel as (
select distinct "KandidatID","StimmkreisId" from erste_stimmzettel);





