DROP TABLE Instrument;
DROP TABLE Componist;
DROP TABLE Album;
DROP TABLE Performer;
DROP TABLE Piece;

delete from Album;
delete from piece;
delete from Componist;
delete from Instrument;

UPDATE Album SET Title = replace(Title, "_", " ");
