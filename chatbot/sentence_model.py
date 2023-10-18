import numpy as np
# module selenium
from sentence_transformers import SentenceTransformer, util


from .dataset import UNNECESSARY_WORDS

model = SentenceTransformer(
    "sentence-transformers/distiluse-base-multilingual-cased-v2"
)
def calculate_similarity_score(question, corpus):
    lst_question = question.lower().split()
    for word in UNNECESSARY_WORDS:
        if word in lst_question:
            lst_question.remove(word)
    cleaned_question = " ".join(lst_question)

    question_vec = model.encode(cleaned_question, convert_to_tensor=True, normalize_embeddings=True)
    corpus_vec = model.encode(corpus, convert_to_tensor=True, normalize_embeddings=True)

    cosine_scores = util.cos_sim(question_vec, corpus_vec)
    entity_vector = np.array(cosine_scores)

    score = np.max(entity_vector)
    if score >= 0.7:
        predict = corpus[np.argmax(entity_vector)]
        return predict, score
    return None, score

