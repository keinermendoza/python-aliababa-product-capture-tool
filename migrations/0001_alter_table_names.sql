-- Fix misspelling in table and column names.
-- Add new tracking columns to the quotations table.
-- Update unique constraint to prevent duplicate products from the same company across multiple pages.

-- rename tables
ALTER TABLE request_cotations RENAME TO request_for_quotations;
ALTER TABLE selected_request_cotation RENAME TO active_request_for_quotations;
ALTER TABLE quotations RENAME TO quotations_temp;

-- rename column in active_request_for_quotations
ALTER TABLE active_request_for_quotations RENAME COLUMN request_cotation_id TO request_for_quotation_id;

-- The previous table constraint was not sufficient to prevent duplicate data.
-- It was necessary to recreate the entire table because SQLite does not support modifying constraints on an existing table
CREATE TABLE IF NOT EXISTS "quotations" (
    id INTEGER NOT NULL, 
    created DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, 
    company_name VARCHAR(200) NOT NULL CHECK (company_name != ''), 
    company_url VARCHAR(300) NOT NULL CHECK (company_url != ''), 
    product_name VARCHAR(200) NOT NULL CHECK (product_name != ''), 
    product_url VARCHAR(300) NOT NULL CHECK (product_url != ''), 
    public_minimum_price VARCHAR(20), 
    public_minimum_quantity VARCHAR(300), 
    request_for_quotation_id INTEGER NOT NULL,
    seller_name VARCHAR(50) NULL,
    cheapest_shipping_company VARCHAR(8) NULL,
    cheapest_shipping_cost NUMERIC NULL,
    unit_product_price_offered NUMERIC NULL,
    PRIMARY KEY (id), 
    CONSTRAINT uix_cotation_company_and_product_names UNIQUE (request_for_quotation_id, product_name, company_name), 
    FOREIGN KEY(request_for_quotation_id) REFERENCES "request_for_quotations" (id) ON DELETE CASCADE
);

INSERT INTO "quotations" (
    id,
    created,
    company_name,
    company_url,
    product_name,
    product_url,
    public_minimum_price,
    public_minimum_quantity,
    request_for_quotation_id,
    seller_name,
    cheapest_shipping_company,
    cheapest_shipping_cost,
    unit_product_price_offered
) 
    SELECT 
        id,
        created,
        company_name,
        company_url,
        product_name,
        product_url,
        public_minimum_price,
        public_minimum_quantity,
        request_cotation_id,
        NULL,
        NULL,
        NULL,
        NULL
    FROM "quotations_temp";

DROP TABLE "quotations_temp";