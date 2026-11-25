import math


def dot_product(vector_a, vector_b):
    total = 0

    for a, b in zip(vector_a, vector_b):
        total += a * b

    return total


def magnitude(vector):
    total = 0

    for a in vector:
        total += a ** 2

    return math.sqrt(total)


def cosine_similarity(vector_a, vector_b):
    if len(vector_a) != len(vector_b):
        raise ValueError("Vectors must have equal dimensions")

    dp = dot_product(vector_a, vector_b)
    ma = magnitude(vector_a)
    mb = magnitude(vector_b)

    if ma == 0 or mb == 0:
        raise ValueError("Vector magnitude must be greater than zero")

    return dp / (ma * mb)
