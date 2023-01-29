CREATE TABLE IF NOT EXISTS offers(
    offer_id SERIAL PRIMARY KEY,
    offer_type_id INTEGER,
    offer_avito_id TEXT,
    offer_title TEXT,
    offer_city TEXT,
    offer_description TEXT NULL,
    offer_price BIGINT NULL,
    offer_currency TEXT NULL,
    seller_id INTEGER NULL, 
    offer_url TEXT
);
