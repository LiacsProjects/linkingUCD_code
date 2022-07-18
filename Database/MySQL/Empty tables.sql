delete from location where LocationID < 100000000;
alter table location AUTO_INCREMENT = 1;

delete from engagement where EngagementID < 100000000;
alter table engagement AUTO_INCREMENT = 1;

delete from person where PersonID < 100000000;
alter table person AUTO_INCREMENT = 1;

delete from type_of_position where PositionID < 100000000;
alter table type_of_position AUTO_INCREMENT = 1;

delete from type_of_engagement where EngagementID < 100000000;
alter table type_of_engagement AUTO_INCREMENT = 1;

delete from type_of_expertise where ExpertiseID < 100000000;
alter table type_of_expertise AUTO_INCREMENT = 1;

delete from type_of_faculty where FacultyID < 100000000;
alter table type_of_faculty AUTO_INCREMENT = 1;

delete from type_of_location where LocationID < 100000000;
alter table type_of_location AUTO_INCREMENT = 1;

delete from type_of_person where PersonID < 100000000;
alter table type_of_person AUTO_INCREMENT = 1;

delete from type_of_relation where RelationID < 100000000;
alter table type_of_relation AUTO_INCREMENT = 1;