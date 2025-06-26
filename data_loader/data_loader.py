# data_loader/data_loader.py
import requests
import streamlit as st

def load_data_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error al cargar los datos desde la URL")
        return None
