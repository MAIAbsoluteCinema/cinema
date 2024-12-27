CREATE TABLE movies (
    movieId BIGINT , -- ID фильма из TMDb, уникальный идентификатор
    title TEXT,
    genres TEXT,
    tmdbid BIGINT , -- ID фильма из TMDb, уникальный идентификатор
    overview TEXT,              -- Описание фильма
    production_countries TEXT, -- Массив стран производства
    -- release_date DATE,          -- Дата выхода
    runtime INT,                -- Продолжительность фильма в минутах
    spoken_languages TEXT,    -- Массив языков
    vote_average NUMERIC(3, 1), -- Средний рейтинг, до 1 знака после запятой
    vote_count INT              -- Количество голосов
);



CREATE TABLE rating (
    userId BIGINT,         -- ID пользователя
    movieId BIGINT,        -- ID фильма
    rating NUMERIC(2, 1),   -- Рейтинг, с одним знаком после запятой
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP    -- Временная метка рейтинга
);


-- Создаем временную таблицу без ограничения PRIMARY KEY

-- Копируем данные во временную таблицу
COPY movies (movieId, title, genres, tmdbid, overview, production_countries, runtime, spoken_languages, vote_average, vote_count)
FROM '/docker-entrypoint-initdb.d/first_1000_movies.csv'
DELIMITER ','
CSV HEADER;

-- COPY movies (movieId, title, genres)
-- FROM '/docker-entrypoint-initdb.d/movie.csv'
-- DELIMITER ','
-- CSV HEADER;

COPY rating (userId, movieId, rating,timestamp)
FROM '/docker-entrypoint-initdb.d/first_3000_rating.csv'
DELIMITER ','
CSV HEADER;