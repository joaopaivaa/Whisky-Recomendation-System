import pandas as pd
import re
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r"\d+", '', text)
    text = ' '.join([word for word in text.split() if ((word not in stop_words) and (len(word) >= 3))])
    return text

df = pd.read_csv('databases/raw/whisky_notes.csv', sep=';')
df = df.drop_duplicates().reset_index(drop=True)

df['review_score'] = df['review_score'].str.replace('+', '').str.replace('.', '')
df = df[~((df['review_score'].isna()) | (df['review_score'] == ''))]
df['review_score'] = df['review_score'].astype(int, errors='ignore')
df = df[(df['review_score'] >= 80) & (df['review_score'] <= 100)]

df['review_title'] = df['review_title'].str.replace('\n', ' ').str.strip()

df = df[['review_title', 'review_full_text', 'review_score', 'review_image']]

df['review_full_text'] = df['review_full_text'].str.lower().str.replace('-', ' ')

df.dropna(inplace=True)
df.reset_index(drop=True, inplace=True)

df.loc[:, 'review_full_text'] = df['review_full_text'].str.replace('nose:|mouth:|finish:', '', regex=True)

parser_porter_stemmer = PorterStemmer()

def stemmer(text):

    y = []

    text_words = text.split()

    for word in text_words:
        y.append(parser_porter_stemmer.stem(word))
    
    stemmed_text = ' '.join(y)

    return stemmed_text

df.loc[:, 'review_full_text_processed'] = [preprocess_text(text) for text in df['review_full_text']]

df.loc[:, 'review_full_text_processed'] = df['review_full_text_processed'].apply(stemmer)

normalize_map = {
    "add": "add",
    "almond": "almond",
    "alcohol": "alcohol",
    "appear": "appear",
    "appl": "apple",
    "apricot": "apricot",
    "ash": "ash",
    "banana": "banana",
    "berri": "berry",
    "best": "best",
    "better": "better",
    "blackberri": "blackberry",
    "bring": "bring",
    "butter": "butter",
    "butteri": "butter",
    "candi": "candy",
    "caramel": "caramel",
    "cask": "cask",
    'chalki': 'chalk',
    "char": "char",
    "chocol": "chocolate",
    "cigar": "cigar",
    "cinnamon": "cinnamon",
    "citru": "citrus",
    "citrusi": "citrus",
    'cherri': 'cherry',
    "clove": "clove",
    "coffe": "coffee",
    "coffee": "coffee",
    "come": "come",
    "cream": "cream",
    "creami": "cream",
    "dark": "dark",
    "darker": "dark",
    "distilleri": "distillery",
    "dri": "dry",
    "drier": "dry",
    "dry": "dry",
    'dusti': 'dust',
    'earthi': 'earthy',
    "eucalyptu": "eucalyptus",
    "fade": "fade",
    "find": "find",
    "finish": "finish",
    "flower": "floral",
    "floral": "floral",
    "fragrant": "aroma",
    "fruit": "fruit",
    "fruiti": "fruit",
    "full": "full",
    "get": "get",
    "gingeri": "ginger",
    "gooseberri": "gooseberry",
    "good": "good",
    "grain": "grain",
    "graini": "grain",
    "grape": "grape",
    "grapefruit": "grapefruit",
    "grass": "grass",
    "grassi": "grass",
    "great": "great",
    "grow": "grow",
    "hazelnut": "hazelnut",
    "heather": "heather",
    "herb": "herb",
    "herbal": "herb",
    "honey": "honey",
    "intens": "intense",
    "iodin": "iodine",
    'leafi': 'leaf',
    'leatheri': 'leather',
    "length": "length",
    'liquoric': 'liqueur',
    "light": "light",
    "lightli": "light",
    "linger": "linger",
    "liqueur": "liqueur",
    "long": "long",
    "juici": "juicy",
    "juic": "juicy",
    "make": "make",
    "malt": "malt",
    "malti": "malt",
    "mango": "mango",
    "marzipan": "marzipan",
    "milk": "milk",
    'miner': 'mineral',
    "mint": "mint",
    "minti": "mint",
    "move": "move",
    "nut": "nut",
    "nutmeg": "nutmeg",
    "nutti": "nut",
    "oak": "oak",
    "oaki": "oak",
    "oil": "oily",
    "oily": "oily",
    "oili": "oily",
    "orange": "orange",
    "orang": "orange",
    'passion': 'passion fruit',
    "pastri": "pastry",
    "peach": "peach",
    "pear": "pear",
    "peat": "peat",
    "peati": "peat",
    "pepper": "pepper",
    "pepperi": "pepper",
    "peppercorn": "peppercorn",
    "pineappl": "pineapple",
    "pink": "pink",
    "plum": "plum",
    "raspberri": "raspberry",
    "red": "red",
    "resin": "resin",
    "rum": "rum",
    "round": "round",
    'salti': 'salt',
    "say": "say",
    "seem": "seem",
    "shake": "smoke",
    "sherri": "sherry",
    "sherry": "sherry",
    "show": "show",
    "smell": "aroma",
    "smoke": "smoke",
    "smoki": "smoke",
    "smooth": "smooth",
    "soft": "soft",
    "spice": "spice",
    "spici": "spice",
    "spirit": "spirit",
    "strength": "strength",
    "strong": "strong",
    "sugar": "sugar",
    "sweet": "sweet",
    "sweeter": "sweet",
    "syrup": "syrup",
    "take": "take",
    "tea": "tea",
    "toast": "toast",
    "toffe": "toffee",
    "tobacco": "tobacco",
    "tri": "try",
    "try": "try",
    "vanilla": "vanilla",
    "wax": "wax",
    "waxi": "wax",
    "white": "white",
    "whiski": "whisky",
    "wine": "wine",
    "wood": "wood",
    "woodi": "wood",
    "yellow": "yellow",
    "zest": "zest",
    "zesti": "zest"
}

def normalize_words(phrase):
    phrase = phrase.split()
    normalized_phrase = [normalize_map.get(word, word) for word in phrase]
    return " ".join(normalized_phrase)

df["review_full_text_processed"] = df["review_full_text_processed"].apply(normalize_words)

counter = CountVectorizer(max_df=0.8, min_df=0.05, strip_accents='unicode', binary=True)

counter.fit_transform(df['review_full_text_processed']).toarray()

reference_words = counter.get_feature_names_out()

tasting_notes_words_filtered = [
    'almond',
    'anise',
    'apple',
    'apricot',
    'ash',
    'banana',
    'barley',
    'berry',
    'bitter',
    'blackberry',
    'bread',
    'brine',
    'burnt',
    'butter',
    'cake',
    'candy',
    'caramel',
    'chalk',
    'char',
    'cherry',
    'chocolate',
    'cigar',
    'cinnamon',
    'citrus',
    'clove',
    'cocoa',
    'coconut',
    'coffee',
    'cream',
    'custard',
    'dust',
    'earthy',
    'eucalyptus',
    'fig',
    'floral',
    'fresh',
    'fruit',
    'ginger',
    'gooseberry',
    'grain',
    'grape',
    'grapefruit',
    'grass',
    'green',
    'hay',
    'hazelnut',
    'heather',
    'herb',
    'honey',
    'iodine',
    'jam',
    'juicy',
    'leather',
    'lemon',
    'lime',
    'liqueur',
    'malt',
    'mango',
    'marmalad',
    'marzipan',
    'medicin',
    'melon',
    'menthol',
    'milk',
    'mineral',
    'mint',
    'mocha',
    'nut',
    'nutmeg',
    'oak',
    'oily',
    'orange',
    'passion fruit',
    'pastry',
    'peach',
    'pear',
    'peat',
    'peel',
    'pepper',
    'peppercorn',
    'pine',
    'pineapple',
    'plum',
    'raisin',
    'raspberry',
    'resin',
    'ripe',
    'roast',
    'rum',
    'salt',
    'sherry',
    'smoke',
    'sour',
    'spice',
    'stew',
    'sugar',
    'sweet',
    'syrup',
    'tangerin',
    'tea',
    'toast',
    'tobacco',
    'toffee',
    'tropic',
    'vanilla',
    'varnish',
    'walnut',
    'warm',
    'wax',
    'wine',
    'wood',
    'zest'
]

counter = CountVectorizer(vocabulary=tasting_notes_words_filtered, max_df=0.8, min_df=0.05, strip_accents='unicode', binary=True)

review_text_vec = counter.fit_transform(df['review_full_text_processed']).toarray()

df['review_text_vector'] = review_text_vec.tolist()

df = df[['review_title', 'review_text_vector', 'review_score', 'review_image']]

#df.to_csv('reviews_vectors.csv', index=False)

df_tasting_notes = []

for i in df.index:

    review_title = df.loc[i, 'review_title']

    for j in range(len(tasting_notes_words_filtered)):

        tasting_note = tasting_notes_words_filtered[j]

        df_tasting_note = {
            'review_title': review_title,
            'tasting_note': tasting_note,
            'has_tasting_note': df.loc[i, 'review_text_vector'][j]
        }

        df_tasting_notes.append(df_tasting_note)

df_tasting_notes = pd.DataFrame(df_tasting_notes)

tasting_notes_groups = {

    "Fruity": [
        "apple", "apricot", "banana", "berry", "blackberry", "fig", "grape",
        "grapefruit", "lemon", "lime", "mango", "melon", "orange", "peach",
        "pear", "pineapple", "plum", "raisin", "jam", "marmalad",
        "gooseberry", "grass", "green", "passion fruit", "tropic",
        "citrus", "tangerin", "zest", "juicy", 'fruit', "ripe", "stew",
        "peel", 'sour', 'cherry', "raisin", "jam", 'raspberry',
        "sherry", "wine", "liqueur"
    ],

    "Floral": [
        "floral", "heather", "herb", "leafy", "fresh", 'tea', 'mint'
    ],

    "Spicy": [
        "anise", "cinnamon", "clove", "ginger", "nutmeg", "pepper",
        "peppercorn", "warm", 'spice'
    ],

    "Woody": [
        "oak", "wood", "pine", "resin", "varnish", "bitter"
    ],

    "Cereal": [
        "barley", "bread", "cake", "grain", "malt", "yeast", "pastry", 'dust', "bread", 'hay'
    ],

    "Peaty": [
        "peat", "smoke", "ash", "burnt", "char", "medicin", "iodine"
    ],

    "Feinty": [
        "leather", "tobacco", "plastic", "oily", "wax", "mineral", "earthy", 'butter', 'chalk', 'cigar'
    ],

    "Sulphury": [
        "menthol", "eucalyptus"
    ],

    "Sweet": [
        "candy", "caramel", "chocolate", "cocoa", "cream", "custard",
        "honey", "sweet", "sugar", "syrup", "toffee", "rum", 'vanilla', "marmalad",
        'cake', 'milk', 'mocha'
    ],

    "Nutty": [
        "almond", "hazelnut", "nut", "walnut", "marzipan", 'coconut'
    ],

    "Coastal": [
        "brine", "salt", "iodine"
    ],

    "Roasted": [
        "coffee", "roast", "toast"
    ]
    
}

df_tasting_notes_group = []

for tasting_notes_group in list(tasting_notes_groups.keys()):

    for tasting_note in tasting_notes_groups.get(tasting_notes_group):

        df_tasting_note_group = {
            'tasting_notes_group': tasting_notes_group,
            'tasting_note': tasting_note
        }

        df_tasting_notes_group.append(df_tasting_note_group)

df_tasting_notes_group = pd.DataFrame(df_tasting_notes_group)

df = df.merge(df_tasting_notes, how='left', on='review_title')
df = df.merge(df_tasting_notes_group, how='left', on='tasting_note')

df_total_tasting_notes = df.groupby(['review_title']).agg(total_tasting_notes=("has_tasting_note", "sum")).reset_index()

df_total_tasting_notes_group = df.groupby(['review_title', 'tasting_notes_group', 'review_score', 'review_image']).agg(total_tasting_notes_group=("has_tasting_note", "sum")).reset_index()

df_tasting_notes_group = df_total_tasting_notes_group.merge(df_total_tasting_notes, how='left', on='review_title')
df_tasting_notes_group['perc_tasting_notes_group'] = round(df_tasting_notes_group['total_tasting_notes_group'] / df_tasting_notes_group['total_tasting_notes'], 2)
df_tasting_notes_group = df_tasting_notes_group.drop(['total_tasting_notes_group', 'total_tasting_notes'], axis=1)

df_tasting_notes_group = df_tasting_notes_group.sort_values("review_score", ascending=False).drop_duplicates(subset=['review_title', 'tasting_notes_group'])

df_tasting_notes_group = df_tasting_notes_group.sort_values(['review_title', 'tasting_notes_group'])

df_tasting_notes_group = df_tasting_notes_group[~df_tasting_notes_group['perc_tasting_notes_group'].isna()].reset_index(drop=True)

df_tasting_notes_group.to_csv('databases/gold/flavour_wheel_long.csv', index=False)

# flavour_wheel_values = (
#   df_tasting_notes_group
#   .groupby('review_title')['perc_tasting_notes_group']
#   .apply(list)
#   .reset_index(name='flavour_wheel_values')
# )

# flavour_wheel_values.to_parquet("flavour_wheel.parquet", index=False)

# df = df.merge(df_tasting_notes_group, how='left', on=['review_title', 'tasting_notes_group'])
# df = df.drop('has_tasting_note', axis=1)

# df[df['tasting_notes_group'].isna()]['tasting_note'].unique()

# freq = review_text_vec.sum(axis=0)

# freq_df = pd.DataFrame({
#     'word': counter.get_feature_names_out(),
#     'frequency': freq
# }).sort_values(by='frequency', ascending=False).reset_index(drop=True)

# print(freq_df)

# words_freq = (review_text_vec.T @ review_text_vec)

# df_words_freq = pd.DataFrame(words_freq, columns=tasting_notes_words_filtered, index=tasting_notes_words_filtered)
# np.fill_diagonal(df_words_freq.values, -1)

# df_words_freq