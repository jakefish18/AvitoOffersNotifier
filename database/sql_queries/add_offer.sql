INSERT INTO offers (
    offer_type_id,
    offer_avito_id,
    offer_title,
    offer_city,
    offer_description,
    offer_price,
    offer_currency,
    seller_id,
    offer_url
) VALUES (
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s
);
