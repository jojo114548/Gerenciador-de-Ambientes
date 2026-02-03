from flask import Blueprint, render_template, jsonify
from flask_jwt_extended import ( get_jwt_identity, jwt_required,get_jwt)
from repository.historico_equipamento_repository import HistoricoEquipamentoRepository
from service.historico_equipamento_service import HistoricoEquipamentoService
from repository.historico_repository import HistoricoRepository
from service.historico_service import HistoricoService
from service.usuario_service import UsuarioService


# Cria o Blueprint para as rotas de histórico
historico_bp = Blueprint("historico", __name__)


@historico_bp.route('/historico')
@jwt_required()
def listar_historico():
    """
    Rota para exibir a página de histórico de agendamentos.
    
    """
    try:
        # Atualizar status de agendamentos concluídos
        # Atualiza o status dos agendamentos de ambientes que já foram concluídos
        HistoricoService.atualizar_concluidos()
        # Atualiza o status dos agendamentos de equipamentos que já foram concluídos
        HistoricoEquipamentoService.atualizar_concluidos()
        
        # Obtém os dados completos do JWT (
        logado = get_jwt()
        # Obtém o ID do usuário logado a partir do token JWT
        id_logado = get_jwt_identity()
        # Busca todos os usuários cadastrados no sistema
        usuarios = UsuarioService.listar()
        
        # Buscar históricos
        # Busca o histórico completo de agendamentos de ambientes
        historico = HistoricoRepository.listar_todos()
        # Busca o histórico completo de agendamentos de equipamentos 
        historico_equipamento = HistoricoEquipamentoRepository.listar()

        
        # Renderiza o template de histórico passando todos os dados necessários
        return render_template('historico.html',
            historico=historico,  # Histórico de agendamentos de ambientes
            historico_equip=historico_equipamento,  # Histórico de agendamentos de equipamentos
            id_logado=id_logado,  # ID do usuário logado
            logado=logado,  # Dados completos do JWT (incluindo role)
            usuarios=usuarios  # Lista de todos os usuários
        ) 

    # Tratamento de erros de validação (ValueError)
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    # Tratamento de erros genéricos
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@historico_bp.route('/historico/cancelar/<int:historico_id>', methods=['POST'])
@jwt_required()
def cancelar_historico(historico_id):
    """
    Rota para cancelar um agendamento de ambiente no histórico.
    
    """
    try:
        # Obtém o ID do usuário logado a partir do token JWT
        user_id = get_jwt_identity()

        # Chama o serviço para cancelar o agendamento de ambiente
        # Passa o ID do histórico e o ID do usuário para verificação de permissão
        HistoricoService.cancelar_historico(historico_id, user_id)

        # Retorna mensagem de sucesso com status 200 (OK)
        return jsonify({"mensagem": "Agendamento cancelado com sucesso"}), 200
    
    # Tratamento de erros de validação (ValueError) - ex: sem permissão, já cancelado
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    # Tratamento de erros genéricos
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@historico_bp.route('/historico_equipamentos/cancelar/<int:historicoEquip_id>', methods=['POST'])
@jwt_required()
def cancelar_historico_equipamentos(historicoEquip_id):
    """
    Rota para cancelar um agendamento de equipamento no histórico.
    
    """
    try:
        # Obtém o ID do usuário logado a partir do token JWT
        user_id = get_jwt_identity()

        # Chama o serviço para cancelar o agendamento de equipamento
        # Passa o ID do histórico e o ID do usuário para verificação de permissão
        HistoricoEquipamentoService.cancelar_historico(
            historicoEquip_id,
            user_id
        )

        # Retorna mensagem de sucesso com status 200 (OK)
        return jsonify({"mensagem": "Agendamento cancelado com sucesso"}), 200

    # Tratamento de erros de validação (ValueError) - ex: sem permissão, já cancelado
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    # Tratamento de erros genéricos
    except Exception as e:
        return jsonify({"erro": str(e)}), 500