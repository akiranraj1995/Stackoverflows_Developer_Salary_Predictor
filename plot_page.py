import  streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
    df = pd.read_csv('survey_results_public.csv')
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

