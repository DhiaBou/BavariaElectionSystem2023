from sqlalchemy import Boolean, Column, Integer, String


from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Parteien(Base):
    __tablename__ = "parteien"
    ParteiID = Column(Integer, primary_key=True)
    Name = Column(String)
    kurzbezeichnung = Column(String)


class Waehler(Base):
    __tablename__ = "waehler"
    WaehlerID = Column(Integer, primary_key=True)
    Vorname = Column(String)
    Nachname = Column(String)
    Geburtsdatum = Column(Date)
    StimmkreisId = Column(Integer, ForeignKey("stimmkreis.StimmkreisId"))


class Stimmkreis(Base):
    __tablename__ = "stimmkreis"
    StimmkreisId = Column(Integer, primary_key=True)
    Name = Column(String)
    Stimmberechtigte = Column(Integer)
    WahlkreisId = Column(Integer, ForeignKey("wahlkreis.WahlkreisId"))


class Kandidaten(Base):
    __tablename__ = "kandidaten"
    KandidatID = Column(Integer, primary_key=True)
    Vorname = Column(String)
    Nachname = Column(String)
    ParteiID = Column(Integer, ForeignKey("parteien.ParteiID"))
    StimmkreisId = Column(Integer, ForeignKey("stimmkreis.StimmkreisId"), nullable=True)
    ListenNummer = Column(Integer)


class Erste_Stimmen(Base):
    __tablename__ = "erste_stimmzettel"
    Erste_StimmzettelID = Column(Integer, primary_key=True)
    KandidatID = Column(Integer, ForeignKey("kandidaten.KandidatID"))
    StimmkreisId = Column(Integer, ForeignKey("stimmkreis.StimmkreisId"))


class Zweite_Stimmzettel(Base):
    __tablename__ = "zweite_stimmzettel"
    Zweite_StimmzettelID = Column(Integer, primary_key=True)
    KandidatID = Column(Integer, ForeignKey("kandidaten.KandidatID"))
    StimmkreisId = Column(Integer, ForeignKey("stimmkreis.StimmkreisId"))


class Wahlkreis(Base):
    __tablename__ = "wahlkreis"
    __table_args__ = {"extend_existing": True}

    WahlkreisId = Column(Integer, primary_key=True)
    Name = Column(String)
    Abgeordnetenmandate = Column(Integer)


class Zweite_Stimme_Ohne_Kandidaten(Base):
    __tablename__ = "zweite_stimme_ohne_kandidaten"
    id = Column(Integer, primary_key=True)
    StimmkreisId = Column(Integer, ForeignKey("stimmkreis.StimmkreisId"))
    ParteiID = Column(Integer, ForeignKey("parteien.ParteiID"))
