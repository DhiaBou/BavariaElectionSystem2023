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
                                                 over (partition by "StimmkreisId" order by stimmenzahl desc) as distance
                                 , rank() over (partition by "StimmkreisId" order by stimmenzahl desc)        as rank_in_stimmkreis
                            from candidatevotes_),
     knappester_sieger AS (SELECT p.kurzbezeichnung,
                                  CONCAT(v."Nachname", ', ', v."Vorname")                               AS name,
                                  v.distance,
                                  ROW_NUMBER() OVER (PARTITION BY p."ParteiID" ORDER BY v.distance ASC) AS rn
                           FROM vote_rank_distance v
                                    JOIN parteien p ON p."ParteiID" = v."ParteiID"
                           WHERE v.rank_in_stimmkreis = 1),
     tmp as (SELECT *
             FROM (SELECT kurzbezeichnung, name as kandidate_name, (select '') as stimmkreis_name, distance
                   FROM knappester_sieger
                   WHERE rn <= 10)
             UNION
             (SELECT p.kurzbezeichnung, (select ''), s."Name", v.distance
              FROM vote_rank_distance v
                       JOIN parteien p ON p."ParteiID" = v."ParteiID"
                       join stimmkreis s on s."StimmkreisId" = v."StimmkreisId"
              WHERE not exists(select *
                               from vote_rank_distance v2
                               where v2."ParteiID" = v."ParteiID" and v2.rank_in_stimmkreis = 1)
                and v.distance =
                    (SELECT min(v2.distance)
                     FROM vote_rank_distance v2
                     WHERE v2."ParteiID" = v."ParteiID")))
select *
from tmp
order by kurzbezeichnung, distance