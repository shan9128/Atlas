import pytest

from atlas.vector_utils import (
    dot_product,
    magnitude,
    cosine_similarity
)


def test_dot_product():
    assert dot_product([1, 2], [3, 4]) == 11


def test_magnitude():
    assert magnitude([3, 4]) == 5


def test_identical_vectors():
    assert cosine_similarity(
        [1, 2], [1, 2]
    ) == pytest.approx(1.0)


def test_orthogonal_vectors():
    assert cosine_similarity(
        [1, 0], [0, 1]
    ) == pytest.approx(0.0)


def test_opposite_vectors():
    assert cosine_similarity(
        [1, 0], [-1, 0]
    ) == pytest.approx(-1.0)


def test_unequal_dimensions():
    with pytest.raises(ValueError):
        cosine_similarity([1, 2], [1])


def test_zero_vector():
    with pytest.raises(ValueError):
        cosine_similarity([0, 0], [1, 2])


def test_empty_vectors():
    with pytest.raises(ValueError):
        cosine_similarity([], [])
