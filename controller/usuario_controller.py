from flask import Blueprint, request, jsonify
from service.usuario_service import UsuarioService
from repository.usuario_repository import UsuarioRepository
from flask_jwt_extended import (
    create_access_token, set_access_cookies, get_jwt_identity, jwt_required, unset_jwt_cookies,get_jwt
)
from datetime import timedelta
import uuid,os
from werkzeug.utils import secure_filename
from service.notificacao_service import NotificacaoService


usuario_bp = Blueprint("usuario", __name__)
    
@usuario_bp.route("/usuarios/<id>", methods=["PUT"])
@jwt_required()
def editar_usuario(id):
    id_logado = get_jwt_identity()

    os.makedirs("static/imgs", exist_ok=True)

    name = request.form.get("name")
    email = request.form.get("email")

    if not name or not email:
        return jsonify({"erro": "Nome e email são obrigatórios"}), 400

    dados = {
        "name": name,
        "email": email,
        "cpf": request.form.get("cpf"),
        "rg": request.form.get("rg"),
        "data_nascimento": request.form.get("data_nascimento"),
        "telefone": request.form.get("telefone"),
        "endereco": request.form.get("endereco"),
        "departamento": request.form.get("departamento"),
        "funcao": request.form.get("funcao"),
        "role": request.form.get("role"),
        "status": request.form.get("status"),
        "image": request.form.get("image_atual")
    }

    imagem = request.files.get("image")
    if imagem and imagem.filename:
        filename = f"{uuid.uuid4()}_{secure_filename(imagem.filename)}"
        caminho = os.path.join("static/imgs", filename)
        imagem.save(caminho)
        dados["image"] = f"/static/imgs/{filename}"

    UsuarioService.atualizar(id, dados)

    

    return jsonify({"mensagem": "Usuário atualizado com sucesso"}), 200


@usuario_bp.route("/usuarios/<id>/senha", methods=["PUT"])
@jwt_required()
def alterar_senha(id):
    id_logado = get_jwt_identity()
    dados = request.get_json()

    senha_atual = dados.get("senha_atual")
    senha_nova = dados.get("senha_nova")
    
    if not senha_nova:
            return jsonify({"erro": "Senha nova é obrigatória"}), 400
        
    # Se o próprio usuário, exige senha atual
    if id == id_logado:
        UsuarioService.alterar_senha(id, senha_atual, senha_nova)
    else:
        # Admin pode resetar sem senha atual
        UsuarioService.resetar_senha(id, senha_nova)

   

    return jsonify({"mensagem": "Senha alterada com sucesso"}), 200


@usuario_bp.route("/usuarios/<id>", methods=["DELETE"])
@jwt_required()
def deletar_usuario(id):
    UsuarioService.deletar(id)
    return jsonify({"mensagem": "Usuário removido"}), 200


@usuario_bp.route("/novo-usuario", methods=["POST"])
@jwt_required()
def novo_usuario():
    id_logado = get_jwt_identity()

    imagem = request.files.get("image")
    image_path = None

    if imagem and imagem.filename != "":
        os.makedirs("static/imgs", exist_ok=True)
        filename = f"{uuid.uuid4()}_{secure_filename(imagem.filename)}"
        caminho = os.path.join("static/imgs", filename)
        imagem.save(caminho)
        image_path = f"/static/imgs/{filename}"

    dados = {
        "name": request.form.get("name"),
        "email": request.form.get("email"),
        "cpf": request.form.get("cpf"),
        "rg": request.form.get("rg"),
        "data_nascimento": request.form.get("data_nascimento"),
        "telefone": request.form.get("telefone"),
        "endereco": request.form.get("endereco"),
        "departamento": request.form.get("departamento"),
        "funcao": request.form.get("funcao"),
         "role": request.form.get("role"),  
        "status": request.form.get("status"), 
        "senha": request.form.get("senha"),
      
    }
    dados["image"] = image_path
  

    resultado = UsuarioService.cadastrar(dados)
    return jsonify({
        "mensagem": "Usuário cadastrado com sucesso",
        "usuario": resultado
    }), 201
    


