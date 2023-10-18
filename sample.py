import numpy as np
from sentence_transformers import SentenceTransformer, util


model = SentenceTransformer(
    "sentence-transformers/distiluse-base-multilingual-cased-v2"
)

LOW_PRICE_CORPUS = ["poor", "cheap", "low price"]
HIGH_PRICE_CORPUS = ["rich", "expensive", "high price"]
CORPUS = LOW_PRICE_CORPUS + HIGH_PRICE_CORPUS
INPUT = "high"

corpus_vec = model.encode(CORPUS, convert_to_tensor=True, normalize_embeddings=True)
input_vec = model.encode(INPUT, convert_to_tensor=True, normalize_embeddings=True)

print("\n========CORPUS========\n")
print("corpus = ", CORPUS)
print("corpus vector size = ", corpus_vec.size())
print(corpus_vec)
print("\n========INPUT========\n")
print("input = ", INPUT)
print("input vector size = ", input_vec.size())
print(input_vec,"\n")

cosine_scores = util.cos_sim(input_vec, corpus_vec)
print("cosine similarity scores:")
print(cosine_scores)

entity_vector = np.array(cosine_scores)
score = np.max(entity_vector)
predict = CORPUS[np.argmax(entity_vector)]
print(f"corpus:\t{CORPUS}")
print(f"input:\t'{INPUT}'")
print(f"\t--------")

predict = None
feature = None
if score >= 0.7:
    predict = CORPUS[np.argmax(entity_vector)]
    if predict in LOW_PRICE_CORPUS:
        feature = 'LOW_PRICE_CORPUS'
    elif predict in HIGH_PRICE_CORPUS:
        feature = 'HIGH_PRICE_CORPUS'
print(f"predict\t'{predict}'")
print(f"\t========")
print(f"feature\t{feature}")
print(f"\t========")


