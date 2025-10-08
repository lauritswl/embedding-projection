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