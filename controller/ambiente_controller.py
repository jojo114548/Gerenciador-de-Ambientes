from flask import Blueprint, render_template, request, jsonify, redirect, url_for, current_app
from service.usuario_service import UsuarioService
from flask_jwt_extended import (
    create_access_token, set_access_cookies, get_jwt_identity, jwt_required, unset_jwt_cookies,get_jwt
)
from service.ambientes_service import AmbientesService
import uuid,os
from werkzeug.utils import secure_filename


ambientes_bp = Blueprint("ambientes", __name__)

@ambientes_bp.route('/ambientes')
@jwt_required()
def ambientes():
    logado = get_jwt()
    id_logado = get_jwt_identity()
    usuarios = UsuarioService.listar()
    ambientes = AmbientesService.listar()
   
    return render_template('ambientes.html',ambientes=ambientes,id_logado=id_logado,logado=logado,usuarios=usuarios)


@ambientes_bp.route('/ambientes/<id>', methods=['POST'])
def atualizar_ambiente(id):
    imagem = request.files.get("image")
    image_path = request.form.get("image_atual")

    if imagem:
        filename = f"{uuid.uuid4()}_{secure_filename(imagem.filename)}"
        caminho = f"static/imgs/{filename}"
        imagem.save(caminho)
        image_path = f"/{caminho}"

    dados = {
        "id": id,
        "name": request.form.get("name"),
       "type": request.form.get("type") or "sala",
        "capacidade": request.form.get("capacidade"),
        "status": request.form.get("status") or "Disponivel",
        "descricao": request.form.get("descricao"),
        "localizacao": request.form.get("localizacao"),
        "area": request.form.get("area"),
        "image": image_path,
        "recursos": request.form.getlist("recursos[]")
    }

    AmbientesService.atualizar_ambiente(dados)
    return jsonify({"mensagem": "Ambiente atualizado com sucesso"}), 200


@ambientes_bp.route("/novo-ambiente", methods=['GET','POST'])
def novo_ambiente():

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
        "type": request.form.get("type"),
        "capacidade": int(request.form.get("capacidade")),
        "status": request.form.get("status", "Disponivel"),
        "descricao": request.form.get("descricao"),
        "localizacao": request.form.get("localizacao"),
        "area": request.form.get("area"),
        "image": image_path,
        "recursos": request.form.getlist("recursos[]")  # LISTA
    }

    AmbientesService.inserir_ambiente(dados)


    return redirect("/ambientes") 

@ambientes_bp.route("/ambientes/<id>/", methods=["DELETE"])
def deletar_ambiente(id):
    AmbientesService.deletar_ambiente(id)
    return jsonify({'mensagem': 'Ambiente excluído com sucesso'}), 200

