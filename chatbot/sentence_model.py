import numpy as np
# module selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from sentence_transformers import SentenceTransformer, util

UNNECESSARY_WORDS = [
    "restaurants",
    "restaurant",
    "stores",
    "store",
    "shops"
    "shop",
    "please",
    "give",
    "me",
    "i",
    "want",
    "some",
    "can",
    "you",
    "just",
    "for",
    "but",
    "type",
    "best",
    "good",
]

model = SentenceTransformer(
    "sentence-transformers/distiluse-base-multilingual-cased-v2"
)
def calculate_similarity_score(question, corpus):
    lst_question = question.lower().split()
    for word in UNNECESSARY_WORDS:
        if word in lst_question:
            lst_question.remove(word)

    cleaned_question = " ".join(lst_question)

    question_vec = model.encode(
        cleaned_question, convert_to_tensor=True, normalize_embeddings=True
    )
    corpus_vec = model.encode(corpus, convert_to_tensor=True, normalize_embeddings=True)

    cosine_scores = util.cos_sim(question_vec, corpus_vec)
    entity_vector = np.array(cosine_scores)

    score = np.max(entity_vector)
    if score >= 0.6:
        match_entity = corpus[np.argmax(entity_vector)]
        return match_entity, score
    return None, score
