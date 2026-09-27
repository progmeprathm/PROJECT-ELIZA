import os
from ecos.memory.system import ECOSMemorySystem, RealEmbeddingProvider, DeterministicPseudoEmbedding

def run_semantic_retrieval_test():
    print("================================================================")
    print("  v0.4 SEMANTIC RETRIEVAL TEST")
    print("================================================================\n")
    
    # Force cloud provider if possible, else it will fallback
    os.environ["ELIZA_EMBEDDING_PROVIDER"] = "cloud"
    
    mem_sys = ECOSMemorySystem()
    
    provider = mem_sys.embedding_provider
    if isinstance(provider, RealEmbeddingProvider):
        if provider.fallback_used:
            print(f"[!] Using Deterministic Fallback. Reason: {provider.fallback_reason}")
        else:
            print("[+] Using Real Embedding Provider.")
    else:
        print("[!] Using Deterministic Pseudo Embedding.")
    
    # Store memory
    target_memory = "The access code written on the note is 8592."
    mem_sys.store("ep1", {"type": "episode", "observation": target_memory})
    
    # Add some distractors
    mem_sys.store("ep2", {"type": "episode", "observation": "The agent moved forward to location 2."})
    mem_sys.store("ep3", {"type": "episode", "observation": "The door is locked and requires a key."})
    
    queries = [
        "What credential did I discover earlier?",
        "security code",
        "passcode",
        "credential",
        "number from the note"
    ]
    
    successes = 0
    for q in queries:
        print(f"\nQuery: '{q}'")
        # Retrieve explicitly to see similarity
        query_vec = mem_sys.embedding_provider.embed(q)
        scored_mems = []
        for key, mem in mem_sys._store_dict.items():
            vec = mem_sys._vectors.get(key, [0.0]*128)
            sim = mem_sys._cosine_similarity(query_vec, vec)
            scored_mems.append((sim, mem.payload["observation"]))
        scored_mems.sort(key=lambda x: x[0], reverse=True)
        
        print(f"Top match: ({scored_mems[0][0]:.3f}) {scored_mems[0][1]}")
        if scored_mems[0][1] == target_memory:
            print("  -> [PASS] Retrieved the correct memory.")
            successes += 1
        else:
            print("  -> [FAIL]")
            
    print(f"\nScore: {successes}/{len(queries)}")

if __name__ == "__main__":
    run_semantic_retrieval_test()
