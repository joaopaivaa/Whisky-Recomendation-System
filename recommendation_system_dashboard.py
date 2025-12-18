import streamlit as st
import pandas as pd
import plotly.express as px
from recommendation_system import make_recommendation
import requests
from PIL import Image
from io import BytesIO

def load_whiskynotes_image(url):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.whiskynotes.be/"
    }
    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()
    loaded_image = Image.open(BytesIO(r.content))
    return loaded_image

df_flavour_wheel = pd.read_csv('flavour_wheel_long.csv')

st.set_page_config(layout='wide')

st.title('DramMatch - Your whisky recommender')

with st.sidebar:

    st.header('Adjust the sliders to reflect your flavour preferences')

    if 'points_remaining' not in st.session_state:
        st.session_state.points_remaining = 100
    
    points_text = st.text(f'Preference points remaining: {st.session_state.points_remaining}/100')

    cereal_level = st.slider('Cereal', min_value=0, max_value=100, value=0)

    coastal_level = st.slider('Coastal', min_value=0, max_value=100, value=0)

    feinty_level = st.slider('Feinty', min_value=0, max_value=100, value=0)

    floral_level = st.slider('Floral', min_value=0, max_value=100, value=0)

    fruity_level = st.slider('Fruity', min_value=0, max_value=100, value=0)

    nutty_level = st.slider('Nutty', min_value=0, max_value=100, value=0)

    peaty_level = st.slider('Peaty', min_value=0, max_value=100, value=0)

    roasted_level = st.slider('Roasted', min_value=0, max_value=100, value=0)

    spicy_level = st.slider('Spicy', min_value=0, max_value=100, value=0)

    sulphury_level = st.slider('Sulphury', min_value=0, max_value=100, value=0)

    sweet_level = st.slider('Sweet', min_value=0, max_value=100, value=0)

    woody_level = st.slider('Woody', min_value=0, max_value=100, value=0)

user_input_vector = [
    cereal_level, coastal_level, feinty_level, floral_level, fruity_level, nutty_level,
    peaty_level, roasted_level, spicy_level, sulphury_level, sweet_level, woody_level
]

sum_user_input_vector = sum(user_input_vector)
points_remaining = 100 - sum_user_input_vector

st.session_state.points_remaining = points_remaining

points_text.text(f'Preference points remaining: {points_remaining}/100')

if st.session_state.points_remaining > 0:
    st.space('small')
    st.info('Please allocate all your preference points using the sliders in the sidebar to get a recommendation.')

elif st.session_state.points_remaining < 0:
    st.space('small')
    st.warning('You have exceeded the 100 preference points limit. Please adjust your sliders accordingly.')

else:

    user_input_vector = [x / 100 for x in user_input_vector]

    recommended_bottle = make_recommendation(user_input_vector)

    df_recommended_bottle = df_flavour_wheel[df_flavour_wheel['review_title'] == recommended_bottle]

    polar_fig = px.bar_polar(df_recommended_bottle, r="perc_tasting_notes_group", theta="tasting_notes_group",
                             template="plotly_white",
                             color='perc_tasting_notes_group',
                             color_continuous_scale= px.colors.sequential.Oranges,
                             title=None)
    
    polar_fig.update_layout(
        coloraxis_showscale=False,
        polar=dict(
            radialaxis=dict(
                tickvals=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
                tickfont=dict(size=12),
                showline=True,
                linewidth=2
            ),
            angularaxis=dict(
                tickfont=dict(
                    size=18
                )
            )
        )
    )

    st.space('small')

    st.subheader(recommended_bottle)

    col_chart, col_image, col_score = st.columns([3, 1, 1], vertical_alignment='center')

    with col_chart:
        
        st.plotly_chart(polar_fig, width='stretch', config={'displayModeBar': False})

    with col_score:

        bottle_grade = df_recommended_bottle['review_score'].values[0]

        st.metric(label='Score on Whisky Notes', value=f"{bottle_grade}/100")
        
    with col_image:
    
        bottle_image = df_recommended_bottle['review_image'].values[0]
        loaded_image = load_whiskynotes_image(bottle_image)

        st.space('small')
        st.image(loaded_image, width=100)
