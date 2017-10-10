CREATE TABLE Album
(
    ID INTEGER PRIMARY KEY ,
    ComponistID INTEGER,
    PerformerID INTEGER,
    InstrumentID INTEGER,
    Title TEXT,
    Label TEXT,
    Path TEXT,
    DiskID TEXT,
    FOREIGN KEY (InstrumentID) REFERENCES Instrument(ID),
    FOREIGN KEY (ComponistID) REFERENCES Componist (ID),
    FOREIGN KEY (PerformerID) REFERENCES Performer (ID)
);
CREATE UNIQUE INDEX Album_ComponistID_Title_uindex ON Album (Title, ComponistID)