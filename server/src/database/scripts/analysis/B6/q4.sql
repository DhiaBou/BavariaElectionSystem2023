--q4
WITH Erststimmen_Max AS (SELECT stimmkreisid,
                                parteiid,
                                parteiname,
                                erststimmen,
                                RANK() OVER (PARTITION BY stimmkreisid ORDER BY erststimmen DESC) as rank
                         FROM gesamt_stimmen_pro_partei_pro_stimmkreis_view),
     Zweitstimmen_Max AS (SELECT stimmkreisid,
                                 parteiid,
                                 parteiname,
                                 zweite_stimme,
                                 RANK() OVER (PARTITION BY stimmkreisid ORDER BY zweite_stimme DESC) as rank
                          FROM gesamt_stimmen_pro_partei_pro_stimmkreis_view)
SELECT e.stimmkreisid,
       e.parteiname as erststimmen_stimmkreissieger,
       z.parteiname as zweitstimmen_stimmkreissieger
FROM Erststimmen_Max e
         JOIN Zweitstimmen_Max z ON e.stimmkreisid = z.stimmkreisid
WHERE e.rank = 1
  AND z.rank = 1;
