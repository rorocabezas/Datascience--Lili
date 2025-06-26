# orders.py
import streamlit as st
from database.db_manager import query_orders_with_details

def show_orders():
    st.title("Lista de Órdenes")

    # Obtener datos de las órdenes con detalles
    orders_df = query_orders_with_details()

    # Verificar si se obtuvieron datos
    if orders_df is not None and not orders_df.empty:
        # Mostrar las órdenes en un formato de tabla
        st.dataframe(orders_df)
    else:
        st.write("No hay órdenes disponibles para mostrar.")

if __name__ == "__main__":
    show_orders()
