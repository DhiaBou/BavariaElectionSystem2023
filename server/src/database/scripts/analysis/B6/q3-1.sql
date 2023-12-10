-- q3.1
select * from direct_candidates;
-- q3.2
with anzahl_stimmen_pro_stimmkreis as (
    select
        g.stimmkreisid, sum(g.gesamt_stimmen) as sum
    from gesamt_stimmen_pro_partei_pro_stimmkreis_view g
    group by g.stimmkreisid
)
select g.stimmkreisid, g.parteiname, g.gesamt_stimmen, g.gesamt_stimmen * 100.00 / a.sum as percentage, (select d."Vorname" from direct_candidates d where d."StimmkreisId"=a.stimmkreisid and d."ParteiID" = g.parteiid) from gesamt_stimmen_pro_partei_pro_stimmkreis_view g, anzahl_stimmen_pro_stimmkreis a
where a.stimmkreisid = g.stimmkreisid
