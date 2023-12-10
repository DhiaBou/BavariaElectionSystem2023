-- q3.1
select d."StimmkreisId", d.stimmkreisname, CONCAT(d."Nachname",  ', ', d."Vorname") from direct_candidates d;
-- q3.2
with anzahl_stimmen_pro_stimmkreis as (
    select
        g.stimmkreisid, sum(g.gesamt_stimmen) as sum
    from gesamt_stimmen_pro_partei_pro_stimmkreis_view g
    group by g.stimmkreisid
)


select g.stimmkreisid, g.parteiname, g.gesamt_stimmen,ROUND(g.gesamt_stimmen * 100.00 / a.sum, 2) AS percentage, (select CONCAT(d."Nachname",  ', ', d."Vorname") from direct_candidates d where d."StimmkreisId"=a.stimmkreisid and d."ParteiID" = g.parteiid) as gewähle_kandidaten from gesamt_stimmen_pro_partei_pro_stimmkreis_view g, anzahl_stimmen_pro_stimmkreis a
where a.stimmkreisid = g.stimmkreisid;


--q1
select k."ParteiID", count(*) from   abgeordnete a, kandidaten k where a."KandidatID" = k."KandidatID" group by k."ParteiID";

--q2
select CONCAT(k."Nachname",  ', ', k."Vorname"), k."ParteiID"  from   abgeordnete a, kandidaten k where a."KandidatID" = k."KandidatID";

--q4
WITH Erststimmen_Max AS (
    SELECT stimmkreisid,
           parteiid,
           parteiname,
           erststimmen,
           RANK() OVER (PARTITION BY stimmkreisid ORDER BY erststimmen DESC) as rank
    FROM gesamt_stimmen_pro_partei_pro_stimmkreis_view
),
Zweitstimmen_Max AS (
    SELECT stimmkreisid,
           parteiid,
           parteiname,
           zweite_stimme,
           RANK() OVER (PARTITION BY stimmkreisid ORDER BY zweite_stimme DESC) as rank
    FROM gesamt_stimmen_pro_partei_pro_stimmkreis_view
)
SELECT e.stimmkreisid,
       e.parteiname as parteiname_erststimmen,
       z.parteiname as parteiname_zweitstimmen
FROM Erststimmen_Max e
JOIN Zweitstimmen_Max z ON e.stimmkreisid = z.stimmkreisid
WHERE e.rank = 1 AND z.rank = 1;

--q5
select "WahlkreisId", "ParteiID", count(*) from ueberhangsmandate group by "WahlkreisId", "ParteiID";

--q6
with ranking as (select g.*, rank() over ( partition by g.stimmkreisid order by g.erststimmen desc) as rank
                 from gesamt_stimmen_pro_partei_pro_stimmkreis_view g)
, ranking_sorted as ( select r.*, r.erststimmen - (select r2. erststimmen from ranking r2 where r2.rank=2 and r2.stimmkreisid = r.stimmkreisid) as difference from ranking r where r.rank = 1 order by difference)
select  d."ParteiID", d."StimmkreisId" from direct_candidates d,  (select r.difference from ranking_sorted r where r.parteiid = d."ParteiID" order by difference limit  10)




