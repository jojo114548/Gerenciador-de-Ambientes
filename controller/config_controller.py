from flask import Blueprint, render_template, request, jsonify
from service.usuario_service import UsuarioService
from flask_jwt_extended import ( get_jwt_identity, jwt_required,get_jwt
)
from service.pendente_service import PendenteService
from service.pendente_equipamentos_service import PendenteServiceEquip


# Cria o Blueprint para as rotas de configuração
config_bp = Blueprint("config", __name__)


@config_bp.route('/config')
@jwt_required()
def config():
    """
    Rota para exibir a página de configurações do sistema.
    
    """
    try:  
        # Obtém os dados completos do JWT 
        logado = get_jwt()
        # Obtém o ID do usuário logado a partir do token JWT
        id_logado = get_jwt_identity()


        # Verifica permissões de acesso à página de configurações
        # Se o ID acessado é diferente do logado E o usuário não é admin
        if id != id_logado and logado["role"] != "admin":
            # Retorna erro 403 - acesso negado
            return jsonify({"erro": "Você não tem permissão para deletar este usuário."}), 403
        

        # Busca todos os usuários cadastrados no sistema
        usuarios = UsuarioService.listar()
        # Busca todas as solicitações pendentes de ambientes
        pendentes_ambientes= PendenteService.listar()
        # Busca todas as solicitações pendentes de equipamentos
        pendentes_equipamentos=PendenteServiceEquip.listar()

        # Renderiza o template de configurações passando todos os dados necessários
        return render_template('config.html', 
        pendentes=pendentes_ambientes,  # Solicitações pendentes de ambientes
        pendentes_equipamentos=pendentes_equipamentos,  # Solicitações pendentes de equipamentos
        id_logado=id_logado,  # ID do usuário logado
        logado=logado,  # Dados completos do JWT (incluindo role)
        usuarios=usuarios)  # Lista de todos os usuários
    
    # Tratamento de erros de validação (ValueError)
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    # Tratamento de erros genéricos
    except Exception as e:
        return jsonify({"erro": str(e)}), 500