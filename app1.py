import streamlit as st
import numpy as np
import string
import pickle
st.set_option('deprecation.showfileUploaderEncoding',False) 
model = pickle.load(open('model_pkl.pkl','rb'))


def main():
  st.sidebar.header("Diabetes Risk Prediction for patient with the datset")
  st.sidebar.text("This a Web app that tells you if you are a diabetes whether you are at risk for Diabetes or not.")
  st.sidebar.header("Just fill in the information below")
  st.sidebar.text("The SVM Classifier was used.")


  id = st.slider("id", "Type Here",1,70000)
  cholesterol = st.slider("Cholesterol", "Type Here",0,1)
  gluc = st.slider("gluc", "Type Here"0,1)
  smoke = st.slider("smoke", "Type Here",0,1)
  alco = st.slider("alco", "Type Here",0,1)
  active = st.slider("active", "Type Here",0,1)
  pressure = st.slider("pressure", "Type Here",40,180)
  age1 = st.slider("age1", "Type Here",39,64)
  height= st.slider("height", "Type Here",150,183)
  weight = st.slider("weight", "Type Here",40,80)
  gender = st.slider("gender", "Type Here",0,1)

  inputs = [[id,cholesterol, gluc,smoke, alco, active, pressure, age1,height,weight]]

  if st.button('Predict'):
    result = model.predict(inputs)
    updated_res = result.flatten()
    if updated_res == 0:
       st.write("Not very Proabable you will get Diabetes soon but still take good care of yourself regardless")
    else:
       st.write("It is Probable you might get a Diabetes soon therfore you should take better care of yourself")
   


if __name__ =='__main__':
  main()