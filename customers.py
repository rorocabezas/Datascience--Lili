# customers.py
import streamlit as st
import pandas as pd
from database.db_manager import query_customers

def show_customers():
    st.title("Lista de Clientes")

    # Obtener datos de la tabla Customers
    customers_df = query_customers()

    # Verificar si se obtuvieron datos
    if customers_df is not None and not customers_df.empty:
        st.dataframe(customers_df)
    else:
        st.write("No hay clientes disponibles para mostrar.")

if __name__ == "__main__":
    show_customers()
