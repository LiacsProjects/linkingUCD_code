-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema Test_via_eer
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema Test_via_eer
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `Test_via_eer` DEFAULT CHARACTER SET utf8 ;
USE `Test_via_eer` ;

-- -----------------------------------------------------
-- Table `Test_via_eer`.`Location`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Test_via_eer`.`Location` (
  `LocationID` INT NOT NULL,
  `Streetname` VARCHAR(100) NULL COMMENT 'Holds street name of the location',
  `Postalcode` VARCHAR(10) NULL COMMENT 'Holds postalcode of the location',
  `City` VARCHAR(50) NULL COMMENT 'Holds city of the location',
  `Country` VARCHAR(30) NULL COMMENT 'Holds country of the location',
  `Housenumber` INT NULL COMMENT 'Holds housenumber of the location',
  PRIMARY KEY (`LocationID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Test_via_eer`.`Person`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Test_via_eer`.`Person` (
  `idPerson` INT NOT NULL,
  `PobID` INT NULL COMMENT 'Holds person place of birth\n',
  `PodID` INT NULL COMMENT 'Holds person place of death\n',
  `Firstname` VARCHAR(45) NULL COMMENT 'Holds person firstname',
  `Lastname` VARCHAR(45) NULL COMMENT 'Holds person lastname',
  `Call sign` VARCHAR(45) NULL COMMENT 'Holds person call sign',
  `Gender` VARCHAR(45) NULL COMMENT 'Possible values:\nF = Female\nM = Male\nX = Not identified',
  `IsEnrolled` TINYINT NULL COMMENT 'Possible values 1 or 0:\n0 = false\n1 = true',
  `Dob` DATE NULL COMMENT 'Holds person date of birth',
  `Dod` DATE NULL COMMENT 'Holds person date of death',
  `Religion` VARCHAR(255) NULL,
  `Dob_original` VARCHAR(255) NULL COMMENT 'Holds person date of birth original',
  `Dod_original` VARCHAR(255) NULL COMMENT 'Holds person date of death original',
  PRIMARY KEY (`idPerson`),
  INDEX `fk_Person_Location1_idx` (`PobID` ASC) VISIBLE,
  INDEX `fk_Person_Location2_idx` (`PodID` ASC) VISIBLE,
  CONSTRAINT `fk_Person_Location1`
    FOREIGN KEY (`PobID`)
    REFERENCES `Test_via_eer`.`Location` (`LocationID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Person_Location2`
    FOREIGN KEY (`PodID`)
    REFERENCES `Test_via_eer`.`Location` (`LocationID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Test_via_eer`.`Paper`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Test_via_eer`.`Paper` (
  `PaperID` INT NOT NULL,
  `PublicationDate` DATE NULL COMMENT 'Holds date of the publication of the paper',
  `PaperName` VARCHAR(255) NULL COMMENT 'Holds name of the paper',
  `Score` INT NULL,
  PRIMARY KEY (`PaperID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Test_via_eer`.`Experiment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Test_via_eer`.`Experiment` (
  `ExperimentID` INT NOT NULL,
  `ExperimentName` VARCHAR(255) NULL COMMENT 'Holds name of the experiment',
  `Paper_PaperID1` INT NOT NULL,
  PRIMARY KEY (`ExperimentID`, `Paper_PaperID1`),
  INDEX `fk_Experiment_Paper2_idx` (`Paper_PaperID1` ASC) VISIBLE,
  CONSTRAINT `fk_Experiment_Paper2`
    FOREIGN KEY (`Paper_PaperID1`)
    REFERENCES `Test_via_eer`.`Paper` (`PaperID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Test_via_eer`.`Presitgous people`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Test_via_eer`.`Presitgous people` (
  `Presitgous_peopleID` INT NOT NULL,
  `Title` VARCHAR(45) NULL COMMENT 'Holds title of the person, e.g. King, Queen, governor, etc..',
  `Person_idPerson` INT NOT NULL,
  PRIMARY KEY (`Presitgous_peopleID`, `Person_idPerson`),
  INDEX `fk_Presitgous people_Person1_idx` (`Person_idPerson` ASC) VISIBLE,
  CONSTRAINT `fk_Presitgous people_Person1`
    FOREIGN KEY (`Person_idPerson`)
    REFERENCES `Test_via_eer`.`Person` (`idPerson`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Test_via_eer`.`Employee`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Test_via_eer`.`Employee` (
  `EmployeeID` INT NOT NULL,
  `Eoe` DATE NULL COMMENT 'Holds the end of employment date of an employee',
  `Soe` DATE NULL COMMENT 'Holds the start of employment date of an employee',
  `Person_idPerson` INT NOT NULL,
  PRIMARY KEY (`EmployeeID`, `Person_idPerson`),
  INDEX `fk_Employee_Person1_idx` (`Person_idPerson` ASC) VISIBLE,
  CONSTRAINT `fk_Employee_Person1`
    FOREIGN KEY (`Person_idPerson`)
    REFERENCES `Test_via_eer`.`Person` (`idPerson`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Test_via_eer`.`Supporting staff`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Test_via_eer`.`Supporting staff` (
  `Supporting_staffID` INT NOT NULL,
  `JobName` VARCHAR(45) NULL COMMENT 'Holds the job name of the employee',
  `Branch` VARCHAR(45) NULL,
  `Employee_EmployeeID` INT NOT NULL,
  `Employee_Person_idPerson` INT NOT NULL,
  PRIMARY KEY (`Supporting_staffID`, `Employee_EmployeeID`, `Employee_Person_idPerson`),
  INDEX `fk_Supporting staff_Employee1_idx` (`Employee_EmployeeID` ASC, `Employee_Person_idPerson` ASC) VISIBLE,
  CONSTRAINT `fk_Supporting staff_Employee1`
    FOREIGN KEY (`Employee_EmployeeID` , `Employee_Person_idPerson`)
    REFERENCES `Test_via_eer`.`Employee` (`EmployeeID` , `Person_idPerson`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Test_via_eer`.`Professor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Test_via_eer`.`Professor` (
  `ProfessorID` INT NOT NULL,
  `Nobelaward` VARCHAR(255) NULL COMMENT 'Holds the name of the nobelaward',
  `Appointment1` VARCHAR(255) NULL COMMENT 'Holds first appointment of professor',
  `Discipline` VARCHAR(100) NULL COMMENT 'Holds discipline of the professor',
  `Doa` DATE NULL COMMENT 'Holds date of appointment',
  `Appointment2` VARCHAR(255) NULL COMMENT 'Holds second appointment of professor',
  `Appointment3` VARCHAR(255) NULL COMMENT 'Holds third appointment of professor',
  `Appointment4` VARCHAR(255) NULL COMMENT 'Holds fourth appointment of professor',
  `Appointment5` VARCHAR(255) NULL COMMENT 'Holds fifth appointment of professor',
  `Employee_EmployeeID` INT NOT NULL,
  `Employee_Person_idPerson` INT NOT NULL,
  PRIMARY KEY (`ProfessorID`, `Employee_EmployeeID`, `Employee_Person_idPerson`),
  INDEX `fk_Professor_Employee1_idx` (`Employee_EmployeeID` ASC, `Employee_Person_idPerson` ASC) VISIBLE,
  CONSTRAINT `fk_Professor_Employee1`
    FOREIGN KEY (`Employee_EmployeeID` , `Employee_Person_idPerson`)
    REFERENCES `Test_via_eer`.`Employee` (`EmployeeID` , `Person_idPerson`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Test_via_eer`.`Student`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Test_via_eer`.`Student` (
  `StudentID` INT NOT NULL,
  `Studentnumber` INT NULL COMMENT 'Holds the student number of a student ',
  `Person_idPerson` INT NOT NULL,
  PRIMARY KEY (`StudentID`, `Person_idPerson`),
  UNIQUE INDEX `Studentnumber_UNIQUE` (`Studentnumber` ASC) VISIBLE,
  INDEX `fk_Student_Person1_idx` (`Person_idPerson` ASC) VISIBLE,
  CONSTRAINT `fk_Student_Person1`
    FOREIGN KEY (`Person_idPerson`)
    REFERENCES `Test_via_eer`.`Person` (`idPerson`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Test_via_eer`.`University`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Test_via_eer`.`University` (
  `UniversityID` INT NOT NULL,
  `UniversityName` VARCHAR(100) NULL COMMENT 'Holds name of the university',
  PRIMARY KEY (`UniversityID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Test_via_eer`.`Faculty`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Test_via_eer`.`Faculty` (
  `FacultyID` INT NOT NULL,
  `FacultyName` VARCHAR(80) NULL COMMENT 'Holds name of the faculty',
  `Doc` VARCHAR(45) NULL COMMENT 'Holds date of creation of faculty',
  `University_UniversityID` INT NOT NULL,
  PRIMARY KEY (`FacultyID`, `University_UniversityID`),
  INDEX `fk_Faculty_University1_idx` (`University_UniversityID` ASC) VISIBLE,
  CONSTRAINT `fk_Faculty_University1`
    FOREIGN KEY (`University_UniversityID`)
    REFERENCES `Test_via_eer`.`University` (`UniversityID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Test_via_eer`.`Institute`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Test_via_eer`.`Institute` (
  `InstituteID` INT NOT NULL,
  `Doc` VARCHAR(45) NULL COMMENT 'Holds date of creation of the institute',
  `Faculty_FacultyID` INT NOT NULL,
  `Faculty_University_UniversityID` INT NOT NULL,
  PRIMARY KEY (`InstituteID`),
  INDEX `fk_Institute_Faculty1_idx` (`Faculty_FacultyID` ASC, `Faculty_University_UniversityID` ASC) VISIBLE,
  CONSTRAINT `fk_Institute_Faculty1`
    FOREIGN KEY (`Faculty_FacultyID` , `Faculty_University_UniversityID`)
    REFERENCES `Test_via_eer`.`Faculty` (`FacultyID` , `University_UniversityID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Test_via_eer`.`Study`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Test_via_eer`.`Study` (
  `StudyID` INT NOT NULL,
  `Studyname` VARCHAR(45) NULL COMMENT 'Holds the study name of the study',
  `Language` VARCHAR(30) NULL COMMENT 'Holds the main language of the study',
  `Croho-number` INT NULL COMMENT 'Holds the coho-number of a study',
  `Faculty_FacultyID` INT NOT NULL,
  `Faculty_University_UniversityID` INT NOT NULL,
  `Institute_InstituteID` INT NOT NULL,
  PRIMARY KEY (`StudyID`, `Faculty_FacultyID`, `Faculty_University_UniversityID`, `Institute_InstituteID`),
  UNIQUE INDEX `Croho-number_UNIQUE` (`Croho-number` ASC) VISIBLE,
  INDEX `fk_Study_Faculty1_idx` (`Faculty_FacultyID` ASC, `Faculty_University_UniversityID` ASC) VISIBLE,
  INDEX `fk_Study_Institute1_idx` (`Institute_InstituteID` ASC) VISIBLE,
  CONSTRAINT `fk_Study_Faculty1`
    FOREIGN KEY (`Faculty_FacultyID` , `Faculty_University_UniversityID`)
    REFERENCES `Test_via_eer`.`Faculty` (`FacultyID` , `University_UniversityID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Study_Institute1`
    FOREIGN KEY (`Institute_InstituteID`)
    REFERENCES `Test_via_eer`.`Institute` (`InstituteID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Test_via_eer`.`Building`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Test_via_eer`.`Building` (
  `BuildingID` INT NOT NULL,
  `BuildingName` VARCHAR(45) NULL COMMENT 'Holds the name of the building',
  `Location_LocationID` INT NOT NULL,
  PRIMARY KEY (`BuildingID`),
  INDEX `fk_Building_Location_idx` (`Location_LocationID` ASC) VISIBLE,
  CONSTRAINT `fk_Building_Location`
    FOREIGN KEY (`Location_LocationID`)
    REFERENCES `Test_via_eer`.`Location` (`LocationID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Test_via_eer`.`Specialization`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Test_via_eer`.`Specialization` (
  `SpecializationID` INT NOT NULL,
  `Studyname` VARCHAR(45) NULL COMMENT 'Holds study name of the specialization',
  `Study_StudyID` INT NOT NULL,
  `Study_Faculty_FacultyID` INT NOT NULL,
  `Study_Faculty_University_UniversityID` INT NOT NULL,
  `Study_Institute_InstituteID` INT NOT NULL,
  PRIMARY KEY (`SpecializationID`, `Study_StudyID`, `Study_Faculty_FacultyID`, `Study_Faculty_University_UniversityID`, `Study_Institute_InstituteID`),
  INDEX `fk_Specialization_Study1_idx` (`Study_StudyID` ASC, `Study_Faculty_FacultyID` ASC, `Study_Faculty_University_UniversityID` ASC, `Study_Institute_InstituteID` ASC) VISIBLE,
  CONSTRAINT `fk_Specialization_Study1`
    FOREIGN KEY (`Study_StudyID` , `Study_Faculty_FacultyID` , `Study_Faculty_University_UniversityID` , `Study_Institute_InstituteID`)
    REFERENCES `Test_via_eer`.`Study` (`StudyID` , `Faculty_FacultyID` , `Faculty_University_UniversityID` , `Institute_InstituteID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Test_via_eer`.`Institute_has_Building`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Test_via_eer`.`Institute_has_Building` (
  `Institute_InstituteID` INT NOT NULL,
  `Building_BuildingID` INT NOT NULL,
  PRIMARY KEY (`Institute_InstituteID`, `Building_BuildingID`),
  INDEX `fk_Institute_has_Building_Building1_idx` (`Building_BuildingID` ASC) VISIBLE,
  INDEX `fk_Institute_has_Building_Institute1_idx` (`Institute_InstituteID` ASC) VISIBLE,
  CONSTRAINT `fk_Institute_has_Building_Institute1`
    FOREIGN KEY (`Institute_InstituteID`)
    REFERENCES `Test_via_eer`.`Institute` (`InstituteID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Institute_has_Building_Building1`
    FOREIGN KEY (`Building_BuildingID`)
    REFERENCES `Test_via_eer`.`Building` (`BuildingID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Test_via_eer`.`Paper_has_Person`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Test_via_eer`.`Paper_has_Person` (
  `Paper_PaperID` INT NOT NULL,
  `Person_idPerson` INT NOT NULL,
  PRIMARY KEY (`Paper_PaperID`, `Person_idPerson`),
  INDEX `fk_Paper_has_Person_Person1_idx` (`Person_idPerson` ASC) VISIBLE,
  INDEX `fk_Paper_has_Person_Paper1_idx` (`Paper_PaperID` ASC) VISIBLE,
  CONSTRAINT `fk_Paper_has_Person_Paper1`
    FOREIGN KEY (`Paper_PaperID`)
    REFERENCES `Test_via_eer`.`Paper` (`PaperID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Paper_has_Person_Person1`
    FOREIGN KEY (`Person_idPerson`)
    REFERENCES `Test_via_eer`.`Person` (`idPerson`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Test_via_eer`.`Study_has_Student`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Test_via_eer`.`Study_has_Student` (
  `Study_StudyID` INT NOT NULL,
  `Study_Faculty_FacultyID` INT NOT NULL,
  `Study_Faculty_University_UniversityID` INT NOT NULL,
  `Study_Institute_InstituteID` INT NOT NULL,
  `Student_StudentID` INT NOT NULL,
  PRIMARY KEY (`Study_StudyID`, `Study_Faculty_FacultyID`, `Study_Faculty_University_UniversityID`, `Study_Institute_InstituteID`, `Student_StudentID`),
  INDEX `fk_Study_has_Student_Student1_idx` (`Student_StudentID` ASC) VISIBLE,
  INDEX `fk_Study_has_Student_Study1_idx` (`Study_StudyID` ASC, `Study_Faculty_FacultyID` ASC, `Study_Faculty_University_UniversityID` ASC, `Study_Institute_InstituteID` ASC) VISIBLE,
  CONSTRAINT `fk_Study_has_Student_Study1`
    FOREIGN KEY (`Study_StudyID` , `Study_Faculty_FacultyID` , `Study_Faculty_University_UniversityID` , `Study_Institute_InstituteID`)
    REFERENCES `Test_via_eer`.`Study` (`StudyID` , `Faculty_FacultyID` , `Faculty_University_UniversityID` , `Institute_InstituteID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Study_has_Student_Student1`
    FOREIGN KEY (`Student_StudentID`)
    REFERENCES `Test_via_eer`.`Student` (`StudentID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Test_via_eer`.`Study_has_Professor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Test_via_eer`.`Study_has_Professor` (
  `Study_StudyID` INT NOT NULL,
  `Study_Faculty_FacultyID` INT NOT NULL,
  `Study_Faculty_University_UniversityID` INT NOT NULL,
  `Study_Institute_InstituteID` INT NOT NULL,
  `Professor_ProfessorID` INT NOT NULL,
  PRIMARY KEY (`Study_StudyID`, `Study_Faculty_FacultyID`, `Study_Faculty_University_UniversityID`, `Study_Institute_InstituteID`, `Professor_ProfessorID`),
  INDEX `fk_Study_has_Professor_Professor1_idx` (`Professor_ProfessorID` ASC) VISIBLE,
  INDEX `fk_Study_has_Professor_Study1_idx` (`Study_StudyID` ASC, `Study_Faculty_FacultyID` ASC, `Study_Faculty_University_UniversityID` ASC, `Study_Institute_InstituteID` ASC) VISIBLE,
  CONSTRAINT `fk_Study_has_Professor_Study1`
    FOREIGN KEY (`Study_StudyID` , `Study_Faculty_FacultyID` , `Study_Faculty_University_UniversityID` , `Study_Institute_InstituteID`)
    REFERENCES `Test_via_eer`.`Study` (`StudyID` , `Faculty_FacultyID` , `Faculty_University_UniversityID` , `Institute_InstituteID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Study_has_Professor_Professor1`
    FOREIGN KEY (`Professor_ProfessorID`)
    REFERENCES `Test_via_eer`.`Professor` (`ProfessorID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Test_via_eer`.`Mother`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Test_via_eer`.`Mother` (
  `WomanID` INT NOT NULL,
  PRIMARY KEY (`WomanID`),
  UNIQUE INDEX `WomanID_UNIQUE` (`WomanID` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Test_via_eer`.`Father`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Test_via_eer`.`Father` (
  `ManID` INT NOT NULL,
  PRIMARY KEY (`ManID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Test_via_eer`.`Person_Is_Father`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Test_via_eer`.`Person_Is_Father` (
  `Person_idPerson` INT NOT NULL,
  `Man_ManID` INT NOT NULL,
  PRIMARY KEY (`Person_idPerson`, `Man_ManID`),
  INDEX `fk_Person_has_Man_Man1_idx` (`Man_ManID` ASC) VISIBLE,
  INDEX `fk_Person_has_Man_Person1_idx` (`Person_idPerson` ASC) VISIBLE,
  CONSTRAINT `fk_Person_has_Man_Person1`
    FOREIGN KEY (`Person_idPerson`)
    REFERENCES `Test_via_eer`.`Person` (`idPerson`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Person_has_Man_Man1`
    FOREIGN KEY (`Man_ManID`)
    REFERENCES `Test_via_eer`.`Father` (`ManID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Test_via_eer`.`Person_Is_Mother`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Test_via_eer`.`Person_Is_Mother` (
  `Person_idPerson` INT NOT NULL,
  `Woman_WomanID` INT NOT NULL,
  PRIMARY KEY (`Person_idPerson`, `Woman_WomanID`),
  INDEX `fk_Person_has_Woman_Woman1_idx` (`Woman_WomanID` ASC) VISIBLE,
  INDEX `fk_Person_has_Woman_Person1_idx` (`Person_idPerson` ASC) VISIBLE,
  CONSTRAINT `fk_Person_has_Woman_Person1`
    FOREIGN KEY (`Person_idPerson`)
    REFERENCES `Test_via_eer`.`Person` (`idPerson`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Person_has_Woman_Woman1`
    FOREIGN KEY (`Woman_WomanID`)
    REFERENCES `Test_via_eer`.`Mother` (`WomanID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Test_via_eer`.`Child`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Test_via_eer`.`Child` (
  `ChildID` INT NOT NULL,
  `Mother_WomanID` INT NOT NULL,
  `Father_ManID` INT NOT NULL,
  PRIMARY KEY (`ChildID`, `Mother_WomanID`, `Father_ManID`),
  INDEX `fk_Child_Mother1_idx` (`Mother_WomanID` ASC) VISIBLE,
  INDEX `fk_Child_Father1_idx` (`Father_ManID` ASC) VISIBLE,
  CONSTRAINT `fk_Child_Mother1`
    FOREIGN KEY (`Mother_WomanID`)
    REFERENCES `Test_via_eer`.`Mother` (`WomanID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Child_Father1`
    FOREIGN KEY (`Father_ManID`)
    REFERENCES `Test_via_eer`.`Father` (`ManID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Test_via_eer`.`Person_has_Child`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Test_via_eer`.`Person_has_Child` (
  `Person_idPerson` INT NOT NULL,
  `Child_ChildID` INT NOT NULL,
  PRIMARY KEY (`Person_idPerson`, `Child_ChildID`),
  INDEX `fk_Person_has_Child_Child1_idx` (`Child_ChildID` ASC) VISIBLE,
  INDEX `fk_Person_has_Child_Person1_idx` (`Person_idPerson` ASC) VISIBLE,
  CONSTRAINT `fk_Person_has_Child_Person1`
    FOREIGN KEY (`Person_idPerson`)
    REFERENCES `Test_via_eer`.`Person` (`idPerson`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Person_has_Child_Child1`
    FOREIGN KEY (`Child_ChildID`)
    REFERENCES `Test_via_eer`.`Child` (`ChildID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Test_via_eer`.`Relation`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Test_via_eer`.`Relation` (
  `RelationID` INT NOT NULL,
  `Relationtype` VARCHAR(255) NULL COMMENT 'Holds the Relationtype, possible options are:\nGetrouwd\nGewezen echtgenoot',
  `Sor` DATE NULL COMMENT 'Holds the startdate of relationship',
  `Eor` DATE NULL COMMENT 'Holds the enddate of relationship',
  PRIMARY KEY (`RelationID`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
