SELECT w."Name", p.kurzbezeichnung, CAST(an.anteil AS DECIMAL(10, 2)), ein.einkommen
from anteil_over_five_percent an,
     wahlkreis w,
     einkommen_pro_wahlkreis ein,
     parteien p
where p."ParteiID" = an.parteiid
  and ein.wahlkreisid = w."WahlkreisId"
  and an.wahlkreisid = w."WahlkreisId"