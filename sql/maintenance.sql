-- 152
-- delete invalid albums that share the same path but have no content
-- (1) Path duplicates
SELECT ID
FROM (
  SELECT
    ID,
    COUNT(*) AS c
  FROM Album
  GROUP BY Path
  ORDER BY c
    DESC
)
WHERE c > 1;

645, 671, 677, 650, 656, 663, 647, 644, 687, 673, 665, 670, 700, 678, 667, 662, 694, 684, 639, 640, 675, 648, 683, 646, 660, 654, 661, 688, 642, 697, 635, 669, 692, 652, 643, 672, 676, 674, 2360, 2012, 2412, 2209, 2648, 2651, 2680, 2152,

-- (2) ID's for the duplicated Path
SELECT Album.ID
FROM Album
  LEFT JOIN Piece ON Piece.AlbumID = Album.ID
WHERE Album.Path IN (
  SELECT Path
  FROM Album
  WHERE ID = 645
)
      AND Piece.Name ISNULL;

198, 273, 345, 417, 489, 561, 633,

-- (3) delete Albums by ID
DELETE FROM Album
WHERE ID IN (
  273, 345, 417, 489, 561, 633
);

-- (2b) delete invalid albums
DELETE FROM Album
WHERE ID IN (
  SELECT Album.ID
  FROM Album
    LEFT JOIN Piece ON Piece.AlbumID = Album.ID
  WHERE Album.Path IN (
    SELECT Path
    FROM Album
    WHERE ID IN (645, 671)
  )
        AND Piece.Name ISNULL
);
-- niet goed, zie volgende (2c)

-- (2c) compleet
DELETE FROM Album


select ID, Title from Album
WHERE ID IN (
  SELECT Album.ID
  FROM Album
    LEFT JOIN Piece ON Piece.AlbumID = Album.ID
  WHERE Album.Path IN (
    SELECT Path
    FROM Album
    WHERE ID IN (
      SELECT ID
      FROM (
        SELECT
          ID,
          COUNT(*) AS c
        FROM Album
        GROUP BY Path
        ORDER BY c
          DESC
      )
      WHERE c > 1
    )
  )
  AND Piece.Name ISNULL
);
-- hiermee vond ik ook album id 674 dat geen stukken, maar wel drie cd's (subdirectories) bevatte
-- dus het filteren op overbodigheid gaat nog niet helemaal goed
-- regel 64 is niet juist

-- orphan pieces: Hoe vind ik alle pieces die in geen album (meer) zitten?
SELECT P.*
FROM Piece P
  LEFT JOIN Album A
    ON A.ID = P.AlbumID
WHERE A.ID ISNULL
ORDER BY P.ID;

-- hoe ruim ik orphan pieces op?
DELETE FROM Piece
WHERE ID IN (
  SELECT P.ID
  FROM Piece P
    LEFT JOIN Album A
      ON A.ID = P.AlbumID
  WHERE A.ID ISNULL
);
VACUUM; -- van 6.7 naar 5.5 MB

