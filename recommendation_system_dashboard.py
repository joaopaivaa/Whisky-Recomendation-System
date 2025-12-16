import streamlit as st
import pandas as pd
import plotly.express as px
from recommendation_system import make_recommendation

df_flavour_wheel = pd.read_csv('flavour_wheel_long.csv')

st.set_page_config(layout='wide')

st.title('DramMatch - Your whisky recommender')

with st.sidebar:

    st.header('Adjust the sliders to reflect your flavour preferences')

    if 'points_remaining' not in st.session_state:
        st.session_state.points_remaining = 100
    
    points_text = st.text(f'Preference points remaining: {st.session_state.points_remaining}/100')

    fruity_level = st.slider('Fruity', min_value=0, max_value=100, value=0)

    floral_level = st.slider('Floral', min_value=0, max_value=100, value=0)

    spicy_level = st.slider('Spicy', min_value=0, max_value=100, value=0)

    woody_level = st.slider('Woody', min_value=0, max_value=100, value=0)

    cereal_level = st.slider('Cereal', min_value=0, max_value=100, value=0)

    peaty_level = st.slider('Peaty', min_value=0, max_value=100, value=0)

    feinty_level = st.slider('Feinty', min_value=0, max_value=100, value=0)

    sulphury_level = st.slider('Sulphury', min_value=0, max_value=100, value=0)

    sweet_level = st.slider('Sweet', min_value=0, max_value=100, value=0)

    nutty_level = st.slider('Nutty', min_value=0, max_value=100, value=0)

    coastal_level = st.slider('Coastal', min_value=0, max_value=100, value=0)

    roasted_level = st.slider('Roasted', min_value=0, max_value=100, value=0)

user_input_vector = [
    fruity_level, floral_level, spicy_level, woody_level, cereal_level, peaty_level,
    feinty_level, sulphury_level, sweet_level, nutty_level, coastal_level, roasted_level
]

sum_user_input_vector = sum(user_input_vector)
points_remaining = 100 - sum_user_input_vector

st.session_state.points_remaining = points_remaining

if st.session_state.points_remaining == 100:
    st.space('small')
    st.info('Please allocate your preference points using the sliders in the sidebar to get a recommendation.')

elif st.session_state.points_remaining < 0:
    st.space('small')
    st.warning('You have exceeded the 100 preference points limit. Please adjust your sliders accordingly.')

else:

    points_text.text(f'Preference points remaining: {points_remaining}/100')

    user_input_vector = [x / 100 for x in user_input_vector]

    recommended_bottle = make_recommendation(user_input_vector)

    df_recommended_bottle = df_flavour_wheel[df_flavour_wheel['review_title'] == recommended_bottle]

    polar_fig = px.line_polar(df_recommended_bottle, r="perc_tasting_notes_group", theta="tasting_notes_group",
                            line_close=True,
                            template="plotly_white",
                            title=None)

    st.space('small')

    st.subheader(recommended_bottle)

    col_chart, col_fake = st.columns([2, 3])

    with col_chart:
        
        st.plotly_chart(polar_fig, width='stretch', config={'displayModeBar': False})