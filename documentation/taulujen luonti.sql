




-- luodaan taulu user_information
CREATE TABLE user_information (
    name VARCHAR(255) PRIMARY KEY
);


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






