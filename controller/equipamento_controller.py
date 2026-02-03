from flask import Blueprint, render_template, request, jsonify,redirect, url_for
from service.usuario_service import UsuarioService
from flask_jwt_extended import (
    create_access_token, set_access_cookies, get_jwt_identity, jwt_required, unset_jwt_cookies,get_jwt
)
from service.ambientes_service import AmbientesService
import uuid,os
from werkzeug.utils import secure_filename
from service.equipamento_service import EquipamentoService

# Cria o Blueprint para as rotas de equipamentos
equipamento_bp = Blueprint("equipamento", __name__)


@equipamento_bp.route('/equipamentos')
@jwt_required()
def equipamentos():
    """
    Rota para exibir a página de listagem de equipamentos.
    
    Funcionalidade:
    - Requer autenticação JWT (usuário deve estar logado)
    - Busca informações do usuário logado (ID e dados do JWT)
    - Lista todos os usuários cadastrados
    - Lista todos os equipamentos cadastrados
    - Renderiza o template de equipamentos com todas as informações
    
    Decorators:
        @jwt_required(): Exige token JWT válido para acessar a rota
    
    Returns:
        Response: Template renderizado com equipamentos, usuários e dados do usuário logado
        tuple: JSON com erro 400/500 em caso de falha
    """
    try:
        # Obtém os dados completos do JWT (incluindo role/função do usuário)
        logado = get_jwt()
        # Obtém o ID do usuário logado a partir do token JWT
        id_logado = get_jwt_identity()

        # Busca todos os usuários cadastrados no sistema
        usuarios = UsuarioService.listar()
        # Busca todos os equipamentos cadastrados
        equipamentos = EquipamentoService.listar()


        # Renderiza o template de equipamentos passando todos os dados necessários
        return render_template('equipamentos.html',
        equipamentos=equipamentos,  # Lista de todos os equipamentos
        id_logado=id_logado,  # ID do usuário logado
        logado=logado,  # Dados completos do JWT (incluindo role)
        usuarios=usuarios)  # Lista de todos os usuários
    
    # Tratamento de erros de validação (ValueError)
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    # Tratamento de erros genéricos
    except Exception as e:
        return jsonify({"erro": "Erro ao alterar senha"}), 500
    

@equipamento_bp.route('/equipamento', methods=['POST'])
@jwt_required()
def cadastrar_equipamento():
    """
    Rota para cadastrar um novo equipamento no sistema.
    
    Funcionalidade:
    - Requer autenticação JWT e permissão de administrador
    - Recebe dados do equipamento via formulário (multipart/form-data)
    - Permite upload de imagem do equipamento (opcional)
    - Se imagem for enviada, salva com nome único (UUID)
    - Converte quantidade disponível para inteiro
    - Cadastra o equipamento com todas as especificações
    
    Decorators:
        @jwt_required(): Exige token JWT válido para acessar a rota
    
    Returns:
        tuple: JSON com mensagem de sucesso (200) ou erro (400, 403, 500)
    """

    try:
        # Obtém os dados completos do JWT (incluindo role/função do usuário)
        logado = get_jwt()
       

        # Verifica se o usuário tem permissão de administrador
        if logado["role"] != "admin":
            # Retorna erro 403 (Forbidden) se não for admin
            return jsonify({"erro": "Você não tem permissão para deletar este usuário."}), 403
         
        # Obtém o arquivo de imagem enviado no formulário (se houver)
        imagem = request.files.get("image")
        # Obtém o caminho da imagem atual (caso não seja enviada nova imagem)
        image_path = request.form.get("image_atual")

        # Se uma nova imagem foi enviada
        if imagem:
            # Gera nome único para o arquivo usando UUID e nome seguro
            filename = f"{uuid.uuid4()}_{secure_filename(imagem.filename)}"
            # Define o caminho onde a imagem será salva
            caminho = f"static/imgs/{filename}"
            # Salva a imagem no servidor
            imagem.save(caminho)
            # Define o caminho da imagem para salvar no banco de dados
            image_path = f"/{caminho}"

        # Monta o dicionário com todos os dados do novo equipamento
        dados = {
            
            "name": request.form.get("name"),  # Nome do equipamento
            "categoria": request.form.get("categoria"),  # Categoria do equipamento
            "status": request.form.get("status") or "Disponivel",  # Status (padrão: "Disponivel")
            "descricao": request.form.get("descricao"),  # Descrição do equipamento
            "marca": request.form.get("marca"),  # Marca do equipamento
            "modelo": request.form.get("modelo"),  # Modelo do equipamento
            "condicao": request.form.get("condicao"),  # Condição física (novo, usado, etc)
            "quantidade_disponivel": int(request.form.get("quantidade_disponivel")),  # Quantidade em estoque
            "image": image_path,  # Caminho da imagem
            "especificacoes": request.form.getlist("especificacoes[]")  # Lista de especificações técnicas
        }

        # Insere o novo equipamento no banco de dados
        EquipamentoService.inserir_equipamento(dados)
        # Retorna mensagem de sucesso com status 200 (OK)
        return jsonify({"mensagem": "Equipamento cadastrado com sucesso"}), 200
    
    # Tratamento de erros de validação (ValueError)
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    # Tratamento de erros genéricos
    except Exception as e:
        return jsonify({"erro": "Erro ao alterar senha"}), 500
    

@equipamento_bp.route('/editar-equipamento/<id>', methods=['POST'])
@jwt_required()
def editar_equipamento(id):
    """
    Rota para atualizar um equipamento existente.
    
    Funcionalidade:
    - Requer autenticação JWT e permissão de administrador
    - Recebe dados do equipamento via formulário (multipart/form-data)
    - Permite upload de nova imagem (mantém atual se não enviar nova)
    - Valida quantidade disponível (campo obrigatório)
    - Atualiza status automaticamente baseado na quantidade:
      * Se quantidade <= 0: status vira "ocupado"
      * Se quantidade > 0: mantém status informado ou "disponivel"
    - Atualiza todos os dados do equipamento incluindo especificações
    
    Args:
        id (str): ID do equipamento a ser atualizado (da URL)
    
    Decorators:
        @jwt_required(): Exige token JWT válido para acessar a rota
    
    Returns:
        tuple: JSON com mensagem de sucesso (200) ou erro (400, 403, 500)
    """
    try:
         
        # Obtém os dados completos do JWT (incluindo role/função do usuário)
        logado = get_jwt()
       
        # Verifica se o usuário tem permissão de administrador
        if logado["role"] != "admin":
            # Retorna erro 403 (Forbidden) se não for admin
            return jsonify({"erro": "Você não tem permissão para deletar este usuário."}), 403
        
        # Obtém o arquivo de imagem enviado no formulário (se houver)
        imagem = request.files.get("image")
        # Obtém o caminho da imagem atual (mantém se não enviar nova)
        image_path = request.form.get("image_atual")

        # Se uma nova imagem foi enviada e tem nome de arquivo válido
        if imagem and imagem.filename:
            # Gera nome único para o arquivo usando UUID e nome seguro
            filename = f"{uuid.uuid4()}_{secure_filename(imagem.filename)}"
            # Define o caminho onde a imagem será salva
            caminho = f"static/imgs/{filename}"
            # Salva a imagem no servidor
            imagem.save(caminho)
            # Define o caminho da imagem para salvar no banco de dados
            image_path = f"/{caminho}"

        # Obtém a quantidade disponível do formulário
        qtd = request.form.get("quantidade_disponivel")
        # Valida se a quantidade foi informada (campo obrigatório)
        if qtd is None or qtd == "":
            return jsonify({"erro": "Quantidade disponível é obrigatória"}), 400

        # Converte a quantidade para inteiro
        quantidade = int(qtd)

        # Obtém o status informado no formulário
        status = request.form.get("status")
        # Atualiza status automaticamente baseado na quantidade
        if quantidade <= 0:
            # Se não houver estoque, marca como ocupado
            status = "ocupado"
        elif not status:
            # Se houver estoque e não foi informado status, marca como disponível
            status = "disponivel"

        # Monta o dicionário com todos os dados atualizados do equipamento
        dados = {
            "id": id,  # ID do equipamento vindo da URL
            "name": request.form.get("name"),  # Nome do equipamento
            "categoria": request.form.get("categoria"),  # Categoria do equipamento
            "status": status,  # Status atualizado automaticamente
            "descricao": request.form.get("descricao"),  # Descrição do equipamento
            "marca": request.form.get("marca"),  # Marca do equipamento
            "modelo": request.form.get("modelo"),  # Modelo do equipamento
            "condicao": request.form.get("condicao"),  # Condição física
            "quantidade_disponivel": quantidade,  # Quantidade em estoque
            "image": image_path,  # Caminho da imagem (nova ou atual)
            "especificacoes": request.form.getlist("especificacoes[]")  # Lista de especificações
        }

        # Atualiza o equipamento no banco de dados
        EquipamentoService.atualizar_equipamento(dados)
        # Retorna mensagem de sucesso com status 200 (OK)
        return jsonify({"mensagem": "Equipamento atualizado com sucesso"}), 200
    
    # Tratamento de erros de validação (ValueError)
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    # Tratamento de erros genéricos
    except Exception as e:
        return jsonify({"erro": "Erro ao alterar senha"}), 500

@equipamento_bp.route("/equipamentos/<id>", methods=["DELETE"])
@jwt_required()
def deletar_equipamento(id):
        """
        Rota para excluir um equipamento do sistema.
        
        """
        try:
            # Obtém os dados completos do JWT 
            logado = get_jwt()
       
            # Verifica se o usuário tem permissão de administrador
            if logado["role"] != "admin":
                # Retorna erro 403  se não for admin
                return jsonify({"erro": "Você não tem permissão para deletar este usuário."}), 403
        
            # Deleta o equipamento do banco de dados pelo ID
            EquipamentoService.deletar_equipamento(id)
            # Retorna mensagem de sucesso com status 200 (OK)
            return jsonify({'mensagem': 'Equipamento excluído com sucesso'}), 200
        # Tratamento de erros de validação (ValueError)
        except ValueError as e:
          return jsonify({"erro": str(e)}), 400
        # Tratamento de erros genéricos
        except Exception as e:
          return jsonify({"erro": str(e)}), 500

@equipamento_bp.route("/novo-equipamento", methods=["GET", "POST"])
@jwt_required()
def novo_equipamento():
    """
    Rota para exibir formulário e cadastrar novo equipamento.
    
    """
    try:
        #  GET apenas exibe a página
        # Se a requisição for GET, apenas renderiza o formulário
        if request.method == "GET":
            return render_template("novo_equipamento.html")

        # POST → cria equipamento
        # Obtém o arquivo de imagem enviado no formulário (se houver)
        imagem = request.files.get("image")
        # Inicializa caminho da imagem como None (caso não seja enviada)
        image_path = None

        # Se uma imagem foi enviada e tem nome de arquivo válido
        if imagem and imagem.filename:
            # Cria o diretório para salvar imagens se não existir
            os.makedirs("static/imgs", exist_ok=True)

            # Gera nome único para o arquivo usando UUID e nome seguro
            filename = f"{uuid.uuid4()}_{secure_filename(imagem.filename)}"
            # Define o caminho completo onde a imagem será salva
            caminho = os.path.join("static/imgs", filename)

            # Salva a imagem no servidor
            imagem.save(caminho)
            # Define o caminho da imagem para salvar no banco de dados
            image_path = f"/static/imgs/{filename}"

        # Monta o dicionário com todos os dados do novo equipamento
        dados = {
            "name": request.form.get("name"),  # Nome do equipamento
            "categoria": request.form.get("categoria"),  # Categoria do equipamento
            "status": request.form.get("status") or "Disponivel",  # Status (padrão: "Disponivel")
            "descricao": request.form.get("descricao"),  # Descrição do equipamento
            "marca": request.form.get("marca"),  # Marca do equipamento
            "modelo": request.form.get("modelo"),  # Modelo do equipamento
            "condicao": request.form.get("condicao"),  # Condição física
            "quantidade_disponivel": int(request.form.get("quantidade", 0)),  # Quantidade em estoque
            "image": image_path,  # Caminho da imagem (ou None)
            "especificacoes": request.form.getlist("especificacoes[]")  # Lista de especificações
        }

       
        # Valida se os campos obrigatórios foram preenchidos
        if not dados["name"] or not dados["categoria"]:
            return "Nome e categoria são obrigatórios", 400

        # Insere o novo equipamento no banco de dados
        EquipamentoService.inserir_equipamento(dados)
        
    # Tratamento de erros de validação (ValueError)
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    # Tratamento de erros genéricos
    except Exception as e:
        print(e)
        return jsonify, 500({"erro": str(e)})