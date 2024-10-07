

-- Varmista että käyttäjällä tarvittavat oikeudet tietokantaan


-- Poista taulut, jos ne ovat jo olemassa:
SET FOREIGN_KEY_CHECKS = 0; -- vierasavainten tarkistukset pois päältä

DROP TABLE goal
DROP TABLE goal_reached
DROP TABLE game



-- luodaan uudet taulut:

-- luodaan taulu user_information
CREATE TABLE user_information (
    name VARCHAR(255) PRIMARY KEY
);

-- luodaan taulu game
CREATE TABLE game (
    game_id INT AUTO_INCREMENT PRIMARY KEY,
    continent VARCHAR(255)
);


-- luodaan taulu user_games
CREATE TABLE user_games (
    game_id INT,
    user_points INT,
    name VARCHAR(255),
    FOREIGN KEY (name) REFERENCES user_information(name),
    FOREIGN KEY (game_id) REFERENCES game(game_id)
);



SET FOREIGN_KEY_CHECKS = 1; -- vierasavainten tarkistukset takaisin päälle
