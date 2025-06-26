# menu.py
import streamlit as st
from app import main as app_main
from productos import show_product_gallery
from customers import show_customers
from orders import show_orders

def show_menu():
    st.sidebar.title("Menú")

    # Opciones del menú
    menu_options = {
        "Inicio": app_main,
        "Productos": show_product_gallery,
        "Clientes": show_customers,
        "Ordenes": show_orders 
    }

    # Mostrar opciones del menú en el sidebar
    selection = st.sidebar.radio("Ir a", list(menu_options.keys()))

    # Llamar a la función correspondiente a la opción seleccionada
    menu_options[selection]()

if __name__ == "__main__":
    show_menu()
