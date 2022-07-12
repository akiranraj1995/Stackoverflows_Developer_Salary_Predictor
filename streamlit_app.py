import  streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pickle
from PIL import Image

image = Image.open('large.png')

from predict_page import show_predict_page
from plot_page import show_plot_page


# SIDEBAR
page = st.sidebar.selectbox("Other Details you can Check ",("Prediction", "Plot"))

if page=="Prediction":
    show_predict_page()
else:
    show_plot_page()

#LOAD MODEL FROM PICKLE
def load_model():
    with open('saved_steps.pkl', "rb") as file:
        data = pickle.load(file)
    return data
data=load_model()


def show_predict_page():
    regressor = data["model"]
    LE_country = data["le_country"]
    LE_education = data["le_education"]


    # WEB APP
    st.header("SALARY PREDICTOR FOR SOFTWARE DEVELOPER")
    st.image(image, caption='SALARY PREDICTOR FOR SOFTWARE DEVELOPER')
    
    st.subheader("ENTER THE DETAILS!")

    country = ("United States",
               "India",
               "United Kingdom",
               "Germany",
               "Canada",
               "Brazil",
               "France",
               "Spain",
               "Australia",
               "Netherlands",
               "Poland",
               "Italy",
               "Russian Federation",
               "Sweden")

    education = ('Bachelor’s degree',
                 'Master’s degree',
                 'Less than a Bachelors',
                 'Post grad')

    # EDUCATION SELECTBOX
    education = st.selectbox("Enter your Education Level", education)
    # EDUCATION SELECTBOX
    country = st.selectbox("Enter your Country Name", country)
    # EXPERIENCE SLIDER
    experience = st.slider('Select the Years of Experience', 0, 50, 1)

    # BUTTON CLICK
    ok = st.button("Calculate the Salary")
    if ok:
        X = np.array([[education, experience, country]])
        X[:, 0] = LE_education.transform(X[:, 0])
        X[:, 2] = LE_country.transform(X[:, 2])
        X = X.astype(float)

        salary = regressor.predict(X)
        st.success(f"The Estimated Salary is ${salary[0]:.2f}")

def short_categories(categories,cutoff):
    categorical_map={}
    for i in range(len(categories)):
        if categories.values[i]>=cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map

def cleaned_experience(x):
    if x=="More than 50 years":
        return 50
    elif x=="Less than 1 year":
        return 0.5
    return float(x)

def cleaned_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'

#To improve performance avoid loading the below data again and again once executed caches it
@st.cache
def load_data():
    #Applying all tranformations
    df = pd.read_csv('/home/expert/MY_END_TO_END_PROJECTS/SoftwareDeveloperSurvey-Salary-Predictor-app/survey_results_public.csv')
    df = df[['EdLevel', 'Employment', 'YearsCodePro', 'ConvertedComp', 'Country']]

    df = df.rename({'ConvertedComp': 'Salary'}, axis=1)
    df[df['Salary'].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == 'Employed full-time']
    df = df.drop("Employment", axis=1)

    country_map = short_categories(df.Country.value_counts(), 400)
    df['Country'] = df['Country'].map(country_map)


    df = df[df["Salary"] <= 250000]
    df = df[df["Salary"] >= 10000]
    df = df[df['Country'] != 'Other']

    df['YearsCodePro'] = df['YearsCodePro'].apply(cleaned_experience)
    df['EdLevel'] = df['EdLevel'].apply(cleaned_education)

    return df
df = load_data()


def show_plot_page():
    st.title(" SOFTWARE DEVELOPERS SURVEY VISUALIZATION PLOT")
    st.write("""
             **Developer Survey 2020**
             """
    )
    data=df["Country"].value_counts()

    fig1,ax1=plt.subplots()
    ax1.pie(data,labels=data.index, autopct="%1.1f%%",shadow=True,startangle=90)
    #pie is drawn as circle
    ax1.axis("equal")

    st.write("""#### Number Of Data from diffrent Countries""")
    st.pyplot(fig1)



