# <u>Motivation for RAG:</u>
* Models hallucinate because they don't know the answer to a question. The knowledge they have depends on their training data; if they don't see it or haven't seen much of it (obscure/rare topics), then they will make stuff up. They are probabilistic models that simply predict the next token; they have no ability to check for factual accuracy.
* Models have a cutoff date (the date they are trained; the model knows nothing about anything that happens after).
* RAG retrieves the information that the model needs to answer a question and provides that context to the model.
* RAG allows us to use a smaller LLM since it retrieves knowledge instead of storing everything internally. This makes RAG more efficient than training a massive LLM with all possible knowledge embedded.

# <u>RAG subsystems</u>

There are 3 RAG subsystems:
* Indexing: Loading, chunking, and embedding your documents and storing the chunks and embeddings into a vector database. The choice of chunking strategy and vector indexing method affects retrieval speed and accuracy.
* Retrieval: Using a similarity search, based on the distance metric and vector indexing method, to retrieve the most relevant chunks from the vector database.
* Augmentation: Augmenting the LLM prompt with the retrieved chunks and generating a response.

## <u>Indexing</u>

Indexing steps:
* Load the documents e.g. presentations, PDF, anything. Oftentimes this involves format conversion.
* Chunk the documents - you need to decide how to split up your documents before embedding
    * Fixed chunking - each chunk is same size, which works well for structured text like tables and lists but is generally not suited for unstructured text since ideas are not neatly conveyed in same-size chunks
    * NLP chunking - using regex, heuristics like sentence segmentation, or semantic chunking (ML) models to preserve meaning. For example, detecting paragraph boundaries and chunking by paragraph. You can chunk by tokens, words, sentences, paragraphs, pages, etc.
    * Hyperparameters
        * Chunk size - number of tokens/words/sentences/paragraphs/pages per chunk 
        * Chunk overlap - how many tokens/words/sentences/paragraphs/pages to overlap b/w adjacent chunks. Having overlap usually helps with retrieval.
* Embed the chunks - convert the chunks from text or other media to vectors. You can choose to normalize the vectors (like L2 norm), e.g. for dot product similarity.
    * OpenAI text embedding model is trained using contrastive learning, where pairs of text are passed to the model. Pairs are either positive (similar) or negative (dissimilar). The pairs are embedded and cosine similarity is calculated for the pair of embeddings. The weights of the model are updated to maximize cosine similarity for positive pairs and minimize cosine similarity for negative pairs.
    * Open source models are available via Hugging Face and the sentence-transformers library
* Store the chunks and the corresponding vectors to a vector store. Vectors require a new kind of DB for fast retrieval (previous DB types: SQL, key-value, document, graph). This step is also when you choose the vector indexing method, which is the search structure that stores the vectors, and this affects the speed and accuracy of the retrieval (see the retrieval section for vector indexing methods).

LangChain and LlamaIndex are two frameworks that support indexing a vector DB.

## <u>Retrieval</u>

Retrieval steps:
* Get the user query
* Embed the user query using the same embedding model used for indexing the document chunks
* Vector search (vector store retriever): Find the vectors in the DB that are most similar to the query vector. This search depends on the indexing method and the distance metric chosen for the collection.
    * Most common distance/similarity metrics for similarity search for dense (floating-point) vectors
        * Cosine similarity: cosine of the angle between two vectors (normalized dot product)
        * Inner (dot) product: projection of one vector onto the other vector
        * Euclidean distance: L2 distance between two vectors
        * Manhattan distance (rarely used because it's less effective than L2 for high-dimensional spaces): L1 distance between two vectors
    * Search and indexing methods
        * Linear search/FLAT index: Calculate the similarity of the embedded query against all vectors in the vector DB. This gives 100% accuracy and is perfectly fine for smaller datasets but is not practical for large datasets because query time grows as $O(n)$.
        * Approximate nearest neighbors search (ANN): This reduces the search space to speed up the search at the expense of some accuracy. There are different implementations of ANN with different indexes.
            * Space partitioning: Split the vector space into a subspaces and limit the search to the nearest subspaces.
                * K-dimensional trees (kd-trees) bisect the search space in a manner similar to binary search trees. kd-trees are inefficient for high-dimensional vectors (>20D).
                * ANNOY, the algorithm used by Spotify for their music recommendation system, uses random projection trees to create a binary search tree.
                * Inverted file index (IVF) splits the vector space into Voronoi cells. The search is first conducted against the centroids to determine the nearest cell(s), and then the search is performed against the vectors in those nearest cell(s). IVF is often combined with PQ (IVF-PQ) for better efficiency.
            * Quantization: By reducing the precision of the embedding vectors, we reduce the database size and also increase search speed because the distance computation requires fewer operations.
                * Scalar quantization (SQ): Multiply high-precision floating-point vectors with a scalar and then cast the product to the nearest integer (e.g. converting from float64 to int8 reduces vector size by a factor of 8)
                * Product quantization (PQ): Split vectors into equally-sized subvectors, and replace each subvector with a centroid. This is similar to dictionary compression.
            * Hierarchical navigable small worlds (HNSW): Builds a multi-layer graph where closer vectors are more densely connected, enabling fast search with logarithmic complexity.
            * LSH
* Return the `top_k` most similar documents


    
* ANN (approximate nearest neighbors). Reduces search space to speed up search. Construct ANN tree. Split vector space into two, and keep splitting. Then you can search the entire dataset in log time, since the height of the tree is log2(total number of data points). Simply traverse the tree until you hit a leaf, and all vectors in that leaf are the neighbors.
            * You can have multiple trees, e.g. forest of trees. You can aggregate the neighbors from all the trees to get a larger sample size of relevant documents. Then you run cosine similarity on the neighbors against the query.
        * Nearest neighbor search is used in collaborative filtering (recommender systems), semantic search, information retrieval
        * This is also called clustering
        * ANN search libraries
            * FAISS (Facebook AI Similarity Search): indexing, searching, and clustering of dense vectors; GPU support; integrates with PyTorch and TensorFlow
            * Spotify Annoy: C++ library, uses random projection trees
            * Google ScaNN: TensorFlow-based library, uses compression and hashing techniques to speed up search
            * NMSLIB: generic similarity search library. Supports both dense and sparse vectors.
            * HNSWLIB: uses hierarchical graph structure to speed up search and supports both dense and sparse vectors

![ANN search tree](./assets/approx_nearest_neighbors_search_tree.png)

How does indexing affect retrieval? Does it affect retrieval? Yes.
Indexing methods:
* Flat - exhaustive search; compare against all vectors
* **IVFFlat** - IVF stands for inverted file index. Voronoi cells and centroids. Compare against `n_probe` centroids; nearest neighbors are in the selected centroid. Clusters the search space. This is a very popular index for vector DB index and retrieval.
* IVFPQ - PQ stands for product quantization. Reduces the dimension of the distance calculation to reduce the calculation time.
* LSH
* **HNSW** - idea comes from traditional search engines and graph search. Does not require much memory; is fast and accurate.

HNSW and IVFFlat are the most popular index and retrieval techniques.

Trade-off between retrieval accuracy and speed.

## <u>Augment</u>

Generally speaking, the LLM will be fine-tuned (and most likely instruction-tuned). Question-answering, etc.






**<u>Fine-tuning vs. RAG vs. prompt engineering:</u>**
* When you want to modify the behavior to your model to align with a particular style or domain expertise, use fine-tuning. For example, use fine-tuning when you want the model to sound like a medical professional, write in a poetic style, or use the jargon of a specific industry.
* When you want the model to incorporate external knowledge in its responses, use RAG.
* Prompt engineering is a quick and easy way to approximate both fine-tuning and RAG. Since the LLM is instruction-tuned, you can prompt the model to follow, for example, a specific formatting. You can also provide some "external" information in the prompt to enable in-context learning. Prompt engineering is always a good idea whether you use RAG or fine-tuning (or both).

![Venn diagram: Fine-tuning vs. RAG vs. prompt engineering](./assets/finetune_rag_prompt-eng_venn_diagram.png)


RAG + fine-tuning: In a RAG pipeline, there are two blocks with parameters, the query embedder and the LLM. The search is non-parametric. If you can compare the LLM output against a target, you can backprop through both LLM and query embedder to fine-tune the entire pipeline. What's interesting here is that you can't really update the embeddings in the vector database even though the vector DB embeddings and the query embedding are typically generated using the same embedder.