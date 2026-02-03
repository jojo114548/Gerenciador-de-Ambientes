
# Importa a função para carregar variáveis de ambiente do arquivo .env
from dotenv import load_dotenv

# Carrega as variáveis de ambiente ANTES de qualquer outra importação

load_dotenv()  

from flask import Flask, request, redirect, url_for, jsonify

from flask_jwt_extended import JWTManager
from service.usuario_service import UsuarioService


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



# Configurações para autenticação baseada em JWT via cookies

# Chave secreta para assinar e validar tokens JWT

app.config["JWT_SECRET_KEY"] = "sua_chave_jwt"

# Define que o token será armazenado em COOKIES (não no header Authorization)
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]

# Define o caminho onde o cookie JWT é válido (raiz = toda aplicação)
app.config["JWT_ACCESS_COOKIE_PATH"] = "/"

# Define se o cookie só pode ser transmitido via HTTPS
# False em desenvolvimento (HTTP), True em produção (HTTPS)
app.config["JWT_COOKIE_SECURE"] = False  # True em produção (HTTPS)

# Proteção CSRF (Cross-Site Request Forgery)

app.config["JWT_COOKIE_CSRF_PROTECT"] = False  


jwt = JWTManager(app)



# Funções que definem o comportamento quando há problemas com o token JWT

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    """
    Callback executado quando o token JWT está EXPIRADO.
    
    """
    # Verifica se a requisição foi feita via AJAX (JavaScript)
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        # Retorna resposta JSON para requisições AJAX
        return jsonify({"msg": "Token expirado"}), 401

    # Para requisições normais, redireciona para a página de login
    return redirect(url_for("login.home"))

@jwt.invalid_token_loader
def invalid_token_callback(error):
    """
    Callback executado quando o token JWT é INVÁLIDO.

    """
    # Redireciona para a página de login
    return redirect(url_for("login.home"))


@jwt.unauthorized_loader
def missing_token_callback(error):
    """
    Callback executado quando o token JWT está AUSENTE.
 
    """
    # Redireciona para a página de login
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



# Variável global para controlar se o admin padrão já foi criado
# Evita que seja executado múltiplas vezes
admin_inicializado = False


@app.before_request
def init_app():
    """
    Função executada ANTES de CADA requisição HTTP.
 
    """
    global admin_inicializado  # Acessa a variável global
    
    # Executa apenas se ainda não foi inicializado
    if not admin_inicializado:
        # Chama o serviço para garantir que existe um admin padrão
        # (cria se não existir, ou apenas verifica se já existe)
        UsuarioService.garantir_admin_padrao()
        
        # Marca como inicializado para não executar novamente
        admin_inicializado = True


if __name__ == '__main__':
    """
    Inicia o servidor Flask.
    
    """
 
    app.run(host='0.0.0.0', debug=False)







