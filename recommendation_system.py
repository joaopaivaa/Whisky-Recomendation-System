import numpy as np
import pandas as pd

def filter_similar_to_high_level_notes(df_tasting_notes, tasting_notes, user_input_vector, similarity_level):

    print('')

    print(user_input_vector)

    higher_level_note_position = user_input_vector.index(sorted(user_input_vector)[-1])
    higher_level_note_name = tasting_notes[higher_level_note_position]
    higher_level_note_value = user_input_vector[higher_level_note_position]

    print(higher_level_note_position)

    selected_bottles_cond1 = df_tasting_notes[(df_tasting_notes['tasting_notes_group'] == higher_level_note_name) &
                                              (df_tasting_notes['perc_tasting_notes_group'] < higher_level_note_value*(1+similarity_level)) &
                                              (df_tasting_notes['perc_tasting_notes_group'] > higher_level_note_value*(1-similarity_level))]['review_title'].values

    second_higher_level_note_position = user_input_vector.index(sorted(user_input_vector)[-2])
    second_higher_level_note_name = tasting_notes[second_higher_level_note_position]
    second_higher_level_note_value = user_input_vector[second_higher_level_note_position]

    print(second_higher_level_note_position)

    selected_bottles_cond2 = df_tasting_notes[(df_tasting_notes['tasting_notes_group'] == second_higher_level_note_name) &
                                              (df_tasting_notes['perc_tasting_notes_group'] < second_higher_level_note_value*(1+similarity_level)) &
                                              (df_tasting_notes['perc_tasting_notes_group'] > second_higher_level_note_value*(1-similarity_level))]['review_title'].values

    selected_bottles = list(set(selected_bottles_cond1) & set(selected_bottles_cond2))

    if len(selected_bottles) > 0:
        df_tasting_notes_filtered = df_tasting_notes[df_tasting_notes['review_title'].isin(selected_bottles)].reset_index(drop=True)
        return df_tasting_notes_filtered
    
    # elif len(selected_bottles_cond1) > 0:
    #     df_tasting_notes_filtered = df_tasting_notes[df_tasting_notes['review_title'].isin(selected_bottles_cond1)].reset_index(drop=True)
    #     return df_tasting_notes_filtered
    
    # elif len(selected_bottles_cond2) > 0:
    #     df_tasting_notes_filtered = df_tasting_notes[df_tasting_notes['review_title'].isin(selected_bottles_cond2)].reset_index(drop=True)
    #     return df_tasting_notes_filtered
    
    else:
        return None

def make_recommendation(user_input_vector):

    df_tasting_notes = pd.read_csv("flavour_wheel_long.csv")

    tasting_notes = sorted(df_tasting_notes['tasting_notes_group'].unique())

    similarity_level = 0.05
    df_tasting_notes_filtered = None

    while df_tasting_notes_filtered is None:
        df_tasting_notes_filtered = filter_similar_to_high_level_notes(df_tasting_notes, tasting_notes, user_input_vector, similarity_level)
        similarity_level += 0.05

    print(similarity_level)

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