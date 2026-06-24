from lodestar_veritas.utils.logger import get_logger


def test_get_logger_returns_logger():
    logger = get_logger("test_logger")

    assert logger.name == "test_logger"
    assert logger.handlers