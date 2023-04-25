-- TODO: adjust to new model

SET @delete_limit = 100000000;

-- MAIN TABLES
delete from location where LocationID < @delete_limit;
alter table location AUTO_INCREMENT = 1;

delete from profession where ProfessionID < @delete_limit;
alter table profession AUTO_INCREMENT = 1;

delete from person where PersonID < @delete_limit;
alter table person AUTO_INCREMENT = 1;

delete from relation where RelationID < @delete_limit;
alter table relation AUTO_INCREMENT = 1;

delete from event where EventID < @delete_limit;
alter table event AUTO_INCREMENT = 1;

delete from source where SourceID < @delete_limit;
alter table source AUTO_INCREMENT = 1;

-- TYPE TABLES
delete from type_of_source where SourceID < @delete_limit;
alter table type_of_source AUTO_INCREMENT = 1;

delete from type_of_position where PositionID < @delete_limit;
alter table type_of_position AUTO_INCREMENT = 1;

delete from type_of_profession where ProfessionID < @delete_limit;
alter table type_of_profession AUTO_INCREMENT = 1;

delete from type_of_expertise where ExpertiseID < @delete_limit;
alter table type_of_expertise AUTO_INCREMENT = 1;

delete from type_of_faculty where FacultyID < @delete_limit;
alter table type_of_faculty AUTO_INCREMENT = 1;

delete from type_of_location where LocationID < @delete_limit;
alter table type_of_location AUTO_INCREMENT = 1;

delete from type_of_person where PersonID < @delete_limit;
alter table type_of_person AUTO_INCREMENT = 1;

delete from type_of_relation where RelationID < @delete_limit;
alter table type_of_relation AUTO_INCREMENT = 1;

-- JOIN TABLES
delete from person_source where PersonID < @delete_limit;
delete from profession_source where ProfessionID < @delete_limit;
delete from relation_source where RelationID < @delete_limit;
delete from location_source where LocationID < @delete_limit;
