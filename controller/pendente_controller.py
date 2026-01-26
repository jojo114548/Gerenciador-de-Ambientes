from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from service.usuario_service import UsuarioService
from flask_jwt_extended import (
    create_access_token, set_access_cookies, get_jwt_identity, jwt_required, unset_jwt_cookies,get_jwt
)
import uuid,os
from werkzeug.utils import secure_filename
from service.pendente_service import PendenteService
from service.pendente_equipamentos_service import PendenteServiceEquip

pendente_bp = Blueprint("pendente", __name__)


@pendente_bp.route('/pendentes/<int:pendente_id>/status', methods=['POST'])
@jwt_required()
def atualizar_status_pendente(pendente_id):
    dados = request.get_json()
    status = dados.get("status")

    PendenteService.atualizar_status(pendente_id, status)

    return jsonify({"mensagem": "Status atualizado com sucesso"}), 200

@pendente_bp.route('/pendentes-equipamentos/<int:pendente_id>/status', methods=['PUT'])
def atualizar_status_pendente_equipamento(pendente_id):
    dados = request.get_json()
    status = dados.get("status")

    PendenteServiceEquip.atualizar_status(pendente_id, status)

    return jsonify({"mensagem": "Status do equipamento atualizado com sucesso"}), 200


