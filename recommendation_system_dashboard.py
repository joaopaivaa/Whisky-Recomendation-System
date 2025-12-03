import streamlit as st
import pandas as pd
import plotly.express as px
from recommendation_system import make_recommendation

df_flavour_wheel = pd.read_csv('flavour_wheel_long.csv')

st.set_page_config(layout='wide')

with st.sidebar:

    fruity_level = st.slider('Fruity', min_value=0, max_value=100, value=9)

    floral_level = st.slider('Floral', min_value=0, max_value=100, value=9)

    spicy_level = st.slider('Spicy', min_value=0, max_value=100, value=9)

    woody_level = st.slider('Woody', min_value=0, max_value=100, value=9)

    cereal_level = st.slider('Cereal', min_value=0, max_value=100, value=8)

    peaty_level = st.slider('Peaty', min_value=0, max_value=100, value=8)

    feinty_level = st.slider('Feinty', min_value=0, max_value=100, value=8)

    sulphury_level = st.slider('Sulphury', min_value=0, max_value=100, value=8)

    sweet_level = st.slider('Sweet', min_value=0, max_value=100, value=8)

    nutty_level = st.slider('Nutty', min_value=0, max_value=100, value=8)

    coastal_level = st.slider('Coastal', min_value=0, max_value=100, value=8)

    roasted_level = st.slider('Roasted', min_value=0, max_value=100, value=8)

user_input_vector = [
    fruity_level, floral_level, spicy_level, woody_level, cereal_level, peaty_level,
    feinty_level, sulphury_level, sweet_level, nutty_level, coastal_level, roasted_level
]

user_input_vector = [x / 100 for x in user_input_vector]

recommended_bottle = make_recommendation(user_input_vector)

df_recommended_bottle = df_flavour_wheel[df_flavour_wheel['review_title'] == recommended_bottle]

print(df_recommended_bottle)

polar_fig = px.line_polar(df_recommended_bottle, r="perc_tasting_notes_group", theta="tasting_notes_group",
                          line_close=True,
                          template="plotly_white",
                          title=recommended_bottle)

st.plotly_chart(polar_fig, width='stretch', config={'displayModeBar': False})