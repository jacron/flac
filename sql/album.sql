CREATE TABLE Album
(
    ID INTEGER PRIMARY KEY,
    ComponistID INTEGER,
    PerformerID INTEGER,
    InstrumentID INTEGER,
    Title TEXT,
    Label TEXT,
    DiskID TEXT,
    FOREIGN KEY (InstrumentID) REFERENCES Instrument(ID),
    FOREIGN KEY (ComponistID) REFERENCES Componist (ID),
    FOREIGN KEY (PerformerID) REFERENCES Performer (ID)
);
CREATE UNIQUE INDEX sqlite_autoindex_Album_1 ON Album (Title, ComponistID)