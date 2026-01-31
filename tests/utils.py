from flask_jwt_extended import create_access_token

def gerar_token(app):
    with app.app_context():
        return create_access_token(
            identity="user-test-id",
            additional_claims={
                "role": "admin",
                "nome": "Teste",
                "email": "teste@nexus.com",
                "status": "ativo"
            }
        )
