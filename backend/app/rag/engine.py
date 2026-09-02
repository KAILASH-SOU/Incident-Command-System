import os
import glob
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
import chromadb
from typing import List, Dict, Any

class HybridRAGEngine:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.documents = []
        self.tokenized_corpus = []
        self.bm25 = None
        
        # Load embedding model
        self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
        
        # Setup ChromaDB
        self.chroma_client = chromadb.Client()
        self.collection = self.chroma_client.get_or_create_collection(name="post_mortems")
        
        self._load_documents()
        
    def _load_documents(self):
        filepaths = glob.glob(f"{self.data_dir}/**/*.md", recursive=True)
        for i, filepath in enumerate(filepaths):
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                
                # Simple chunking by paragraphs for demonstration
                chunks = [chunk.strip() for chunk in content.split("\n\n") if chunk.strip()]
                
                for j, chunk in enumerate(chunks):
                    doc_id = f"doc_{i}_chunk_{j}"
                    self.documents.append({"id": doc_id, "content": chunk, "source": filepath})
                    
                    # For BM25
                    self.tokenized_corpus.append(chunk.lower().split())
                    
                    # For Vector DB
                    embedding = self.encoder.encode(chunk).tolist()
                    self.collection.add(
                        ids=[doc_id],
                        embeddings=[embedding],
                        documents=[chunk],
                        metadatas=[{"source": filepath}]
                    )
                    
        if self.tokenized_corpus:
            self.bm25 = BM25Okapi(self.tokenized_corpus)
            
    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        if not self.documents:
            return []
            
        # BM25 Search
        tokenized_query = query.lower().split()
        bm25_scores = self.bm25.get_scores(tokenized_query)
        bm25_ranking = sorted(range(len(bm25_scores)), key=lambda i: bm25_scores[i], reverse=True)[:top_k*2]
        
        # Vector Search
        query_embedding = self.encoder.encode(query).tolist()
        vector_results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k*2
        )
        
        # Safe fallback if chromadb returns empty or different format
        vector_ranking = []
        if vector_results and "ids" in vector_results and vector_results["ids"]:
            vector_ranking = vector_results["ids"][0]
        
        # Reciprocal Rank Fusion (RRF)
        rrf_scores = {}
        k = 60
        
        for rank, doc_idx in enumerate(bm25_ranking):
            doc_id = self.documents[doc_idx]["id"]
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0) + 1 / (k + rank + 1)
            
        for rank, doc_id in enumerate(vector_ranking):
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0) + 1 / (k + rank + 1)
            
        # Sort by RRF score
        sorted_doc_ids = sorted(rrf_scores.keys(), key=lambda x: rrf_scores[x], reverse=True)[:top_k]
        
        # Retrieve actual documents
        results = []
        for doc_id in sorted_doc_ids:
            doc = next((d for d in self.documents if d["id"] == doc_id), None)
            if doc:
                results.append(doc)
            
        return results

rag_engine = HybridRAGEngine()
