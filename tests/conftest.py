import sys
import os
import pytest
from unittest.mock import Mock, patch, MagicMock
from flask_jwt_extended import create_access_token

# 🔥 garante que a raiz do projeto está no PYTHONPATH
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

from app import app as flask_app


@pytest.fixture
def app():
    """Aplicação Flask configurada para testes"""
    flask_app.config["TESTING"] = True
    flask_app.config["JWT_SECRET_KEY"] = "test-secret"
    flask_app.config["JWT_TOKEN_LOCATION"] = ["cookies", "headers"]
    flask_app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    return flask_app


@pytest.fixture
def client(app):
    """Cliente de teste Flask"""
    return app.test_client()


@pytest.fixture
def client_autenticado(app):
    """Cliente com token JWT válido nos headers"""
    client = app.test_client()
    
    with app.app_context():
        token = create_access_token(
            identity="user-test-id",
            additional_claims={
                "role": "user",
                "nome": "Usuário Teste",
                "email": "teste@nexus.com",
                "status": "ativo"
            }
        )
    
    # Injeta o token no header
    client.environ_base['HTTP_AUTHORIZATION'] = f'Bearer {token}'
    return client


@pytest.fixture
def client_admin(app):
    """Cliente com token JWT de admin nos headers"""
    client = app.test_client()
    
    with app.app_context():
        token = create_access_token(
            identity="admin-test-id",
            additional_claims={
                "role": "admin",
                "nome": "Admin Teste",
                "email": "admin@nexus.com",
                "status": "ativo"
            }
        )
    
    client.environ_base['HTTP_AUTHORIZATION'] = f'Bearer {token}'
    return client


@pytest.fixture(autouse=True)
def mock_render_template(monkeypatch):
    """Mock automático do render_template para evitar erros de template"""
    monkeypatch.setattr(
        "flask.render_template",
        lambda *args, **kwargs: ""
    )


@pytest.fixture
def mock_jwt_user():
    """Mock para get_jwt retornando usuário comum"""
    with patch('flask_jwt_extended.get_jwt') as mock:
        mock.return_value = {
            'role': 'user',
            'nome': 'Usuário Teste',
            'email': 'teste@nexus.com',
            'status': 'ativo'
        }
        yield mock


@pytest.fixture
def mock_jwt_admin():
    """Mock para get_jwt retornando admin"""
    with patch('flask_jwt_extended.get_jwt') as mock:
        mock.return_value = {
            'role': 'admin',
            'nome': 'Admin Teste',
            'email': 'admin@nexus.com',
            'status': 'ativo'
        }
        yield mock


@pytest.fixture
def mock_jwt_identity():
    """Mock para get_jwt_identity"""
    with patch('flask_jwt_extended.get_jwt_identity') as mock:
        mock.return_value = 'user-test-id'
        yield mock


# ===== FIXTURES DE DADOS MOCK =====

@pytest.fixture
def mock_usuario():
    """Dados de usuário para testes"""
    return {
        'id': 'user-test-id',
        'name': 'Teste Silva',
        'email': 'teste@nexus.com',
        'cpf': '12345678901',
        'role': 'user',
        'status': 'ativo',
        'senha': '$2b$12$hashedpassword',
        'image': '/static/imgs/test.jpg'
    }


@pytest.fixture
def mock_ambiente():
    """Dados de ambiente para testes"""
    return {
        'id': 1,
        'name': 'Sala de Testes',
        'type': 'sala',
        'capacidade': 20,
        'status': 'Disponivel',
        'descricao': 'Sala para testes',
        'localizacao': '1º andar',
        'area': '30m²',
        'image': '/static/imgs/sala.jpg',
        'recursos': ['TV', 'Projetor']
    }


@pytest.fixture
def mock_equipamento():
    """Dados de equipamento para testes"""
    return {
        'id': 1,
        'name': 'Projetor Teste',
        'categoria': 'Audiovisual',
        'status': 'Disponivel',
        'descricao': 'Projetor para testes',
        'marca': 'Sony',
        'modelo': 'VPL-TEST',
        'condicao': 'Novo',
        'quantidade_disponivel': 5,
        'image': '/static/imgs/projetor.jpg',
        'especificacoes': ['Full HD', 'HDMI']
    }


@pytest.fixture
def mock_evento():
    """Dados de evento para testes"""
    return {
        'id': 1,
        'titulo': 'Workshop de Testes',
        'data_evento': '2024-12-20',
        'hora_evento': '14:00',
        'localizacao': 'Sala de Testes',
        'descricao': 'Workshop sobre testes',
        'participantes': 10,
        'capacidade': 30,
        'instrutor': 'João Silva',
        'tipo': 'workshop',
        'ambiente_id': 1,
        'image': '/static/imgs/workshop.jpg',
        'inscrito': False
    }


@pytest.fixture
def mock_agendamento():
    """Dados de agendamento para testes"""
    return {
        'id': 1,
        'ambiente_id': 1,
        'user_id': 'user-test-id',
        'data': '2024-12-20',
        'hora_inicio': '14:00',
        'hora_fim': '16:00',
        'finalidade': 'Reunião de testes',
        'status': 'pendente'
    }


# ===== HELPERS =====

def gerar_token(app, role="user", user_id="test-user-id"):
    """Helper para gerar tokens JWT"""
    with app.app_context():
        return create_access_token(
            identity=user_id,
            additional_claims={
                "role": role,
                "nome": "Teste",
                "email": "teste@nexus.com",
                "status": "ativo"
            }
        )