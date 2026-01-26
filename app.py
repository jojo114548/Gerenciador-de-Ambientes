
from flask import Flask,request,redirect,url_for,jsonify
from flask_jwt_extended import JWTManager
from controller.usuario_controller import usuario_bp
from controller.pendente_controller import pendente_bp
from controller.notificacao_controller import notificacao_bp
from controller.historico_controller import historico_bp
from controller.evento_controller import eventos_bp
from controller.equipamento_controller import equipamento_bp
from controller.ambiente_controller import ambientes_bp
from controller.agendamento_controller import agendamento_bp
from controller.admin_controller import painelAdm_bp
from controller.login_controller import login_bp
from controller.config_controller import config_bp


app = Flask(__name__)

app.secret_key = "sua_chave_super_secreta"

# JWT via cookie 
app.config["JWT_SECRET_KEY"] = "sua_chave_jwt"
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_ACCESS_COOKIE_PATH"] = "/"
app.config["JWT_COOKIE_SECURE"] = False  # True em produção (HTTPS)
app.config["JWT_COOKIE_CSRF_PROTECT"] = False  # pode ativar em produção
jwt = JWTManager(app)


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({"msg": "Token expirado"}), 401

    return redirect(url_for("login.home"))


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return redirect(url_for("login.home"))


@jwt.unauthorized_loader
def missing_token_callback(error):
    return redirect(url_for("login.home"))

app.register_blueprint(login_bp)
app.register_blueprint(usuario_bp)
app.register_blueprint(pendente_bp)
app.register_blueprint(notificacao_bp)
app.register_blueprint(historico_bp)
app.register_blueprint(eventos_bp)
app.register_blueprint(equipamento_bp)
app.register_blueprint(ambientes_bp)
app.register_blueprint(agendamento_bp)
app.register_blueprint(painelAdm_bp)
app.register_blueprint(config_bp)



if __name__ == '__main__':
    app.run(debug=True)
