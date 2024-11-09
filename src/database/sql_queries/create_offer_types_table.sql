CREATE TABLE IF NOT EXISTS offer_type_items(
    offer_type_item_id SERIAL PRIMARY KEY,
    offer_type TEXT,
    offer_type_item TEXT,
    offer_type_city TEXT,
    offer_type_item_url TEXT,
    strict_match_flag BOOLEAN
);
