from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_jwt_extended import (
    create_access_token, set_access_cookies, get_jwt_identity, jwt_required, unset_jwt_cookies,get_jwt
)
from repository.historico_equipamento_repository import HistoricoEquipamentoRepository
from service.historico_equipamento_service import HistoricoEquipamentoService
from repository.historico_repository import HistoricoRepository
from service.historico_service import HistoricoService
from service.usuario_service import UsuarioService


historico_bp = Blueprint("historico", __name__)


@historico_bp.route('/historico')
@jwt_required()
def listar_historico():
    logado = get_jwt()
    id_logado = get_jwt_identity()
    usuarios = UsuarioService.listar()
    historico = HistoricoRepository.listar_todos()
    historico_equipamento=HistoricoEquipamentoRepository.listar()

    
          

    return render_template('historico.html', historico=historico,historico_equip=historico_equipamento,id_logado=id_logado,logado=logado,usuarios=usuarios) 



@historico_bp.route('/historico/cancelar/<id>', methods=['POST'])
@jwt_required()
def cancelar_historico(id):
    print("AGENDAMENTO_ID:", id)
    user_id = get_jwt_identity()

    HistoricoRepository.atualizar_status(id,
        "Cancelado"
    )
    return jsonify({"mensagem": "Agendamento cancelado com sucesso"}), 200
    


@historico_bp.route('/historico_equipamentos/cancelar/<agendamento_id>', methods=['POST'])
@jwt_required()
def cancelar_historico_equipamentos(id):
    user_id = get_jwt_identity()

    HistoricoEquipamentoRepository.atualizar_status(
        id,
        "Cancelado"
    )
    return jsonify({"mensagem": "Agendamento cancelado com sucesso"}), 200