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

 UPDATE Album
    SET Title='Socrate (2016)'
    WHERE Album.ID=23;

 SELECT Name, ID from Piece
      WHERE LibraryCode LIKE 'K%'
      ORDER BY LibraryCode;

update Piece
set LibraryCode = 'K ' || Piece.LibraryCode
where LibraryCode!=0 and Piece.LibraryCode not like 'K%';

    SELECT LibraryCode, Name, Performer.FirstName, Performer.LastName, Piece.ID
      from Piece
       join Album
       on Piece.AlbumID = Album.ID
       join Performer_Album
       on Performer_Album.AlbumID = Album.ID
       join Performer
       on Performer_Album.PerformerID = Performer.ID
      WHERE LibraryCode LIKE 'K%'
      ORDER BY LENGTH(LibraryCode), LibraryCode;

    SELECT
      Child.Title,
      Child.Label,
      Child.Path,
      Child.ComponistID,
      Child.AlbumID,
      Mother.Title,
      Child.ID
    from Album as Child
    join Album as Mother
    on Child.AlbumID = Mother.ID
    WHERE Child.ID=36;

UPDATE Album
SET Title = REPLACE(
    Title,
    'archivproduktion19472013',
    'Archiv Produktion 1947-2013 - ')
where Title LIKE ('archivproduktion19472013%');

select Title from Album
where Album.Title LIKE ('archivproduktion19472013%');

update Album
set ComponistID=9  -- bach
where ID in (95, 96, 97, 100, 101, 103, 104, 105, 106);

INSERT INTO Componist_Album (ComponistID, AlbumID)
    select ComponistID, ID FROM Album
WHERE ComponistID=4;

    select ComponistID, ID FROM Album
where ComponistID=8;

    SELECT
            FirstName,
            LastName,
            Componist.ID
        FROM Componist_Album
            JOIN Componist ON Componist.ID = Componist_Album.ComponistID
            JOIN Album ON Album.ID = Componist_Album.AlbumID
        WHERE
          Componist_Album.AlbumID =95;

  SELECT
ComponistID        FROM Componist_Album
        WHERE Componist_Album.AlbumID =95;


 SELECT Title, Album.ID, Componist.FirstName, Componist.LastName
      from Album
      LEFT JOIN Componist_Album ON Componist_Album.AlbumID=Album.ID
      LEFT JOIN Componist ON Componist.ID=Componist_Album.ComponistID
      WHERE Album.AlbumID=94
      GROUP BY Title
      ORDER BY Title COLLATE NOCASE;

select * from Piece
where AlbumID=151;

select Name from Piece
where Piece.AlbumID not in (select ID from Album);

select C.*
from Piece C
left join Album M
on M.ID = C.AlbumID
where M.ID ISNULL ;

update Album set IsCollection=0
where Title like 'BBCL%';

select Title from Album
where Title like 'BBCL%';

select Title from Album
where AlbumID=168 and Title like 'cd %';

update Album
set AlbumID=194
where AlbumID=168 and Title like 'cd %';

--    path="/Volumes/Media/Audio/Klassiek/Componisten/Bach/Cello"
select Title, ID from Album
where Path like '/Volumes/Media/Audio/Klassiek/Componisten/Bach/Cello%';

update Album
set AlbumID=2221
where ID in (2160,2153,2159,2163,2166,2167,2164,2165,2162,2156);

select Title
from Album
where ID in (2160,2153,2159,2163,2166,2167,2164,2165,2162,2156);
