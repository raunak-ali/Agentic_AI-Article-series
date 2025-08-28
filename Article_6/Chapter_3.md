---

# 🔹 3. Document Ingestion & Chunking

If Article 5 was about “memory,” then this chapter is about **feeding your agents reliable knowledge**. In RAG (Retrieval-Augmented Generation), your LLM is only as good as the data pipeline behind it. That pipeline starts with **document ingestion and chunking**.

---

## 🏗️ The Ingestion Pipeline

Here’s the high-level flow every RAG project follows:

```
[Raw Documents]  
      │
      ▼
[Preprocessing] → clean text, normalize, remove PII  
      │
      ▼
[Chunking] → split into 500–1,200 tokens w/ overlap  
      │
      ▼
[Attach Metadata] → {source, page, timestamp}  
      │
      ▼
[Vector Database] (FAISS, Chroma, Pinecone)  
      │
      ▼
[Retriever] → feeds context into LLM  
```

---

## 🧹 Step 1. Preprocessing

Before splitting, make the text **clean and uniform**.

* Remove headers/footers that repeat on every page.
* Normalize whitespace, Unicode symbols, weird line breaks.
* Strip sensitive data (PII) if your use case demands compliance.

**Tools:**

* `pdfplumber`, `pymupdf`, or `pypdf` → for PDFs.
* `python-docx` → for Word files.
* `BeautifulSoup4` → for HTML.
* Custom scrapers → for websites or databases.

---

## ✂️ Step 2. Chunking

Chunking = splitting text into **bite-sized pieces** the LLM can handle.

* **Size:** 500–1,200 tokens is the sweet spot.

  * Too small = no context.
  * Too large = wasted tokens + poor retrieval.
* **Overlap:** add 50–200 tokens of overlap between chunks.

  * Prevents “cut-off” mid-thought.
* **Boundaries:** split at natural paragraph/sentence breaks.

**Pseudo Code:**

```python
chunks = chunk_document(text, chunk_size=800, overlap=150)
for i, ch in enumerate(chunks):
    upsert_to_vector_db(
        id=f"{doc_id}_{i}", 
        text=ch, 
        metadata={"source": doc_name, "page": i}
    )
```

---

## ✅ Good vs ❌ Bad Chunking

| Aspect               | ❌ Bad Chunking Example                                | ✅ Good Chunking Example                                   |
| -------------------- | ----------------------------------------------------- | --------------------------------------------------------- |
| **Split Size**       | 50–100 tokens → too small, loses context              | 800 tokens → enough context for retrieval                 |
| **Overlap**          | 0 overlap → broken thoughts mid-paragraph             | 150 token overlap → smooth continuity                     |
| **Coherence**        | Splits mid-sentence (“Employees are entitled… / 18…”) | Splits at sentence or paragraph boundaries                |
| **Metadata**         | No metadata attached                                  | Metadata includes `{"source": "handbook.pdf", "page": 3}` |
| **Retrieval Output** | “18” → ambiguous, useless                             | “Employees are entitled to 18 vacation days per year”     |
| **Business Impact**  | Misleading answers, hallucinations                    | Clear, grounded answers users can trust                   |

👉 Think of it like cutting a book into flashcards:

* Bad chunking = random sentences, shuffled order.
* Good chunking = coherent paragraphs with page numbers.

---

## 🧾 Deliverable: Ingestion Checklist

When preparing docs for RAG:

1. ✅ Clean the text.
2. ✅ Choose chunk size (500–1,200 tokens).
3. ✅ Add overlaps (50–200).
4. ✅ Keep splits at natural boundaries.
5. ✅ Attach metadata (source, page, timestamp).
6. ✅ Store in a vector DB (FAISS, Pinecone, Chroma, Weaviate).

---

📖 Reference:

* [LangChain Document Loaders](https://python.langchain.com/docs/modules/data_connection/document_loaders/)
* [LangChain Text Splitters](https://python.langchain.com/docs/modules/data_connection/document_transformers/text_splitters/)

---
## 🔹 Real Code: Chunking in LangChain

LangChain comes with built-in text splitters. The most common is `RecursiveCharacterTextSplitter`, which tries to split at natural boundaries (paragraphs, then sentences, then words).

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Sample text (pretend this is extracted from a PDF or DOCX)
doc_text = """
Employees are entitled to 18 vacation days per year. 
Unused days cannot be carried over to the next year. 
Sick leave is separate and must be approved by HR. 
Benefits include healthcare coverage, retirement plan options, 
and wellness stipends provided quarterly.
"""

# ❌ BAD CHUNKING: tiny chunks, no overlap
bad_splitter = RecursiveCharacterTextSplitter(
    chunk_size=50,   # way too small
    chunk_overlap=0  # no overlap
)
bad_chunks = bad_splitter.split_text(doc_text)
print("❌ Bad Chunks:")
for ch in bad_chunks:
    print("-", ch)

# ✅ GOOD CHUNKING: balanced size, overlap included
good_splitter = RecursiveCharacterTextSplitter(
    chunk_size=120,   # larger, keeps context
    chunk_overlap=30  # overlap avoids cutting mid-thought
)
good_chunks = good_splitter.split_text(doc_text)
print("\n✅ Good Chunks:")
for ch in good_chunks:
    print("-", ch)
```

### 🔎 What You’ll See:

* **Bad chunks**: Random sentence fragments like *“Employees are entitled to 18…”*.
* **Good chunks**: Full, coherent segments like *“Employees are entitled to 18 vacation days per year. Unused days cannot be carried…”*.

---
👉 Next step would be **Chapter 4: Vector Databases**, where we show *where these chunks live* and *how retrievers pull them back*.

