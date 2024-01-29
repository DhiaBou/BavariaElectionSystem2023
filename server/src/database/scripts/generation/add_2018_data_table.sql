CREATE TABLE wahlergebnisse2018
(
    Partei                       VARCHAR(255),
    Erststimmen                  INT,
    Zweitstimmen                 INT,
    Gesamtstimmen                INT,
    SummeInProzent               DECIMAL(5, 2),
    DifferenzZu2013              DECIMAL(5, 2),
    SitzeGesamt                  INT,
    DifferenzSitzeZu2013         INT,
    Direktmandate                INT,
    DifferenzDirektmandateZu2013 INT
);

INSERT INTO wahlergebnisse2018 (Partei, Erststimmen, Zweitstimmen, Gesamtstimmen, SummeInProzent, DifferenzZu2013,
                                SitzeGesamt, DifferenzSitzeZu2013, Direktmandate, DifferenzDirektmandateZu2013)
VALUES ('CSU', 2495186, 2550895, 5046081, 37.2, -10.5, 85, -16, 85, -4),
       ('GRÜNE', 1196575, 1195781, 2392356, 17.6, 9.0, 38, 20, 6, 6),
       ('FREIE WÄHLER', 809666, 763126, 1572792, 11.6, 2.6, 27, 8, 0, 0),
       ('AfD', 701384, 687238, 1388622, 10.2, 10.2, 22, 22, 0, 0),
       ('SPD', 680180, 628898, 1309078, 9.7, -11.0, 22, -20, 0, -1),
       ('FDP', 353800, 336699, 690499, 5.1, 1.8, 11, 11, 0, 0),
       ('DIE LINKE', 220031, 217857, 437888, 3.2, 1.1, NULL, NULL, NULL, NULL),
       ('BP', 122266, 109465, 231731, 1.7, -0.4, NULL, NULL, NULL, NULL),
       ('ÖDP', 111212, 100739, 211951, 1.6, -0.5, NULL, NULL, NULL, NULL),
       ('PIRATEN', 23900, 35245, 59145, 0.4, -1.5, NULL, NULL, NULL, NULL),
       ('Die PARTEI', 18561, 40535, 59096, 0.4, 0.4, NULL, NULL, NULL, NULL),
       ('mut', 17992, 27498, 45490, 0.3, 0.3, NULL, NULL, NULL, NULL),
       ('Tierschutzpartei', 11616, 29281, 40897, 0.3, 0.3, NULL, NULL, NULL, NULL),
       ('V-Partei³', 15266, 19243, 34509, 0.3, 0.3, NULL, NULL, NULL, NULL),
       ('DIE FRANKEN', 17075, 14378, 31453, 0.2, -0.5, NULL, NULL, NULL, NULL),
       ('Gesundheitsforschung', 1006, 6744, 7750, 0.1, 0.1, NULL, NULL, NULL, NULL),
       ('Die Humanisten', 159, 3234, 3393, 0.0, 0.0, NULL, NULL, NULL, NULL),
       ('LKR', 374, 1642, 2016, 0.0, 0.0, NULL, NULL, NULL, NULL);