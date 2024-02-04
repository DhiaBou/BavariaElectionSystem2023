with candidatevotes_ AS (SELECT erste_stimmzettel."StimmkreisId",
                                kandidaten."KandidatID",
                                kandidaten."Vorname",
                                kandidaten."Nachname",
                                kandidaten."ParteiID",
                                count(erste_stimmzettel."KandidatID") AS stimmenzahl
                         FROM erste_stimmzettel
                                  JOIN kandidaten ON erste_stimmzettel."KandidatID" = kandidaten."KandidatID"
                         GROUP BY erste_stimmzettel."StimmkreisId", kandidaten."KandidatID")
        ,
     vote_rank_distance as (select *
                                 , stimmenzahl - lead(stimmenzahl)
             over
                                (partition by "StimmkreisId" order by stimmenzahl desc) as distance
                                 , rank() over (partition by "StimmkreisId" order by stimmenzahl desc)        as rank_in_stimmkreis
                            from candidatevotes_),
     vote_rank_distance_to_winner AS (SELECT *,
                                             FIRST_VALUE(stimmenzahl)
                                                 OVER (PARTITION BY "StimmkreisId" ORDER BY stimmenzahl DESC) -
                                             stimmenzahl                                                         AS distance_to_first, RANK() OVER (PARTITION BY "StimmkreisId" ORDER BY stimmenzahl DESC) AS rank_in_stimmkreis
                                      FROM candidatevotes_),
     knappester_sieger AS (SELECT p.kurzbezeichnung,
                                  CONCAT(v."Nachname", ', ', v."Vorname") AS name,
                                  v."StimmkreisId"                        as stimmkreisid,
                                  v.distance,
                                  ROW_NUMBER()                               OVER (PARTITION BY p."ParteiID" ORDER BY v.distance ASC) AS rn
                           FROM vote_rank_distance v
                                    JOIN parteien p ON p."ParteiID" = v."ParteiID"
                           WHERE v.rank_in_stimmkreis = 1),
     knappester_loser AS (SELECT p.kurzbezeichnung,
                                 CONCAT(v."Nachname", ', ', v."Vorname") AS name,
                                 v."StimmkreisId",
                                 v.distance_to_first,
                                 ROW_NUMBER()                               OVER (PARTITION BY p."ParteiID" ORDER BY v.distance_to_first ASC) AS rn
                          FROM vote_rank_distance_to_winner v
                                   JOIN parteien p ON p."ParteiID" = v."ParteiID"
                          WHERE v.rank_in_stimmkreis > 1),
     tmp as ((SELECT *, 'winner' as winner_or_loser
              FROM knappester_sieger
              WHERE rn <= 10)
             UNION
             (SELECT *, 'loser'
              FROM knappester_loser kl
              WHERE rn <= 10
                and not exists(select *
                               from vote_rank_distance vrd,
                                    parteien p
                               where p."ParteiID" = vrd."ParteiID"
                                 and vrd.rank_in_stimmkreis = 1
                                 and p.kurzbezeichnung = kl.kurzbezeichnung)))
select *
from tmp
order by kurzbezeichnung, distance