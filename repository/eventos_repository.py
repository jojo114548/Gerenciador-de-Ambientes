import psycopg2
from psycopg2.extras import RealDictCursor
import os

def get_connection():
    return psycopg2.connect(
        os.environ["postgresql://nexus_6t82_user:2O9D5klSvNu91o0022tuIWY7u3N7eOZE@dpg-d5va85coud1c738c6l1g-a/nexus_6t82"],
        options="-c search_path=nexus"
    )


class EventosRepository:

    @staticmethod
    def listar():
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute("""
                SELECT 
                    e.id,
                    e.titulo,
                    e.data_evento,
                    e.hora_evento,
                    e.localizacao,
                    e.descricao,
                    e.participantes,
                    e.capacidade,
                    e.instrutor,
                    e.tipo,
                    e.image,
                    e.ambiente_id,
                    e.created_at,
                    a.name AS ambiente_nome,
                    a.capacidade AS ambiente_capacidade,
                    a.type AS ambiente_tipo
                FROM nexus.eventos e
                LEFT JOIN nexus.ambientes a ON e.ambiente_id = a.id
                ORDER BY e.data_evento DESC, e.hora_evento DESC
            """)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def buscar_por_id(id):
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute("""
                SELECT 
                    e.id,
                    e.titulo,
                    e.data_evento,
                    e.hora_evento,
                    e.localizacao,
                    e.descricao,
                    e.participantes,
                    e.capacidade,
                    e.instrutor,
                    e.tipo,
                    e.image,
                    e.ambiente_id,
                    e.created_at,
                    a.name AS ambiente_nome,
                    a.capacidade AS ambiente_capacidade,
                    a.type AS ambiente_tipo,
                    a.localizacao AS ambiente_localizacao
                FROM nexus.eventos e
                LEFT JOIN nexus.ambientes a ON e.ambiente_id = a.id
                WHERE e.id = %s
            """, (id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def inserir(dados):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO nexus.eventos
                (titulo, data_evento, hora_evento, localizacao, descricao,
                 participantes, capacidade, instrutor, tipo, image, ambiente_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (
                dados["titulo"],
                dados["data_evento"],
                dados["hora_evento"],
                dados["localizacao"],
                dados.get("descricao"),
                dados.get("participantes", 0),
                dados["capacidade"],
                dados.get("instrutor"),
                dados["tipo"],
                dados.get("image"),
                dados.get("ambiente_id")
            ))

            evento_id = cursor.fetchone()[0]
            conn.commit()
            return evento_id

        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def atualizar(id, dados):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE nexus.eventos
                SET titulo = %s,
                    data_evento = %s,
                    hora_evento = %s,
                    localizacao = %s,
                    descricao = %s,
                    capacidade = %s,
                    instrutor = %s,
                    tipo = %s,
                    image = %s,
                    ambiente_id = %s
                WHERE id = %s
            """, (
                dados["titulo"],
                dados["data_evento"],
                dados["hora_evento"],
                dados["localizacao"],
                dados.get("descricao"),
                dados["capacidade"],
                dados.get("instrutor"),
                dados["tipo"],
                dados.get("image"),
                dados.get("ambiente_id"),
                id
            ))

            if cursor.rowcount == 0:
                raise ValueError("Evento não encontrado")

            conn.commit()
            return True

        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def deletar(id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM nexus.eventos WHERE id = %s", (id,))
            if cursor.rowcount == 0:
                raise ValueError("Evento não encontrado")
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def usuario_ja_inscrito(evento_id, user_id):
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute("""
                SELECT id
                FROM nexus.inscricoes_eventos
                WHERE evento_id = %s AND user_id = %s
            """, (evento_id, user_id))
            return cursor.fetchone() is not None
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def registrar_inscricao(evento_id, user_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO nexus.inscricoes_eventos (evento_id, user_id)
                VALUES (%s, %s)
            """, (evento_id, user_id))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def cancelar_inscricao(evento_id, user_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                DELETE FROM nexus.inscricoes_eventos
                WHERE evento_id = %s AND user_id = %s
            """, (evento_id, user_id))

            if cursor.rowcount == 0:
                raise ValueError("Inscrição não encontrada")

            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def incrementar_participantes(evento_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE nexus.eventos
                SET participantes = participantes + 1
                WHERE id = %s
            """, (evento_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def decrementar_participantes(evento_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE nexus.eventos
                SET participantes = GREATEST(participantes - 1, 0)
                WHERE id = %s
            """, (evento_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def listar_proximos():
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute("""
                SELECT 
                    e.id,
                    e.titulo,
                    e.data_evento,
                    e.hora_evento,
                    e.localizacao,
                    e.descricao,
                    e.participantes,
                    e.capacidade,
                    e.instrutor,
                    e.tipo,
                    e.image,
                    a.name AS ambiente_nome,
                    a.capacidade AS ambiente_capacidade
                FROM nexus.eventos e
                LEFT JOIN nexus.ambientes a ON e.ambiente_id = a.id
                WHERE e.data_evento >= CURRENT_DATE
                ORDER BY e.data_evento ASC, e.hora_evento ASC
            """)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def listar_disponiveis():
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute("""
                SELECT 
                    e.id,
                    e.titulo,
                    e.data_evento,
                    e.hora_evento,
                    e.localizacao,
                    e.descricao,
                    e.participantes,
                    e.capacidade,
                    e.instrutor,
                    e.tipo,
                    e.image,
                    a.name AS ambiente_nome,
                    (e.capacidade - e.participantes) AS vagas_disponiveis
                FROM nexus.eventos e
                LEFT JOIN nexus.ambientes a ON e.ambiente_id = a.id
                WHERE e.participantes < e.capacidade
                  AND e.data_evento >= CURRENT_DATE
                ORDER BY e.data_evento ASC, e.hora_evento ASC
            """)
            return cursor.fetchall()
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
                    e.id,
                    e.titulo,
                    e.data_evento,
                    e.hora_evento,
                    e.localizacao,
                    e.descricao,
                    e.participantes,
                    e.capacidade,
                    e.instrutor,
                    e.tipo,
                    e.image,
                    a.name AS ambiente_nome
                FROM nexus.eventos e
                LEFT JOIN nexus.ambientes a ON e.ambiente_id = a.id
                WHERE e.titulo ILIKE %s
                   OR e.descricao ILIKE %s
                   OR e.instrutor ILIKE %s
                ORDER BY e.data_evento DESC
            """, (f"%{termo}%", f"%{termo}%", f"%{termo}%"))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
