<h1 align="center">Embedding Projection</h1>
<p align="center">
    <a href="https://arxiv.org/abs/2508.14620">
        <img alt="arXiv" src="https://img.shields.io/badge/arXiv-2508.14620-b31b1b.svg">
    </a>
    <a href="https://huggingface.co/datasets/chcaa/fiction4sentiment">
        <img alt="arXiv" src=https://img.shields.io/badge/Fiction4_Data-hugginface-yellow>
    </a>
    <a href="https://github.com/JULIELab/EmoBank/blob/master/corpus/emobank.csv">
        <img alt="Emobank" src="https://img.shields.io/badge/Emobank_Data-github-blue">
    </a>
</p>

## 🔍 Overview
A project developing a technique for extracting information from contextual sentence embeddings ([model="paraphrase-multilingual-mpnet-base-v2"](https://huggingface.co/sentence-transformers/paraphrase-multilingual-mpnet-base-v2)) by utilizing projection of embeddings onto a [concept vector](data/concept_vectors/vectors).

This repository is build with the objective of reproducing the results from the accompanying research paper:


<p align="center">
    <a href="https://arxiv.org/abs/2508.14620">Continuous sentiment scores for literary and multilingual contexts</a>
    <br>
    <a href="https://arxiv.org/abs/2508.14620">
        <img alt="arXiv" src="https://img.shields.io/badge/arXiv-2508.14620-b31b1b.svg">
    </a>
</p>


The repository contains the datasets used, the functions used to embbed the data, and a method for projecting new data onto the 'Concept Vector'.

The main pipeline of the project is visualised below.
![Projection Pipeline](powerpoints/Projection_Pipeline.png)


## 🛠️ Installation
1. Clone the repository and navigate to it
```bash
git clone https://github.com/centre-for-humanities-computing/embedding-projection.git
cd embedding-projection
```

2. Create and activate virtual environment with uv
```bash
uv venv
source .venv/bin/activate
```

3. Install dependencies from pyproject.toml
```bash
python -m venv venv
source venv/bin/activate
pip install -e .
```
**Requirements:**
Dependencies needed to run main.py can be found in the [pyproject.toml](pyproject.toml). 

## 🚀 Usage
### ⚡ Quick Start
**WIP: I'm currently working on a lightweight package for this.**

Until the package has been deployed, a working solution can be found in the [quick_sentiment.py](quick_sentiment.py) script


```python
from src.embedder import Embedder
from src.projecter import ProjectionAnalyzer

# Setup - Define your project_name and texts as a list of strings:
project_name = "My_Text_Projection"
texts = [
    "This is amazing!", 
    "This is okay.", 
    "This is terrible."
]

# 1. Create embeddings
MultiLingMPNET = Embedder(model_name="paraphrase-multilingual-mpnet-base-v2")
embeddings = MultiLingMPNET.embed(
    texts=texts,
    cache_path=f"data/embeddings/{project_name}.csv")
embeddings["text"] = texts # Append text to embeddings

# 2. Project onto sentiment vector
projector = ProjectionAnalyzer(
    matrix_project=embeddings,
    use_concept_vector=True,
    concept_vector_path="data/concept_vectors/vectors/Fiction4Sentiment_concept_vector.csv"
)
projector.project()

# 3. Save results
import pandas as pd
results = pd.DataFrame({
    "text": texts,
    "sentiment_score": projector.projected_in_1D
})
results.to_csv(f"data/processed/{project_name}_projections.csv", index=False)
```

#### Output Format
The script produces a CSV file with text and their corresponding sentiment scores:
```csv
text,sentiment_score
This is amazing!,1.047
This is okay.,0.681
This is terrible.,-1.366
```

### 📊 Reproducing Paper Results
Run main.py to reproduce the plots and results used in the paper:

```bash
# Make sure your virtual environment is activated
source .venv/bin/activate

# Run the main script
python main.py

# The script will:
# 1. Load and preprocess the datasets
# 2. Create embeddings using MPNET
# 3. Generate concept vectors
# 4. Project test data onto concept vectors
# 5. Create plots in the plots/ directory
```

## 🧪 Sanity-Check of the Sentiment Vector
It seems that there is a rather strong correlation between average human anotator and the projection method!
This is seen in the scatterplot below, visualising the correlation between predictions and annotators for the EmoBank dataset (which is left out of training dataset):

![Human Annotator Correlation with Semantic Projection](plots/Scatterplot_Emobank_MultiLingMPNET_standardized.png)



### 📈 Distribution Analysis
The projection of binary-classified IMDB reviews onto our Sentiment Vector shows clear separation between positive and negative sentiments:

![Projection of Reviews onto Sentiment Vector](plots/IMDb_Sentiment_Distributions.png)

### 🔤 Word-Level Analysis
To validate our approach, we projected individual words from the corpus onto the Sentiment Vector. This method, inspired by [S3 - Semantic Signal Separation](https://arxiv.org/abs/2406.09556). The script for doing this is not included in the repo:


#### ⬆️ Highest Projection Score
```
pleasure    anytime     admired     admire      fabulous
classical   beloved     romantic    anthologies  lovely
```

#### ⬇️ Lowest Projection Score
```
worse       terrible    sucked      horrible    worst
bad         rotten      unacceptable stupidity   awful
```
*⚠️ Note: it seems that the vector might be correlated with the romantic literature period (H.C.Andersen), i.e. "anthologies, classical, romantic". This might be a byproduct of fairytales having a high density of positive semantics, thus being overrepresented in the training set.*

## 📂 Directory Structure
```bash
EMBEDDING-PROJECTION/
│
├── README.md
├── pyproject.toml
├── main.py
├── quick_sentiment.py
│
├── src/
│   ├── loader.py
│   ├── embedder.py
│   ├── projecter.py
│   ├── pipeline.py
│   └── plotter.py
│
├── data/
│   ├── raw/
│   │   ├── fiction4_data
│   │   └── emobank_data
│   ├── embeddings/
│   │   └──gitignored_embedding_cache
│   ├── processed/
│   │   └──...Sentiment.csv
│   └── concept_vectors/
│       ├── text/
│       └── vectors/
│
└── plots/
```

## ⚖️ License
embedding-projection is available under the MIT license. See the LICENSE file for more info.
