import chromadb


if __name__ == '__main__':
    
    client = chromadb.HttpClient(host="chromadb",
                                 port=8000)
    
    collection = client.get_collection(name="games")
    collection.query(
        query_texts=["apple"]
    )