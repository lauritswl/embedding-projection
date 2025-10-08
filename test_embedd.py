from src.embedder import Embedder
from src.projecter import ProjectionAnalyzer

# Write your project name:
project_name = "My_Text_Projection"
# Define your texts as a list of strings:
texts = ["This is amazing!", "This is Okay." ,"This is terrible."]

# --- Embed the texts ---:
MultiLingMPNET = Embedder(model_name="paraphrase-multilingual-mpnet-base-v2")
Text_Embedding = MultiLingMPNET.embed(
    texts=texts,
    cache_path=f"data/embeddings/{project_name}.csv")
Text_Embedding["text"] = texts # Append text to embeddings

# --- Project Embeddings ---
ProjectionAnalyzer = ProjectionAnalyzer(matrix_project=Text_Embedding, use_concept_vector=True, concept_vector_path="data/concept_vectors/vectors/Fiction4Sentiment_concept_vector.csv")
ProjectionAnalyzer.project()

# --- Save results ---
import pandas as pd
results = pd.DataFrame({
        "text": Text_Embedding["text"],
        "prediction": ProjectionAnalyzer.projected_in_1D
})
results.to_csv(f"data/processed/{project_name}_projections.csv", index=False)