-- Active: 1779073942272@@127.0.0.1@3306@steam_games_db

SELECT COUNT(*) AS total_reviews
FROM reviews;

SELECT COUNT(*) AS total_genres
FROM genres;

SELECT *
FROM applications
LIMIT 10;

-- 1. Tổng số Games
SELECT COUNT(*) AS total_games
FROM applications;

-- 2. Số lượng game free và paid
SELECT 
    is_free,
    COUNT(*) AS total
FROM applications
GROUP BY is_free;

-- 3. Top 10 games có nhiều recommendations nhất
SELECT
    appid,
    name,
    recommendations_total
FROM applications
WHERE recommendations_total IS NOT NULL
ORDER BY recommendations_total DESC
LIMIT 10;


-- 4. Thống kê số game hỗ trợ từng nền tảng
SELECT
    SUM(mat_supports_windows) AS windows_games,
    SUM(mat_supports_mac) AS mac_games,
    SUM(mat_supports_linux) AS linux_games
FROM applications;


-- 5. Top games có giá cao nhất
SELECT
    appid,
    name,
    mat_final_price
FROM applications
WHERE mat_final_price IS NOT NULL
ORDER BY mat_final_price DESC
LIMIT 9;

-- 6. Các game có số lượng recommendations cao hơn mức trung bình toàn bộ dataset
SELECT
    appid,
    name,
    recommendations_total
FROM applications
WHERE recommendations_total > (
    SELECT AVG(recommendations_total)
    FROM applications
    WHERE recommendations_total IS NOT NULL
)
ORDER BY recommendations_total DESC
LIMIT 20;

-- 7. Kiểm tra missing values ở một số cột quan trọng
SELECT
    SUM(CASE WHEN name IS NULL THEN 1 ELSE 0 END) AS missing_name,
    SUM(CASE WHEN release_date IS NULL THEN 1 ELSE 0 END) AS missing_release_date,
    SUM(CASE WHEN metacritic_score IS NULL THEN 1 ELSE 0 END) AS missing_metacritic_score,
    SUM(CASE WHEN recommendations_total IS NULL THEN 1 ELSE 0 END) AS missing_recommendations,
    SUM(CASE WHEN mat_final_price IS NULL THEN 1 ELSE 0 END) AS missing_final_price,
    SUM(CASE WHEN mat_initial_price IS NULL THEN 1 ELSE 0 END) AS missing_initial_price
FROM applications;

   
--8. Tính tỷ lệ missing của một số cột quan trọng
SELECT
    ROUND (SUM(CASE WHEN metacritic_score IS NULL THEN 1 ELSE 0 END) * 100.0 /COUNT(*), 2) AS missing_metarcritic_percent,
    ROUND (SUM(CASE WHEN recommendations_total IS NULL THEN 1 ELSE 0 END) * 100.0 /COUNT(*), 2) AS missing_recommendations_percent,
    ROUND (SUM(CASE WHEN mat_final_price IS NULL THEN 1 ELSE 0 END) * 100.0 /COUNT(*), 2) AS missing_final_price_percent,
    ROUND (SUM(CASE WHEN release_date IS NULL THEN 1 ELSE 0 END) * 100.0 /COUNT(*), 2) AS missing_release_date_percent
FROM applications;


-- 9. View data nền dùng cho DS/ML
CREATE OR REPLACE VIEW vw_applications_ml_base AS
SELECT
    appid,
    name,
    type,
    is_free,
    required_age,
    release_date,
    metacritic_score,
    recommendations_total,
    mat_initial_price,
    mat_final_price,
    mat_discount_percent,
    mat_currency,
    mat_achievement_count,
    mat_supports_windows,
    mat_supports_mac,
    mat_supports_linux,
    short_description,
    supported_languages,
    created_at,
    updated_at
FROM applications
WHERE name IS NOT NULL;


-- 10. Check view vừa tạo
SELECT * FROM vw_applications_ml_base LIMIT 10;

-- 11. Đếm số bản ghi trong view
SELECT COUNT(*) AS total_records_in_view
FROM vw_applications_ml_base;

-- 12. View dữ liệu recommendation dùng cho hệ khuyến nghị content-based
CREATE OR REPLACE VIEW vw_recommendation_base AS
SELECT
    appid,
    name,
    type,
    short_description
FROM applications
WHERE name IS NOT NULL
  AND short_description IS NOT NULL;

-- 13. Check view recommendation
SELECT * FROM vw_recommendation_base LIMIT 10;

-- 14. Thống kê số lượng game theo type
SELECT
    type,
    COUNT(*) AS total
FROM applications
GROUP BY type
ORDER BY total DESC;

-- 15. Thống kê giá trung bình theo từng loại game
SELECT
    type,
    ROUND(AVG(mat_final_price), 2) AS avg_final_price
FROM applications
WHERE mat_final_price IS NOT NULL
GROUP BY type   
ORDER BY avg_final_price DESC;

-- 16. Game trả phí có discount cao nhất
SELECT
    appid,
    name,
    mat_initial_price,
    mat_final_price,
    mat_discount_percent
FROM applications
WHERE mat_discount_percent IS NOT NULL AND mat_discount_percent > 0
ORDER BY mat_discount_percent DESC LIMIT 20;

-- 17.join game và genre
SELECT
    a.appid,
    a.name,
    g.name AS genre_name
FROM applications a
JOIN application_genres ag
    ON a.appid = ag.appid
JOIN genres g
    ON ag.genre_id = g.id
LIMIT 20;
