--q5
select "WahlkreisId", "ParteiID", count(*) from ueberhangsmandate group by "WahlkreisId", "ParteiID";
