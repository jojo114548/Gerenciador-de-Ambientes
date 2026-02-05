import psycopg2
from psycopg2.extras import RealDictCursor
import os

def get_connection():
    try:
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            raise ValueError("DATABASE_URL não encontrada no .env")
        conn = psycopg2.connect(db_url)
        return conn
    except Exception as e:
        raise


class HistoricoEquipamentoRepository:

    @staticmethod
    def inserir(dados: dict):
        """
        ✅ CORRIGIDO: Insere registro no histórico de equipamentos
        """
        conn = get_connection()
        cursor = conn.cursor()

        try:
            print(f"\n=== INSERIR HISTÓRICO EQUIPAMENTO ===")
            print(f"Dados recebidos: {dados}")
            
            # ✅ Verificar se todos os campos estão presentes
            campos_obrigatorios = [
                "agendamento_id", "equipamento_id", "user_id",
                "equipamento_nome", "data_equip", "hora_inicio",
                "hora_fim", "finalidade", "status"
            ]
            
            for campo in campos_obrigatorios:
                if campo not in dados:
                    raise ValueError(f"Campo obrigatório ausente: {campo}")
                if dados[campo] is None:
                    raise ValueError(f"Campo {campo} não pode ser NULL")
            
            # ✅ CORRIGIDO: Executar INSERT com VALUES e RETURNING
            cursor.execute("""
                INSERT INTO nexus.historico_equipamentos (
                    agendamento_id,
                    equipamento_id,
                    user_id,
                    equipamento_nome,
                    data_equip,
                    hora_inicio,
                    hora_fim,
                    finalidade,
                    status
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s::nexus.status_historico)
                RETURNING id
            """, (
                dados["agendamento_id"],
                dados["equipamento_id"],
                dados["user_id"],
                dados["equipamento_nome"],
                dados["data_equip"],
                dados["hora_inicio"],
                dados["hora_fim"],
                dados["finalidade"],
                dados["status"]
            ))

            historico_id = cursor.fetchone()[0]
            conn.commit()
            
            print(f"✅ Histórico inserido com sucesso! ID: {historico_id}")
            print(f"=== FIM INSERIR HISTÓRICO ===\n")
            
            return historico_id

        except psycopg2.Error as e:
            conn.rollback()
            print(f"❌ ERRO PostgreSQL ao inserir histórico:")
            print(f"   Código: {e.pgcode}")
            print(f"   Mensagem: {e.pgerror}")
            raise
            
        except Exception as e:
            conn.rollback()
            print(f"❌ ERRO ao inserir histórico: {e}")
            import traceback
            traceback.print_exc()
            raise
            
        finally:
            cursor.close()
            conn.close()

    
    @staticmethod
    def listar():
        """Lista todos os equipamentos com suas especificações"""
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute("""
                SELECT
                    he.id,
                    he.agendamento_id,
                    he.equipamento_id,
                    he.user_id,
                    he.equipamento_nome,
                    he.data_equip,
                    he.hora_inicio,
                    he.hora_fim,
                    he.finalidade,
                    he.status,
                    he.criado_em,
                    u.name AS usuario_nome,
                    u.email AS usuario_email,
                    e.categoria,
                    e.marca,
                    e.modelo
                FROM nexus.historico_equipamentos he
                INNER JOIN nexus.users u ON he.user_id = u.id
                LEFT JOIN nexus.equipamentos e ON e.id = he.equipamento_id
                ORDER BY he.data_equip DESC, he.hora_inicio DESC
            """)
              
                    
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def buscar_por_id(historico_id):
        """Busca um histórico por ID"""
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            print(f"\n=== BUSCAR HISTÓRICO POR ID ===")
            print(f"ID buscado: {historico_id}")
            
            cursor.execute("""
                SELECT
                    id,
                    agendamento_id,
                    equipamento_id,
                    user_id,
                    equipamento_nome,
                    data_equip,
                    hora_inicio,
                    hora_fim,
                    finalidade,
                    status,
                    criado_em
                FROM nexus.historico_equipamentos
                WHERE id = %s
            """, (historico_id,))
            
            resultado = cursor.fetchone()
            
            print(f"Resultado encontrado: {resultado}")
            print(f"=== FIM BUSCAR ===\n")
            
            return resultado
            
        except Exception as e:
            print(f"❌ ERRO ao buscar histórico: {e}")
            import traceback
            traceback.print_exc()
            return None
        finally:
            cursor.close()
            conn.close()
      
                 


    @staticmethod
    def listar_por_usuario(user_id):
        """Lista histórico de um usuário"""
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute("""
                SELECT
                    he.*,
                    e.categoria,
                    e.marca,
                    e.modelo
                FROM nexus.historico_equipamentos he
                LEFT JOIN nexus.equipamentos e ON e.id = he.equipamento_id
                WHERE he.user_id = %s
                ORDER BY he.data_equip DESC, he.hora_inicio DESC
            """, (user_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def listar_por_equipamento(equipamento_id):
        """Lista histórico de um equipamento"""
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute("""
                SELECT
                    he.*,
                    u.name AS usuario_nome,
                    u.email AS usuario_email
                FROM nexus.historico_equipamentos he
                INNER JOIN nexus.users u ON he.user_id = u.id
                WHERE he.equipamento_id = %s
                ORDER BY he.data_equip DESC, he.hora_inicio DESC
            """, (equipamento_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def marcar_concluidos():
        """Marca agendamentos concluídos automaticamente"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE nexus.historico_equipamentos
                SET status = 'Concluido'
                WHERE status = 'Confirmado'
                  AND (
                        data_equip < CURRENT_DATE
                        OR (
                            data_equip = CURRENT_DATE
                            AND hora_fim <= CURRENT_TIME
                        )
                  )
            """)
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    
    @staticmethod
    def atualizar_status_por_id(historicoEquip_id, status):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE nexus.historico_equipamentos
                SET status = %s
                WHERE id = %s
            """, (status, historicoEquip_id))
            conn.commit()
            return cursor.rowcount
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()


    @staticmethod
    def buscar_por_agendamento(agendamento_id):
        """ Verifica se já existe histórico para um agendamento"""
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            print(f"\n Verificando se já existe histórico para agendamento {agendamento_id}...")
            
            cursor.execute("""
                SELECT id, status, equipamento_nome, criado_em
                FROM nexus.historico_equipamentos
                WHERE agendamento_id = %s
                ORDER BY criado_em DESC
                LIMIT 1
            """, (agendamento_id,))
            
            resultado = cursor.fetchone()
            
            return resultado
            
        finally:
            cursor.close()
            conn.close()