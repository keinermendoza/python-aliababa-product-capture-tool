from sqlalchemy import (
    text,
    func,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Numeric,
    Text,
    Date,
    DateTime,
    Boolean,
    ForeignKey,
    CheckConstraint,
    UniqueConstraint,
    Index
)

metadata = MetaData()

request_for_quotations_table = Table(
    "request_for_quotations",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(50), CheckConstraint("title != ''"), unique=True, nullable=False),
    Column("quantity", Integer, CheckConstraint("quantity > 0"), nullable=False),
    Column("created", DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP')),
)

active_request_for_quotations_table = Table(
    "active_request_for_quotations",
    metadata,
    Column("request_for_quotation_id", Integer, ForeignKey('request_for_quotations.id', ondelete='CASCADE'), nullable=False)
)

quotation_status_table = Table(
    "quotation_status",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(20), unique=True, nullable=False)
)

quotations_table = Table(
    "quotations",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("created", DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP')),
    Column("company_name", String(200), CheckConstraint("company_name != ''"), nullable=False),
    Column("company_url", String(300), CheckConstraint("company_url != ''"), nullable=False),
    Column("product_name", String(200), CheckConstraint("product_name != ''"), nullable=False),
    Column("product_url", String(300), CheckConstraint("product_url != ''"), nullable=False),
    Column("request_for_quotation_id", Integer, ForeignKey('request_for_quotations.id', ondelete='CASCADE'), nullable=False),
    Column("public_minimum_price", String(20), nullable=True),
    Column("public_minimum_quantity", String(300), nullable=True),
    Column("seller_name", String(50), nullable=True),
    Column("cheapest_shipping_company", String(8), nullable=True),
    Column("cheapest_shipping_cost", Numeric(8, 2), nullable=True),
    Column("unit_product_price_offered", Numeric(8, 2), nullable=True),
    Column("description", Text, nullable=True),
    Column("status_id", Integer, ForeignKey('quotation_status.id', ondelete='RESTRICT'), nullable=False),
    UniqueConstraint("request_for_quotation_id", 'product_name', 'company_name', name='uix_cotation_company_and_product_names')
)

