CREATE TABLE Componist
(
    ID INTEGER PRIMARY KEY ,
    FirstName TEXT,
    LastName TEXT,
    Born INT,
    Death INT
);
CREATE UNIQUE INDEX sqlite_autoindex_Componist_1 ON Componist (FirstName, LastName)