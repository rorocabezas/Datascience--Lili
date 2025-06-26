# database/db_manager.py
import sqlite3
import pandas as pd

from .db_schema import (
    CREATE_PRODUCTS_TABLE, CREATE_CATEGORIES_TABLE, CREATE_IMAGES_TABLE,
    CREATE_VARIANTS_TABLE, CREATE_OPTIONS_TABLE, CREATE_ORDERS_TABLE,
    CREATE_CUSTOMERS_TABLE, CREATE_SHIPPING_ADDRESSES_TABLE,
    CREATE_BILLING_ADDRESSES_TABLE, CREATE_ORDER_PRODUCTS_TABLE
)

def create_db():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    cursor.execute(CREATE_PRODUCTS_TABLE)
    cursor.execute(CREATE_CATEGORIES_TABLE)
    cursor.execute(CREATE_IMAGES_TABLE)
    cursor.execute(CREATE_VARIANTS_TABLE)
    cursor.execute(CREATE_OPTIONS_TABLE)
    cursor.execute(CREATE_ORDERS_TABLE)
    cursor.execute(CREATE_CUSTOMERS_TABLE)
    cursor.execute(CREATE_SHIPPING_ADDRESSES_TABLE)
    cursor.execute(CREATE_BILLING_ADDRESSES_TABLE)
    cursor.execute(CREATE_ORDER_PRODUCTS_TABLE)

    conn.commit()
    conn.close()

def insert_product_data_into_db(data):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    for item in data:
        product = item['product']

        cursor.execute('''
        INSERT OR IGNORE INTO Products (id, name, page_title, description, meta_description, price, weight, stock, sku, brand, barcode, status, created_at, updated_at, currency)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            product['id'], product['name'], product['page_title'], product['description'],
            product['meta_description'], product['price'], product['weight'], product['stock'],
            product['sku'], product['brand'], product['barcode'], product['status'],
            product['created_at'], product['updated_at'], product['currency']
        ))

        for category in product['categories']:
            cursor.execute('''
            INSERT OR IGNORE INTO Categories (id, product_id, name, description)
            VALUES (?, ?, ?, ?)
            ''', (category['id'], product['id'], category['name'], category.get('description', '')))

        for image in product['images']:
            cursor.execute('''
            INSERT OR IGNORE INTO Images (id, product_id, url, position)
            VALUES (?, ?, ?, ?)
            ''', (image['id'], product['id'], image['url'], image['position']))

        for variant in product['variants']:
            cursor.execute('''
            INSERT OR IGNORE INTO Variants (id, product_id, price, stock, weight, discount)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (variant['id'], product['id'], variant['price'], variant['stock'], variant['weight'], variant['discount']))

            for option in variant['options']:
                cursor.execute('''
                INSERT OR IGNORE INTO Options (id, variant_id, product_option_id, product_option_value_id, option_type, name, value)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (option['product_option_value_id'], variant['id'], option['product_option_id'], option['product_option_value_id'], option['option_type'], option['name'], option['value']))

    conn.commit()
    conn.close()

def insert_order_data_into_db(data):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    for order_data in data:
        order = order_data['order']

        cursor.execute('''
        INSERT OR IGNORE INTO Orders (
            id, number, status, payment_status, payment_method, shipping_method,
            shipping_status, created_at, completed_at, currency, subtotal, tax,
            shipping_tax, shipping, total, discount, shipping_discount,
            gift_cards_discount, fulfillment_status, shipping_required, additional_information
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            order['id'], order.get('number'), order['status'], order.get('payment_status'),
            order.get('payment_method_name'), order.get('shipping_method_name'),
            order.get('shipping_status'), order['created_at'], order['completed_at'],
            order['currency'], order['subtotal'], order['tax'], order['shipping_tax'],
            order['shipping'], order['total'], order['discount'], order['shipping_discount'],
            order['gift_cards_discount'], order['fulfillment_status'], order['shipping_required'],
            order['additional_information']
        ))

        customer = order['customer']
        cursor.execute('''
        INSERT OR IGNORE INTO Customers (id, order_id, email, phone, fullname)
        VALUES (?, ?, ?, ?, ?)
        ''', (customer['id'], order['id'], customer['email'], customer['phone'], customer['fullname']))

        shipping_address = order['shipping_address']
        cursor.execute('''
        INSERT OR IGNORE INTO ShippingAddresses (
            id, order_id, name, surname, address, city, postal, region, country,
            complement, latitude, longitude, municipality
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            shipping_address.get('id'), order['id'], shipping_address['name'], shipping_address['surname'],
            shipping_address['address'], shipping_address['city'], shipping_address['postal'],
            shipping_address['region'], shipping_address['country'], shipping_address.get('complement', ''),
            shipping_address.get('latitude'), shipping_address.get('longitude'), shipping_address.get('municipality', '')
        ))

        billing_address = order['billing_address']
        cursor.execute('''
        INSERT OR IGNORE INTO BillingAddresses (
            id, order_id, name, surname, taxid, address, city, postal, region, country,
            complement, municipality
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            billing_address.get('id'), order['id'], billing_address['name'], billing_address['surname'],
            billing_address['taxid'], billing_address['address'], billing_address['city'],
            billing_address['postal'], billing_address['region'], billing_address['country'],
            billing_address.get('complement', ''), billing_address.get('municipality', '')
        ))

        for product in order['products']:
            cursor.execute('''
            INSERT OR IGNORE INTO OrderProducts (
                id, order_id, variant_id, sku, name, qty, price, tax, discount, weight, image, type
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                product['id'], order['id'], product['variant_id'], product['sku'], product['name'],
                product['qty'], product['price'], product['tax'], product['discount'], product['weight'],
                product['image'], product['type']
            ))

    conn.commit()
    conn.close()
    
def query_products_with_images():
    conn = sqlite3.connect('data.db')
    query = '''
    SELECT
        Products.id,
        Products.page_title,
        Products.meta_description,
        Products.price,
        Products.status,
        Images.url,
        Images.position,
        Products.stock,
        Products.sku,
        Products.brand,
        Products.weight,
        Products.description,
        Categories.name AS categoria
    FROM
        Products
    LEFT JOIN
        Images ON Products.id = Images.product_id
    INNER JOIN
        Categories ON Products.id = Categories.product_id
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def query_customers():
    conn = sqlite3.connect('data.db')
    query = 'SELECT * FROM Customers'
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def query_data_from_db(table_name):
    conn = sqlite3.connect('data.db')
    query = f'SELECT * FROM {table_name}'
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# database/db_manager.py
import sqlite3
import pandas as pd

def query_orders_with_details():
    conn = sqlite3.connect('data.db')
    query = '''
    SELECT
        Orders.id AS order_id,
        Orders.status AS order_status,
        Orders.payment_method,
        Orders.shipping_method,
        Orders.created_at AS order_created_at,
        Orders.completed_at AS order_completed_at,
        Orders.currency,
        Orders.subtotal,
        Orders.tax AS order_tax,
        Orders.shipping_tax,
        Orders.shipping,
        Orders.discount AS order_discount,
        Orders.total,
        Orders.shipping_discount,
        Orders.gift_cards_discount,
        Orders.fulfillment_status,
        Orders.shipping_required,
        Orders.additional_information,
        BillingAddresses.name AS billing_name,
        BillingAddresses.surname AS billing_surname,
        BillingAddresses.taxid,
        BillingAddresses.address AS billing_address,
        BillingAddresses.city AS billing_city,
        BillingAddresses.postal AS billing_postal,
        BillingAddresses.country AS billing_country,
        BillingAddresses.region AS billing_region,
        OrderProducts.variant_id,
        OrderProducts.name AS product_name,
        OrderProducts.qty,
        OrderProducts.price,
        OrderProducts.tax AS product_tax,
        OrderProducts.discount AS product_discount,
        OrderProducts.weight,
        OrderProducts.image,
        OrderProducts.type,
        BillingAddresses.complement,
        BillingAddresses.municipality
    FROM
        Orders
    INNER JOIN
        BillingAddresses ON Orders.id = BillingAddresses.order_id
    INNER JOIN
        OrderProducts ON Orders.id = OrderProducts.order_id
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

