from flask import Blueprint, render_template, jsonify
from flask_jwt_extended import ( get_jwt_identity, jwt_required,get_jwt)
from repository.historico_equipamento_repository import HistoricoEquipamentoRepository
from service.historico_equipamento_service import HistoricoEquipamentoService
from repository.historico_repository import HistoricoRepository
from service.historico_service import HistoricoService
from service.usuario_service import UsuarioService


historico_bp = Blueprint("historico", __name__)


@historico_bp.route('/historico')
@jwt_required()
def listar_historico():
    
    try:
        HistoricoService.atualizar_concluidos()
        HistoricoEquipamentoService.atualizar_concluidos()
        
        logado = get_jwt()
        id_logado = get_jwt_identity()
        usuarios = UsuarioService.listar()
        historico = HistoricoRepository.listar_todos()
        historico_equipamento=HistoricoEquipamentoRepository.listar()

      
        return render_template('historico.html',
         historico=historico,
         historico_equip=historico_equipamento,
         id_logado=id_logado,
         logado=logado,
         usuarios=usuarios) 

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@historico_bp.route('/historico/cancelar/<int:historico_id>', methods=['POST'])
@jwt_required()
def cancelar_historico(historico_id):
    try:
        user_id = get_jwt_identity()

        HistoricoService.cancelar_historico(historico_id, user_id)

        return jsonify({"mensagem": "Agendamento cancelado com sucesso"}), 200
    
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@historico_bp.route('/historico_equipamentos/cancelar/<int:historico_id>', methods=['POST'])
@jwt_required()
def cancelar_historico_equipamentos(historico_id):
    try:
        user_id = get_jwt_identity()

        HistoricoEquipamentoService.cancelar_historico(
            historico_id,
            user_id
        )

        return jsonify({"mensagem": "Agendamento cancelado com sucesso"}), 200

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500