import numpy as np
import pandas as pd
import ast
#from text_processing import flavour_wheel_values

df = pd.read_parquet("flavour_wheel.parquet")

def make_recommendation(user_input_vector):

    vectors = df['flavour_wheel_values'].values
    vectors = np.vstack(vectors)

    distances = np.linalg.norm(vectors - user_input_vector, axis=1)

    nearest_index = np.argmin(distances)
    nearest_vector = vectors[nearest_index]
    nearest_distance = distances[nearest_index]

    recommended_bottle_title = df.loc[nearest_index, 'review_title']

    return recommended_bottle_title

make_recommendation([0.8]*12)