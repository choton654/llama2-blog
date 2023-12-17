import pymongo
import requests
import openai

# openai.api_key = "<your openai_api_key>"
# hf_token = "<your hf_token>"
embedding_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"

client = pymongo.MongoClient(
    "mongodb+srv://choton654:m3j4Y3lwUVx1HVF6@cluster0.prdkh.mongodb.net/?retryWrites=true&w=majority"
)

db = client.sample_mflix
collection = db.movies
# collection = db.embedded_movies


def generate_embedding(text: str) -> list[float]:
    # for hugging face api //////////

    response = requests.post(
        url=embedding_url,
        headers={"Authorization": f"Bearer {hf_token}"},
        json={"inputs": text},
    )

    if response.status_code != 200:
        raise ValueError(
            f"Request failed with status code {response.status_code} {response.text}"
        )

    return response.json()

    # for openai api //////////
    # response = openai.embeddings.create(model="text-embedding-ada-002", input=text)
    # # print('---openai res---',response.data[0].embedding)
    # return response.data[0].embedding


# comment out thisstep to add embedding to database////

# for doc in collection.find({"plot": {"$exists": True}}).skip(39).limit(60):
#     doc["plot_embedding_hf"] = generate_embedding(doc["plot"])
#     collection.replace_one({"_id": doc["_id"]}, doc)

# print(generate_embedding("freecodecamp is awesome"))


query = "imaginary characters from outer space at war"

result = collection.aggregate(
    [
        # for hugging face api //////////
        {
            "$vectorSearch": {
                "queryVector": generate_embedding(query),
                "path": "plot_embedding_hf",
                "numCandidates": 100,
                "limit": 4,
                "index": "PlotSemanticSearch2",
            }
        }
        # for openai api //////////
        # {
        #     "$vectorSearch": {
        #         "queryVector": generate_embedding(query),
        #         "path": "plot_embedding",
        #         "numCandidates": 100,
        #         "limit": 4,
        #         "index": "PlotSemanticSearch",
        #     }
        # }
    ]
)

for document in result:
    print(f'Movie name: {document["title"]},\nMovie plot: {document["plot"]} ')
