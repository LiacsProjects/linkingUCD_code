-- Timeline query for gender_df
SELECT p.Gender as 'Gender', count(p.Gender) as 'Count', SUBSTRING(professionStartDate, 1, 4) as 'Year', SUBSTRING(professionStartDate, 1, 2) + 1 as 'Century'
FROM profession
JOIN person ON professionPersonID = personPersonID AND TypeOfPerson = 1
WHERE professionStartDate IS NOT NULL AND p.Gender IS NOT NULL
GROUP BY SUBSTRING(professionStartDate, 1, 4), p.Gender
ORDER BY SUBSTRING(professionStartDate, 1, 4) ASC;

SELECT Gender as 'Gender', count(Gender) as 'Count', SUBSTRING(professionStartDate, 1, 4) as 'Year', SUBSTRING(professionStartDate, 1, 2) + 1 as 'Century'
FROM profession
JOIN person ON professionPersonID = personPersonID
WHERE professionStartDate IS NOT NULL AND Gender IS NOT NULL AND TypeOfPerson = 1
GROUP BY SUBSTRING(professionStartDate, 1, 4), Gender
ORDER BY SUBSTRING(professionStartDate, 1, 4) ASC;

-- Timeline query for birth(year)_df
SELECT SUBSTRING(locationStartDate, 1, 4) as "Birth year", count(SUBSTRING(locationStartDate, 1, 4)) as "Count", SUBSTRING(locationStartDate, 1, 4) as 'Year', SUBSTRING(locationStartDate, 1, 2) + 1 as 'Century'
FROM location
JOIN person ON personPersonID = locationPersonID AND TypeOfPerson = 1
WHERE TypeOfLocation = 1 AND locationStartDate IS NOT NULL
GROUP BY SUBSTRING(locationStartDate, 1, 4) -- , locationStartDate
ORDER BY SUBSTRING(locationStartDate, 1, 4) ASC;

-- Timeline query for birthplace_df
SELECT City as "Birthplace", count(City) as "Count", SUBSTRING(locationStartDate, 1, 4) as 'Year', SUBSTRING(locationStartDate, 1, 2) + 1 as 'Century'
FROM location
JOIN person ON personPersonID = locationPersonID AND TypeOfPerson = 1
WHERE TypeOfLocation = 1 AND locationStartDate IS NOT NULL AND City IS NOT NULL
GROUP BY SUBSTRING(locationStartDate, 1, 4), City
ORDER BY SUBSTRING(locationStartDate, 1, 4) ASC;

-- Timeline query for Appointment year
SELECT SUBSTRING(professionStartDate, 1, 4) as "Appointment year", count(SUBSTRING(professionStartDate, 1, 4)) as "Count", SUBSTRING(professionStartDate, 1, 4) as 'Year', SUBSTRING(professionStartDate, 1, 2) + 1 as 'Century'
FROM profession
JOIN person ON personPersonID = professionPersonID AND TypeOfPerson = 1
WHERE TypeOfProfession = 2 AND professionStartDate IS NOT NULL -- "TypeOfProfession" 2 = University Employment
GROUP BY SUBSTRING(professionStartDate, 1, 4)
ORDER BY SUBSTRING(professionStartDate, 1, 4) ASC;

-- Timeline query for professor_job_df
SELECT PositionType as "Job", count(PositionType) as 'Count', SUBSTRING(professionStartDate, 1, 4) as 'Year', SUBSTRING(professionStartDate, 1, 2) + 1 as 'Century'
FROM profession
JOIN person ON personPersonID = professionPersonID AND TypeOfPerson = 1
JOIN type_of_position ON TypeOfPosition = PositionID
WHERE professionStartDate IS NOT NULL
GROUP BY SUBSTRING(professionStartDate, 1, 4), PositionType
ORDER BY SUBSTRING(professionStartDate, 1, 4);

-- Timeline query for subject_df
SELECT ExpertiseType as "Subject Area", count(ExpertiseType) as 'Count', SUBSTRING(professionStartDate, 1, 4) as 'Year', SUBSTRING(professionStartDate, 1, 2) + 1 as 'Century'
FROM profession
JOIN person ON personPersonID = professionPersonID AND TypeOfPerson = 1
JOIN type_of_expertise toe ON TypeOfExpertise = ExpertiseID
WHERE professionStartDate IS NOT NULL
GROUP BY SUBSTRING(professionStartDate, 1, 4), toe.ExpertiseType
ORDER BY SUBSTRING(professionStartDate, 1, 4);

-- Timeline query for faculty_df
SELECT FacultyType as "Faculty", count(tof.FacultyType) as 'Count', SUBSTRING(professionStartDate, 1, 4) as 'Year', SUBSTRING(professionStartDate, 1, 2) + 1 as 'Century'
FROM profession
JOIN person ON personPersonID = professionPersonID AND TypeOfPerson = 1
JOIN type_of_faculty tof ON TypeOfFaculty = FacultyID
WHERE professionStartDate IS NOT NULL
GROUP BY SUBSTRING(professionStartDate, 1, 4), tof.FacultyType
ORDER BY SUBSTRING(professionStartDate, 1, 4);

-- Timeline query for End of Employment year
SELECT SUBSTRING(professionEndDate, 1, 4) as "End of Employment", count(SUBSTRING(professionEndDate, 1, 4)) as "Count", SUBSTRING(professionEndDate, 1, 4) as 'Year', SUBSTRING(professionEndDate, 1, 2) + 1 as 'Century'
FROM profession
JOIN person ON personPersonID = professionPersonID AND TypeOfPerson = 1
WHERE TypeOfProfession = 2 AND professionEndDate IS NOT NULL -- "TypeOfProfession" 2 = University Employment
GROUP BY SUBSTRING(professionEndDate, 1, 4)
ORDER BY SUBSTRING(professionEndDate, 1, 4) ASC;
