import streamlit as st
import random
import numpy as np
import pandas as pd
import datetime
import requests
from streamlit_lottie import st_lottie
def load_lotti(url):
    r = requests.get(url)
    if r.status_code !=200:
        return None
    return r.json()
def generate_dish(df):
 
    numbers =np.random.choice(df['title'],size=14)
    # steps = df[df["title"].isin(numbers)]['instructions']
    # ingredients = df[df["title"].isin(numbers)]['ingredients']
    # prices = df[df["title"].isin(numbers)]['estimated_price']
    # return numbers,steps,prices,ingredients
    result = df[df["title"].isin(numbers)]
    result = result.sort_values(by='title', key=lambda x: pd.Categorical(x, categories=numbers))
    return result
cooking_animation = load_lotti('https://assets1.lottiefiles.com/packages/lf20_p1bmwqtk.json')
pan = load_lotti('https://assets1.lottiefiles.com/packages/lf20_fefIZO.json')
with st.container():
    st_lottie(cooking_animation, height = 300, key="cooking")
    st.title("Stephen Food Recommendation of The week")
    uploaded_file = st.file_uploader("Upload your food recipe")
    if uploaded_file is not None:
        left, right = st.columns(2)

        upload = pd.read_csv(uploaded_file)
        file= upload.drop_duplicates(subset=['title'],keep='first')
    
        st.write("Click the button to generate a recipe for everyday dish.")

        d = st.date_input("What is the date of today?")
        date_range = pd.date_range(d, periods=14,freq="12H").tolist()
        date_range=[str(i).replace('00:00:00', 'Lunch')  if '00:00:00' in str(i) else str(i).replace('12:00:00', 'Dinner') for i in date_range]
        st.write('Your week is from: ' + str(date_range[0]) + ' to ' + str(date_range[-1]))

        if st.button("CLICK HERE"):
                st_lottie(pan, key="pan")
                ratings = [1,2,3,4,5,6,7,8,9,10,11,12,13,14]

                data = generate_dish(file)
                # rating = st.selectbox("Rate this recipe from 1 (not good) to 5 (very good):", [1, 2, 3, 4, 5],key='test')
                # ratings[i] = rating
                # st.write("Your Ratings: ",ratings[day])
                # data = {'Day': date_range, 'Food': result['title'],"Price":result['estimated_price'],'Steps': , "Ingredients":ingredients,'Rating': ratings}
                data = data[['title', 'estimated_price','instructions', 'ingredients', ]]
                data.columns = ['Food','Price', 'Steps', 'Ingredients', ]
                data = data.reset_index(drop=True)
                total = data['Price'].sum()
                data.insert(0, 'Day', date_range)
                data.insert(5, 'Rating', range(1, 15))
                st.write(pd.DataFrame(data))
                st.write("TOTAL SPENDING THIS WEEK: $", total)
                st.write("Data saved to Excel file:")
                st.download_button(label="Download data as Excel",data=data.to_excel(f"{date_range[-1]}"+".xlsx", index=False))
                st.write("Excel file saved to disk.")
