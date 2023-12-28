-- q3.1
select d."StimmkreisId", d.stimmkreisname, CONCAT(d."Nachname",  ', ', d."Vorname") as Kandidat from direct_candidates d;
-- q3.2
with anzahl_stimmen_pro_stimmkreis as (
    select
        g.stimmkreisid, sum(g.gesamt_stimmen) as sum
    from gesamt_stimmen_pro_partei_pro_stimmkreis_view g
    group by g.stimmkreisid
),

voters_pro_stimmkreis as  (select "StimmkreisId" , count(*) as Count_Voters from erste_stimmzettel group by "StimmkreisId"),
wahlbeteiligung as (select s."StimmkreisId", v.count_voters , s."Stimmberechtigte",  ROUND(v.Count_Voters * 100.0 / s."Stimmberechtigte", 2)as Wahlbeteiligung from voters_pro_stimmkreis v, stimmkreis s where s."StimmkreisId" = v."StimmkreisId")


--q3

select g.stimmkreisid,
       g.parteiname,
       w.wahlbeteiligung,
       g.gesamt_stimmen,
       ROUND(g.gesamt_stimmen * 100.00 / a.sum, 2) AS percentage,
       COALESCE((SELECT CONCAT(d."Nachname", ', ', d."Vorname")
              FROM direct_candidates d
              WHERE d."StimmkreisId" = a.stimmkreisid AND d."ParteiID" = g.parteiid), 'none') AS gewählte_kandidaten
from gesamt_stimmen_pro_partei_pro_stimmkreis_view g, anzahl_stimmen_pro_stimmkreis a, wahlbeteiligung w
where a.stimmkreisid = g.stimmkreisid and w."StimmkreisId" = a.stimmkreisid;
