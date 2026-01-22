-- Create lokup table for store the available quation status
CREATE TABLE IF NOT EXISTS "quotation_status" (
    "id" INTEGER,
    "name" UNIQUE TEXT NOT NULL,
    PRIMARY KEY("id")
);

-- Alter name table for make changes in foreing key
ALTER TABLE quotations RENAME TO quotations_temp;

-- Recreate the quotations table with new foreing key
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
    status_id INTEGER,
    PRIMARY KEY (id), 
    CONSTRAINT uix_cotation_company_and_product_names UNIQUE (request_for_quotation_id, product_name, company_name), 
    FOREIGN KEY(request_for_quotation_id) REFERENCES "request_for_quotations" (id) ON DELETE CASCADE,
    FOREIGN KEY(status_id) REFERENCES "quotation_status" (id) ON DELETE RESTRICT
);

-- Populates the quotation status table
INSERT INTO "quotation_status" ("name")
VALUES
    ('just quoted'),
    ('waiting for me'),
    ('need shipping quotation'),
    ('completed'),
    ('discarted'),
    ('selected');

-- fill the new quotations table with old data and default value
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
    unit_product_price_offered,
    status_id
) SELECT
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
    unit_product_price_offered,
    1
    FROM "quotations_temp";

-- Drop temporary table
DROP TABLE quotations_temp;