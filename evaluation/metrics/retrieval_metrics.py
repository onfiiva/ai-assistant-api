def precision_at_k(retrieved, relevant, k=5):
    """
    retrieved: list of retrieved chunks id/text
    relevant: list of relevant chunks
    """

    retrieved_k = retrieved[:k]

    hits = sum(1 for r in retrieved_k if r in relevant)

    return hits / k


def recall_at_k(retrieved, relevant, k=5):
    """
    how many relevant found
    """

    retrieved_k = retrieved[:k]

    hits = sum(1 for r in retrieved_k if r in relevant)

    if len(relevant) == 0:
        return 0

    return hits / len(relevant)


def reciprocal_rank(retrieved, relevant):
    """
    MRR for one req
    """

    for idx, r in enumerate(retrieved, 1):
        if r in relevant:
            return 1 / idx

    return 0
