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

select Title, Path
from Album
where ID in (2348, 2352, 2349, 2346, 2347, 2350, 2351);

select ID, Title from Album
where AlbumID=169;

select ID from Album
where Title='BBCL4015 - Gilels - Schumane, Scarlatti, Bach';

select ID, Path
from Album
where Path in (
  select Path
  from Album
  group by Path
  having COUNT(*) = 1
);

-- select albums that have no children?
  select AlbumID from Album
  group by AlbumID;

select a.ID, a.AlbumID from Album as a
where a.AlbumID is not null;

select
  ID
from
  Album
where
  ID not in (
  select
    AlbumID
  from
    Album
    GROUP BY AlbumID
);


-- select album without pieces
  select AlbumID from Piece
  group by AlbumID;
-- 4735
select id,AlbumID from Album
WHERE ID BETWEEN 4735 and 5151 AND ID in (
  select AlbumID from Piece
  group by AlbumID
);

update Album
set AlbumID = 5025
where AlbumID=4735;
select id from Album
where AlbumID=4735;

select * from Componist
where LastName='Sweelinc';


select ID, Path
from Album
where Path IN (
  select Path from Album
  where ID IN (
    select ID
FROM (
  SELECT
    ID,
    Path,
    COUNT(*) AS c
  FROM Album
  GROUP BY Path
  ORDER BY c
    DESC
) WHERE c > 1
  )
);

update Album
set AlbumID=41
where (ID between 2365 AND 2373);

SELECT *
FROM (
  SELECT
    FirstName,
    LastName,
    C.Path,
    Birth,
    Death,
    C.ID,
    COUNT(A.ID) AS Albums
  FROM Componist C
    JOIN Componist_Album CA
      ON CA.ComponistID = C.ID
    JOIN Album A
      ON CA.AlbumID = A.ID
  GROUP BY C.ID
  ORDER BY Albums
    DESC
)
WHERE Albums > 1;


SELECT ID FROM Componist
    WHERE FirstName || ' ' || LastName='JS Bach';


SELECT Path
    FROM Componist
    WHERE ID=175;

update Album
set InstrumentID=4
where AlbumID=4511;

update Performer_Album
set PerformerID=279
where AlbumID in (
select ID from Album
where AlbumID=4646);

-- verwijder album en zijn stukken
-- set id=5049;

select * from Piece
where AlbumID=5049;

    UPDATE Componist
    SET Birth=1694
    WHERE ID=344;

  SELECT Name, Tag.ID
        FROM Tag
         JOIN Tag_Album
        ON TagID=Tag.ID
        where AlbumID=3380;

select Name, ID, instr(Name, 'BWV') position1,
  instr(substr(Name, instr(Name, 'BWV') + 4), ' ') position2
from Piece
where Name like '%BWV%';




        SELECT
            Album.Title,
            Album.AlbumID,
            Album.ID
        FROM Album

            JOIN Componist_Album ON Componist_Album.AlbumID = Album.ID
        WHERE Componist_Album.ComponistID=9 AND Album.InstrumentID=1
        ORDER BY Album.Title COLLATE NOCASE