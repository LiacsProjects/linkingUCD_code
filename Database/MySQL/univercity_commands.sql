select * from type_of_source;
select * from type_of_position;

select * from person;
select * from location;
select * from profession;


select * from person where PersonID = 1392;
select * from location where PersonID_location = 425;

-- SELECT PersonID, FirstName, LastName, Gender, Nationality 
SELECT *
FROM person P, location L, profession PR
WHERE TypeOfPerson = 1	AND
P.PersonID = L.PersonID_location AND
P.PersonID = PR.PersonID_profession;

select * from person where AVG="VRIJ" and TypeOfPerson=1;
-- Output full schema for (requested) persons
SELECT *
FROM person
-- Joins 
JOIN location ON person.PersonID = location.PersonID_location
WHERE person.AVG = "VRIJ";
-- GROUP BY P.PersonID; 