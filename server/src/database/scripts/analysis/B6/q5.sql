--q5
select "WahlkreisId", p.kurzbezeichnung as parteiname, count(*) as anzahl_ueberhangsmandate
from ueberhangsmandate ue,
     parteien p
where p."ParteiID" = ue."ParteiID"
group by "WahlkreisId", p.kurzbezeichnung
order by ue."WahlkreisId";
