https://www.deeplearning.ai/short-courses/building-ai-applications-with-haystack/
* Main components: pipelines, components, document stores
* Abstracts the pipeline components so you can, e.g., easily swap in different vector databases
* Open source
* Branching (e.g. fall back to web search if retrieved document does not contain answer in RAG pipeline) and looping (e.g. LLM can iteratively refine its answer) pipelines. Branching gives the pipeline decision-making capability.
* Can create custom components - simply wrap code to be Haystack compatible


* AI application is composed of smaller tasks combined into a larger use-case. These smaller tasks are represented by components. For example, in a RAG application, the components are retrieval and generation. Connect components to form a pipeline, which is the application.
* Pipelines have access to document stores (databases of various types) through components
* Example pipelines
    * Embedder + retriever = document search pipeline
    * Question answering with RAG
        * Semantic search: Embedder -> Embedding Retriever -> PromptBuilder -> Generator
        * Keyword-based retrieval: Keyword Retriever (like BM25) -> PromptBuilder -> Generator
        * Retrieval + Reranking: BM25/Embedding Retriever -> Ranker -> PromptBuilder -> Generator
    * Indexing (embedding and storing to vector DB): Clean -> Split -> Embed -> DocumentWriter
    * Chat
    * Question generation
    * Output validation
* Ready-made components: generators (generative LLMs), embedders, retrievers (database search), converters (format-to-format), rankers, routers, preprocessors, etc.

* Integrations: https://haystack.deepset.ai/integrations 

I think Haystack has built-in components, integrated components, and you can also create custom components if neither of the first two options support your use case.

Haystack integration = user-uploaded custom components (maintained by the company that is integrated or by deepset)

Prompts in prompt builder use Jinja template for control flow, etc.

You can provide Haystack pipelines as functions to LLMs, which LLMs can call and use as agents.