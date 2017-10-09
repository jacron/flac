CREATE TABLE Piece
(
    ID INTEGER PRIMARY KEY,
    Name TEXT,
    File TEXT,
    AlbumID INTEGER,
    LibraryCode TEXT,
    FOREIGN KEY (AlbumID) REFERENCES Album (ID)
)