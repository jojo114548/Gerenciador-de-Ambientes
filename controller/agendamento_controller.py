from flask import Blueprint, request, jsonify
from service.usuario_service import UsuarioService
from flask_jwt_extended import (get_jwt_identity, jwt_required
)
from service.pendente_service import PendenteService
from service.pendente_equipamentos_service import PendenteServiceEquip
from service.agendamentos_service import AgendamentosService
from repository.agendamentos_repository import AgendamentosRepository
from service.agendamentos_equipamentos_service import AgendamentoEquipamentoService
from repository.agendamentos_equipamentos_repository import AgendamentoEquipamentoRepository
from service.notificacao_service import NotificacaoService

# Cria o Blueprint para as rotas de agendamentos
agendamento_bp = Blueprint("agendamento", __name__)


@agendamento_bp.route('/agendamentos', methods=['POST'])
@jwt_required()
def criar_agendamento():
    """
    Rota para criar um novo agendamento de ambiente.
    
    
    """
    try:
        # Obtém o ID do usuário logado a partir do token JWT
        id_logado = get_jwt_identity()
        # Obtém os dados do agendamento enviados no corpo da requisição (JSON)
        dados = request.get_json()

        # Extrai os dados principais do agendamento
        ambiente_id = dados.get("ambiente_id")
        data = dados.get("data")
        hora_inicio = dados.get("hora_inicio")
        hora_fim = dados.get("hora_fim")

        
        # Verifica se já existe um agendamento para este ambiente no mesmo horário
        conflito = AgendamentosRepository.existe_conflito(
            ambiente_id,
            data,
            hora_inicio,
            hora_fim
        )

        # Se houver conflito, retorna erro 409 
        if conflito:
            return jsonify({
                "erro": "Já existe um agendamento para este ambiente nesse horário."
            }), 409

        
        # Cria o agendamento no banco de dados com status "pendente"
        agendamento_id = AgendamentosService.criar_agendamento({
            "ambiente_id": ambiente_id,
            "data": data,
            "hora_inicio": hora_inicio,
            "hora_fim": hora_fim,
            "finalidade": dados.get("finalidade"),
            "status": "pendente"
        })

        # Se falhar ao criar o agendamento, retorna erro 500 
        if not agendamento_id:
            return jsonify({"erro": "Erro ao criar agendamento"}), 500

        
        # Cria registro de pendência vinculado ao agendamento para aprovação administrativa
        PendenteService.criar_pendente({
            "agendamento_id": agendamento_id,
            "user_id": id_logado,
            "status": "pendente"
        })
        
        
        # Retorna mensagem de sucesso com status 201 (Created)
        return jsonify({
            "mensagem": "Agendamento enviado para aprovação"
        }), 201

    # Tratamento de erros de validação (ValueError)
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    
@agendamento_bp.route('/agendamentos_equipamentos', methods=['POST'])
@jwt_required()
def criar_agendamento_equipamentos():
    """
    Rota para criar um novo agendamento de equipamento.
    
    """
    try:
    
        # Obtém o ID do usuário logado a partir do token JWT
        id_logado = get_jwt_identity()

        # Obtém os dados do agendamento enviados no corpo da requisição (JSON)
        dados = request.get_json()

        # Extrai os dados principais do agendamento de equipamento
        equipamento_id = dados.get("equipamento_id")
        data = dados.get("data")
        hora_inicio = dados.get("hora_inicio")
        hora_fim = dados.get("hora_fim")
       
    
        
        # Verifica se já existe um agendamento para este equipamento no mesmo horário
        conflito = AgendamentoEquipamentoRepository.existe_conflito(
            equipamento_id,
            data,
            hora_inicio,
            hora_fim,
        
        )

        # Se houver conflito, retorna erro 409 
        if conflito:
            return jsonify({
                "erro": "Já existe um agendamento para este Equipamento nesse horário."
            }), 409
        
      
        # Verifica se data e finalidade foram informados
        if not dados.get("data") or not dados.get("finalidade"):
            return jsonify({"erro": "Data e finalidade são obrigatórias"}), 400

        # Cria o agendamento de equipamento no banco de dados com status "pendente"
        agendamento_id = AgendamentoEquipamentoService.criar_agendamento({
            "equipamento_id": dados.get("equipamento_id"),
            "user_id": id_logado,
            "data": dados.get("data"),
            "hora_inicio": dados.get("hora_inicio"),
            "hora_fim": dados.get("hora_fim"),
            "finalidade": dados.get("finalidade"),
            "status": "pendente"
        })

        # Se falhar ao criar o agendamento, retorna erro 500 
        if not agendamento_id:
            return jsonify({"erro": "Erro ao criar agendamento de equipamento"}), 500

     
        # Cria registro de pendência vinculado ao agendamento de equipamento para aprovação
        PendenteServiceEquip.criar_pendente({
            "agendamento_id": agendamento_id,
            "user_id": id_logado,
            "status": "pendente"
        })
        
        # Retorna mensagem de sucesso com status 201 (Created)
        return jsonify({
            "mensagem": "Agendamento de equipamento enviado para aprovação"
        }), 201


    # Tratamento de erros de validação (ValueError)
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500