CREATE TABLE movies (
    movieId BIGINT PRIMARY KEY, -- ID фильма из TMDb, уникальный идентификатор
    title TEXT,
    genres TEXT
    -- tmdb_id BIGINT, -- ID фильма из TMDb, уникальный идентификатор
    -- overview TEXT,              -- Описание фильма
    -- production_countries TEXT[], -- Массив стран производства
    -- release_date DATE,          -- Дата выхода
    -- runtime INT,                -- Продолжительность фильма в минутах
    -- spoken_languages TEXT[],    -- Массив языков
    -- vote_average NUMERIC(3, 1), -- Средний рейтинг, до 1 знака после запятой
    -- vote_count INT              -- Количество голосов
    -- poster_path TEXT,           -- Путь к постеру
    -- backdrop_path TEXT          -- Путь к фоновой картинке
);



CREATE TABLE rating (
    userId BIGINT,         -- ID пользователя
    movieId BIGINT,        -- ID фильма
    rating NUMERIC(2, 1),   -- Рейтинг, с одним знаком после запятой
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP    -- Временная метка рейтинга
);


-- COPY movies (movie_id, title, genres, tmdb_id, overview, production_countries, release_date, runtime, spoken_languages, vote_average, vote_count)
-- FROM '/docker-entrypoint-initdb.d/first_1000_movies.csv'
-- DELIMITER ','
-- CSV HEADER;

COPY movies (movieId, title, genres)
FROM '/docker-entrypoint-initdb.d/movie.csv'
DELIMITER ','
CSV HEADER;