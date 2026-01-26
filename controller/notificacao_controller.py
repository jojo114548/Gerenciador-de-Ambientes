from flask import Blueprint, render_template, request, jsonify,redirect, url_for
from service.usuario_service import UsuarioService
from flask_jwt_extended import (
    create_access_token, set_access_cookies, get_jwt_identity, jwt_required, unset_jwt_cookies,get_jwt
)
from service.notificacao_service import NotificacaoService



notificacao_bp = Blueprint("notificacao", __name__)

@notificacao_bp.route("/notificacoes/<usuario_id>", methods=["GET"])
@jwt_required()
def listar_notificacoes(usuario_id):
    notificacoes = NotificacaoService.listar_nao_lidas(usuario_id)
    return jsonify(notificacoes)

@notificacao_bp.route("/notificacoes", methods=["POST"])
@jwt_required()
def criar_notificacao():
    dados = request.json

    try:
        NotificacaoService.criar_notificacao(
            user_id=dados["user_id"],
            titulo=dados["titulo"],
            mensagem=dados["mensagem"],
            tipo=dados.get("tipo", "info")
        )
        return jsonify({"mensagem": "Notificação criada"}), 201

    except Exception as e:
        return jsonify({"erro": str(e)}), 400

@notificacao_bp.route("/notificacoes/<id>/lida", methods=["PUT"])
@jwt_required()
def marcar_lida(id):
    sucesso = NotificacaoService.marcar_lida(id)

    if not sucesso:
        return jsonify({"erro": "Notificação não encontrada"}), 404

    return jsonify({"mensagem": "Notificação marcada como lida"})

