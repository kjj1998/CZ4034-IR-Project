import pandas as pd
import numpy as np
import requests
import csv

from sentence_transformers import SentenceTransformer
from PIL import Image
from tqdm import tqdm

CSV_FILENAME = "./overall_sentiment_classification_output.csv"


amzn_df = pd.read_csv("./overall_sentiment_classification_output.csv", encoding = "ISO-8859-1")
img_model = SentenceTransformer('clip-ViT-B-32')

image_urls = amzn_df['amazon_image_url'].to_numpy()
images = [Image.open(requests.get(url, stream=True).raw) for url in tqdm(image_urls, total=len(image_urls))]
vectors = img_model.encode(images, convert_to_numpy=True, show_progress_bar=True)

vectors_df = pd.DataFrame({'vector': [list(vector) for vector in list(vectors)] })
amzn_with_embeddings_df = pd.concat([amzn_df, vectors_df], axis = 1)
amzn_with_embeddings_df = amzn_with_embeddings_df.rename(columns={'index':'id'})
amzn_with_embeddings_df = amzn_with_embeddings_df.rename(columns={'title':'name'})
amzn_with_embeddings_df["review"] = amzn_with_embeddings_df["review"].str.replace('"', '""' )
amzn_with_embeddings_df.to_csv('amzn_with_embeddings_and_polarity.csv', index=False, quoting=csv.QUOTE_ALL)