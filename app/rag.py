import chromadb
import os

def setup_rag():
    # 1. Initialize a local ChromaDB client in memory
    chroma_client = chromadb.Client()

    # 2. Create a collection (similar to a table in SQL)
    collection = chroma_client.create_collection(name="aws_runbooks")

    # 3. Read your markdown runbook
    base_dir = os.path.dirname(os.path.dirname(__file__))
    runbook_path = os.path.join(base_dir, "sample-data", "runbook_cost_spike.md")

    with open(runbook_path, "r") as f:
        runbook_text = f.read()

    # 4. Add the text to the database. 
    # ChromaDB will automatically download a small AI model to create embeddings!
    collection.add(
        documents=[runbook_text],
        metadatas=[{"source": "runbook_cost_spike.md", "topic": "cost optimization"}],
        ids=["doc_1"]
    )

    return collection

def query_rag(collection, question):
    # Search the vector database for the most relevant context
    results = collection.query(
        query_texts=[question],
        n_results=1
    )

    # Return the found text, or a default message if nothing is found
    if results['documents'] and results['documents'][0]:
        return results['documents'][0][0]
    return "No relevant runbook found."