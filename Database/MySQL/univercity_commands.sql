select * from type_of_source;
select * from type_of_person;
select * from type_of_location;
select * from type_of_profession;
select * from type_of_position;
select * from type_of_faculty;
select * from type_of_expertise;
select * from type_of_relation;


select * from person; -- where PersonID = 19606; -- where TypeOfPerson = 1;
select * from location where TypeOfLocation = 1;
select * from profession; -- where TypeOfProfession = 2;
select * from publication;

SHOW INDEX FROM profession;

# Individual information query
SELECT p.PersonID, p.FirstName AS 'First name', p.LastName AS 'Last name', p.Gender, 
		birth_loc.StartDate AS 'Birth date', birth_loc.City AS 'Birth place', birth_loc.Country AS 'Birth country',
        death_loc.StartDate AS 'Death date', death_loc.City AS 'Death place', death_loc.Country AS 'Death country',
        -- pub.ExaminationType AS 'Examination Type', pub.PublicationDate AS 'Publication date', pub.PublicationDate AS 'Publication date',
        prof.TypeOfPosition, prof.StartDate, prof.EndDate
FROM person p
LEFT OUTER JOIN location birth_loc ON birth_loc.PersonID = p.PersonID AND birth_loc.TypeOfLocation = 1
LEFT OUTER JOIN location death_loc ON death_loc.PersonID = p.PersonID AND death_loc.TypeOfLocation = 2
-- TODO: How to append multiple professions/publications
-- LEFT OUTER JOIN publication pub ON pub.PersonID_Publication = p.PersonID
LEFT OUTER JOIN profession prof ON prof.PersonID_profession = p.PersonID
WHERE AVG='VRIJ' AND TypeOfPerson=1 # Where clause for person table
GROUP BY prof.TypeOfPosition;


# Python version
SELECT p.PersonID, p.FirstName AS 'First name', p.LastName AS 'Last name', p.Gender, 
		birth_loc.StartDate AS 'Birth date', birth_loc.City AS 'Birth place', birth_loc.Country AS 'Birth country',
        death_loc.StartDate AS 'Death date', death_loc.City AS 'Death place', death_loc.Country AS 'Death country'
FROM person p 
LEFT OUTER JOIN location birth_loc ON birth_loc.PersonID = p.PersonID AND birth_loc.TypeOfLocation = 1
LEFT OUTER JOIN location death_loc ON death_loc.PersonID = p.PersonID AND death_loc.TypeOfLocation = 2
WHERE AVG='VRIJ';-- AND TypeOfPerson=1;

SELECT prof.StartDate
FROM person p
LEFT OUTER JOIN profession prof ON p.PersonID = prof.PersonID_profession
WHERE TypeOfPerson = 1;

SELECT professionStartDate, FirstName
FROM person, profession;

SELECT FirstName, StartDate
FROM person
JOIN profession ON personID = professionPersonID and TypeOfPerson = 1
WHERE FirstName IS NOT NULL AND StartDate IS NOT NULL;

-- Output full schema for (requested) persons
SELECT *
FROM person w
-- Joins 
JOIN location ON person.PersonID = location.PersonID_location
WHERE person.AVG = "VRIJ";
-- GROUP BY P.PersonID; 

SELECT *  FROM person WHERE LastName = levenshtein('%abraham%') AND TypeOfPerson = 1;