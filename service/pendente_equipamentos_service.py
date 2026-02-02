from repository.pendente_equipamento_repository import (
    PendenteEquipamentoRepository
)
from service.historico_equipamento_service import (
    HistoricoEquipamentoService
)
from repository.historico_equipamento_repository import (
    HistoricoEquipamentoRepository  # ✅ ADICIONE ESTA IMPORTAÇÃO
)
from service.notificacao_service import NotificacaoService


class PendenteServiceEquip:

    @staticmethod
    def criar_pendente(dados):
        if not dados:
            raise Exception("Dados do pendente não informados")

        if not dados.get("user_id"):
            raise ValueError("Usuário não informado para criação de pendente")
        
        try:
            return PendenteEquipamentoRepository.inserir(dados)
        except Exception as e:
            if "uq_pendente_agendamento" in str(e):
                return None
            raise

    @staticmethod
    def listar():
        return PendenteEquipamentoRepository.listar()

    @staticmethod
    def atualizar_status(pendente_id, status):
        print(f"\n{'='*60}")
        print(f"🔄 ATUALIZANDO STATUS DO PENDENTE {pendente_id} para {status}")
        print(f"{'='*60}")

        pendente = PendenteEquipamentoRepository.buscar_por_id(pendente_id)
        if not pendente:
            raise ValueError("Pendente não encontrado")

        print(f"📦 Pendente encontrado:")
        print(f"   Agendamento ID: {pendente['agendamento_id']}")
        print(f"   Equipamento: {pendente['equipamento_nome']}")
        print(f"   User ID: {pendente['user_id']}")

        # 🔍 Verifica se já existe histórico para o agendamento
        historico_existente = HistoricoEquipamentoRepository.buscar_por_agendamento(
            pendente["agendamento_id"]
        )

        if historico_existente:
            print(f"\n⚠️ HISTÓRICO JÁ EXISTE!")
            print(f"   Histórico ID: {historico_existente['id']}")
            print(f"   Status atual do histórico: {historico_existente['status']}")

        # 🔄 Atualiza status do pendente (sempre)
        print(f"\n🔄 Atualizando status do pendente no banco...")
        PendenteEquipamentoRepository.atualizar_status(pendente_id, status)

        # 📝 Cria histórico APENAS se:
        # - status for final
        # - NÃO existir histórico ainda
        if status in ['Confirmado', 'Rejeitado', 'Cancelado'] and not historico_existente:
            try:
                print(f"\n📝 Criando histórico para equipamento...")
                print(f"   Status: {status}")

                historico_id = HistoricoEquipamentoService.criar_historico({
                    "agendamento_id": pendente["agendamento_id"],
                    "equipamento_id": pendente["equipamento_id"],
                    "user_id": pendente["user_id"],
                    "equipamento_nome": pendente["equipamento_nome"],
                    "data_equip": pendente["data"],
                    "hora_inicio": pendente["hora_inicio"],
                    "hora_fim": pendente["hora_fim"],
                    "finalidade": pendente["finalidade"],
                    "status": status
                })

                print(f"✅ Histórico criado com sucesso! ID: {historico_id}")

            except Exception as e:
                print(f"❌ Erro ao criar histórico: {e}")
                import traceback
                traceback.print_exc()

        # 🔔 Notificações por status
        try:
            if status == 'Confirmado':
                NotificacaoService.criar_notificacao({
                    "user_id": pendente["user_id"],
                    "titulo": "Agendamento Aprovado",
                    "mensagem": (
                        f"Seu agendamento do equipamento "
                        f"'{pendente['equipamento_nome']}' foi aprovado para "
                        f"{pendente['data']} às {pendente['hora_inicio']}."
                    ),
                    "tipo": "sucesso"
                })

            elif status == 'Rejeitado':
                NotificacaoService.criar_notificacao({
                    "user_id": pendente["user_id"],
                    "titulo": "Agendamento Rejeitado",
                    "mensagem": (
                        f"Seu agendamento do equipamento "
                        f"'{pendente['equipamento_nome']}' foi rejeitado."
                    ),
                    "tipo": "aviso"
                })

            elif status == 'Cancelado':
                NotificacaoService.criar_notificacao({
                    "user_id": pendente["user_id"],
                    "titulo": "Agendamento Cancelado",
                    "mensagem": (
                        f"Seu agendamento do equipamento "
                        f"'{pendente['equipamento_nome']}' foi cancelado."
                    ),
                    "tipo": "info"
                })
        except Exception as e:
            print(f"Erro ao criar notificação: {e}")

        print(f"✅ Processo completo!")
        print(f"{'='*60}\n")

        return {
            **pendente,
            "status": status
        }
