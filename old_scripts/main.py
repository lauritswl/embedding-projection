# %%
from utils import *
from old_scripts.functions import *

# %%
# Load the dataset:
IMDb_df = pd.read_csv('../data/raw/imdb.csv')
print(IMDb_df['review'] [1:5])
from old_scripts.functions import clean_string
# Slice the DataFrame first:
subset_df  = IMDb_df.iloc[1:2000].reset_index(drop=True)

# Clean the reviews:
subset_df['review'] = subset_df ['review'].apply(clean_string)
subset_corpus= subset_df['review'].tolist()

# Load the SentenceTransformer model:
MPNET_Model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2', device="cuda" if torch.cuda.is_available() else "cpu")

# %%
# Encode reviews:
MPNET_Embedding = MPNET_Model.encode(subset_corpus, show_progress_bar=True, device="cuda" if torch.cuda.is_available() else "cpu")
# Save embeddings as a CSV:
embedding = pd.DataFrame(MPNET_Embedding)
embedding['sentiment'] = subset_df['sentiment']
embedding['review'] = subset_df['review']
embedding.to_csv('../data/processed/embeddings/MPNET_Embeddings.csv', index=False)


# %%
# Load the embeddings from the file:
embedding = pd.read_csv('../data/processed/embeddings/MPNET_Embeddings.csv')
# Check the first 5 rows and columns of the dataframe:
embedding.iloc[-5:-1] # Check the first 5 rows of the dataframe



# %%
# Filter pandas dataframe for positive and negative sentiment:
positive = embedding[embedding['sentiment'] == "positive"]
negative = embedding[embedding['sentiment'] == "negative"]
# Investigate the shape of the dataframes:
print(positive.shape)
print(negative.shape)

# %%
from old_scripts.functions import positive_to_negative_vector, express_matrix_by_vector

# Define the sentiment vector by subtracting the mean of the negative from the mean of the positive:
sentiment_vector = positive_to_negative_vector(positive.iloc[:, :-2], negative.iloc[:, :-2])
projection, projection_in_1D_subspace = express_matrix_by_vector(embedding.iloc[:, :-2], sentiment_vector)

# Check mean projection_in_1D_subspace for positive and negative sentiment:
print(projection_in_1D_subspace[embedding['sentiment'] == "positive"].mean())
print(projection_in_1D_subspace[embedding['sentiment'] == "negative"].mean())


# %%
# Plot histogram of the projection_in_1D_subspace, colored by sentiment:
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
# Plot histogram of projections colored by sentiment
plt.figure(figsize=(10, 6))
sns.histplot(data=embedding, x=projection_in_1D_subspace, hue='sentiment', element='step', stat='density', common_norm=False, palette='coolwarm', bins=30)
plt.title('Distribution of Reviews Along the Sentiment Vector')
plt.xlabel('Projection onto Sentiment Vector')
plt.ylabel('Density')
plt.grid(True)
plt.show()

# %%
# Plot KDE of projections colored by sentiment
plt.figure(figsize=(10, 6))
sns.kdeplot(
    x=projection_in_1D_subspace[embedding['sentiment'] == 'positive'],
    label='Positive',
    fill=True,
    alpha=0.4,
    linewidth=2,
    color='blue'
)
sns.kdeplot(
    x=projection_in_1D_subspace[embedding['sentiment'] == 'negative'],
    label='Negative',
    fill=True,
    alpha=0.4,
    linewidth=2,
    color='red'
)
plt.title('Sentiment Distributions Of Reviews Along Projection Vector')
plt.xlabel('Projection onto Sentiment Vector')
plt.ylabel('Density')
plt.legend()
plt.grid(True)
plt.tight_layout()
# Save plot in img folder:
plt.savefig('../img/sentiment_distributions.png', dpi=300, bbox_inches='tight')
# Show plot:
plt.show()


# %%
from old_scripts.functions import get_clean_words
# Get the most common words in the positive and negative reviews:
mapped_set = map(get_clean_words, embedding['review'])
my_set = set().union(*mapped_set)

# Convert set to list
words = list(my_set)
# Initialize the tokenizer, good basic tokenizer
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-mpnet-base-v2')


# Tokenize each word in the list
tokenized_words = [tokenizer.tokenize(word) for word in words]
# Flatten the tokenized words list
flat_tokens = [token for sublist in tokenized_words for token in sublist]

# Save each unique element:
review_tokens_corpus =  list(set(flat_tokens))


# %%
review_tokens_corpus

# %%
# Encode the words:
word_embeddings = MPNET_Model.encode(review_tokens_corpus, show_progress_bar=True, device="cuda" if torch.cuda.is_available() else "cpu")
# %% 
word_embeddings=pd.DataFrame(word_embeddings)
word_embeddings.iloc[0:5] # Check the first 5 rows and columns of the word embeddings

# %%
projected_variance, projection_in_1D_subspace = express_matrix_by_vector(matrix=word_embeddings, vector=sentiment_vector)

# Find the 10 smallest values' indices
smallest_indices = projection_in_1D_subspace.nsmallest(10).index
# Map indices to words in the corpus
smallest_words = [review_tokens_corpus[i] for i in smallest_indices]

print("Words corresponding to the 10 smallest embeddings:")
print(smallest_words)

# find the 10 largest values' indices
largest_indices = projection_in_1D_subspace.nlargest(10).index
# Map indices to words in the corpus
largest_words = [review_tokens_corpus[i] for i in largest_indices]
print("Words corresponding to the 10 largest embeddings:")
print(largest_words)


# %%
import json
# Path to your JSON file
with open('../data/raw/fiction4_data.json', 'r') as f:
    data = json.load(f)



# %% 
print("Top-level type:", type(data))
print("Top-level keys:" if isinstance(data, dict) else "First items:")
print(list(data.keys()) if isinstance(data, dict) else data[:3])
# %%
# Transform sentences to lists:
sentences_fiction4 = list(data['SENTENCE_ENGLISH'].values())
# Embed sentences_fiction4:
# fiction4_Embedding = MPNET_Model.encode(sentences_fiction4, show_progress_bar=True, device="cuda" if torch.cuda.is_available() else "cpu")


# %%
fiction4_Embedding = pd.DataFrame(fiction4_Embedding)
fiction4_Embedding['sentiment'] = list(data['HUMAN'].values())
fiction4_Embedding['review'] = sentences_fiction4
fiction4_Embedding.to_csv('../data/processed/embeddings/fiction4_Embeddings.csv', index=False)
# %%
fiction4_Embedding = pd.read_csv('../data/processed/embeddings/fiction4_Embeddings.csv')
# Check the las 5 rows of the dataframe:
fiction4_Embedding.iloc[-5:-1]

# %%
fiction4, fiction4_in_1D_subspace = express_matrix_by_vector(fiction4_Embedding.iloc[:, :-2], sentiment_vector)
# %%

fiction4_in_1D_subspace
fiction4_Embedding['sentiment']

# %%
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# Assuming both are lists or 1D numpy arrays of length 6300
x = fiction4_in_1D_subspace
y = fiction4_Embedding['sentiment']

# Plotting
plt.scatter(x, y, alpha=0.5)
plt.xlabel('IMDb-defined Subspace Projection')
plt.ylabel('Human Annotation')
plt.title('Scatterplot with Correlation')

# Compute correlation
corr, _ = pearsonr(x, y)
plt.figtext(0.15, 0.85, f'Pearson r = {corr:.2f}', fontsize=12, color='blue')
# Save plot in img folder:
plt.savefig('../img/Scatterplot_w_Person.png', dpi=300, bbox_inches='tight')
plt.show()

# %%
import pandas as pd

# If it's a dictionary
df = pd.DataFrame({
    'ANNOTATOR_1': data['ANNOTATOR_1'],
    'ANNOTATOR_2': data['ANNOTATOR_2'],
    'ANNOTATOR_3': data['ANNOTATOR_3'],
})

# Pearson correlation matrix
correlation_matrix = df.corr(method='pearson')
# Create the heatmap
plt.figure(figsize=(6, 4))  # optional: adjust size
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=0, vmax=1)

# Title and layout
plt.title('Pearson Correlation Between Annotators')
plt.tight_layout()
# Save plot in img folder:
plt.savefig('../img/Annotator_Corr.png', dpi=300, bbox_inches='tight')
plt.show()










# %%
# ______________________________________________________________________________
#### LINGUISTIC ACCEPTABILITY ####
# ______________________________________________________________________________
# Load the dataset:
from datasets import load_dataset

# Load GLUE dataset subset (e.g., SST-2)
dataset = load_dataset("nyu-mll/glue", "cola")
dataset['train']
dataset['train']['label']

#%%
# filter postivie and negative subset:
LA_positive = dataset['train'].filter(lambda x: x['label'] == 1).select(range(1000))
LA_negative = dataset['train'].filter(lambda x: x['label'] == 0).select(range(1000))

# Investigate the shape of the dataframes:
print(LA_positive.shape)
print(LA_negative.shape)

#%%
# EMBEDDING of LINGUISTIC ACCEPTABILITY DATASET:
# Encode reviews:
LA_positive_emb = MPNET_Model.encode(LA_positive['sentence'], show_progress_bar=True, device="cuda" if torch.cuda.is_available() else "cpu")
# Save embeddings as a CSV:
LA_positive_emb = pd.DataFrame(LA_positive_emb)
LA_positive_emb.to_csv('../data/embeddings/LA_positive_emb.csv', index=False)


LA_negative_emb = MPNET_Model.encode(LA_negative['sentence'], show_progress_bar=True, device="cuda" if torch.cuda.is_available() else "cpu")
# Save embeddings as a CSV:
LA_negative_emb = pd.DataFrame(LA_negative_emb)
LA_negative_emb.to_csv('../data/embeddings/LA_negative_emb.csv', index=False)

#%%
# Embed test set:
LA_validation_embedding = MPNET_Model.encode(dataset['validation']['sentence'], show_progress_bar=True, device="cuda" if torch.cuda.is_available() else "cpu")
LA_validation_embedding =  pd.DataFrame(LA_validation_embedding)
# %%
from old_scripts.functions import positive_to_negative_vector, express_matrix_by_vector
# Define the acceptability vector by subtracting the mean of the negative from the mean of the positive:
ling_accept_vector = positive_to_negative_vector(LA_positive_emb, LA_negative_emb)
# Project validation embedding onto the acceptability vector:
projection, projection_in_1D_subspace = express_matrix_by_vector(LA_validation_embedding, ling_accept_vector)
# %%

import matplotlib.pyplot as plt

# Extract labels from test set
test_labels = dataset['validation']['label']  # assuming this gives a list or Series of 0s and 1s

# Convert to a pandas Series to align with projection_in_1D_subspace
import pandas as pd
test_labels = pd.Series(test_labels)

# Filter projections by label
positive_proj = projection_in_1D_subspace[test_labels == 1]
negative_proj = projection_in_1D_subspace[test_labels == 0]

# Plot histogram
plt.figure(figsize=(10, 6))
plt.hist(positive_proj, bins=50, alpha=0.6, label='Positive (label = 1)', color='green')
plt.hist(negative_proj, bins=50, alpha=0.6, label='Negative (label = 0)', color='red')
plt.xlabel("Projection on Acceptability Vector")
plt.ylabel("Frequency")
plt.title("Histogram of Validation-set Embeddings Projected onto Acceptability Vector")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Save plot in img folder:
plt.savefig('../img/LA_validation_histogram.png', dpi=300, bbox_inches='tight')


# %%
