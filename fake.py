quotation_status = [
    {"name": "just quoted"},
    {"name": "waiting for me"},
    {"name": "need shipping quotation"},
    {"name": "completed"},
    {"name": "discarted"},
    {"name": "selected"},
]

fake_request_for_quotations = [
    {
        "request": {"title": "sportive shoes", "quantity": 200},
        "quotations": [
            {
                "company_name": "Global Sports Corp",
                "company_url": "https://globalsports.com",
                "product_name": "AirMax Runner Z",
                "product_url": "https://globalsports.com/products/airmax-runner-z",
                "public_minimum_price": "$45.00",
                "public_minimum_quantity": "100 units",
                "seller_name": "John Doe",
                "cheapest_shipping_company": "DHL",
                "cheapest_shipping_cost": 150.50,
                "unit_product_price_offered": 42.00,
                "status_id": 1
            },
            {
                "company_name": "Footwear Factory Inc",
                "company_url": "https://ffactory.net",
                "product_name": "Elite Sport Sneakers",
                "product_url": "https://ffactory.net/catalog/elite-sport",
                "public_minimum_price": "$38.50",
                "public_minimum_quantity": "500 units",
                "seller_name": "Alice Smith",
                "cheapest_shipping_company": "FedEx",
                "cheapest_shipping_cost": 210.00,
                "unit_product_price_offered": 40.00,
                "status_id": 1

            }
        ]
    },
    {
        "request": {"title": "smarthwatch", "quantity": 50},
        "quotations": [
            {
                "company_name": "Tech Gadgets Ltd",
                "company_url": "https://techgadgets.io",
                "product_name": "Smart-V2 Pro",
                "product_url": "https://techgadgets.io/v2-pro",
                "public_minimum_price": "$89.99",
                "public_minimum_quantity": "10 units",
                "seller_name": "Roberto Tech",
                "cheapest_shipping_company": "UPS",
                "cheapest_shipping_cost": 45.00,
                "unit_product_price_offered": 85.50,
                "status_id": 1
            },
            {
                "company_name": "Future Electronics",
                "company_url": "https://future-elec.com",
                "product_name": "Z-Watch Edition",
                "product_url": "https://future-elec.com/z-watch",
                "public_minimum_price": "$110.00",
                "public_minimum_quantity": "1 unit",
                "seller_name": "Lin Xiao",
                "cheapest_shipping_company": "EMS",
                "cheapest_shipping_cost": 30.25,
                "unit_product_price_offered": 98.00,
                "status_id": 1
            }
        ]
    }
]