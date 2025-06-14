import os
import tempfile
import shutil
from pathlib import Path
from typing import Generator, Dict, Any
import pytest


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for testing."""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def mock_config() -> Dict[str, Any]:
    """Provide a mock configuration dictionary."""
    return {
        "api_key": "test_api_key",
        "base_url": "https://api.example.com",
        "timeout": 30,
        "retries": 3,
        "debug": True,
    }


@pytest.fixture
def sample_repos() -> list:
    """Provide a list of sample repository URLs for testing."""
    return [
        "https://github.com/user/repo1.git",
        "https://github.com/user/repo2.git",
        "https://github.com/user/repo3.git",
    ]


@pytest.fixture
def mock_env_vars(monkeypatch) -> Dict[str, str]:
    """Set up mock environment variables for testing."""
    env_vars = {
        "TEST_API_KEY": "mock_api_key",
        "TEST_ENV": "testing",
        "TEST_DEBUG": "true",
    }
    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)
    return env_vars


@pytest.fixture
def test_file_content() -> str:
    """Provide sample file content for testing."""
    return """# Sample Test File
This is a sample file content for testing purposes.
It contains multiple lines and various characters.

- Item 1
- Item 2
- Item 3

End of file.
"""


@pytest.fixture
def create_test_file(temp_dir: Path) -> Generator[Path, None, None]:
    """Create a test file in the temporary directory."""
    def _create_file(filename: str, content: str = "") -> Path:
        file_path = temp_dir / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
        return file_path
    
    yield _create_file


@pytest.fixture(autouse=True)
def change_test_dir(request, monkeypatch):
    """Automatically change to test directory for each test."""
    monkeypatch.chdir(request.fspath.dirname)


@pytest.fixture
def mock_subprocess(mocker):
    """Mock subprocess calls for testing."""
    mock = mocker.patch("subprocess.run")
    mock.return_value.returncode = 0
    mock.return_value.stdout = "Success"
    mock.return_value.stderr = ""
    return mock


@pytest.fixture
def captured_logs(caplog):
    """Capture and provide access to log messages during tests."""
    with caplog.at_level("DEBUG"):
        yield caplog


@pytest.fixture
def mock_requests(mocker):
    """Mock requests library for API testing."""
    mock = mocker.patch("requests.get")
    mock.return_value.status_code = 200
    mock.return_value.json.return_value = {"status": "success"}
    return mock