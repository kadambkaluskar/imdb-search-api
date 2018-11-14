CREATE SCHEMA `imdb_movie` DEFAULT CHARACTER SET swe7 COLLATE swe7_swedish_ci ;


CREATE TABLE `imdb_movie`.`users` (
  `user_id` INT NOT NULL AUTO_INCREMENT COMMENT 'to store user details',
  `username` VARCHAR(45) NOT NULL,
  `phone` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `password` VARCHAR(100) NOT NULL,
  `is_admin` TINYINT NULL DEFAULT 0,
  PRIMARY KEY (`user_id`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC),
  UNIQUE INDEX `phone_UNIQUE` (`phone` ASC),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC));


CREATE TABLE `imdb_movie`.`movies` (
  `movie_id` INT NOT NULL AUTO_INCREMENT,
  `movie_name` VARCHAR(45) NOT NULL,
  `movie_director` VARCHAR(45) NOT NULL,
  `movie_99_popularity` DECIMAL(6,3) NOT NULL,
  `movie_genre` VARCHAR(100) NOT NULL,
  `movie_imdb_score` DECIMAL(6,3) NOT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`movie_id`),
  UNIQUE INDEX `movie_name_UNIQUE` (`movie_name` ASC));


INSERT INTO `imdb_movie`.`users` (`user_id`, `username`, `phone`, `email`, `token`, `is_admin`) VALUES ('1', 'kadamb', '911234567890', 'k@k.com', '46a3635656d81e4ff9a01867806bd3fb0abf95f5ba7cc5a37ba4bb3a4b359aad', '1');
INSERT INTO `imdb_movie`.`users` (`user_id`, `username`, `phone`, `email`, `token`, `is_admin`) VALUES ('2', 'kaluskar', '910987654321', 'j@j.com', '46a3635656d81e4ff9a01867806bd3fb0abf95f5ba7cc5a37ba4bb3a4b359aad', '0');

