import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Configuración inicial
st.set_page_config(page_title="Smoothie Maker", page_icon=":cup_with_straw:")
st.title(f"Custom Smoothie App :cup_with_straw:")

st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

#session = get_active_session()

# Cargamos los datos de las frutas
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Multiselect de ingredientes
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    # Creamos el string de ingredientes
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
    
    # Limpiamos espacios sobrantes al final
    ingredients_string = ingredients_string.strip()

    # CONSTRUCCIÓN DE LA QUERY (Corregida y simplificada)
    # Importante: El orden de las columnas en el INSERT debe coincidir con tu tabla
    my_insert_stmt = f""" 
        insert into smoothies.public.orders(ingredients, name_on_order)
        values ('{ingredients_string}', '{name_on_order}')
    """

    # Quitamos el st.stop() para que el botón pueda ejecutarse
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
