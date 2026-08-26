"""Core RAG pipeline — retrieve relevant chunks, generate cited answer."""

from __future__ import annotations

from app.config import get_settings
from app.services.embeddings import embed_query
from app.services.llm import llm_complete
from app.models.schemas import Source

RAG_SYSTEM_PROMPT = """You are BIS Mitra — an AI-powered assistant for Indian Standards and BIS (Bureau of Indian Standards) services.

STRICT RULES:
1. Answer ONLY using the context provided below.
2. If the context does not contain enough information, say: "I don't have enough information in my knowledge base to answer this accurately. Please refer to bis.gov.in for official details."
3. Always cite the source document and clause/section number where you found the answer.
4. Format citations as: [Source: <document>, <clause>]
5. Be precise, technical, and helpful. Write in clear, simple language.
6. If asked about certification processes, provide step-by-step guidance.
7. Never make up IS numbers or clause references — only use what appears in the context."""

def _get_chroma_collection():
    """Get or create the ChromaDB collection."""
    import chromadb
    settings = get_settings()
    client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)
    return client.get_or_create_collection(
        name=settings.CHROMA_COLLECTION,
        metadata={"hnsw:space": "cosine"},
    )


def retrieve_chunks(query: str, top_k: int | None = None) -> list[dict]:
    """Retrieve the most relevant chunks from ChromaDB for the given query."""
    settings = get_settings()
    k = top_k or settings.RAG_TOP_K
    collection = _get_chroma_collection()
    query_embedding = embed_query(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )

    chunks = []
    if results and results["documents"] and results["documents"][0]:
        for i, doc in enumerate(results["documents"][0]):
            metadata = results["metadatas"][0][i] if results["metadatas"] else {}
            distance = results["distances"][0][i] if results["distances"] else 1.0
            chunks.append({
                "text": doc,
                "metadata": metadata,
                "distance": distance,
            })
    return chunks


def build_rag_prompt(query: str, chunks: list[dict]) -> tuple[str, str]:
    """Build the system prompt and user prompt for the LLM from retrieved chunks."""
    context_parts = []
    sources = []
    for i, chunk in enumerate(chunks):
        meta = chunk["metadata"]
        doc_name = meta.get("source", "Unknown document")
        clause = meta.get("clause", "")
        header = f"[Chunk {i+1} — Source: {doc_name}" + (f", {clause}" if clause else "") + "]"
        context_parts.append(f"{header}\n{chunk['text']}")
        sources.append(Source(document=doc_name, clause=clause, excerpt=chunk["text"][:200]))

    context = "\n\n---\n\n".join(context_parts)
    user_prompt = f"""Context from BIS documents:
{context}

---

User Question: {query}

Answer the question using ONLY the context above. Cite sources."""

    return RAG_SYSTEM_PROMPT, user_prompt


def rag_query(query: str, top_k: int | None = None) -> tuple[str, list[Source]]:
    """Full RAG pipeline: retrieve → build prompt → LLM → (answer, sources)."""
    chunks = retrieve_chunks(query, top_k)

    if not chunks:
        return (
            "I don't have any relevant documents indexed for this query yet. "
            "Please check bis.gov.in for official information, or try rephrasing your question.",
            [],
        )

    system_prompt, user_prompt = build_rag_prompt(query, chunks)
    answer = llm_complete(system_prompt, user_prompt)

    # Extract unique sources
    seen = set()
    unique_sources = []
    for src in Source(
        document=chunks[0]["metadata"].get("source", ""),
        clause=chunks[0]["metadata"].get("clause", ""),
        excerpt=chunks[0]["text"][:200],
    ).__class__.__fields__:
        pass  # we build from the chunks directly

    for chunk in chunks:
        meta = chunk["metadata"]
        key = (meta.get("source", ""), meta.get("clause", ""))
        if key not in seen:
            seen.add(key)
            unique_sources.append(
                Source(
                    document=meta.get("source", "Unknown"),
                    clause=meta.get("clause", ""),
                    excerpt=chunk["text"][:200],
                )
            )

    return answer, unique_sources
