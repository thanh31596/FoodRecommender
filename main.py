import streamlit as st
import random
import numpy as np
import pandas as pd
import datetime
import requests
from streamlit_lottie import st_lottie
if 'data' not in st.session_state:
    st.session_state.data = []
if 'date' not in st.session_state:
    st.session_state.date= []
def generate_tabs(a,i):
    """generate number of tabs

    Args:
        i (int): index number of the date range
    """
    with a:
        col1, col2,col3 = st.columns(3)
        with col1:
            st.image(data['smallImageUrls'][i], caption = data['recipeName'][i], width= 200)
        col2.metric("Rating",data['rating'][i])
        col2.metric("Time Making (seconds)", data['totalTimeInSeconds'][i])
        with col3:
            st.bar_chart(graph.loc[i],width=200,height=260)
        with st.expander("Ingredients"):
            st.write(data['ingredients'][i])

        # ratings = st.slider("YOUR RATING", min_value=1, max_value=5, step=1,key=i)

def load_lotti(url):
    r = requests.get(url)
    if r.status_code !=200:
        return None
    return r.json()
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')
def generate_dish(df):
    numbers =set(np.random.choice(df['recipeName'],size=14))
    verbose = False
    if len(numbers) < 14:
        verbose = True
        while verbose:
            numbers =set(np.random.choice(df['recipeName'],size=14))
            if len(numbers)==14:
                verbose=False
    result = df[df["recipeName"].isin(numbers)]
    result = result.sort_values(by='recipeName', key=lambda x: pd.Categorical(x, categories=numbers))
    return result
cooking_animation = load_lotti('https://assets1.lottiefiles.com/packages/lf20_p1bmwqtk.json')
pan = load_lotti('https://assets1.lottiefiles.com/packages/lf20_fefIZO.json')
with st.container():
    st_lottie(cooking_animation, height = 300, key="cooking")
    st.title("Stephen Food Recommendation of The week")
    today = datetime.date.today()
    d1 = today.strftime("%d/%m/%YYYY")
    st.session_state.date.append(d1)
    if len(st.session_state.data)==0: 
        uploaded_file = st.file_uploader("Upload your food recipe")
        if uploaded_file is not None:
            left, right = st.columns(2)

            upload = pd.read_csv(uploaded_file)
            file= upload.drop_duplicates(subset=['recipeName'],keep='first')
        
            st.write("Click the button to generate a recipe for everyday dish.")

            d = st.date_input("What is the date of today?")
            date_range = pd.date_range(d, periods=14,freq="12H").tolist()
            date_range=[str(i).replace('00:00:00', 'Lunch')  if '00:00:00' in str(i) else str(i).replace('12:00:00', 'Dinner') for i in date_range]
            st.write('Your week is from: ' + str(date_range[0]) + ' to ' + str(date_range[-1]))
            my_rate= [1,2,3,4,5,6,7,8,9,10,11,12,13,14]
            if st.button("CLICK HERE"):
                    st_lottie(pan, key="pan", height = 100)

                    data = generate_dish(file)
                    data = data.reset_index(drop=True)
                    graph = data[['piquant','meaty','bitter','sweet','sour','salty']]
                    total = data['Threshold_purchase'].sum()
                    data.insert(0, 'Day', date_range)
                    data.insert(5, 'Rating', range(1, 15))
                    date_box=st.tabs(date_range)
                    st.session_state.data.append(data)

                    for ind,val in enumerate(date_box):
                    
                        generate_tabs(val,ind)

                    #st.write(pd.DataFrame(data))

                    # st.write("TOTAL SPENDING THIS WEEK: $", total)
                    st.write("Data saved to Excel file:")
                    csv = convert_df(data)
                    if st.download_button(label="Download data as Excel",data=csv,file_name='large_df.csv',mime='text/csv',):
                        st.write("CSV file saved to disk.")
    else: 
        st_lottie(pan, key="pan", height = 180)

        data = st.session_state.data[0]
        data =pd.DataFrame(data)
        graph = data[['piquant','meaty','bitter','sweet','sour','salty']]

        #data.insert(5, 'Rating', range(1, 15))
        date_box=st.tabs(list(data['Day'].values))

        for ind,val in enumerate(date_box):
        
            r =generate_tabs(val,ind)

        #st.write(pd.DataFrame(data))

        st.write("TOTAL SPENDING THIS WEEK: $", )
        st.write("Data saved to Excel file:")
        csv = convert_df(data)
        if st.download_button(label="Download data as Excel",data=csv,file_name='large_df.csv',mime='text/csv',):
            st.write("CSV file saved to disk.")
