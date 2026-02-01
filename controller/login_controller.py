from flask import Blueprint, render_template, request, jsonify,redirect, url_for
from service.usuario_service import UsuarioService
from repository.usuario_repository import UsuarioRepository
from flask_jwt_extended import (
    create_access_token, set_access_cookies, get_jwt_identity, jwt_required, unset_jwt_cookies,get_jwt
)
from datetime import timedelta
from repository.eventos_repository import EventosRepository
from service.ambientes_service import AmbientesService
from service.equipamento_service import EquipamentoService
from werkzeug.utils import secure_filename
import uuid,os,bcrypt
from model.usuarios import Usuario
from datetime import datetime




login_bp = Blueprint("login", __name__)


@login_bp.route("/")
def home():
    return render_template("login.html")

@login_bp.route('/login', methods=["POST"])
def login_post():
    email = request.form.get("email")
    senha = request.form.get("senha")

    usuario = UsuarioService.autenticar(email, senha)

    if not usuario:
        return "Email ou senha inválidos", 401
    
    access_token = create_access_token(
        identity=usuario["id"],
        additional_claims={
            "nome": usuario["name"],
            "email": usuario["email"],
            "role": usuario["role"],
            "image": usuario["image"],
            "status": usuario["status"]
        },
        expires_delta=timedelta(hours=1)
    )

    response = redirect(url_for("login.index"))
    set_access_cookies(response, access_token)
    return response

@login_bp.route('/index')
@jwt_required()
def index():
    try:

        logado = get_jwt()
        id_logado = get_jwt_identity()
        ambientes = AmbientesService.listar()
        equipamentos = EquipamentoService.listar()
        usuarios = UsuarioService.listar()
        evento=EventosRepository.listar()

        for event in evento:
            event["inscrito"] = EventosRepository.usuario_ja_inscrito(
                event["id"],
                id_logado
            )

    
        return render_template('logado.html',
        ambientes=ambientes,
        equipamentos=equipamentos,
        evento=evento,
        usuarios=usuarios,
        id_logado=id_logado, 
        logado=logado)

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    
@login_bp.route("/logout")
@jwt_required()
def logout():
  try:
   
    response = redirect(url_for("login.home"))
    unset_jwt_cookies(response)
    return response
  
  except ValueError as e:
        return jsonify({"erro": str(e)}), 400
  except Exception as e:
        return jsonify({"erro": str(e)}), 500
    