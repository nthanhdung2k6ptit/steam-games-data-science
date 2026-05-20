-- Active: 1779073942272@@127.0.0.1@3306@steam_games_db
CREATE DATABASE steam_games_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE steam_games_db;

SHOW TABLES;
DESCRIBE application_genres;
DESCRIBE genres;
DESCRIBE application_developers;
DESCRIBE developers;
DESCRIBE application_publishers;
DESCRIBE publishers;

-- Check duplicate applications
SELECT appid, COUNT(*) AS total
FROM applications
GROUP BY appid
HAVING COUNT(*) > 1
LIMIT 10;

-- Check duplicate genres
SELECT id, COUNT(*) AS total
FROM genres
GROUP BY id
HAVING COUNT(*) > 1
LIMIT 10;

-- Check duplicate developers
SELECT id, COUNT(*) AS total
FROM developers
GROUP BY id
HAVING COUNT(*) > 1
LIMIT 10;

-- Check duplicate publishers
SELECT id, COUNT(*) AS total
FROM publishers
GROUP BY id
HAVING COUNT(*) > 1
LIMIT 10;

-- application_genres có appid không tồn tại trong applications?
SELECT ag.appid
FROM application_genres ag
LEFT JOIN applications a
    ON ag.appid = a.appid
WHERE a.appid IS NULL
LIMIT 10;

-- application_genres có genre_id không tồn tại trong genres?
SELECT ag.genre_id
FROM application_genres ag
LEFT JOIN genres g
    ON ag.genre_id = g.id
WHERE g.id IS NULL
LIMIT 10;


-- application_developers có appid không tồn tại?
SELECT ad.appid
FROM application_developers ad
LEFT JOIN applications a
    ON ad.appid = a.appid
WHERE a.appid IS NULL
LIMIT 10;

-- application_developers có developer_id không tồn tại?
SELECT ad.developer_id
FROM application_developers ad
LEFT JOIN developers d
    ON ad.developer_id = d.id
WHERE d.id IS NULL
LIMIT 10;


-- application_publishers có appid không tồn tại?
SELECT ap.appid
FROM application_publishers ap
LEFT JOIN applications a
    ON ap.appid = a.appid
WHERE a.appid IS NULL
LIMIT 10;

-- application_publishers có publisher_id không tồn tại?
SELECT ap.publisher_id
FROM application_publishers ap
LEFT JOIN publishers p
    ON ap.publisher_id = p.id
WHERE p.id IS NULL
LIMIT 10;