BEGIN TRANSACTION;

DROP TABLE Instrument;
DROP TABLE Componist;
DROP TABLE Album;
DROP TABLE Performer;
DROP TABLE Piece;

CREATE TABLE Instrument
(
    ID INTEGER PRIMARY KEY,
    Name TEXT
);

CREATE TABLE Componist
(
    ID INTEGER PRIMARY KEY ,
    FirstName TEXT,
    LastName TEXT,
    Born INT,
    Death INT
);
CREATE UNIQUE INDEX Componist__FirstName_LastName_uindex ON Componist (FirstName, LastName);

CREATE TABLE Performer
(
    ID INTEGER PRIMARY KEY ,
    FirstName TEXT,
    LastName TEXT,
    Instrument TEXT,
    Born DATE
);
CREATE UNIQUE INDEX Performer_FirstName_LastName_uindex ON Performer (FirstName, LastName);

CREATE TABLE Collection
(
    ID INTEGER PRIMARY KEY,
    Name TEXT,
    Label TEXT
);

CREATE TABLE Album
(
    ID INTEGER PRIMARY KEY ,
    ComponistID INTEGER,
    PerformerID INTEGER,
    InstrumentID INTEGER,
    CollectionID INTEGER,
    Title TEXT,
    Label TEXT,
    Path TEXT,
    DiskID TEXT,
    FOREIGN KEY (InstrumentID) REFERENCES Instrument(ID),
    FOREIGN KEY (ComponistID) REFERENCES Componist (ID),
    FOREIGN KEY (PerformerID) REFERENCES Performer (ID),
    FOREIGN KEY (CollectionID) REFERENCES Collection(ID)
);
CREATE UNIQUE INDEX Album_ComponistID_Title_uindex ON Album (Title, ComponistID);;

CREATE TABLE Piece
(
    ID INTEGER PRIMARY KEY,
    Name TEXT,
    File TEXT,
    AlbumID INTEGER,
    LibraryCode TEXT,
    FOREIGN KEY (AlbumID) REFERENCES Album (ID)
);
COMMIT;
