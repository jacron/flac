CREATE TABLE Piece
(
    ID INTEGER PRIMARY KEY,
    Name TEXT,
    File TEXT,
    AlbumID INTEGER,
    LibraryCode TEXT,
    FOREIGN KEY (AlbumID) REFERENCES Album (ID)
)


-- detect duplicates
select Name, AlbumID, count(*) c from Piece
group by Name having c > 1;

select Name, AlbumID from Piece
where Name like '% Pathetique.cue';