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

class PendenteRepository:

    @staticmethod
    def inserir(dados):
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        try:
            cursor.execute("""
                INSERT INTO nexus.pendentes_ambientes
                    (agendamento_id, user_id, status)
                VALUES (%s, %s, %s)
                RETURNING id
            """, (
                dados["agendamento_id"],
                dados["user_id"],
                dados["status"]
            ))

            pendente_id = cursor.fetchone()["id"]
            conn.commit()

            return {
                "id": pendente_id,
                "agendamento_id": dados["agendamento_id"],
                "user_id": dados["user_id"],
                "status": dados["status"]
            }

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def buscar_por_id(pendente_id):
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("""
            SELECT
                p.id AS pendente_id,
                p.status,
                p.user_id,

                a.id AS agendamento_id,
                a.ambiente_id,
                a.data,
                a.hora_inicio,
                a.hora_fim,
                a.finalidade,

                amb.name AS ambiente_nome
            FROM nexus.pendentes_ambientes p
            JOIN nexus.agendamentos a ON a.id = p.agendamento_id
            JOIN nexus.ambientes amb ON amb.id = a.ambiente_id
            WHERE p.id = %s
        """, (pendente_id,))

        result = cursor.fetchone()
        cursor.close()
        conn.close()

        return result

    @staticmethod
    def listar():
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("""
            SELECT
                p.id AS pendente_id,
                p.agendamento_id,
                p.user_id,
                p.status,

                amb.id AS ambiente_id,
                amb.name AS ambiente_nome,

                a.data,
                a.hora_inicio,
                a.hora_fim,
                a.finalidade
            FROM nexus.pendentes_ambientes p
            JOIN nexus.agendamentos a ON a.id = p.agendamento_id
            JOIN nexus.ambientes amb ON amb.id = a.ambiente_id
        """)

        result = cursor.fetchall()
        cursor.close()
        conn.close()

        return result

    @staticmethod
    def atualizar_status(pendente_id, status):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE nexus.pendentes_ambientes
            SET status = %s
            WHERE id = %s
        """, (status, pendente_id))

        conn.commit()
        cursor.close()
        conn.close()
