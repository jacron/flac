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


SELECT
    FirstName,
    LastName,
    Birth,
    Death,
    Performer.Path,
    Performer.ID
FROM Performer_Album
    JOIN Performer ON Performer.ID = Performer_Album.PerformerID
    JOIN Album ON Album.ID = Performer_Album.AlbumID
WHERE Performer_Album.AlbumID = 25;


        SELECT
            FirstName,
            LastName,
            Performer.ID
        FROM Performer_Album
            JOIN Performer ON Performer.ID = Performer_Album.PerformerID
            JOIN Album ON Album.ID = Performer_Album.AlbumID
        WHERE Performer_Album.AlbumID =23;

