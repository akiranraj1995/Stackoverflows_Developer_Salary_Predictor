import streamlit as st
import numpy as np
import pickle


from PIL import Image
image = Image.open('large.jpg')


#LOAD MODEL FROM PICKLE
def load_model():
    with open('/home/expert/MY_END_TO_END_PROJECTS/SoftwareDeveloperSurvey-Salary-Predictor-app/saved_steps.pkl', "rb") as file:
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


