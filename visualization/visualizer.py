# visualization/visualizer.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def plot_product_distribution(df):
    st.write("### Distribución de Productos por Precio")
    fig, ax = plt.subplots()
    sns.histplot(df['price'], bins=30, kde=True, ax=ax)
    st.pyplot(fig)

def plot_order_status(df):
    st.write("### Estado de las Órdenes")
    fig, ax = plt.subplots()
    df['status'].value_counts().plot(kind='bar', ax=ax)
    st.pyplot(fig)

def plot_stock_levels(df):
    st.write("### Niveles de Stock de Productos")
    fig, ax = plt.subplots()
    sns.histplot(df['stock'], bins=30, kde=True, ax=ax)
    st.pyplot(fig)

def plot_sales_over_time(df):
    st.write("### Ventas a lo Largo del Tiempo")
    df['created_at'] = pd.to_datetime(df['created_at'])
    df.set_index('created_at', inplace=True)
    monthly_sales = df.resample('M').size()
    fig, ax = plt.subplots()
    monthly_sales.plot(ax=ax)
    st.pyplot(fig)
