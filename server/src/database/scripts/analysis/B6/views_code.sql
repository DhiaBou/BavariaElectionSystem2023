DROP MATERIALIZED VIEW IF EXISTS Wahlergebnisse_difference_2018_zu_2023;
DROP MATERIALIZED VIEW IF EXISTS Wahlergebnisse2023;
DROP TABLE IF EXISTS wahlergebnisse2018;
DROP MATERIALIZED VIEW IF EXISTS erst_stimmzettel;
DROP MATERIALIZED VIEW IF EXISTS kandidat_gasammt_stimmen;
DROP MATERIALIZED VIEW IF EXISTS gesamt_stimmen_pro_partei_pro_stimmkreis_view;
DROP MATERIALIZED VIEW IF EXISTS direct_candidates;
DROP MATERIALIZED VIEW IF EXISTS anteil_over_five_percent;
DROP MATERIALIZED VIEW IF EXISTS gesamt_stimmen_pro_partei_pro_wahlkreis_view;

CREATE TABLE wahlergebnisse2018
(
    Partei                       VARCHAR(255),
    Erststimmen                  INT,
    Zweitstimmen                 INT,
    Gesamtstimmen                INT,
    SummeInProzent               DECIMAL(5, 2),
    DifferenzZu2013              DECIMAL(5, 2),
    SitzeGesamt                  INT,
    DifferenzSitzeZu2013         INT,
    Direktmandate                INT,
    DifferenzDirektmandateZu2013 INT
);

INSERT INTO wahlergebnisse2018 (Partei, Erststimmen, Zweitstimmen, Gesamtstimmen, SummeInProzent, DifferenzZu2013,
                                SitzeGesamt, DifferenzSitzeZu2013, Direktmandate, DifferenzDirektmandateZu2013)
VALUES ('CSU', 2495186, 2550895, 5046081, 37.2, -10.5, 85, -16, 85, -4),
       ('GRÜNE', 1196575, 1195781, 2392356, 17.6, 9.0, 38, 20, 6, 6),
       ('FREIE WÄHLER', 809666, 763126, 1572792, 11.6, 2.6, 27, 8, 0, 0),
       ('AfD', 701384, 687238, 1388622, 10.2, 10.2, 22, 22, 0, 0),
       ('SPD', 680180, 628898, 1309078, 9.7, -11.0, 22, -20, 0, -1),
       ('FDP', 353800, 336699, 690499, 5.1, 1.8, 11, 11, 0, 0),
       ('DIE LINKE', 220031, 217857, 437888, 3.2, 1.1, NULL, NULL, NULL, NULL),
       ('BP', 122266, 109465, 231731, 1.7, -0.4, NULL, NULL, NULL, NULL),
       ('ÖDP', 111212, 100739, 211951, 1.6, -0.5, NULL, NULL, NULL, NULL),
       ('PIRATEN', 23900, 35245, 59145, 0.4, -1.5, NULL, NULL, NULL, NULL),
       ('Die PARTEI', 18561, 40535, 59096, 0.4, 0.4, NULL, NULL, NULL, NULL),
       ('mut', 17992, 27498, 45490, 0.3, 0.3, NULL, NULL, NULL, NULL),
       ('Tierschutzpartei', 11616, 29281, 40897, 0.3, 0.3, NULL, NULL, NULL, NULL),
       ('V-Partei³', 15266, 19243, 34509, 0.3, 0.3, NULL, NULL, NULL, NULL),
       ('DIE FRANKEN', 17075, 14378, 31453, 0.2, -0.5, NULL, NULL, NULL, NULL),
       ('Gesundheitsforschung', 1006, 6744, 7750, 0.1, 0.1, NULL, NULL, NULL, NULL),
       ('Die Humanisten', 159, 3234, 3393, 0.0, 0.0, NULL, NULL, NULL, NULL),
       ('LKR', 374, 1642, 2016, 0.0, 0.0, NULL, NULL, NULL, NULL);



create MATERIALIZED view gesamt_stimmen_pro_partei_pro_wahlkreis_view as
(
WITH gesamt_erststimmen_pro_partei_pro_wahlkreis AS (SELECT w."WahlkreisId"       AS wahlkreisid,
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
create MATERIALIZED view anteil_over_five_percent as
(
WITH totalvotes AS (SELECT g.wahlkreisid,
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


create MATERIALIZED view direct_candidates as
(
with candidatevotes AS (SELECT erste_stimmzettel."StimmkreisId",
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
create MATERIALIZED view gesamt_stimmen_pro_partei_pro_stimmkreis_view as
(
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
                                                                       GROUP BY s."StimmkreisId", s."Name", p."ParteiID", p."Name"),
     gesamt_stimmen_pro_partei_pro_stimmkreis AS (SELECT g1.stimmkreisid,
                                                         g1.stimmkreisname,
                                                         g1.parteiid,
                                                         g1.parteiname,
                                                         g1.erststimmen + g2.zweitstimmen + g3.zweitstimmen_ohne_kandidaten AS gesamt_stimmen,
                                                         g1.erststimmen,
                                                         g2.zweitstimmen + g3.zweitstimmen_ohne_kandidaten                  as zweite_stimme
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
create MATERIALIZED view kandidat_gasammt_stimmen as
(
with erste_stimme as (select k."KandidatID", count(*) as count
                      from kandidaten k,
                           erste_stimmzettel e
                      where e."KandidatID" = k."KandidatID"
                      group by k."KandidatID"),
     zweite_stimme as (select k."KandidatID", count(*) as count
                       from kandidaten k,
                            zweite_stimmzettel e
                       where e."KandidatID" = k."KandidatID"
                       group by k."KandidatID")
select k.*, e2.count + e2.count as gesammt_stimmen
from kandidaten k,
     erste_stimme e1,
     zweite_stimme e2
where e1."KandidatID" = k."KandidatID"
  and e2."KandidatID" = k."KandidatID"
order by gesammt_stimmen desc, "Nachname" asc
    );

create MATERIALIZED view erst_stimmzettel as
(
select distinct "KandidatID", "StimmkreisId"
from erste_stimmzettel);

create MATERIALIZED VIEW Wahlergebnisse2023 as
(
with seats_party as (select p."ParteiID", count(*) as seats
                     from abgeordnete a,
                          kandidaten k,
                          parteien p
                     where a."KandidatID" = k."KandidatID"
                       and p."ParteiID" = k."ParteiID"
                     group by p."ParteiID"),
     anzahl_direct_candidates_pro_party as (select d."ParteiID", count(*) as anz_direct_candidates
                                            from direct_candidates d
                                            group by d."ParteiID")
        ,
     total_votes as (select sum(gesamt_stimmen) as total
                     from gesamt_stimmen_pro_partei_pro_stimmkreis_view),
     without_percentage as (select g.parteiid,
                                   parteiname,
                                   coalesce(seats, 0)                 as seats,
                                   coalesce(anz_direct_candidates, 0) as direct_candidates,
                                   sum(gesamt_stimmen)                as Gesamt_stimmen,
                                   sum(erststimmen)                   as Erststimmen,
                                   sum(zweite_stimme)                 as Zweitestimmen
                            from gesamt_stimmen_pro_partei_pro_stimmkreis_view g
                                     left outer join seats_party s on
                                g.parteiid = s."ParteiID"
                                     left outer join anzahl_direct_candidates_pro_party a on a."ParteiID" = s."ParteiID"
                            group by g.ParteiID, parteiname, seats, direct_candidates)
select w.*, Round(w.gesamt_stimmen / total, 4) * 100 as Vote_percentage
from without_percentage w,
     total_votes
    );


create MATERIALIZED VIEW Wahlergebnisse_difference_2018_zu_2023 as
(
select w.parteiid,
       w.parteiname,
       w.erststimmen,
       w.zweitestimmen,
       w.gesamt_stimmen,
       coalesce(w_old.erststimmen, 0)             as erstimmen2018,
       coalesce(w_old.zweitstimmen, 0)            as zweitstimmen2018,
       coalesce(w_old.gesamtstimmen, 0)           as gesammtstimmen2018,
       w.vote_percentage,
       (w.vote_percentage - w_old.summeinprozent) as difference_gesamt_stimmen,
       w.seats                                    as Anzahl_Sitze,
       (w.seats - w_old.sitzegesamt)              as difference_Anzahl_sitze
from wahlergebnisse2023 w
         join parteien p on p."ParteiID" = w.parteiid
         left outer join wahlergebnisse2018 w_old on p.kurzbezeichnung = w_old.partei

    );




