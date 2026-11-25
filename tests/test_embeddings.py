import pytest
from unittest.mock import patch
from atlas.embeddings import generate_embedding


def test_generate_document_embedding():
    with patch("atlas.embeddings.ollama.embed") as mock_embed:

        mock_embed.return_value = {
            "embeddings": [[0.1, 0.2, 0.3]]
        }

        result = generate_embedding("Healthcare policy")

        assert result == [0.1, 0.2, 0.3]

        mock_embed.assert_called_once_with(
            model="nomic-embed-text",
            input="search_document: Healthcare policy"
        )


def test_generate_query_embedding():
    with patch("atlas.embeddings.ollama.embed") as mock_embed:

        mock_embed.return_value = {
            "embeddings": [[0.4, 0.5, 0.6]]
        }

        result = generate_embedding(
            "Is MRI covered?",
            task="search_query"
        )

        assert result == [0.4, 0.5, 0.6]

        mock_embed.assert_called_once_with(
            model="nomic-embed-text",
            input="search_query: Is MRI covered?"
        )


def test_empty_text():
    with pytest.raises(ValueError):
        generate_embedding("")


def test_whitespace_text():
    with pytest.raises(ValueError):
        generate_embedding("   ")


def test_invalid_task():
    with pytest.raises(ValueError):
        generate_embedding(
            "Healthcare policy",
            task="invalid_task"
        )
