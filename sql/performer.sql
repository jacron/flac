CREATE TABLE Performer
(
    ID INTEGER PRIMARY KEY ,
    FirstName TEXT,
    LastName TEXT,
    Instrument TEXT,
    Born DATE
);
CREATE UNIQUE INDEX sqlite_autoindex_Performer_1 ON Performer (FirstName, LastName)