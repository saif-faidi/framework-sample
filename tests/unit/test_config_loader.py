import pytest


from src.config_loader import ConfigLoader

@pytest.fixture
def config_loader():
    yield ConfigLoader()

def test_get_current_directory(config_loader):
    print(config_loader._get_current_directory())
    assert isinstance(config_loader._get_current_directory(), str)

