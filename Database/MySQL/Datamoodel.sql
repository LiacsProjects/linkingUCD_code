-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema LUCD_schema
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema LUCD_schema
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `LUCD_schema` DEFAULT CHARACTER SET utf8 ;
USE `LUCD_schema` ;

-- -----------------------------------------------------
-- Table `LUCD_schema`.`Location`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LUCD_schema`.`Location` (
  `LocationID` INT NOT NULL,
  `Streetname` VARCHAR(100) NULL DEFAULT NULL COMMENT 'Holds street name of the location',
  `Postalcode` VARCHAR(10) NULL DEFAULT NULL COMMENT 'Holds postalcode of the location',
  `City` VARCHAR(50) NULL DEFAULT NULL COMMENT 'Holds city of the location',
  `Country` VARCHAR(30) NULL DEFAULT NULL COMMENT 'Holds country of the location',
  `Housenumber` INT NULL DEFAULT NULL COMMENT 'Holds housenumber of the location',
  `Location date` DATE NULL COMMENT 'Holds the date of when a location is changed',
  PRIMARY KEY (`LocationID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `LUCD_schema`.`Building`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LUCD_schema`.`Building` (
  `BuildingID` INT NOT NULL,
  `BuildingName` VARCHAR(45) NULL DEFAULT NULL COMMENT 'Holds the name of the building',
  `Location_LocationID` INT NOT NULL,
  PRIMARY KEY (`BuildingID`, `Location_LocationID`),
  INDEX `fk_Building_Location1_idx` (`Location_LocationID` ASC) VISIBLE,
  CONSTRAINT `fk_Building_Location1`
    FOREIGN KEY (`Location_LocationID`)
    REFERENCES `LUCD_schema`.`Location` (`LocationID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `LUCD_schema`.`Stored_data`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LUCD_schema`.`Stored_data` (
  `Stored_dataID` INT NOT NULL,
  `Data` MEDIUMTEXT NULL,
  PRIMARY KEY (`Stored_dataID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `LUCD_schema`.`Person`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LUCD_schema`.`Person` (
  `idPerson` INT NOT NULL,
  `PobID` VARCHAR(55) NULL DEFAULT NULL COMMENT 'Holds person place of birth\\n',
  `PodID` INT NULL DEFAULT NULL COMMENT 'Holds person place of death\\n',
  `Firstname` VARCHAR(255) NULL DEFAULT NULL COMMENT 'Holds person firstname',
  `Lastname` VARCHAR(255) NULL DEFAULT NULL COMMENT 'Holds person lastname',
  `Call sign` VARCHAR(255) NULL DEFAULT NULL COMMENT 'Holds person call sign',
  `Gender` VARCHAR(45) NULL DEFAULT NULL COMMENT 'Possible values:\\nF = Female\\nM = Male\\nX = Not identified',
  `IsEnrolled` TINYINT NULL DEFAULT NULL COMMENT 'Possible values 1 or 0:\\n0 = false\\n1 = true',
  `Dob` DATE NULL DEFAULT NULL COMMENT 'Holds person date of birth',
  `Dod` DATE NULL DEFAULT NULL COMMENT 'Holds person date of death',
  `Religion` VARCHAR(255) NULL DEFAULT NULL,
  `Dob_original` VARCHAR(255) NULL DEFAULT NULL COMMENT 'Holds person date of birth original',
  `Dod_original` VARCHAR(255) NULL DEFAULT NULL COMMENT 'Holds person date of death original',
  `Nationality` VARCHAR(255) NULL COMMENT 'Holds the nationality of the person',
  `Suffix` VARCHAR(45) NULL COMMENT 'Holds the nationality of the person',
  `JobName` VARCHAR(45) NULL COMMENT 'Holds the job name of the person',
  `Stored_data_Stored_dataID` INT NOT NULL,
  PRIMARY KEY (`idPerson`, `Stored_data_Stored_dataID`),
  INDEX `fk_Person_Location1_idx` (`PobID` ASC) VISIBLE,
  INDEX `fk_Person_Location2_idx` (`PodID` ASC) VISIBLE,
  INDEX `fk_Person_Stored_data1_idx` (`Stored_data_Stored_dataID` ASC) VISIBLE,
  CONSTRAINT `fk_Person_Location1`
    FOREIGN KEY (`PobID`)
    REFERENCES `LUCD_schema`.`Location` (`LocationID`),
  CONSTRAINT `fk_Person_Location2`
    FOREIGN KEY (`PodID`)
    REFERENCES `LUCD_schema`.`Location` (`LocationID`),
  CONSTRAINT `fk_Person_Stored_data1`
    FOREIGN KEY (`Stored_data_Stored_dataID`)
    REFERENCES `LUCD_schema`.`Stored_data` (`Stored_dataID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `LUCD_schema`.`Father`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LUCD_schema`.`Father` (
  `ManID` INT NOT NULL,
  `Person_idPerson` INT NOT NULL,
  PRIMARY KEY (`ManID`, `Person_idPerson`),
  INDEX `fk_Father_Person1_idx` (`Person_idPerson` ASC) VISIBLE,
  CONSTRAINT `fk_Father_Person1`
    FOREIGN KEY (`Person_idPerson`)
    REFERENCES `LUCD_schema`.`Person` (`idPerson`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `LUCD_schema`.`Mother`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LUCD_schema`.`Mother` (
  `WomanID` INT NOT NULL,
  `Person_idPerson` INT NOT NULL,
  PRIMARY KEY (`WomanID`, `Person_idPerson`),
  UNIQUE INDEX `WomanID_UNIQUE` (`WomanID` ASC) VISIBLE,
  INDEX `fk_Mother_Person1_idx` (`Person_idPerson` ASC) VISIBLE,
  CONSTRAINT `fk_Mother_Person1`
    FOREIGN KEY (`Person_idPerson`)
    REFERENCES `LUCD_schema`.`Person` (`idPerson`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `LUCD_schema`.`Child`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LUCD_schema`.`Child` (
  `ChildID` INT NOT NULL,
  `Person_idPerson` INT NOT NULL,
  `Father_ManID` INT NOT NULL,
  `Mother_WomanID` INT NOT NULL,
  PRIMARY KEY (`ChildID`, `Person_idPerson`, `Father_ManID`, `Mother_WomanID`),
  INDEX `fk_Child_Person1_idx` (`Person_idPerson` ASC) VISIBLE,
  INDEX `fk_Child_Father1_idx` (`Father_ManID` ASC) VISIBLE,
  INDEX `fk_Child_Mother1_idx` (`Mother_WomanID` ASC) VISIBLE,
  CONSTRAINT `fk_Child_Person1`
    FOREIGN KEY (`Person_idPerson`)
    REFERENCES `LUCD_schema`.`Person` (`idPerson`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Child_Father1`
    FOREIGN KEY (`Father_ManID`)
    REFERENCES `LUCD_schema`.`Father` (`ManID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Child_Mother1`
    FOREIGN KEY (`Mother_WomanID`)
    REFERENCES `LUCD_schema`.`Mother` (`WomanID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `LUCD_schema`.`Employee`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LUCD_schema`.`Employee` (
  `EmployeeID` INT NOT NULL,
  `Eoe` DATE NULL DEFAULT NULL COMMENT 'Holds the end of employment date of an employee',
  `Soe` DATE NULL DEFAULT NULL COMMENT 'Holds the start of employment date of an employee',
  `Person_idPerson` INT NOT NULL,
  PRIMARY KEY (`EmployeeID`, `Person_idPerson`),
  INDEX `fk_Employee_Person1_idx` (`Person_idPerson` ASC) VISIBLE,
  CONSTRAINT `fk_Employee_Person1`
    FOREIGN KEY (`Person_idPerson`)
    REFERENCES `LUCD_schema`.`Person` (`idPerson`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `LUCD_schema`.`Publication`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LUCD_schema`.`Publication` (
  `PublicationID` INT NOT NULL,
  `PublicationDate` DATE NULL DEFAULT NULL COMMENT 'Holds date of the publication of the paper',
  `PaperName` VARCHAR(255) NULL DEFAULT NULL COMMENT 'Holds name of the paper',
  `Score` INT NULL DEFAULT NULL,
  PRIMARY KEY (`PublicationID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `LUCD_schema`.`Experiment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LUCD_schema`.`Experiment` (
  `ExperimentID` INT NOT NULL,
  `ExperimentName` VARCHAR(255) NULL DEFAULT NULL COMMENT 'Holds name of the experiment',
  `Date` DATE NULL COMMENT 'Holds the date of the experiment',
  `Publication_PublicationID` INT NOT NULL,
  PRIMARY KEY (`ExperimentID`, `Publication_PublicationID`),
  INDEX `fk_Experiment_Publication1_idx` (`Publication_PublicationID` ASC) VISIBLE,
  CONSTRAINT `fk_Experiment_Publication1`
    FOREIGN KEY (`Publication_PublicationID`)
    REFERENCES `LUCD_schema`.`Publication` (`PublicationID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `LUCD_schema`.`University`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LUCD_schema`.`University` (
  `UniversityID` INT NOT NULL,
  `UniversityName` VARCHAR(100) NULL DEFAULT NULL COMMENT 'Holds name of the university',
  `Doc` VARCHAR(45) NULL COMMENT 'Holds the creation date of the university.',
  PRIMARY KEY (`UniversityID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `LUCD_schema`.`Faculty`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LUCD_schema`.`Faculty` (
  `FacultyID` INT NOT NULL,
  `FacultyName` VARCHAR(80) NULL DEFAULT NULL COMMENT 'Holds name of the faculty',
  `Doc` VARCHAR(45) NULL DEFAULT NULL COMMENT 'Holds date of creation of faculty',
  `University_UniversityID` INT NOT NULL,
  PRIMARY KEY (`FacultyID`, `University_UniversityID`),
  INDEX `fk_Faculty_University1_idx` (`University_UniversityID` ASC) VISIBLE,
  CONSTRAINT `fk_Faculty_University1`
    FOREIGN KEY (`University_UniversityID`)
    REFERENCES `LUCD_schema`.`University` (`UniversityID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `LUCD_schema`.`Institute`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LUCD_schema`.`Institute` (
  `InstituteID` INT NOT NULL,
  `InstituteName` VARCHAR(45) NULL,
  `Doc` VARCHAR(45) NULL DEFAULT NULL COMMENT 'Holds date of creation of the institute',
  `Faculty_FacultyID` INT NOT NULL,
  `Faculty_University_UniversityID` INT NOT NULL,
  PRIMARY KEY (`InstituteID`, `Faculty_FacultyID`, `Faculty_University_UniversityID`),
  INDEX `fk_Institute_Faculty1_idx` (`Faculty_FacultyID` ASC, `Faculty_University_UniversityID` ASC) VISIBLE,
  CONSTRAINT `fk_Institute_Faculty1`
    FOREIGN KEY (`Faculty_FacultyID` , `Faculty_University_UniversityID`)
    REFERENCES `LUCD_schema`.`Faculty` (`FacultyID` , `University_UniversityID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `LUCD_schema`.`Institute_has_Building`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LUCD_schema`.`Institute_has_Building` (
  `Institute_InstituteID` INT NOT NULL,
  `Building_BuildingID` INT NOT NULL,
  PRIMARY KEY (`Institute_InstituteID`, `Building_BuildingID`),
  INDEX `fk_Institute_has_Building_Building1_idx` (`Building_BuildingID` ASC) VISIBLE,
  INDEX `fk_Institute_has_Building_Institute1_idx` (`Institute_InstituteID` ASC) VISIBLE,
  CONSTRAINT `fk_Institute_has_Building_Building1`
    FOREIGN KEY (`Building_BuildingID`)
    REFERENCES `LUCD_schema`.`Building` (`BuildingID`),
  CONSTRAINT `fk_Institute_has_Building_Institute1`
    FOREIGN KEY (`Institute_InstituteID`)
    REFERENCES `LUCD_schema`.`Institute` (`InstituteID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `LUCD_schema`.`Prestigious_people`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LUCD_schema`.`Prestigious_people` (
  `Presitgous_peopleID` INT NOT NULL,
  `Title` VARCHAR(255) NULL DEFAULT NULL COMMENT 'Holds title of the person, e.g. King, Queen, governor, rectores magnificus etc..',
  `Person_idPerson` INT NOT NULL,
  PRIMARY KEY (`Presitgous_peopleID`, `Person_idPerson`),
  INDEX `fk_Prestigious_people_Person1_idx` (`Person_idPerson` ASC) VISIBLE,
  CONSTRAINT `fk_Prestigious_people_Person1`
    FOREIGN KEY (`Person_idPerson`)
    REFERENCES `LUCD_schema`.`Person` (`idPerson`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `LUCD_schema`.`Professor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LUCD_schema`.`Professor` (
  `ProfessorID` INT NOT NULL,
  `Nobelaward` VARCHAR(255) NULL DEFAULT NULL COMMENT 'Holds the name of the nobelaward',
  `Appointment1` VARCHAR(255) NULL DEFAULT NULL COMMENT 'Holds first appointment of professor',
  `Appointment2` VARCHAR(255) NULL DEFAULT NULL COMMENT 'Holds second appointment of professor',
  `Appointment3` VARCHAR(255) NULL DEFAULT NULL COMMENT 'Holds third appointment of professor',
  `Appointment4` VARCHAR(255) NULL DEFAULT NULL COMMENT 'Holds fourth appointment of professor',
  `Doa1` DATE NULL DEFAULT NULL COMMENT 'Holds first date of appointment',
  `Doa2` DATE NULL DEFAULT NULL COMMENT 'Holds second date of appointment',
  `Doa3` DATE NULL DEFAULT NULL COMMENT 'Holds third date of appointment',
  `Doa4` DATE NULL DEFAULT NULL COMMENT 'Holds fourth date of appointment',
  `Discipline1` VARCHAR(100) NULL DEFAULT NULL COMMENT 'Holds first discipline of the professor',
  `Discipline2` VARCHAR(100) NULL DEFAULT NULL COMMENT 'Holds second discipline of the professor',
  `Discipline3` VARCHAR(100) NULL DEFAULT NULL COMMENT 'Holds third discipline of the professor',
  `Discipline4` VARCHAR(100) NULL DEFAULT NULL COMMENT 'Holds fourth discipline of the professor',
  `Eoa1` DATE NULL DEFAULT NULL COMMENT 'Holds end of first appointment',
  `Eoa2` DATE NULL DEFAULT NULL COMMENT 'Holds end of second appointment',
  `Eoa3` DATE NULL DEFAULT NULL COMMENT 'Holds end of third appointment',
  `Eoa4` DATE NULL DEFAULT NULL COMMENT 'Holds end of fourth appointment',
  `Employee_EmployeeID` INT NOT NULL,
  `Employee_Person_idPerson` INT NOT NULL,
  PRIMARY KEY (`ProfessorID`, `Employee_EmployeeID`, `Employee_Person_idPerson`),
  INDEX `fk_Professor_Employee1_idx` (`Employee_EmployeeID` ASC, `Employee_Person_idPerson` ASC) VISIBLE,
  CONSTRAINT `fk_Professor_Employee1`
    FOREIGN KEY (`Employee_EmployeeID` , `Employee_Person_idPerson`)
    REFERENCES `LUCD_schema`.`Employee` (`EmployeeID` , `Person_idPerson`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `LUCD_schema`.`Relation`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LUCD_schema`.`Relation` (
  `RelationID` INT NOT NULL,
  `Relationtype` VARCHAR(255) NULL DEFAULT NULL COMMENT 'Holds the relationtype, possible options are:\\nGetrouwd\\nGewezen echtgenoot\\nGemeenschap van goederen',
  `Sor` DATE NULL DEFAULT NULL COMMENT 'Holds the startdate of relationship',
  `Eor` DATE NULL DEFAULT NULL COMMENT 'Holds the enddate of relationship',
  `Mother_WomanID` INT NOT NULL,
  `Father_ManID` INT NOT NULL,
  PRIMARY KEY (`RelationID`, `Mother_WomanID`, `Father_ManID`),
  INDEX `fk_Relation_Mother1_idx` (`Mother_WomanID` ASC) VISIBLE,
  INDEX `fk_Relation_Father1_idx` (`Father_ManID` ASC) VISIBLE,
  CONSTRAINT `fk_Relation_Father1`
    FOREIGN KEY (`Father_ManID`)
    REFERENCES `LUCD_schema`.`Father` (`ManID`),
  CONSTRAINT `fk_Relation_Mother1`
    FOREIGN KEY (`Mother_WomanID`)
    REFERENCES `LUCD_schema`.`Mother` (`WomanID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `LUCD_schema`.`Study`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LUCD_schema`.`Study` (
  `StudyID` INT NOT NULL,
  `Studyname` VARCHAR(45) NULL DEFAULT NULL COMMENT 'Holds the study name of the study',
  `Language` VARCHAR(30) NULL DEFAULT NULL COMMENT 'Holds the main language of the study',
  `Croho-number` INT NULL DEFAULT NULL COMMENT 'Holds the coho-number of a study',
  `Faculty_FacultyID` INT NOT NULL,
  `Faculty_University_UniversityID` INT NOT NULL,
  `Institute_InstituteID` INT NOT NULL,
  PRIMARY KEY (`StudyID`, `Faculty_FacultyID`, `Faculty_University_UniversityID`, `Institute_InstituteID`),
  UNIQUE INDEX `Croho-number_UNIQUE` (`Croho-number` ASC) VISIBLE,
  INDEX `fk_Study_Faculty1_idx` (`Faculty_FacultyID` ASC, `Faculty_University_UniversityID` ASC) VISIBLE,
  INDEX `fk_Study_Institute1_idx` (`Institute_InstituteID` ASC) VISIBLE,
  CONSTRAINT `fk_Study_Faculty1`
    FOREIGN KEY (`Faculty_FacultyID` , `Faculty_University_UniversityID`)
    REFERENCES `LUCD_schema`.`Faculty` (`FacultyID` , `University_UniversityID`),
  CONSTRAINT `fk_Study_Institute1`
    FOREIGN KEY (`Institute_InstituteID`)
    REFERENCES `LUCD_schema`.`Institute` (`InstituteID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `LUCD_schema`.`Specialization`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LUCD_schema`.`Specialization` (
  `SpecializationID` INT NOT NULL,
  `Studyname` VARCHAR(45) NULL DEFAULT NULL COMMENT 'Holds study name of the specialization',
  `Study_StudyID` INT NOT NULL,
  `Study_Faculty_FacultyID` INT NOT NULL,
  `Study_Faculty_University_UniversityID` INT NOT NULL,
  `Study_Institute_InstituteID` INT NOT NULL,
  PRIMARY KEY (`SpecializationID`, `Study_StudyID`, `Study_Faculty_FacultyID`, `Study_Faculty_University_UniversityID`, `Study_Institute_InstituteID`),
  INDEX `fk_Specialization_Study1_idx` (`Study_StudyID` ASC, `Study_Faculty_FacultyID` ASC, `Study_Faculty_University_UniversityID` ASC, `Study_Institute_InstituteID` ASC) VISIBLE,
  CONSTRAINT `fk_Specialization_Study1`
    FOREIGN KEY (`Study_StudyID` , `Study_Faculty_FacultyID` , `Study_Faculty_University_UniversityID` , `Study_Institute_InstituteID`)
    REFERENCES `LUCD_schema`.`Study` (`StudyID` , `Faculty_FacultyID` , `Faculty_University_UniversityID` , `Institute_InstituteID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `LUCD_schema`.`Student`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LUCD_schema`.`Student` (
  `StudentID` INT NOT NULL,
  `Studentnumber` INT NULL DEFAULT NULL COMMENT 'Holds the student number of a student ',
  `Person_idPerson` INT NOT NULL,
  PRIMARY KEY (`StudentID`, `Person_idPerson`),
  UNIQUE INDEX `Studentnumber_UNIQUE` (`Studentnumber` ASC) VISIBLE,
  INDEX `fk_Student_Person1_idx` (`Person_idPerson` ASC) VISIBLE,
  CONSTRAINT `fk_Student_Person1`
    FOREIGN KEY (`Person_idPerson`)
    REFERENCES `LUCD_schema`.`Person` (`idPerson`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `LUCD_schema`.`Study_has_Professor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LUCD_schema`.`Study_has_Professor` (
  `Study_StudyID` INT NOT NULL,
  `Study_Faculty_FacultyID` INT NOT NULL,
  `Study_Faculty_University_UniversityID` INT NOT NULL,
  `Study_Institute_InstituteID` INT NOT NULL,
  `Professor_ProfessorID` INT NOT NULL,
  PRIMARY KEY (`Study_StudyID`, `Study_Faculty_FacultyID`, `Study_Faculty_University_UniversityID`, `Study_Institute_InstituteID`, `Professor_ProfessorID`),
  INDEX `fk_Study_has_Professor_Professor1_idx` (`Professor_ProfessorID` ASC) VISIBLE,
  INDEX `fk_Study_has_Professor_Study1_idx` (`Study_StudyID` ASC, `Study_Faculty_FacultyID` ASC, `Study_Faculty_University_UniversityID` ASC, `Study_Institute_InstituteID` ASC) VISIBLE,
  CONSTRAINT `fk_Study_has_Professor_Professor1`
    FOREIGN KEY (`Professor_ProfessorID`)
    REFERENCES `LUCD_schema`.`Professor` (`ProfessorID`),
  CONSTRAINT `fk_Study_has_Professor_Study1`
    FOREIGN KEY (`Study_StudyID` , `Study_Faculty_FacultyID` , `Study_Faculty_University_UniversityID` , `Study_Institute_InstituteID`)
    REFERENCES `LUCD_schema`.`Study` (`StudyID` , `Faculty_FacultyID` , `Faculty_University_UniversityID` , `Institute_InstituteID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `LUCD_schema`.`Study_has_Student`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LUCD_schema`.`Study_has_Student` (
  `Study_StudyID` INT NOT NULL,
  `Study_Faculty_FacultyID` INT NOT NULL,
  `Study_Faculty_University_UniversityID` INT NOT NULL,
  `Study_Institute_InstituteID` INT NOT NULL,
  `Student_StudentID` INT NOT NULL,
  PRIMARY KEY (`Study_StudyID`, `Study_Faculty_FacultyID`, `Study_Faculty_University_UniversityID`, `Study_Institute_InstituteID`, `Student_StudentID`),
  INDEX `fk_Study_has_Student_Student1_idx` (`Student_StudentID` ASC) VISIBLE,
  INDEX `fk_Study_has_Student_Study1_idx` (`Study_StudyID` ASC, `Study_Faculty_FacultyID` ASC, `Study_Faculty_University_UniversityID` ASC, `Study_Institute_InstituteID` ASC) VISIBLE,
  CONSTRAINT `fk_Study_has_Student_Student1`
    FOREIGN KEY (`Student_StudentID`)
    REFERENCES `LUCD_schema`.`Student` (`StudentID`),
  CONSTRAINT `fk_Study_has_Student_Study1`
    FOREIGN KEY (`Study_StudyID` , `Study_Faculty_FacultyID` , `Study_Faculty_University_UniversityID` , `Study_Institute_InstituteID`)
    REFERENCES `LUCD_schema`.`Study` (`StudyID` , `Faculty_FacultyID` , `Faculty_University_UniversityID` , `Institute_InstituteID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `LUCD_schema`.`Supporting staff`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LUCD_schema`.`Supporting staff` (
  `Supporting_staffID` INT NOT NULL,
  `JobName` VARCHAR(45) NULL DEFAULT NULL COMMENT 'Holds the job name of the employee',
  `Field` VARCHAR(45) NULL DEFAULT NULL COMMENT 'Holds the field of job',
  `Employee_EmployeeID` INT NOT NULL,
  `Employee_Person_idPerson` INT NOT NULL,
  PRIMARY KEY (`Supporting_staffID`, `Employee_EmployeeID`, `Employee_Person_idPerson`),
  INDEX `fk_Supporting staff_Employee1_idx` (`Employee_EmployeeID` ASC, `Employee_Person_idPerson` ASC) VISIBLE,
  CONSTRAINT `fk_Supporting staff_Employee1`
    FOREIGN KEY (`Employee_EmployeeID` , `Employee_Person_idPerson`)
    REFERENCES `LUCD_schema`.`Employee` (`EmployeeID` , `Person_idPerson`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `LUCD_schema`.`Person_has_Location`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LUCD_schema`.`Person_has_Location` (
  `Person_idPerson` INT NOT NULL,
  `Location_LocationID` INT NOT NULL,
  PRIMARY KEY (`Person_idPerson`, `Location_LocationID`),
  INDEX `fk_Person_has_Location_Location1_idx` (`Location_LocationID` ASC) VISIBLE,
  INDEX `fk_Person_has_Location_Person1_idx` (`Person_idPerson` ASC) VISIBLE,
  CONSTRAINT `fk_Person_has_Location_Person1`
    FOREIGN KEY (`Person_idPerson`)
    REFERENCES `LUCD_schema`.`Person` (`idPerson`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Person_has_Location_Location1`
    FOREIGN KEY (`Location_LocationID`)
    REFERENCES `LUCD_schema`.`Location` (`LocationID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `LUCD_schema`.`Professor_has_Publication`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LUCD_schema`.`Professor_has_Publication` (
  `Professor_ProfessorID` INT NOT NULL,
  `Professor_Employee_EmployeeID` INT NOT NULL,
  `Professor_Employee_Person_idPerson` INT NOT NULL,
  `Publication_PublicationID` INT NOT NULL,
  PRIMARY KEY (`Professor_ProfessorID`, `Professor_Employee_EmployeeID`, `Professor_Employee_Person_idPerson`, `Publication_PublicationID`),
  INDEX `fk_Professor_has_Publication_Publication1_idx` (`Publication_PublicationID` ASC) VISIBLE,
  INDEX `fk_Professor_has_Publication_Professor1_idx` (`Professor_ProfessorID` ASC, `Professor_Employee_EmployeeID` ASC, `Professor_Employee_Person_idPerson` ASC) VISIBLE,
  CONSTRAINT `fk_Professor_has_Publication_Professor1`
    FOREIGN KEY (`Professor_ProfessorID` , `Professor_Employee_EmployeeID` , `Professor_Employee_Person_idPerson`)
    REFERENCES `LUCD_schema`.`Professor` (`ProfessorID` , `Employee_EmployeeID` , `Employee_Person_idPerson`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Professor_has_Publication_Publication1`
    FOREIGN KEY (`Publication_PublicationID`)
    REFERENCES `LUCD_schema`.`Publication` (`PublicationID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `LUCD_schema`.`Faculty_has_Building`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LUCD_schema`.`Faculty_has_Building` (
  `Faculty_FacultyID` INT NOT NULL,
  `Faculty_University_UniversityID` INT NOT NULL,
  `Building_BuildingID` INT NOT NULL,
  `Building_Location_LocationID` INT NOT NULL,
  PRIMARY KEY (`Faculty_FacultyID`, `Faculty_University_UniversityID`, `Building_BuildingID`, `Building_Location_LocationID`),
  INDEX `fk_Faculty_has_Building_Building1_idx` (`Building_BuildingID` ASC, `Building_Location_LocationID` ASC) VISIBLE,
  INDEX `fk_Faculty_has_Building_Faculty1_idx` (`Faculty_FacultyID` ASC, `Faculty_University_UniversityID` ASC) VISIBLE,
  CONSTRAINT `fk_Faculty_has_Building_Faculty1`
    FOREIGN KEY (`Faculty_FacultyID` , `Faculty_University_UniversityID`)
    REFERENCES `LUCD_schema`.`Faculty` (`FacultyID` , `University_UniversityID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Faculty_has_Building_Building1`
    FOREIGN KEY (`Building_BuildingID` , `Building_Location_LocationID`)
    REFERENCES `LUCD_schema`.`Building` (`BuildingID` , `Location_LocationID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
