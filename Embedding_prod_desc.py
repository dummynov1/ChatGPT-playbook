import pandas as pd
import torch
from transformers import BertTokenizer, BertModel
from sklearn.cluster import KMeans

# Load the product dataset
df = pd.read_csv('products.csv')

# Create a tokenizer instance
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Load the pre-trained BERT model
model = BertModel.from_pretrained('bert-base-uncased')

# Preprocess the text data
descs = df['DESC'].tolist()
inputs = tokenizer.batch_encode_plus(descs, 
                                       add_special_tokens=True, 
                                       max_length=512, 
                                       padding='max_length', 
                                       truncation=True, 
                                       return_attention_mask=True, 
                                       return_tensors='pt')

# Generate embeddings
with torch.no_grad():
    outputs = model(inputs['input_ids'], attention_mask=inputs['attention_mask'])
    embeddings = outputs.last_hidden_state[:, 0, :]  # Take the embedding of the [CLS] token

# Convert to Pandas DataFrame
emb_df = pd.DataFrame(embeddings.numpy())

# Concatenate with continuous variables
df_cont = df.drop(['DESC'], axis=1)  # assume continuous variables are in the remaining columns
df_combined = pd.concat([df_cont, emb_df], axis=1)

# Perform K-Means clustering
kmeans = KMeans(n_clusters=8, random_state=42)
kmeans.fit(df_combined)

# Get the cluster labels
labels = kmeans.labels_

# Add the cluster labels to the original DataFrame
df['cluster'] = labels

# Save the updated DataFrame
df.to_csv('products_with_clusters.csv', index=False)
