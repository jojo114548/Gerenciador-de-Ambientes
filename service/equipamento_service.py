from repository.equipamento_repository import EquipamentoRepository
from service.notificacao_service import NotificacaoService
from model.equipamentos import Equipamento


class EquipamentoService:

    @staticmethod
    def listar():
        """Lista todos os equipamentos com especificações formatadas"""
        equipamentos = EquipamentoRepository.listar()

        for eq in equipamentos:
            if eq.get("specifications"):
                eq["specifications"] = eq["specifications"].split(" | ")
            else:
                eq["specifications"] = []

        return equipamentos

    @staticmethod
    def inserir_equipamento(dados):
        # 🔒 Validação mínima
        if "quantidade_disponivel" not in dados:
            raise ValueError("Quantidade disponível é obrigatória")

        dados["quantidade_disponivel"] = int(dados["quantidade_disponivel"])

        # 🔄 Status automático opcional
        if dados["quantidade_disponivel"] <= 0:
            dados["status"] = "Ocupado"
        else:
            dados["status"] = dados.get("status", "Disponivel")

        equipamento_id = EquipamentoRepository.inserir_equipamento(dados)

        especificacoes = dados.get("especificacoes", [])

        if especificacoes:
            EquipamentoRepository.inserir_especificacoes(
                equipamento_id,
                especificacoes
            )

        

        return equipamento_id

    @staticmethod
    def deletar_equipamento(equipamento_id):
        EquipamentoRepository.deletar_equipamento(equipamento_id)

       

    @staticmethod
    def atualizar_equipamento(dados):
        """Atualiza um equipamento com validações"""
        if "quantidade_disponivel" not in dados:
            raise ValueError("Quantidade disponível é obrigatória")

        dados["quantidade_disponivel"] = int(dados["quantidade_disponivel"])

        # 🔄 Atualiza status automaticamente
        if dados["quantidade_disponivel"] <= 0:
            dados["status"] = "Ocupado"
        else:
            dados["status"] = dados.get("status", "Disponivel")

        equipamento = Equipamento(**dados)

        EquipamentoRepository.atualizar_equipamento(equipamento)

        
