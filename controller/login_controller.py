
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from service.usuario_service import UsuarioService
from flask_jwt_extended import (
    create_access_token, set_access_cookies, get_jwt_identity, jwt_required, unset_jwt_cookies, get_jwt
)
from datetime import timedelta
from repository.eventos_repository import EventosRepository
from service.ambientes_service import AmbientesService
from service.equipamento_service import EquipamentoService



# Cria um Blueprint chamado "login" para organizar as rotas relacionadas à autenticação
login_bp = Blueprint("login", __name__)



@login_bp.route("/")
def home():
    """
    Rota pública que exibe a página de login.
   
    """
    try:
        # Renderiza o template da página de login
        return render_template("login.html")
    
    except Exception as e:
        return jsonify({"erro": str(e)}), 500



@login_bp.route('/login', methods=["POST"])
def login_post():
    """
    Rota que processa o formulário de login.
   
    """
    # Captura os dados do formulário enviados via POST
    email = request.form.get("email")
    senha = request.form.get("senha")

    # Chama o serviço para autenticar o usuário (verifica email e senha)
    usuario = UsuarioService.autenticar(email, senha)

    # Se as credenciais forem inválidas, retorna erro 401
    if not usuario:
        return "Email ou senha inválidos", 401
    
    # Cria um token JWT (JSON Web Token) com informações do usuário

    access_token = create_access_token(
        identity=usuario["id"], 
        additional_claims={      
            "nome": usuario["name"],
            "email": usuario["email"],
            "role": usuario["role"],     
            "image": usuario["image"],   
            "status": usuario["status"]  
        },
        expires_delta=timedelta(hours=1)  # Token válido por 1 hora
    )

    # Cria uma resposta de redirecionamento para a página index
    response = redirect(url_for("login.index"))
    
    # Define o token JWT nos cookies HTTP (autenticação via cookies)
    set_access_cookies(response, access_token)
    
    return response


@login_bp.route('/index')
@jwt_required()  
def index():
    """
    Rota principal do sistema após login bem-sucedido.
   
    """
    try:
        # Obtém todas as informações do token JWT 
        logado = get_jwt()
        
        # Obtém apenas o ID do usuário logado 
        id_logado = get_jwt_identity()
        
        # Busca todos os dados necessários para a página principal
        ambientes = AmbientesService.listar()      # Lista todos os ambientes
        equipamentos = EquipamentoService.listar() # Lista todos os equipamentos
        usuarios = UsuarioService.listar()         # Lista todos os usuários
        evento = EventosRepository.listar()        # Lista todos os eventos

        # Para cada evento, verifica se o usuário logado já está inscrito
        for event in evento:
            event["inscrito"] = EventosRepository.usuario_ja_inscrito(
                event["id"],   
                id_logado      
            )

        # Renderiza o template da página principal passando todos os dados
        return render_template('logado.html',
            ambientes=ambientes,
            equipamentos=equipamentos,
            evento=evento,
            usuarios=usuarios,
            id_logado=id_logado, 
            logado=logado)       

    except ValueError as e:
        # Captura erros de validação e retorna status 400 
        return jsonify({"erro": str(e)}), 400
    
    except Exception as e:
        # Captura qualquer outro erro e retorna status 500 
        return jsonify({"erro": str(e)}), 500



@login_bp.route("/logout")
@jwt_required()  
def logout():
    """
    Rota que realiza o logout do usuário.
    
    """
    try:
        # Cria uma resposta de redirecionamento para a página de login
        response = redirect(url_for("login.home"))
        
        # Remove todos os cookies JWT 
        unset_jwt_cookies(response)
        
        return response
    
    except ValueError as e:
        # Captura erros de validação e retorna status 400
        return jsonify({"erro": str(e)}), 400
    
    except Exception as e:
        # Captura qualquer outro erro e retorna status 500
        return jsonify({"erro": str(e)}), 500