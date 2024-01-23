-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema dnd_db
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `dnd_db` ;

-- -----------------------------------------------------
-- Schema dnd_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `dnd_db` DEFAULT CHARACTER SET utf8mb3 ;
USE `dnd_db` ;

-- -----------------------------------------------------
-- Table `dnd_db`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dnd_db`.`users` ;

CREATE TABLE IF NOT EXISTS `dnd_db`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NULL DEFAULT NULL,
  `last_name` VARCHAR(45) NULL DEFAULT NULL,
  `email` VARCHAR(45) NULL DEFAULT NULL,
  `password` CHAR(60) NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `dnd_db`.`parties`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dnd_db`.`parties` ;

CREATE TABLE IF NOT EXISTS `dnd_db`.`parties` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL DEFAULT NULL,
  `amount_characters` TINYINT NULL DEFAULT '0',
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_parties_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_parties_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `dnd_db`.`users` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `dnd_db`.`characters`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `dnd_db`.`characters` ;

CREATE TABLE IF NOT EXISTS `dnd_db`.`characters` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL DEFAULT NULL,
  `race` VARCHAR(45) NULL DEFAULT NULL,
  `dnd_class` VARCHAR(45) NULL DEFAULT NULL,
  `background` VARCHAR(45) NULL DEFAULT NULL,
  `alignment` VARCHAR(45) NULL DEFAULT NULL,
  `user_id` INT NOT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `party_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_character_users_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_characters_parties1_idx` (`party_id` ASC) VISIBLE,
  CONSTRAINT `fk_character_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `dnd_db`.`users` (`id`),
  CONSTRAINT `fk_characters_parties1`
    FOREIGN KEY (`party_id`)
    REFERENCES `dnd_db`.`parties` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 9
DEFAULT CHARACTER SET = utf8mb3;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
