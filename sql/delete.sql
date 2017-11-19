delete from Componist_Album
where AlbumID BETWEEN 5095 AND 5109;

where ComponistID=379;
delete from Componist
where ID=379;

-- 152
-- delete invalid albums that share the same path but have no content
-- (1) Path duplicates
select ID
FROM (
  SELECT
    ID,
    COUNT(*) AS c
  FROM Album
  GROUP BY Path
  ORDER BY c
    DESC
) WHERE c > 1;

633,645,671,677,650,656,663,647,644,687,673,665,670,700,678,667,662,694,684,639,640,675,648,683,646,660,654,661,688,642,697,635,669,692,652,643,672,676,674,2360,2012,2412,2209,2648,2651,2680,2152,

-- (2) ID's for the duplicated Path
select ID
from Album
where Path IN (
  select Path from Album
  where ID=633
);

198,273,345,417,489,561,633,

-- (3) delete Albums by ID
delete from Album
where ID in (
273,345,417,489,561,633
);


delete from Album
where ID in(
    5116
);

delete from Album
where ID in (267, 339, 411, 483, 555, 627);

-- Hoe vind ik alle pieces die in geen album (meer) zitten?
select C.*
from Piece C
left join Album M
on M.ID = C.AlbumID
where M.ID ISNULL ;

-- hoe ruim ik die op?
delete from Piece where ID in (
  select C.ID
  from Piece C
  left join Album M
  on M.ID = C.AlbumID
  where M.ID ISNULL
);

