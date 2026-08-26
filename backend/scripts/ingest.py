#!/usr/bin/env python3
"""
BIS Mitra — Document Ingestion Script

Extracts text from BIS standard PDFs, chunks them, generates embeddings,
and stores everything in ChromaDB for the RAG pipeline.

Usage:
    python -m scripts.ingest                    # Ingest all PDFs in data/standards/
    python -m scripts.ingest --file path/to.pdf  # Ingest a specific PDF
    python -m scripts.ingest --reset             # Reset ChromaDB and re-ingest
"""

from __future__ import annotations

import sys
import os
import re
import argparse
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pdfplumber
from sentence_transformers import SentenceTransformer

# ── Configuration ─────────────────────────────────────────────────────────────

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
STANDARDS_DIR = DATA_DIR / "standards"
SCHEMES_DIR = DATA_DIR / "schemes"
CHROMA_DIR = Path(__file__).resolve().parent.parent / "chroma_db"
COLLECTION_NAME = "bis_standards"

CHUNK_SIZE = 600       # approximate tokens (chars / 4)
CHUNK_OVERLAP = 100    # overlap in tokens
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


# ── PDF Text Extraction ───────────────────────────────────────────────────────

def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extract all text from a PDF file using pdfplumber."""
    text_parts = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
    except Exception as e:
        print(f"  ⚠️ Error extracting {pdf_path.name}: {e}")
        return ""
    return "\n\n".join(text_parts)


def extract_clause_numbers(text: str) -> list[tuple[str, str]]:
    """Extract clause/section numbers from BIS standard text.
    Returns list of (clause_number, clause_text) tuples."""
    # BIS standards typically have clauses like 4.2.1, 5.3, etc.
    clause_pattern = re.compile(r'(?m)^(\d+(?:\.\d+)*)\s+(.{20,})')
    matches = clause_pattern.findall(text)
    return [(m[0], m[1]) for m in matches]


# ── Chunking ──────────────────────────────────────────────────────────────────

def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split text into overlapping chunks. chunk_size and overlap are in approximate tokens."""
    # Convert to character counts (rough: 1 token ≈ 4 chars)
    char_size = chunk_size * 4
    char_overlap = overlap * 4

    if len(text) <= char_size:
        return [text.strip()] if text.strip() else []

    chunks = []
    start = 0
    while start < len(text):
        end = start + char_size

        # Try to break at a paragraph or sentence boundary
        if end < len(text):
            # Look for a good break point
            for break_char in ["\n\n", "\n", ". ", " "]:
                last_break = text.rfind(break_char, start + char_size // 2, end + char_size // 4)
                if last_break > start:
                    end = last_break + len(break_char)
                    break

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        start = end - char_overlap

    return chunks


def chunk_with_clause_tracking(text: str, source_name: str) -> list[dict]:
    """Chunk text and track which clause each chunk belongs to."""
    # Try to split by major sections first
    section_splits = re.split(r'(?m)^(\d+(?:\.\d+)*)\s+', text)

    chunks_with_meta = []

    if len(section_splits) > 3:
        # We successfully split by sections
        current_clause = ""
        for i in range(1, len(section_splits), 2):
            clause_num = section_splits[i] if i < len(section_splits) else ""
            clause_text = section_splits[i + 1] if i + 1 < len(section_splits) else ""
            current_clause = clause_num

            # Chunk the clause text
            sub_chunks = chunk_text(clause_text)
            for chunk in sub_chunks:
                chunks_with_meta.append({
                    "text": chunk,
                    "clause": f"Clause {current_clause}" if current_clause else "",
                })
    else:
        # Fallback: just chunk the whole text
        sub_chunks = chunk_text(text)
        for chunk in sub_chunks:
            # Try to find the nearest clause number in the chunk
            clause_match = re.search(r'(\d+(?:\.\d+)*)', chunk[:100])
            clause = f"Clause {clause_match.group(1)}" if clause_match else ""
            chunks_with_meta.append({
                "text": chunk,
                "clause": clause,
            })

    return chunks_with_meta


# ── Ingestion Pipeline ────────────────────────────────────────────────────────

def ingest_pdf(pdf_path: Path, collection, embedder) -> int:
    """Ingest a single PDF into ChromaDB. Returns number of chunks added."""
    source_name = pdf_path.stem  # e.g. "IS_302_Part_1"

    print(f"  📄 Extracting text from: {pdf_path.name}")
    text = extract_text_from_pdf(pdf_path)
    if not text.strip():
        print(f"  ⚠️ No text extracted from {pdf_path.name}")
        return 0

    print(f"  ✂️  Chunking ({len(text)} chars)...")
    chunks = chunk_with_clause_tracking(text, source_name)

    if not chunks:
        print(f"  ⚠️ No chunks generated from {pdf_path.name}")
        return 0

    # Generate embeddings
    print(f"  🧮 Generating embeddings for {len(chunks)} chunks...")
    texts = [c["text"] for c in chunks]
    embeddings = embedder.encode(texts, show_progress_bar=False).tolist()

    # Prepare ChromaDB data
    ids = [f"{source_name}_chunk_{i}" for i in range(len(chunks))]
    metadatas = [
        {
            "source": source_name,
            "clause": c["clause"],
            "file": pdf_path.name,
            "chunk_index": i,
        }
        for i, c in enumerate(chunks)
    ]

    # Upsert into ChromaDB
    collection.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(f"  ✅ Ingested {len(chunks)} chunks from {pdf_path.name}")
    return len(chunks)


def run_ingestion(reset: bool = False, single_file: str | None = None):
    """Run the full ingestion pipeline."""
    import chromadb

    print("=" * 60)
    print("🚀 BIS Mitra — Document Ingestion Pipeline")
    print("=" * 60)

    # Initialize ChromaDB
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    if reset:
        print("🗑️  Resetting ChromaDB collection...")
        try:
            client.delete_collection(COLLECTION_NAME)
        except Exception:
            pass

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    # Load embedding model
    print(f"🧠 Loading embedding model: {EMBEDDING_MODEL}")
    embedder = SentenceTransformer(EMBEDDING_MODEL)

    # Collect PDFs
    pdf_files = []
    if single_file:
        pdf_path = Path(single_file)
        if pdf_path.exists():
            pdf_files = [pdf_path]
        else:
            print(f"❌ File not found: {single_file}")
            return
    else:
        # Ingest from both standards and schemes directories
        for pdf_dir in [STANDARDS_DIR, SCHEMES_DIR]:
            if pdf_dir.exists():
                pdf_files.extend(sorted(pdf_dir.glob("*.pdf")))

        # Also check for user-created sample PDFs
        if not pdf_files:
            print(f"\n📁 No PDFs found in {STANDARDS_DIR} or {SCHEMES_DIR}")
            print("   Place BIS standard PDFs in: data/standards/")
            print("   Place scheme documents in:  data/schemes/")
            print("   Then run this script again.")
            print("\n   For now, ingesting sample/placeholder data...\n")

    # Ingest PDFs
    total_chunks = 0
    for pdf_path in pdf_files:
        total_chunks += ingest_pdf(pdf_path, collection, embedder)

    # Print summary
    print("\n" + "=" * 60)
    print(f"✅ Ingestion complete!")
    print(f"   PDFs processed: {len(pdf_files)}")
    print(f"   Total chunks:   {total_chunks}")
    print(f"   Collection:     {COLLECTION_NAME}")
    print(f"   ChromaDB dir:   {CHROMA_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest BIS documents into ChromaDB")
    parser.add_argument("--file", type=str, help="Ingest a single PDF file")
    parser.add_argument("--reset", action="store_true", help="Reset ChromaDB before ingesting")
    args = parser.parse_args()

    run_ingestion(reset=args.reset, single_file=args.file)
