import streamlit as st
import sqlite3
import requests
import pandas as pd

# Función para crear la base de datos y las tablas
def create_db():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Tabla para productos
    cursor.execute('''
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
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Categories (
        id INTEGER PRIMARY KEY,
        product_id INTEGER,
        name TEXT,
        description TEXT,
        FOREIGN KEY (product_id) REFERENCES Products (id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Images (
        id INTEGER PRIMARY KEY,
        product_id INTEGER,
        url TEXT,
        position INTEGER,
        FOREIGN KEY (product_id) REFERENCES Products (id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Variants (
        id INTEGER PRIMARY KEY,
        product_id INTEGER,
        price REAL,
        stock INTEGER,
        weight REAL,
        discount REAL,
        FOREIGN KEY (product_id) REFERENCES Products (id)
    )
    ''')

    cursor.execute('''
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
    ''')

    # Tabla para órdenes
    cursor.execute('''
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
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Customers (
        id INTEGER PRIMARY KEY,
        order_id INTEGER,
        email TEXT,
        phone TEXT,
        fullname TEXT,
        FOREIGN KEY (order_id) REFERENCES Orders (id)
    )
    ''')

    cursor.execute('''
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
    ''')

    cursor.execute('''
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

    ''')

    cursor.execute('''
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
    ''')

    conn.commit()
    conn.close()

# Función para cargar datos desde la URL
def load_data_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error al cargar los datos desde la URL")
        return None

# Función para insertar datos de productos en la base de datos
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

# Función para insertar datos de órdenes en la base de datos
def insert_order_data_into_db(data):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    for order_data in data:
        order = order_data['order']

        # Insertar en la tabla Orders
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

        # Insertar en la tabla Customers
        customer = order['customer']
        cursor.execute('''
        INSERT OR IGNORE INTO Customers (id, order_id, email, phone, fullname)
        VALUES (?, ?, ?, ?, ?)
        ''', (customer['id'], order['id'], customer['email'], customer['phone'], customer['fullname']))

        # Insertar en la tabla ShippingAddresses
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

        
        # Insertar en la tabla BillingAddresses
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


        # Insertar en la tabla OrderProducts
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

# Función para consultar datos de la base de datos
def query_data_from_db(table_name):
    conn = sqlite3.connect('data.db')
    query = f'SELECT * FROM {table_name}'
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Interfaz de Streamlit
def main():
    st.title("Aplicación de Gestión de Productos y Órdenes")

    if st.button("Crear Base de Datos"):
        create_db()
        st.success("Base de datos creada exitosamente")

    product_url = "https://api.jumpseller.com/v1/products/status/available.json?login=9d260f55a91a210392015ba6dedf8fe2&authtoken=2bc4b1f726025f372b4f7d1d42e1e86c"
    if st.button("Cargar Datos de Productos desde URL"):
        product_data = load_data_from_url(product_url)
        if product_data:
            insert_product_data_into_db(product_data)
            st.success("Datos de productos cargados exitosamente")

    order_url = "https://api.jumpseller.com/v1/orders/status/paid.json?login=9d260f55a91a210392015ba6dedf8fe2&authtoken=2bc4b1f726025f372b4f7d1d42e1e86c"
    if st.button("Cargar Datos de Órdenes desde URL"):
        order_data = load_data_from_url(order_url)
        if order_data:
            insert_order_data_into_db(order_data)
            st.success("Datos de órdenes cargados exitosamente")

    table_name = st.selectbox("Seleccionar tabla para consultar", [
        "Products", "Categories", "Images", "Variants", "Options",
        "Orders", "Customers", "ShippingAddresses", "BillingAddresses", "OrderProducts"
    ])
    if st.button("Consultar Datos"):
        df = query_data_from_db(table_name)
        st.write(df)

if __name__ == "__main__":
    main()
