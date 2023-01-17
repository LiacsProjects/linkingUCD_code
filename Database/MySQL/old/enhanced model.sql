SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema lucd_reduced
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema lucd_reduced
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `lucd_reduced` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `lucd_reduced` ;

-- -----------------------------------------------------
-- Table `lucd_reduced`.`type_of_person`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `lucd_reduced`.`type_of_person` (
  `PersonID` INT NOT NULL AUTO_INCREMENT,
  `PersonType` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`PersonID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `lucd_reduced`.`type_of_relation`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `lucd_reduced`.`type_of_relation` (
  `RelationID` INT NOT NULL AUTO_INCREMENT,
  `RelationType` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`RelationID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `lucd_reduced`.`person`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `lucd_reduced`.`person` (
  `PersonID` INT NOT NULL AUTO_INCREMENT,
  `TypeOfPerson` INT NULL DEFAULT NULL,
  `FirstName` VARCHAR(50) NULL DEFAULT NULL,
  `LastName` VARCHAR(50) NULL DEFAULT NULL,
  `FamilyName` VARCHAR(50) NULL DEFAULT NULL,
  `Affix` VARCHAR(45) NULL DEFAULT NULL COMMENT 'de, van, van der, etc.',
  `Nickname` VARCHAR(50) NULL DEFAULT NULL,
  `Gender` VARCHAR(45) NULL DEFAULT NULL,
  `Nationality` VARCHAR(100) NULL DEFAULT NULL,
  `Religion` VARCHAR(100) NULL DEFAULT NULL,
  `Status` VARCHAR(100) NULL DEFAULT NULL,
  `Job` VARCHAR(100) NULL DEFAULT NULL,
  `SourceName` VARCHAR(50) NULL DEFAULT NULL,
  `SourceRating` INT NULL DEFAULT NULL,
  PRIMARY KEY (`PersonID`),
  INDEX `TypeOfPerson_idx` (`TypeOfPerson` ASC) VISIBLE,
  CONSTRAINT `TypeOfPerson_person`
    FOREIGN KEY (`TypeOfPerson`)
    REFERENCES `lucd_reduced`.`type_of_person` (`PersonID`))
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `lucd_reduced`.`type_of_engagement`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `lucd_reduced`.`type_of_engagement` (
  `EngagementID` INT NOT NULL AUTO_INCREMENT,
  `EngagementType` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`EngagementID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `lucd_reduced`.`type_of_expertise`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `lucd_reduced`.`type_of_expertise` (
  `ExpertiseID` INT NOT NULL AUTO_INCREMENT,
  `ExpertiseType` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`ExpertiseID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `lucd_reduced`.`type_of_faculty`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `lucd_reduced`.`type_of_faculty` (
  `FacultyID` INT NOT NULL AUTO_INCREMENT,
  `FacultyType` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`FacultyID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `lucd_reduced`.`type_of_position`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `lucd_reduced`.`type_of_position` (
  `PositionID` INT NOT NULL AUTO_INCREMENT,
  `PositionType` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`PositionID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `lucd_reduced`.`engagement`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `lucd_reduced`.`engagement` (
  `EngagementID` INT NOT NULL AUTO_INCREMENT,
  `TypeOfEngagement` INT NOT NULL,
  `TypeOfPosition` INT NULL DEFAULT NULL,
  `TypeOfExpertise` INT NULL DEFAULT NULL,
  `TypeOfFaculty` INT NULL DEFAULT NULL,
  `StartDate` DATE NULL DEFAULT NULL,
  `EndDate` DATE NULL DEFAULT NULL,
  `SourceName` VARCHAR(50) NULL DEFAULT NULL,
  `SourceRating` INT NULL DEFAULT NULL,
  `PersonID_engagement` INT NOT NULL,
  PRIMARY KEY (`EngagementID`),
  INDEX `TypeOfPosition_idx` (`TypeOfPosition` ASC) VISIBLE,
  INDEX `TypeOfExpertise_engagement_idx` (`TypeOfExpertise` ASC) VISIBLE,
  INDEX `TypeOfEngagement_engagement_idx` (`TypeOfEngagement` ASC) VISIBLE,
  INDEX `TypeOfFaculty_engagement_idx` (`TypeOfFaculty` ASC) VISIBLE,
  INDEX `PersonID_engagement_idx` (`PersonID_engagement` ASC) VISIBLE,
  CONSTRAINT `TypeOfEngagement_engagement`
    FOREIGN KEY (`TypeOfEngagement`)
    REFERENCES `lucd_reduced`.`type_of_engagement` (`EngagementID`),
  CONSTRAINT `TypeOfExpertise_engagement`
    FOREIGN KEY (`TypeOfExpertise`)
    REFERENCES `lucd_reduced`.`type_of_expertise` (`ExpertiseID`),
  CONSTRAINT `TypeOfFaculty_engagement`
    FOREIGN KEY (`TypeOfFaculty`)
    REFERENCES `lucd_reduced`.`type_of_faculty` (`FacultyID`),
  CONSTRAINT `TypeOfPosition_engagement`
    FOREIGN KEY (`TypeOfPosition`)
    REFERENCES `lucd_reduced`.`type_of_position` (`PositionID`),
  CONSTRAINT `PersonID_engagement`
    FOREIGN KEY (`PersonID_engagement`)
    REFERENCES `lucd_reduced`.`person` (`PersonID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `lucd_reduced`.`type_of_location`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `lucd_reduced`.`type_of_location` (
  `LocationID` INT NOT NULL AUTO_INCREMENT,
  `LocationType` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`LocationID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `lucd_reduced`.`location`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `lucd_reduced`.`location` (
  `LocationID` INT NOT NULL AUTO_INCREMENT,
  `TypeOfLocation` INT NOT NULL,
  `Country` VARCHAR(100) NULL DEFAULT NULL,
  `City` VARCHAR(100) NULL DEFAULT NULL,
  `Street` VARCHAR(100) NULL DEFAULT NULL,
  `HouseNumber` VARCHAR(10) NULL DEFAULT NULL COMMENT 'VARCHAR to include entries such 10a',
  `Region` VARCHAR(100) NULL DEFAULT NULL,
  `StartDate` DATE NULL DEFAULT NULL,
  `EndDate` DATE NULL DEFAULT NULL,
  `SourceName` VARCHAR(50) NULL DEFAULT NULL,
  `SourceRating` INT NULL DEFAULT NULL,
  `PersonID_location` INT NOT NULL,
  PRIMARY KEY (`LocationID`),
  INDEX `TypeOfLocation_location_idx` (`TypeOfLocation` ASC) VISIBLE,
  INDEX `PersonID_location_idx` (`PersonID_location` ASC) VISIBLE,
  CONSTRAINT `PersonID_location`
    FOREIGN KEY (`PersonID_location`)
    REFERENCES `lucd_reduced`.`person` (`PersonID`),
  CONSTRAINT `TypeOfLocation_location`
    FOREIGN KEY (`TypeOfLocation`)
    REFERENCES `lucd_reduced`.`type_of_location` (`LocationID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `lucd_reduced`.`relation`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `lucd_reduced`.`relation` (
  `RelationID` INT NOT NULL AUTO_INCREMENT,
  `TypeOfRelation` INT NOT NULL,
  `FromPersonID` INT NOT NULL,
  `ToPersonID` INT NOT NULL,
  `Event` VARCHAR(50) NULL,
  `EventDate` DATE NULL,
  `EventPlace` VARCHAR(100) NULL,
  `SourceName` VARCHAR(50) NULL,
  `SourceWebLink` VARCHAR(150) NULL,
  `SourceRating` INT NULL,
  `LinkClass` INT NULL COMMENT '0 = Potential Link (needs second/human verification)\n1 = Certain Link',
  `Remark` VARCHAR(150) NULL,
  PRIMARY KEY (`RelationID`),
  INDEX `ToPersonID_ptp_idx` (`ToPersonID` ASC) VISIBLE,
  INDEX `FromPersonID_ptp` (`FromPersonID` ASC) VISIBLE,
  INDEX `TypeOfRelation_ptp_idx` (`TypeOfRelation` ASC) VISIBLE,
  CONSTRAINT `FromPersonID_ptp`
    FOREIGN KEY (`FromPersonID`)
    REFERENCES `lucd_reduced`.`person` (`PersonID`),
  CONSTRAINT `ToPersonID_ptp`
    FOREIGN KEY (`ToPersonID`)
    REFERENCES `lucd_reduced`.`person` (`PersonID`),
  CONSTRAINT `TypeOfRelation_ptp`
    FOREIGN KEY (`TypeOfRelation`)
    REFERENCES `lucd_reduced`.`type_of_relation` (`RelationID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
