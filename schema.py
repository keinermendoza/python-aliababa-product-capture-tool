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

request_cotations_table = Table(
    "request_cotations",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(50), CheckConstraint("title != ''"), unique=True, nullable=False),
    Column("created", Date, nullable=False, server_default=text('CURRENT_TIMESTAMP')),
)

selected_request_cotation_table = Table(
    "selected_request_cotation",
    metadata,
    Column("request_cotation_id", Integer, ForeignKey('request_cotations.id', ondelete='CASCADE'), nullable=False)
)

cotations_table = Table(
    "cotations",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("created", DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP')),
    Column("company_name", String(200), CheckConstraint("company_name != ''"), nullable=False),
    Column("company_url", String(300), CheckConstraint("company_url != ''"), nullable=False),
    Column("product_name", String(200), CheckConstraint("product_name != ''"), nullable=False),
    Column("product_url", String(300), CheckConstraint("product_url != ''"), nullable=False),
    Column("public_minimum_price", Numeric(precision=9, scale=2), CheckConstraint('public_minimum_price >= 0'), nullable=False),
    Column("public_minimum_quantity", String(300), CheckConstraint("public_minimum_quantity != ''"), nullable=False),
    Column("request_cotation_id", Integer, ForeignKey('request_cotations.id', ondelete='CASCADE'), nullable=False),
)
