import os
import pytest

from kandji import Kandji
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture
def client():
    return Kandji(
        api_url=os.getenv("API_URL"),
        api_token=os.getenv("API_TOKEN"),
    )


@pytest.fixture
def ade_token_id():
    return os.getenv("TEST_ADE_TOKEN_ID")


@pytest.fixture
def blueprint_id():
    return os.getenv("TEST_BLUEPRINT_ID")


@pytest.fixture
def device_id():
    return os.getenv("TEST_DEVICE_ID")


@pytest.fixture
def note_id():
    return os.getenv("TEST_NOTE_ID")
