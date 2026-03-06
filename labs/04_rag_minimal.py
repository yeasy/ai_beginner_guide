"""
Minimal RAG (Retrieval-Augmented Generation) Pipeline Example

Corresponds to: Chapter 7.5 - 上下文工程（Context Engineering）

This module demonstrates the core concepts of RAG:
1. Document ingestion and embedding
2. Vector similarity search (retrieval)
3. Context-augmented generation

TODO:
- Implement document chunking strategy (size & overlap)
- Set up vector database (faiss, chromadb, or pinecone)
- Integrate with LLM API (OpenAI, Anthropic, DeepSeek, etc.)
- Add evaluation metrics (retrieval precision, answer relevance)
- Optimize prompt template for RAG context injection
- Handle edge cases (empty results, long context truncation)
"""

# Placeholder implementation - expand based on requirements
def retrieve(query: str, k: int = 3) -> list[str]:
    """
    Retrieve top-k relevant documents based on query.

    Args:
        query: User's question or search query
        k: Number of documents to retrieve

    Returns:
        List of retrieved document chunks

    TODO: Implement vector similarity search
    """
    pass


def augment_context(query: str, retrieved_docs: list[str]) -> str:
    """
    Prepare augmented context by combining query and retrieved documents.

    Args:
        query: Original user query
        retrieved_docs: Documents retrieved from knowledge base

    Returns:
        Formatted context string for LLM

    TODO: Design optimal context ordering and formatting
    """
    pass


def generate(context: str, query: str) -> str:
    """
    Generate answer using LLM with augmented context.

    Args:
        context: Retrieved and formatted context
        query: User's question

    Returns:
        Generated answer from LLM

    TODO: Integrate with LLM API and optimize prompts
    """
    pass


def rag_pipeline(query: str) -> str:
    """
    Complete RAG pipeline: Retrieve -> Augment -> Generate.

    Args:
        query: User's question

    Returns:
        Generated answer augmented with retrieved context
    """
    retrieved = retrieve(query)
    context = augment_context(query, retrieved)
    answer = generate(context, query)
    return answer


if __name__ == "__main__":
    # Example usage
    sample_query = "How does transformer attention mechanism work?"
    # answer = rag_pipeline(sample_query)
    # print(answer)
    print("RAG pipeline stub - implementation pending")
