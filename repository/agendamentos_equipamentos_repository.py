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
    


class AgendamentoEquipamentoRepository:

    @staticmethod
    def inserir(agendamento: dict):
        """
        Insere um novo agendamento de equipamento
        """
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO nexus.agendamentos_equipamentos
                (equipamento_id, user_id, data, hora_inicio, hora_fim, finalidade, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (
                agendamento["equipamento_id"],
                agendamento["user_id"],
                agendamento["data"],
                agendamento["hora_inicio"],
                agendamento["hora_fim"],
                agendamento["finalidade"],
                agendamento.get("status", "Pendente")  
            ))

            agendamento_id = cursor.fetchone()[0]
            conn.commit()
            return agendamento_id

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def existe_conflito(equipamento_id, data, hora_inicio, hora_fim, agendamento_id=None):
        """
        Verifica conflito de horário para equipamento
        """
        conn = get_connection()
        cursor = conn.cursor()

        try:
            # ✅ CORRIGIDO: Exclui o próprio agendamento se estiver editando
            if agendamento_id:
                cursor.execute("""
                    SELECT 1
                    FROM nexus.agendamentos_equipamentos
                    WHERE equipamento_id = %s
                      AND data = %s
                      AND status NOT IN ('Rejeitado', 'Cancelado')
                      AND id != %s
                      AND (
                          (%s >= hora_inicio AND %s < hora_fim) OR
                          (%s > hora_inicio AND %s <= hora_fim) OR
                          (%s <= hora_inicio AND %s >= hora_fim)
                      )
                    LIMIT 1
                """, (
                    equipamento_id, data, agendamento_id,
                    hora_inicio, hora_inicio,
                    hora_fim, hora_fim,
                    hora_inicio, hora_fim
                ))
            else:
                cursor.execute("""
                    SELECT 1
                    FROM nexus.agendamentos_equipamentos
                    WHERE equipamento_id = %s
                      AND data = %s
                      AND status NOT IN ('Rejeitado', 'Cancelado')
                      AND (
                          (%s >= hora_inicio AND %s < hora_fim) OR
                          (%s > hora_inicio AND %s <= hora_fim) OR
                          (%s <= hora_inicio AND %s >= hora_fim)
                      )
                    LIMIT 1
                """, (
                    equipamento_id, data,
                    hora_inicio, hora_inicio,
                    hora_fim, hora_fim,
                    hora_inicio, hora_fim
                ))

            return cursor.fetchone() is not None

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def buscar_por_id(agendamento_id):
        """Busca agendamento por ID"""
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        try:
            cursor.execute("""
                SELECT 
                    ae.*,
                    e.name AS equipamento_nome,
                    e.categoria,
                    e.marca,
                    e.modelo,
                    u.name AS usuario_nome,
                    u.email AS usuario_email
                FROM nexus.agendamentos_equipamentos ae
                JOIN nexus.equipamentos e ON e.id = ae.equipamento_id
                JOIN nexus.users u ON u.id = ae.user_id
                WHERE ae.id = %s
            """, (agendamento_id,))

            return cursor.fetchone()

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def listar_por_equipamento(equipamento_id):
        """Lista todos os agendamentos de um equipamento"""
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        try:
            cursor.execute("""
                SELECT 
                    ae.*,
                    u.name AS usuario_nome,
                    u.email AS usuario_email
                FROM nexus.agendamentos_equipamentos ae
                JOIN nexus.users u ON u.id = ae.user_id
                WHERE ae.equipamento_id = %s
                ORDER BY ae.data DESC, ae.hora_inicio DESC
            """, (equipamento_id,))

            return cursor.fetchall()

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def listar_por_usuario(user_id):
        """Lista todos os agendamentos feitos por um usuário"""
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        try:
            cursor.execute("""
                SELECT 
                    ae.*,
                    e.name AS equipamento_nome,
                    e.categoria,
                    e.marca
                FROM nexus.agendamentos_equipamentos ae
                JOIN nexus.equipamentos e ON e.id = ae.equipamento_id
                WHERE ae.user_id = %s
                ORDER BY ae.data DESC, ae.hora_inicio DESC
            """, (user_id,))

            return cursor.fetchall()

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def listar_todos():
        """Lista todos os agendamentos"""
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        try:
            cursor.execute("""
                SELECT 
                    ae.*,
                    e.name AS equipamento_nome,
                    e.categoria,
                    u.name AS usuario_nome,
                    u.email AS usuario_email
                FROM nexus.agendamentos_equipamentos ae
                JOIN nexus.equipamentos e ON e.id = ae.equipamento_id
                JOIN nexus.users u ON u.id = ae.user_id
                ORDER BY ae.data DESC, ae.hora_inicio DESC
            """)

            return cursor.fetchall()

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def atualizar_status(agendamento_id, status):
        """Atualiza o status do agendamento"""
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                UPDATE nexus.agendamentos_equipamentos
                SET status = %s
                WHERE id = %s
            """, (status, agendamento_id))

            if cursor.rowcount == 0:
                raise ValueError("Agendamento não encontrado")

            conn.commit()

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def deletar(agendamento_id):
        """Remove o agendamento"""
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                DELETE FROM nexus.agendamentos_equipamentos
                WHERE id = %s
            """, (agendamento_id,))

            if cursor.rowcount == 0:
                raise ValueError("Agendamento não encontrado")

            conn.commit()

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cursor.close()
            conn.close()