 with candidatevotes_ AS (SELECT erste_stimmzettel."StimmkreisId",
                               kandidaten."KandidatID",
                               kandidaten."Vorname",
                               kandidaten."Nachname",
                               kandidaten."ParteiID",
                               count(erste_stimmzettel."KandidatID") AS stimmenzahl
                        FROM erste_stimmzettel
                                 JOIN kandidaten ON erste_stimmzettel."KandidatID" = kandidaten."KandidatID"
                        GROUP BY erste_stimmzettel."StimmkreisId", kandidaten."KandidatID"),


  CandidateVotes_ranked_pro_stimmkreis as (   SELECT
        kgs."StimmkreisId",
        kgs."ParteiID",
        kgs."KandidatID",
        kgs.stimmenzahl,
        ROW_NUMBER() OVER (
            PARTITION BY kgs."StimmkreisId" ORDER BY kgs.stimmenzahl DESC
        ) AS vote_rank
    FROM candidatevotes_ kgs),
     TotalVotesInStimmkreis AS (
    SELECT
        "StimmkreisId",
        SUM(stimmenzahl) AS total_votes
    FROM candidatevotes_
    GROUP BY "StimmkreisId"
),



VictoryMargins AS (
    SELECT
        cv."StimmkreisId",
        cv."ParteiID",
        cv."KandidatID",
        cv.stimmenzahl,
        (cv.stimmenzahl - COALESCE(LAG(cv.stimmenzahl) OVER (
            PARTITION BY cv."StimmkreisId" ORDER BY cv.stimmenzahl DESC
        ), 0)) / tv.total_votes AS relative_margin
    FROM CandidateVotes_ranked_pro_stimmkreis cv
    JOIN TotalVotesInStimmkreis tv ON cv."StimmkreisId" = tv."StimmkreisId"
    WHERE cv.vote_rank = 1
),
TopNarrowestVictories AS (
    SELECT
        vm."ParteiID",
        vm."StimmkreisId",
        vm."KandidatID",
        vm.stimmenzahl,
        vm.relative_margin,
        ROW_NUMBER() OVER (
            PARTITION BY vm."ParteiID" ORDER BY vm.relative_margin ASC
        ) AS rank
    FROM VictoryMargins vm
),
 top_ten_winners_id as (
SELECT
    tnv."ParteiID",
    tnv."StimmkreisId",
    tnv."KandidatID",
    tnv.stimmenzahl,
    tnv.relative_margin,
    tnv.rank
FROM TopNarrowestVictories tnv
WHERE tnv.rank <= 10
ORDER BY tnv."ParteiID", tnv.rank )


 select  k."Vorname", k."Nachname",  t."ParteiID",
    t."StimmkreisId"
 from kandidaten k  ,  top_ten_winners_id  t
 where t."KandidatID" = k."KandidatID";

 ;