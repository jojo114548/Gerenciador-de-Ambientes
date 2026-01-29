from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from service.usuario_service import UsuarioService
from flask_jwt_extended import (
    create_access_token, set_access_cookies, get_jwt_identity, jwt_required, unset_jwt_cookies,get_jwt
)
from service.pendente_service import PendenteService
from service.pendente_equipamentos_service import PendenteServiceEquip
from service.agendamentos_service import AgendamentosService
from repository.agendamentos_repository import AgendamentosRepository
from service.agendamentos_equipamentos_service import AgendamentoEquipamentoService
from repository.agendamentos_equipamentos_repository import AgendamentoEquipamentoRepository
from service.notificacao_service import NotificacaoService

agendamento_bp = Blueprint("agendamento", __name__)


@agendamento_bp.route('/agendamentos', methods=['POST'])
@jwt_required()
def criar_agendamento():
    try:
        id_logado = get_jwt_identity()
        dados = request.get_json()

        ambiente_id = dados.get("ambiente_id")
        data = dados.get("data")
        hora_inicio = dados.get("hora_inicio")
        hora_fim = dados.get("hora_fim")

        # 1️⃣ VERIFICA CONFLITO ANTES
        conflito = AgendamentosRepository.existe_conflito(
            ambiente_id,
            data,
            hora_inicio,
            hora_fim
        )

        if conflito:
            return jsonify({
                "erro": "Já existe um agendamento para este ambiente nesse horário."
            }), 409

        # 2️⃣ CRIA AGENDAMENTO
        agendamento_id = AgendamentosService.criar_agendamento({
            "ambiente_id": ambiente_id,
            "data": data,
            "hora_inicio": hora_inicio,
            "hora_fim": hora_fim,
            "finalidade": dados.get("finalidade"),
            "status": "pendente"
        })

        if not agendamento_id:
            return jsonify({"erro": "Erro ao criar agendamento"}), 500

        # 3️⃣ CRIA PENDÊNCIA
        PendenteService.criar_pendente({
            "agendamento_id": agendamento_id,
            "user_id": id_logado,
            "status": "pendente"
        })
        NotificacaoService.criar_notificacao(
            user_id=id_logado,
            titulo=f"Agendamento solicitado",
            mensagem=f"Agendamento solicitado para dia {dados['data']}, Ambiente {dados['ambiente_id']}.",
            tipo="aviso"
        )
        
        return jsonify({
            "mensagem": "Agendamento enviado para aprovação"
        }), 201

    
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    
@agendamento_bp.route('/agendamentos_equipamentos', methods=['POST'])
@jwt_required()
def criar_agendamento_equipamentos():
    try:
    
        id_logado = get_jwt_identity()

        dados = request.get_json()

        equipamento_id = dados.get("equipamento_id")
        data_equip = dados.get("data_equip")
        hora_inicio = dados.get("hora_inicio")
        hora_fim = dados.get("hora_fim")
    
        # 1️⃣ VERIFICA CONFLITO ANTES
        conflito =AgendamentoEquipamentoRepository.existe_conflito(
            equipamento_id,
            data_equip,
            hora_inicio,
            hora_fim,
        
        )

        if conflito:
            return jsonify({
                "erro": "Já existe um agendamento para este Equipamento nesse horário."
            }), 409
        
        if not dados.get("data_equip") or not dados.get("finalidade"):
            return jsonify({"erro": "Data e finalidade são obrigatórias"}), 400

        agendamento_id = AgendamentoEquipamentoService.criar_agendamento({
            "equipamento_id": dados.get("equipamento_id"),
            "user_id": id_logado,
            "data_equip": dados.get("data_equip"),
            "hora_inicio": dados.get("hora_inicio"),
            "hora_fim": dados.get("hora_fim"),
            "finalidade": dados.get("finalidade"),
            "status": "pendente"
        })

        if not agendamento_id:
            return jsonify({"erro": "Erro ao criar agendamento de equipamento"}), 500

        # ✅ pendência correta para EQUIPAMENTO
        PendenteServiceEquip.criar_pendente({
            "agendamento_id": agendamento_id,
            "user_id": id_logado,
            "status": "pendente"
        })
        NotificacaoService.criar_notificacao(
            user_id=id_logado,
            titulo="Agendamento solicitado",
            mensagem=f"Agendamento solicitado para dia '{dados['data_equip']}',Equipamentos '{dados['equipamento_id']}.",
            tipo="aviso"
        )
        return jsonify({
            "mensagem": "Agendamento de equipamento enviado para aprovação"
        }), 201


    
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    