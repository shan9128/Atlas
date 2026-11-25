import pytest
from unittest.mock import patch

from atlas.tools.semantic_retriever import (
    build_vector_index,
    semantic_search
)


def test_build_vector_index():
    with patch(
        "atlas.tools.semantic_retriever.generate_embedding",
        return_value=[1, 0]
    ):
        index = build_vector_index()

    assert len(index) == 4
    assert "policy" in index[0]
    assert "embedding" in index[0]


@pytest.fixture
def sample_index():
    return [
        {"policy": "CL-201", "embedding": [0, 1]},
        {"policy": "PA-101", "embedding": [1, 0]},
        {"policy": "EL-301", "embedding": [1, 1]}
    ]


def test_semantic_ranking(sample_index):
    with patch(
        "atlas.tools.semantic_retriever.generate_embedding",
        return_value=[1, 0]
    ):
        results = semantic_search(
            "MRI approval", sample_index, top_k=3
        )

    assert results[0]["policy"] == "PA-101"
    assert results[1]["policy"] == "EL-301"
    assert results[2]["policy"] == "CL-201"


@pytest.mark.parametrize("top_k, expected_count", [
    (1, 1),
    (2, 2),
    (3, 3),
    (10, 3)
])
def test_top_k(sample_index, top_k, expected_count):
    with patch(
        "atlas.tools.semantic_retriever.generate_embedding",
        return_value=[1, 0]
    ):
        results = semantic_search(
            "MRI approval", sample_index, top_k=top_k
        )

    assert len(results) == expected_count


@pytest.mark.parametrize("top_k", [0, -1])
def test_invalid_top_k(sample_index, top_k):
    with pytest.raises(ValueError):
        semantic_search(
            "MRI approval", sample_index, top_k=top_k
        )
