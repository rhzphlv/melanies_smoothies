# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
  """
  Choose the fruit you want in yout smoothie
  """
)

name_on_order = st.text_input("Name on the smoothie")
st.write("The name on your smoothie will be :", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('SEARCH_ON'),col('FRUIT_NAME'))
pd_df = my_dataframe.to_pandas()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.text(pd_df)
ingredients_list = st.multiselect(
    "Choose up to 5 Fruit",
    my_dataframe,
    max_selections = 5
)
if ingredients_list:
    #st.write("You selected:", ingredients_list)
    #st.text(ingredients_list)

    ingredients_string = ''
    for fruit in ingredients_list:
        ingredients_string += fruit + ' '
    #st.text(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""
    submit_Button = st.button("Submit Order")
    if submit_Button:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered '+name_on_order, icon="✅")

if ingredients_list:
  ingredients_string = ''
  for fruit_chosen in ingredients_list:
    ingredients_string += fruit_chosen + ' '
    search_on=pd_df[pd_df['FRUIT_NAME'] == fruit_chosen]
    st.text(search_on)
    search_on=search_on["SEARCH_ON"]
    st.text(search_on)
    search_on=search_on.reset_index().loc[0]
    st.text(search_on)
    #st.text(search_on)
    smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+str(search_on))
    #st.text(smoothiefroot_response.json())
    st.subheader(fruit_chosen + " Nutrition Information")
    sf_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width = True)
