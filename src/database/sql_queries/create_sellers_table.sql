CREATE TABLE IF NOT EXISTS sellers(
    seller_id SERIAL PRIMARY KEY,
    seller_avito_id BIGINT,
    seller_name TEXT,
    seller_rating REAL NULL
);