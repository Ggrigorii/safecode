import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="security_knowledge")

model = SentenceTransformer('all-MiniLM-L6-v2')

def load_docs_from_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        chunks = content.split('\n\n')
        return chunks

def setup_rag():
    docs = []
    for filename in ["owasp_top10.txt", "cwe_common_weaknesses.txt", "xss_guide.txt", "sql_injection_guide.txt"]:
        docs.extend(load_docs_from_file(f"data/{filename}"))

    embeddings = model.encode(docs).tolist()

    collection.add(
        embeddings=embeddings,
        documents=docs,
        ids=[f"doc_{i}" for i in range(len(docs))]
    )
    print("✅ База знаний загружена!")

def get_relevant_context(query):
    query_embedding = model.encode(query).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=3)
    return "\n\n".join(results['documents'][0]) if results['documents'] else ""