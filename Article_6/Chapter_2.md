---

# 🔹 2. Retriever Basics + Chunking

### Why Retrieval Matters

In RAG, the **retriever** is the component that searches your knowledge base. Instead of the LLM “guessing,” the retriever finds the most relevant chunks of text/documents.

Think of it as the **search engine for your agent**. The better the retriever, the smarter the answers.

---

### Chunking: Why Not Store Whole Documents?

If you feed an entire 50-page PDF into your retriever, every query will return *too much* irrelevant text.
That’s why we **chunk** documents into smaller, semantically meaningful pieces (like 300–800 tokens).

* ✅ Fine-grained retrieval (only fetch what’s needed).
* ✅ Less wasted context → cheaper + faster.
* ✅ Better accuracy.

---

### Types of Retrievers (LangChain)

* **VectorStoreRetriever** → most common; uses embeddings + similarity search.
* **BM25Retriever** → traditional keyword-based search.
* **Hybrid** → combines vector + keyword for better coverage.

Most production RAG setups use **vector retrievers** with FAISS, Chroma, Pinecone, or Weaviate.

---

### Tiny Example: Chunking & Storing Docs

Here’s a simple walk-through in Python with LangChain + Chroma (local vector DB):

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# 1. Example raw document
docs = ["ACME Employee Handbook: Employees are entitled to 18 vacation days per year."]

# 2. Split into smaller chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
chunks = splitter.create_documents(docs)

# 3. Convert chunks into embeddings & store in Chroma
embeddings = OpenAIEmbeddings()   # uses OpenAI for simplicity
db = Chroma.from_documents(chunks, embedding=embeddings)

# 4. Create retriever
retriever = db.as_retriever()

# 5. Ask a question
query = "How many vacation days do ACME employees get?"
results = retriever.get_relevant_documents(query)

print(results[0].page_content)
```

👉 Output:

```
"Employees are entitled to 18 vacation days per year."
```

This shows how the retriever pinpoints only the **relevant chunk** instead of dumping an entire handbook.

---

### Visualization Analogy

```
Big Document (50 pages)
   ↓  (chunking)
[ Chunk 1 ][ Chunk 2 ][ Chunk 3 ] … [ Chunk N ]
   ↓  (embed + store in vector DB)
Retriever → finds only Chunk 14 + Chunk 32
   ↓
Passes them into LLM for grounded answer
```

---

### Transition to Next Chapter

So now we know **how retrievers work and why chunking is crucial**.
👉 Next, we’ll explore how these chunks and retrievers connect with the **generator (LLM)** to form the classic **RAG pipeline**.

---