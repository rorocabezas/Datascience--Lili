# productos.py
import streamlit as st
import pandas as pd
from database.db_manager import query_products_with_images

def show_product_gallery():
    st.title("Catálogo de Productos")

    # Obtener datos de productos con imágenes y categorías
    products_df = query_products_with_images()

    # Verificar si se obtuvieron datos
    if products_df is not None and not products_df.empty:
        # Agrupar por producto para manejar múltiples imágenes y categorías
        grouped_products = products_df.groupby('id')

        for product_id, group in grouped_products:
            group = group.sort_values(by='position')  # Ordenar imágenes por posición
            first_row = group.iloc[0]  # Tomar la primera fila para los detalles del producto

            with st.container():
                col1, col2 = st.columns([1, 3])

                with col1:
                    # Mostrar la primera imagen del producto
                    if pd.notna(first_row['url']):
                        st.image(first_row['url'], width=150)
                    else:
                        st.image("https://via.placeholder.com/150", width=150)  # Imagen de marcador de posición

                with col2:
                    st.subheader(first_row['page_title'])
                    st.write(f"**Precio:** {first_row['price']}")
                    st.write(f"**Marca:** {first_row['brand']}")
                    st.write(f"**Categoría:** {first_row['categoria']}")

                    # Mostrar la descripción como HTML
                    st.markdown(f"**Descripción:**", unsafe_allow_html=True)
                    st.markdown(first_row['description'], unsafe_allow_html=True)

                    st.write(f"**Stock:** {first_row['stock']}")
                    st.write(f"**SKU:** {first_row['sku']}")
                    st.write("---")
    else:
        st.write("No hay productos disponibles para mostrar.")

if __name__ == "__main__":
    show_product_gallery()
