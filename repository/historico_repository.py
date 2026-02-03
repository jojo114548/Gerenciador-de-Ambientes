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

class HistoricoRepository:

    @staticmethod
    def listar_todos():
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute("""
                SELECT
                    he.id,
                    he.agendamento_id,
                    he.user_id,
                    he.type,
                    he.name,
                    he.historico_date,
                    he.start_time,
                    he.end_time,
                    he.purpose,
                    he.status,
                    u.name AS usuario_nome,
                    u.email AS usuario_email
                FROM nexus.historico he
                INNER JOIN nexus.users u ON he.user_id = u.id
                ORDER BY he.historico_date DESC, he.start_time DESC
            """)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def buscar_por_id(historico_id):
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute("""
                SELECT
                    he.id,
                    he.agendamento_id,
                    he.user_id,
                    he.type,
                    he.name,
                    he.historico_date,
                    he.start_time,
                    he.end_time,
                    he.purpose,
                    he.status,
                    u.name AS usuario_nome,
                    u.email AS usuario_email,
                    u.departamento
                FROM nexus.historico he
                INNER JOIN nexus.users u ON he.user_id = u.id
                WHERE he.id = %s
            """, (historico_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def inserir(dados):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # ✅ CORRIGIDO: Usar INSERT com VALUES e RETURNING
            cursor.execute("""
                INSERT INTO nexus.historico (
                    agendamento_id,
                    user_id,
                    type,
                    name,
                    historico_date,
                    start_time,
                    end_time,
                    purpose,
                    status
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s::nexus.status_historico)
                RETURNING id
            """, (
                dados["agendamento_id"],
                dados["user_id"],
                dados["type"],
                dados["name"],
                dados["historico_date"],
                dados["start_time"],
                dados["end_time"],
                dados.get("purpose"),
                dados["status"]
            ))
            historico_id = cursor.fetchone()[0]
            conn.commit()
            return historico_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def listar_por_usuario(user_id):
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute("""
                SELECT
                    he.id,
                    he.agendamento_id,
                    he.type,
                    he.name,
                    he.historico_date,
                    he.start_time,
                    he.end_time,
                    he.purpose,
                    he.status
                FROM nexus.historico he
                WHERE he.user_id = %s
                ORDER BY he.historico_date DESC, he.start_time DESC
            """, (user_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def listar_por_tipo(tipo):
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute("""
                SELECT
                    he.id,
                    he.agendamento_id,
                    he.user_id,
                    he.type,
                    he.name,
                    he.historico_date,
                    he.start_time,
                    he.end_time,
                    he.purpose,
                    he.status,
                    u.name AS usuario_nome,
                    u.email AS usuario_email
                FROM nexus.historico he
             INNER JOIN nexus.users u ON he.user_id = u.id
                WHERE he.type = %s
                ORDER BY he.historico_date DESC, he.start_time DESC
            """, (tipo,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def listar_por_status(status):
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute("""
                SELECT
                    he.id,
                    he.agendamento_id,
                    he.user_id,
                    he.type,
                    he.name,
                    he.historico_date,
                    he.start_time,
                    he.end_time,
                    he.purpose,
                    he.status,
                    u.name AS usuario_nome,
                    u.email AS usuario_email
                FROM nexus.historico he
               INNER JOIN nexus.users u ON he.user_id = u.id
                WHERE he.status = %s
                ORDER BY he.historico_date DESC, he.start_time DESC
            """, (status,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def listar_por_periodo(data_inicio, data_fim):
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute("""
                SELECT
                    he.id,
                    he.agendamento_id,
                    he.user_id,
                    he.type,
                    he.name,
                    he.historico_date,
                    he.start_time,
                    he.end_time,
                    he.purpose,
                    he.status,
                    u.name AS usuario_nome,
                    u.email AS usuario_email
                FROM nexus.historico he
                INNER JOIN nexus.users u ON he.user_id = u.id
                WHERE he.historico_date BETWEEN %s AND %s
                ORDER BY he.historico_date DESC, he.start_time DESC
            """, (data_inicio, data_fim))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def atualizar_status(id, status):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE nexus.historico
                SET status = %s
                WHERE agendamento_id = %s
            """, (status, id))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def atualizar_status_por_id(historico_id, status):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE nexus.historico
                SET status = %s
                WHERE id = %s
            """, (status, historico_id))
            conn.commit()
            return cursor.rowcount
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()
       
    @staticmethod
    def cancelar(historico_id, user_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE nexus.historico
                SET status = 'cancelado'
                WHERE id = %s AND user_id = %s
            """, (historico_id, user_id))
            if cursor.rowcount == 0:
                raise ValueError("Registro não encontrado ou sem permissão")
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def deletar(historico_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                DELETE FROM nexus.historico
                WHERE id = %s
            """, (historico_id,))
            if cursor.rowcount == 0:
                raise ValueError("Registro não encontrado")
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def contar_por_status(user_id=None):
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            query = """
                SELECT status, COUNT(*) AS total
                FROM nexus.historico
            """
            params = []
            if user_id:
                query += " WHERE user_id = %s"
                params.append(user_id)
            query += " GROUP BY status"
            cursor.execute(query, tuple(params))
            return {r["status"]: r["total"] for r in cursor.fetchall()}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def contar_por_tipo(user_id=None):
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            query = """
                SELECT type, COUNT(*) AS total
                FROM nexus.historico
            """
            params = []
            if user_id:
                query += " WHERE user_id = %s"
                params.append(user_id)
            query += " GROUP BY type"
            cursor.execute(query, tuple(params))
            return {r["type"]: r["total"] for r in cursor.fetchall()}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def buscar(termo):
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute("""
                SELECT
                    he.id,
                    he.agendamento_id,
                    he.user_id,
                    he.type,
                    he.name,
                    he.historico_date,
                    he.start_time,
                    he.end_time,
                    he.purpose,
                    he.status,
                    u.name AS usuario_nome,
                    u.email AS usuario_email
                FROM nexus.historico he
              INNER JOIN nexus.users u ON he.user_id = u.id
                WHERE he.name ILIKE %s
                   OR u.name ILIKE %s
                   OR he.purpose ILIKE %s
                ORDER BY he.historico_date DESC, he.start_time DESC
            """, (f"%{termo}%", f"%{termo}%", f"%{termo}%"))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()



    @staticmethod
    def marcar_concluidos():
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
            UPDATE nexus.historico
            SET status = 'Concluido'
            WHERE status = 'Confirmado'
              AND (
                    historico_date < CURRENT_DATE
                    OR (
                        historico_date = CURRENT_DATE
                        AND end_time < CURRENT_TIME
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