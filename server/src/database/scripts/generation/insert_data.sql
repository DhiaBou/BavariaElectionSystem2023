INSERT INTO wahlkreis("WahlkreisId", "Name", "Abgeordnetenmandate")
VALUES (901, 'Oberbayern', 61),
       (902, 'Niederbayern', 18),
       (903, 'Oberpfalz', 16),
       (904, 'Oberfranken', 16),
       (905, 'Mittelfranken', 24),
       (906, 'Unterfranken', 19),
       (907, 'Schwaben', 26);

INSERT INTO stimmkreis("StimmkreisId",  "Name", "Stimmberechtigte", "WahlkreisId")
VALUES (101,'München-Hadern',98320,901),
(102,'München-Bogenhausen',86064,901),
(103,'München-Giesing',123365,901),
(104,'München-Milbertshofen',106590,901),
(105,'München-Moosach',95838,901),
(106,'München-Pasing',113745,901),
(107,'München-Ramersdorf',105532,901),
(108,'München-Schwabing',90960,901),
(109,'München-Mitte',89670,901),
(110,'Altötting',81837,901),
(111,'Bad Tölz-Wolfratshausen Garmisch-Partenkirchen',124169,901),
(112,'Berchtesgadener Land',94118,901),
(113,'Dachau',105133,901),
(114,'Ebersberg',99620,901),
(115,'Eichstätt',98262,901),
(116,'Erding',100244,901),
(117,'Freising',120611,901),
(118,'Fürstenfeldbruck-Ost',115125,901),
(119,'Ingolstadt',88380,901),
(120,'Landsberg am Lech Fürstenfeldbruck-West',126865,901),
(121,'Miesbach',86860,901),
(122,'Mühldorf a.Inn',85893,901),
(123,'München-Land-Nord',117322,901),
(124,'München-Land-Süd',114782,901),
(125,'Neuburg-Schrobenhausen',82521,901),
(126,'Pfaffenhofen a.d.Ilm',83487,901),
(127,'Rosenheim-Ost',111416,901),
(128,'Rosenheim-West',110999,901),
(129,'Starnberg',102352,901),
(130,'Traunstein',113330,901),
(131,'Weilheim-Schongau',129001,901),
(201,'Deggendorf',90871,902),
(202,'Dingolfing',113713,902),
(203,'Kelheim',88537,902),
(204,'Landshut',125480,902),
(205,'Passau-Ost',116773,902),
(206,'Passau-West',91847,902),
(207,'Regen Freyung-Grafenau',102878,902),
(208,'Rottal-Inn',91483,902),
(209,'Straubing',111662,902),
(301,'Amberg-Sulzbach',112521,903),
(302,'Cham',101618,903),
(303,'Neumarkt i.d.OPf.',101714,903),
(304,'Regensburg-Land',125815,903),
(305,'Regensburg-Stadt',127108,903),
(306,'Schwandorf',114383,903),
(307,'Tirschenreuth',79921,903),
(308,'Weiden i.d.OPf.',83680,903),
(401,'Bamberg-Land',84945,904),
(402,'Bamberg-Stadt',84971,904),
(403,'Bayreuth',126445,904),
(404,'Coburg',98960,904),
(405,'Forchheim',89855,904),
(406,'Hof',106015,904),
(407,'Kronach Lichtenfels',105179,904),
(408,'Wunsiedel Kulmbach',123720,904),
(501,'Nürnberg-Nord',99119,905),
(502,'Nürnberg-Ost',95738,905),
(503,'Nürnberg-Süd',95582,905),
(504,'Nürnberg-West',89539,905),
(505,'Ansbach-Nord',115412,905),
(506,'Ansbach-Süd Weissenburg-Gunzenhausen',126068,905),
(507,'Erlangen-Höchstadt',94323,905),
(508,'Erlangen-Stadt',85416,905),
(509,'Fürth',129900,905),
(510,'Neustadt a.d.Aisch-Bad Windsheim Fürth-Land',124296,905),
(511,'Nürnberger Land',108614,905),
(512,'Roth',98244,905),
(601,'Aschaffenburg-Ost',87813,906),
(602,'Aschaffenburg-West',92664,906),
(603,'Bad Kissingen',96776,906),
(604,'Hassberge Rhön-Grabfeld',114595,906),
(605,'Kitzingen',86288,906),
(606,'Main-Spessart',98118,906),
(607,'Miltenberg',94300,906),
(608,'Schweinfurt',108232,906),
(609,'Würzburg-Land',117144,906),
(610,'Würzburg-Stadt',104300,906),
(701,'Augsburg-Stadt-Ost',107797,907),
(702,'Augsburg-Stadt-West',109163,907),
(703,'Aichach-Friedberg',101113,907),
(704,'Augsburg-Land Dillingen',112661,907),
(705,'Augsburg-Land-Süd',117476,907),
(706,'Donau-Ries',100364,907),
(707,'Günzburg',90085,907),
(708,'Kaufbeuren',92655,907),
(709,'Kempten Oberallgäu',107588,907),
(710,'Lindau Sonthofen',118666,907),
(711,'Marktoberdorf',97558,907),
(712,'Memmingen',97347,907),
(713,'Neu-Ulm',113141,907);

INSERT
INTO Parteien("Name", kurzbezeichnung)
VALUES ('Christlich-Soziale Union in Bayern e.V.', 'CSU'),
       ('BÜNDNIS 90/DIE GRÜNEN', 'GRÜNE'),
       ('FREIE WÄHLER Bayern', 'FREIE WÄHLER'),
       ('Alternative für Deutschland', 'AfD'),
       ('Sozialdemokratische Partei Deutschlands', 'SPD'),
       ('Freie Demokratische Partei', 'FDP'),
       ('DIE LINKE', 'DIE LINKE'),
       ('Bayernpartei', 'BP'),
       ('Ökologisch-Demokratische Partei', 'ÖDP'),
       ('Partei für Arbeit, Rechtsstaat, Tierschutz, Elitenförderung und basisdemokratische Initiative', 'Die PARTEI'),
       ('PARTEI MENSCH UMWELT TIERSCHUTZ', 'Tierschutzpartei'),
       ('V-Partei³ – Partei für Veränderung, Vegetarier und Veganer', 'V-Partei³'),
       ('Partei der Humanisten', 'PdH'),
       ('Basisdemokratische Partei Deutschland', 'dieBasis'),
       ('Volt Deutschland', 'Volt'),
       ('Piratenpartei Deutschland', 'PIRATEN'),
       ('Partei für Franken', 'DIE FRANKEN'),
       ('Liberal-Konservative Reformer - Die EURO-Kritiker', 'LKR'),
       ('mut', 'mut'),
       ('Partei für Gesundheitsforschung', 'Gesundheitsforschung');


CREATE TABLE IF NOT EXISTS wahlergebnisse2018
(
    Partei VARCHAR
(
    255
),
    Erststimmen INT,
    Zweitstimmen INT,
    Gesamtstimmen INT,
    SummeInProzent DECIMAL
(
    5,
    2
),
    DifferenzZu2013 DECIMAL
(
    5,
    2
),
    SitzeGesamt INT,
    DifferenzSitzeZu2013 INT,
    Direktmandate INT,
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

CREATE TABLE IF NOT EXISTS Einkommen_pro_wahlkreis
(
    WahlkreisID
    INT,
    Einkommen
    INT
);

INSERT INTO Einkommen_pro_wahlkreis (WahlkreisID, Einkommen)
VALUES (901, 29909),
       (902, 24756),
       (903, 24561),
       (904, 24459),
       (905, 25440),
       (906, 24962),
       (907, 25343);
