import requests
import pandas
import streamlit as st
from snowflake.snowpark.functions import col
 
# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in the custom smoothie
    """
  
) 
import streamlit as st
 
name_on_order = st.text_input('Name on Smoothie:')
st.write('The Name on your smoothie will be:', name_on_order)
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()
pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()
 
 
Ingredients_list = st.multiselect(
    'choose up to 5 ingredients:',
    my_dataframe,
    
    
)
if Ingredients_list:
    # st.write(Ingredients_list)
    # st.text(Ingredients_list)
    Ingredients_string = ''
 
    for fruit_chosen in Ingredients_list:
        Ingredients_string += fruit_chosen + ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        
        st.subheader = (fruit_chosen + 'Nutrition Information')
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
 
    #st.write(Ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + Ingredients_string + """','""" +name_on_order+ """')"""
 
    st.write(my_insert_stmt)
    time_to_insert= st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()# if Ingredients_string:
        st.success('Your Smoothie is ordered!', icon="✅")
