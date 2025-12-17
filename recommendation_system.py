import numpy as np
import pandas as pd

def make_recommendation(user_input_vector):

    df_tasting_notes = pd.read_csv("flavour_wheel_long.csv")

    df_vectors = (
        df_tasting_notes
        .groupby('review_title')['perc_tasting_notes_group']
        .apply(list)
        .reset_index(name='flavour_wheel_values')
    )
    
    vectors = df_vectors['flavour_wheel_values'].values
    vectors = np.vstack(vectors)

    distances = np.linalg.norm(vectors - user_input_vector, axis=1)

    nearest_index = np.argmin(distances)
    nearest_vector = vectors[nearest_index]
    nearest_distance = distances[nearest_index]

    recommended_bottle_title = df_vectors.loc[nearest_index, 'review_title']

    return recommended_bottle_title