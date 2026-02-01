import psycopg2
from psycopg2.extras import RealDictCursor
import os

def get_connection():
    return psycopg2.connect(
        os.environ["postgresql://nexus_6t82_user:2O9D5klSvNu91o0022tuIWY7u3N7eOZE@dpg-d5va85coud1c738c6l1g-a/nexus_6t82"],
        options="-c search_path=nexus"
    )


class NotificacaoRepository:

    @staticmethod
    def criar(users_id, titulo, mensagem, tipo):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
        INSERT INTO nexus.notificacoes (user_id, titulo, mensagem, tipo)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (users_id, titulo, mensagem, tipo))

        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def listar_nao_lidas(users_id):
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        sql = """
        SELECT id, titulo, mensagem, tipo, data_criacao
        FROM nexus.notificacoes
        WHERE user_id = %s AND lida = FALSE
        ORDER BY data_criacao DESC
        """
        cursor.execute(sql, (users_id,))
        dados = cursor.fetchall()

        cursor.close()
        conn.close()

        return dados

    @staticmethod
    def marcar_como_lida(notificacao_id):
        conn = get_connection()
        cursor = conn.cursor()

        sql = "UPDATE nexus.notificacoes SET lida = TRUE WHERE id = %s"
        cursor.execute(sql, (notificacao_id,))

        conn.commit()
        linhas = cursor.rowcount

        cursor.close()
        conn.close()

        return linhas > 0

    @staticmethod
    def contar_nao_lidas(users_id):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
        SELECT COUNT(*) FROM nexus.notificacoes
        WHERE users_id = %s AND lida = FALSE
        """
        cursor.execute(sql, (users_id,))
        total = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return total
