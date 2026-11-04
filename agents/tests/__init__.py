"""Agents service tests."""

import pytest

from app.core.config import Settings

Settings.model_config["env_file"] = None

pytest.register_assert_rewrite("tests.helpers.agent_api")
