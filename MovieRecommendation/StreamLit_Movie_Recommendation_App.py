import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd
import spacy

st.title("Movie Recommendation Engine")

data = pd.read_csv("data/movie_overviews.csv")

st.sidebar.markdown("Select Any Movie from the List to find similar movies. This similarity is based on the movie plot.")

title = st.sidebar.selectbox("Select Movie Title", data['title'].unique())

# Generate mapping between titles and index
indices = pd.Series(data.index, index=data['title']).drop_duplicates()

## Stopwords
stopwords = ['fifteen','noone','whereupon','could','ten','all','please','indeed','whole','beside','therein','using','but','very','already','about','no','regarding','afterwards','front','go','in','make','three','here','what','without','yourselves','which','nothing','am','between','along','herein','sometimes','did','as','within','elsewhere','was','forty','becoming','how','will','other','bottom','these','amount','across','the','than','first','namely','may','none','anyway','again','eleven','his','meanwhile','name','re','from','some','thru','upon','whither','he','such','down','my','often','whether','made','while','empty','two','latter','whatever','cannot','less','many','you','ours','done','thus','since','everything','for','more','unless','former','anyone','per','seeming','hereafter','on','yours','always','due','last','alone','one','something','twenty','until','latterly','seems','were','where','eight','ourselves','further','themselves','therefore','they','whenever','after','among','when','at','through','put','thereby','then','should','formerly','third','who','this','neither','others','twelve','also','else','seemed','has','ever','someone','its','that','does','sixty','why','do','whereas','are','either','hereupon','rather','because','might','those','via','hence','itself','show','perhaps','various','during','otherwise','thereafter','yourself','become','now','same','enough','been','take','their','seem','there','next','above','mostly','once','a','top','almost','six','every','nobody','any','say','each','them','must','she','throughout','whence','hundred','not','however','together','several','myself','i','anything','somehow','or','used','keep','much','thereupon','ca','just','behind','can','becomes','me','had','only','back','four','somewhere','if','by','whereafter','everywhere','beforehand','well','doing','everyone','nor','five','wherein','so','amongst','though','still','move','except','see','us','your','against','although','is','became','call','have','most','wherever','few','out','whom','yet','be','own','off','quite','with','and','side','whoever','would','both','fifty','before','full','get','sometime','beyond','part','least','besides','around','even','whose','hereby','up','being','we','an','him','below','moreover','really','it','of','our','nowhere','whereby','too','her','toward','anyhow','give','never','another','anywhere','mine','herself','over','himself','to','onto','into','thence','towards','hers','nevertheless','serious','under','nine']


# Load the spacy model
nlp = spacy.load('en_core_web_sm')

# Function to preprocess text
def preprocessing(text):
	# Create Doc object
    doc = nlp(text)
    # Generate tokens
    tokens = [token.text for token in doc]
    # Remove stopwords and non-alphabetic characters
    tokened = [token for token in tokens 
            if token.isalpha() and token not in stopwords]
    return ' '.join(tokened)

# Apply preprocess to overview
data['cleaned'] = data['overview'].apply(preprocessing)

## Get the cleaned movie plots
movie_plots = data['cleaned']

## Getting the recommendations
@st.cache
def get_recommendations(title, similarity, indices):
    # Get index of movie that matches title
    idx = indices[title]
    # Sort the movies based on the similarity scores
    sim_scores = list(enumerate(similarity[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # Get the scores for 10 most similar movies
    sim_scores = sim_scores[1:11]
    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]
    # Return the top 10 most similar movies
    return data[['title', 'overview']].iloc[movie_indices]

@st.cache
def get_similarity_matrix(movie_plots):
	# Initialize the TfidfVectorizer 
	tfidf = TfidfVectorizer(stop_words='english')
	# Construct the TF-IDF matrix
	tfidf_matrix = tfidf.fit_transform(movie_plots)
	# Generate the similarity matrix
	sim_matrix = linear_kernel(tfidf_matrix, tfidf_matrix)
	return sim_matrix

similarity = get_similarity_matrix(movie_plots)

## Adding text to the main page
st.write('Showing the movies similar to :: ', title)

# Generate recommendations 
st.table(get_recommendations(title, similarity, indices))