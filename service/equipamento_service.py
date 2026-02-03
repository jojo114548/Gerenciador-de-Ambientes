from repository.equipamento_repository import EquipamentoRepository
from service.notificacao_service import NotificacaoService
from model.equipamentos import Equipamento


class EquipamentoService:
    

    @staticmethod
    def listar():
        """
        Lista todos os equipamentos cadastrados com especificações formatadas.
        
        """
        # Busca todos os equipamentos cadastrados no banco de dados
        equipamentos = EquipamentoRepository.listar()

        # Processa cada equipamento para formatar as especificações
        for eq in equipamentos:
            # Se o equipamento possui especificações (campo preenchido)
            if eq.get("especificacoes"):
                # Converte a string de especificações em lista, separando por " | "
                eq["especificacoes"] = eq["especificacoes"].split(" | ")
            else:
                # Se não houver especificações, define como lista vazia
                eq["especificacoes"] = []

        return equipamentos

    @staticmethod
    def inserir_equipamento(dados):
        """
        Insere um novo equipamento no sistema com validações.
        
        """
        #  Validação mínima
        # Obtém o valor da quantidade disponível 
        qtd = dados.get("quantidade_disponivel")

        # Verifica se a quantidade foi informada (não pode ser None ou string vazia)
        if qtd is None or qtd == "":
            raise ValueError("Quantidade disponível é obrigatória")

        # Converte a quantidade para inteiro e atualiza nos dados
        dados["quantidade_disponivel"] = int(qtd)

        # Insere o equipamento no banco de dados e obtém o ID gerado
        equipamento_id = EquipamentoRepository.inserir_equipamento(dados)

        # Obtém a lista de especificações (se houver), caso contrário lista vazia
        especificacoes = dados.get("especificacoes", [])

        # Se houver especificações para inserir
        if especificacoes:
            # Insere as especificações vinculadas ao equipamento recém-criado
            EquipamentoRepository.inserir_especificacoes(
                equipamento_id,
                especificacoes
            )

        

        return equipamento_id

    @staticmethod
    def deletar_equipamento(equipamento_id):
        """
        Remove um equipamento do sistema pelo seu ID.
        
        """
        # Remove o equipamento do banco de dados pelo ID
        EquipamentoRepository.deletar_equipamento(equipamento_id)

       

    @staticmethod
    def atualizar_equipamento(dados):
        """
        Atualiza as informações de um equipamento existente com validações e lógica automática.
        
        """
        # Valida se a quantidade disponível foi informada (campo obrigatório)
        if "quantidade_disponivel" not in dados:
            raise ValueError("Quantidade disponível é obrigatória")

        # Converte a quantidade disponível para inteiro
        dados["quantidade_disponivel"] = int(dados["quantidade_disponivel"])

        # Atualiza status automaticamente baseado na quantidade disponível
        # Se a quantidade disponível for zero ou negativa
        if dados["quantidade_disponivel"] <= 0:
            # Define status como "Ocupado"
            dados["status"] = "Ocupado"
        else:
            # Se houver quantidade disponível, mantém status informado ou define "Disponivel"
            dados["status"] = dados.get("status", "Disponivel")

        # Cria objeto Equipamento 
        equipamento = Equipamento(**dados)

        # Atualiza o equipamento no banco de dados
        EquipamentoRepository.atualizar_equipamento(equipamento)