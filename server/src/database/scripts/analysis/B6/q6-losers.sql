with candidatevotes_ AS (SELECT erste_stimmzettel."StimmkreisId",
                                kandidaten."KandidatID",
                                kandidaten."Vorname",
                                kandidaten."Nachname",
                                kandidaten."ParteiID",
                                count(erste_stimmzettel."KandidatID") AS stimmenzahl
                         FROM erste_stimmzettel
                                  JOIN kandidaten ON erste_stimmzettel."KandidatID" = kandidaten."KandidatID"
                         GROUP BY erste_stimmzettel."StimmkreisId", kandidaten."KandidatID"),


     PartiesWithNoWin AS (select Distinct p."ParteiID"
                          from candidatevotes_ p
                          where p."ParteiID" not in (select Distinct "ParteiID" from direct_candidates)),
     TotalVotesInStimmkreis AS (SELECT "StimmkreisId",
                                       SUM(stimmenzahl) AS total_votes
                                FROM candidatevotes_
                                GROUP BY "StimmkreisId"),
     ClosestLosers AS (SELECT cv."StimmkreisId",
                              cv."ParteiID",
                              cv."KandidatID",
                              cv.stimmenzahl,
                              (wc.stimmenzahl - cv.stimmenzahl) / CAST(tv.total_votes AS FLOAT) AS relative_loss_margin,
                              ROW_NUMBER()                                                         OVER (
            PARTITION BY cv."StimmkreisId"
            ORDER BY cv.stimmenzahl DESC
        ) AS rank_in_stimmkreis
                       FROM candidatevotes_ cv
                                JOIN direct_candidates wc ON cv."StimmkreisId" = wc."StimmkreisId"
                                JOIN TotalVotesInStimmkreis tv ON cv."StimmkreisId" = tv."StimmkreisId"
                       WHERE cv."ParteiID" IN (SELECT "ParteiID" FROM PartiesWithNoWin)),
     TopClosestLosers AS (SELECT cl."ParteiID",
                                 cl."StimmkreisId",
                                 cl."KandidatID",
                                 cl.stimmenzahl,
                                 cl.relative_loss_margin,
                                 ROW_NUMBER() OVER (
            PARTITION BY cl."ParteiID"
            ORDER BY cl.relative_loss_margin ASC
        ) AS rank
                          FROM ClosestLosers cl),
     closest_losers_ids as (SELECT tcl."ParteiID",
                                   tcl."StimmkreisId",
                                   tcl."KandidatID",
                                   tcl.stimmenzahl,
                                   tcl.relative_loss_margin

                            FROM TopClosestLosers tcl
                            WHERE tcl.rank <= 10
                            ORDER BY tcl."ParteiID", tcl.rank)

select k."Vorname",
       k."Nachname",
       c."ParteiID",
       c."StimmkreisId"
from kandidaten k,
     closest_losers_ids c
where c."KandidatID" = k."KandidatID";
