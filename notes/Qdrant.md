Apparently you can define the storage location of the embeddings. This code tells your local computer to use its memory as temporary storage: `client = QdrantClient(":memory:")`

This is how you create a collection. You need to provide the name, the vector size, and the function to measure the distance between vectors (in this case, cosine similarity). **Can you update this function on the fly?**
```python
client.create_collection(
    collection_name="my_books",
    vectors_config=models.VectorParams(
        size=encoder.get_sentence_embedding_dimension(),  # Vector size is defined by used model
        distance=models.Distance.COSINE,
    ),
)
```

