# app.py
import streamlit as st
from database.db_manager import create_db, insert_product_data_into_db, insert_order_data_into_db, query_data_from_db
from data_loader.data_loader import load_data_from_url
from visualization.visualizer import plot_product_distribution, plot_order_status, plot_stock_levels, plot_sales_over_time

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

        if table_name == "Products":
            plot_product_distribution(df)
            plot_stock_levels(df)
        elif table_name == "Orders":
            plot_order_status(df)
            plot_sales_over_time(df)

if __name__ == "__main__":
    main()
