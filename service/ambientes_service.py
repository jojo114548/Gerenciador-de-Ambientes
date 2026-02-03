from repository.ambientes_repository import AmbientesRepository
from service.notificacao_service import NotificacaoService
from model.ambientes import Ambiente


class AmbientesService:
   
    
    @staticmethod
    def listar():
        """
        Lista todos os ambientes cadastrados com recursos formatados.
        
        """
        # Busca todos os ambientes cadastrados no banco de dados
        ambientes = AmbientesRepository.listar()

        # Processa cada ambiente para formatar os recursos
        for ambiente in ambientes:
            # Se o ambiente possui recursos 
            if ambiente["recursos"]:
                # Converte a string de recursos em lista, separando por " | "
                ambiente["recursos"] = ambiente["recursos"].split(" | ")
            else:
                # Se não houver recursos, define como lista vazia
                ambiente["recursos"] = []

        return ambientes
    
    @staticmethod
    def inserir_ambiente(dados):
        """
        Insere um novo ambiente no sistema com seus recursos.

        """
        # Cria objeto Ambiente a partir dos dados fornecidos
        ambiente = Ambiente(**dados)

       
        # Insere o ambiente no banco de dados e obtém o ID gerado automaticamente
        ambiente_id = AmbientesRepository.inserir_ambiente(ambiente)

        # recursos vindos do form
        # Obtém a lista de recursos (se houver), caso contrário lista vazia
        recursos = dados.get("recursos", [])

    
        # Se houver recursos para inserir
        if recursos:
            # Insere os recursos vinculados ao ambiente recém-criado usando o ID 
            AmbientesRepository.inserir_recursos(ambiente_id, recursos)

    @staticmethod
    def deletar_ambiente(ambiente_id):
        """
        Remove um ambiente do sistema pelo seu ID.
        
        """
        # Remove o ambiente do banco de dados pelo ID
        AmbientesRepository.deletar_ambiente(ambiente_id)

    @staticmethod
    def atualizar_ambiente(dados):
        """
        Atualiza as informações de um ambiente existente e seus recursos.
        
        """
        # Cria objeto Ambiente a partir dos dados fornecidos pelo backend 
        ambiente = Ambiente(**dados)
        
      
        # Atualiza os dados principais do ambiente no banco de dados
        AmbientesRepository.atualizar_ambiente(ambiente)
        
        # Atualiza os recursos
        # Obtém a lista de recursos atualizada (se houver), caso contrário lista vazia
        recursos = dados.get("recursos", [])

        # Atualiza os recursos vinculados ao ambiente (remove antigos e insere novos)
        AmbientesRepository.atualizar_recursos(ambiente.id, recursos)