import copy
import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from app.models import RailKitResponse

MOCK_FILE = Path(__file__).parent.parent / "app" / "mock_railkit_live_train.json"

# Keys that are in the RailKit JSON on purpose but that we do not model.
IGNORED_PATHS = {".data._provider"}


@pytest.fixture
def payload():
    with open(MOCK_FILE, encoding="utf-8") as file:
        return json.load(file)


def missing_paths(original, parsed, path=""):
    """List the keys that are in the original JSON but are missing from the parsed model."""
    missing = []
    if isinstance(original, dict):
        for key, value in original.items():
            if key not in parsed:
                missing.append(f"{path}.{key}")
            else:
                missing += missing_paths(value, parsed[key], f"{path}.{key}")
    elif isinstance(original, list):
        for item, parsed_item in zip(original, parsed):
            missing += missing_paths(item, parsed_item, f"{path}[]")
    return missing


def test_mock_payload_is_valid(payload):
    response = RailKitResponse.model_validate(payload)
    assert response.data.trainInfo[0].number == "12626"


def test_missing_route_is_rejected(payload):
    broken = copy.deepcopy(payload)
    del broken["data"]["route"]
    with pytest.raises(ValidationError):
        RailKitResponse.model_validate(broken)


def test_wrong_type_is_rejected(payload):
    broken = copy.deepcopy(payload)
    broken["data"]["delayMinutes"] = "late"
    with pytest.raises(ValidationError):
        RailKitResponse.model_validate(broken)


def test_models_keep_every_field_of_the_mock(payload):
    parsed = RailKitResponse.model_validate(payload).model_dump()
    dropped = [
        path for path in missing_paths(payload, parsed) if path not in IGNORED_PATHS
    ]
    assert dropped == []
