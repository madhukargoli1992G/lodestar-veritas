from lodestar_veritas.config import get_config


def test_get_config():
    config = get_config()

    assert config.app_name == "Lodestar Veritas"
    assert config.embedding_dimensions == 384
    assert config.retrieval_mode == "hybrid"