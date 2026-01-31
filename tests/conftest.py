import sys
import os
import pytest

# 🔥 garante que a raiz do projeto está no PYTHONPATH
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

from app import app as flask_app


@pytest.fixture
def app():
    flask_app.config["TESTING"] = True
    flask_app.config["JWT_SECRET_KEY"] = "test-secret"
    return flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def mock_render_template(monkeypatch):
    monkeypatch.setattr(
        "flask.render_template",
        lambda *args, **kwargs: ""
    )
