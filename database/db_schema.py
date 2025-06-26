# database/db_schema.py

CREATE_PRODUCTS_TABLE = '''
CREATE TABLE IF NOT EXISTS Products (
    id INTEGER PRIMARY KEY,
    name TEXT,
    page_title TEXT,
    description TEXT,
    meta_description TEXT,
    price REAL,
    weight REAL,
    stock INTEGER,
    sku TEXT,
    brand TEXT,
    barcode TEXT,
    status TEXT,
    created_at TEXT,
    updated_at TEXT,
    currency TEXT
)
'''

CREATE_CATEGORIES_TABLE = '''
CREATE TABLE IF NOT EXISTS Categories (
    id INTEGER PRIMARY KEY,
    product_id INTEGER,
    name TEXT,
    description TEXT,
    FOREIGN KEY (product_id) REFERENCES Products (id)
)
'''

CREATE_IMAGES_TABLE = '''
CREATE TABLE IF NOT EXISTS Images (
    id INTEGER PRIMARY KEY,
    product_id INTEGER,
    url TEXT,
    position INTEGER,
    FOREIGN KEY (product_id) REFERENCES Products (id)
)
'''

CREATE_VARIANTS_TABLE = '''
CREATE TABLE IF NOT EXISTS Variants (
    id INTEGER PRIMARY KEY,
    product_id INTEGER,
    price REAL,
    stock INTEGER,
    weight REAL,
    discount REAL,
    FOREIGN KEY (product_id) REFERENCES Products (id)
)
'''

CREATE_OPTIONS_TABLE = '''
CREATE TABLE IF NOT EXISTS Options (
    id INTEGER PRIMARY KEY,
    variant_id INTEGER,
    product_option_id INTEGER,
    product_option_value_id INTEGER,
    option_type TEXT,
    name TEXT,
    value TEXT,
    FOREIGN KEY (variant_id) REFERENCES Variants (id)
)
'''

CREATE_ORDERS_TABLE = '''
CREATE TABLE IF NOT EXISTS Orders (
    id INTEGER PRIMARY KEY,
    number INTEGER,
    status TEXT,
    payment_status TEXT,
    payment_method TEXT,
    shipping_method TEXT,
    shipping_status TEXT,
    created_at TEXT,
    completed_at TEXT,
    currency TEXT,
    subtotal REAL,
    tax REAL,
    shipping_tax REAL,
    shipping REAL,
    total REAL,
    discount REAL,
    shipping_discount REAL,
    gift_cards_discount REAL,
    fulfillment_status TEXT,
    shipping_required BOOLEAN,
    additional_information TEXT
)
'''

CREATE_CUSTOMERS_TABLE = '''
CREATE TABLE IF NOT EXISTS Customers (
    id INTEGER PRIMARY KEY,
    order_id INTEGER,
    email TEXT,
    phone TEXT,
    fullname TEXT,
    FOREIGN KEY (order_id) REFERENCES Orders (id)
)
'''

CREATE_SHIPPING_ADDRESSES_TABLE = '''
CREATE TABLE IF NOT EXISTS ShippingAddresses (
    id INTEGER PRIMARY KEY,
    order_id INTEGER,
    name TEXT,
    surname TEXT,
    address TEXT,
    city TEXT,
    postal TEXT,
    region TEXT,
    country TEXT,
    complement TEXT,
    latitude REAL,
    longitude REAL,
    municipality TEXT,
    FOREIGN KEY (order_id) REFERENCES Orders (id)
)
'''

CREATE_BILLING_ADDRESSES_TABLE = '''
CREATE TABLE IF NOT EXISTS BillingAddresses (
    id INTEGER PRIMARY KEY,
    order_id INTEGER,
    name TEXT,
    surname TEXT,
    taxid TEXT,
    address TEXT,
    city TEXT,
    postal TEXT,
    region TEXT,
    country TEXT,
    complement TEXT,
    municipality TEXT,
    FOREIGN KEY (order_id) REFERENCES Orders (id)
)
'''

CREATE_ORDER_PRODUCTS_TABLE = '''
CREATE TABLE IF NOT EXISTS OrderProducts (
    id INTEGER PRIMARY KEY,
    order_id INTEGER,
    variant_id INTEGER,
    sku TEXT,
    name TEXT,
    qty INTEGER,
    price REAL,
    tax REAL,
    discount REAL,
    weight REAL,
    image TEXT,
    type TEXT,
    FOREIGN KEY (order_id) REFERENCES Orders (id)
)
'''
