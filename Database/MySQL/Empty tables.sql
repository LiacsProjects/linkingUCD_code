SET @delete_limit = 100000000;

delete from location where LocationID < @delete_limit;
alter table location AUTO_INCREMENT = 1;

delete from engagement where EngagementID < @delete_limit;
alter table engagement AUTO_INCREMENT = 1;

delete from person where PersonID < @delete_limit;
alter table person AUTO_INCREMENT = 1;

delete from type_of_position where PositionID < @delete_limit;
alter table type_of_position AUTO_INCREMENT = 1;

delete from type_of_engagement where EngagementID < @delete_limit;
alter table type_of_engagement AUTO_INCREMENT = 1;

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