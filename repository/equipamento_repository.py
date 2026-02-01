import psycopg2
from psycopg2.extras import RealDictCursor
import os

def get_connection():
    return psycopg2.connect(
        os.environ["postgresql://nexus_6t82_user:2O9D5klSvNu91o0022tuIWY7u3N7eOZE@dpg-d5va85coud1c738c6l1g-a/nexus_6t82"],
        options="-c search_path=nexus"
    )


class EquipamentoRepository:

    @staticmethod
    def listar():
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute("""
                SELECT 
                    e.id,
                    e.name,
                    e.categoria,
                    e.status,
                    e.descricao,
                    e.marca,
                    e.modelo,
                    e.condicao,
                    e.quantidade_disponivel,
                    e.image,
                    e.created_at,
                    STRING_AGG(es.especificacao, ' | ') AS especificacoes
                FROM nexus.equipamentos e
                LEFT JOIN nexus.equipamentos_especificacoes es 
                    ON e.id = es.equipamento_id
                GROUP BY e.id
                ORDER BY e.name
            """)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def buscar_por_id(equipamento_id):
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute("""
                SELECT 
                    e.id,
                    e.name,
                    e.categoria,
                    e.status,
                    e.descricao,
                    e.marca,
                    e.modelo,
                    e.condicao,
                    e.quantidade_disponivel,
                    e.image,
                    e.created_at,
                    STRING_AGG(es.especificacao, ' | ') AS especificacoes
                FROM nexus.equipamentos e
                LEFT JOIN nexus.equipamentos_especificacoes es 
                    ON e.id = es.equipamento_id
                WHERE e.id = %s
                GROUP BY e.id
            """, (equipamento_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def inserir_equipamento(dados):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO nexus.equipamentos
                (name, categoria, status, descricao, marca, modelo, condicao, quantidade_disponivel, image)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (
                dados["name"],
                dados["categoria"],
                dados.get("status", "Disponivel"),
                dados.get("descricao"),
                dados.get("marca"),
                dados.get("modelo"),
                dados.get("condicao"),
                dados.get("quantidade_disponivel", 1),
                dados.get("image")
            ))

            equipamento_id = cursor.fetchone()[0]
            conn.commit()
            return equipamento_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def inserir_especificacoes(equipamento_id, especificacoes):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            for especificacao in especificacoes:
                if especificacao.strip():
                    cursor.execute("""
                        INSERT INTO nexus.equipamentos_especificacoes
                        (equipamento_id, especificacao)
                        VALUES (%s, %s)
                    """, (equipamento_id, especificacao.strip()))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def atualizar_equipamento(equipamento):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE nexus.equipamentos
                SET name = %s,
                    categoria = %s,
                    status = %s,
                    descricao = %s,
                    marca = %s,
                    modelo = %s,
                    condicao = %s,
                    quantidade_disponivel = %s,
                    image = %s
                WHERE id = %s
            """, (
                equipamento.name,
                equipamento.categoria,
                equipamento.status,
                equipamento.descricao,
                equipamento.marca,
                equipamento.modelo,
                equipamento.condicao,
                equipamento.quantidade_disponivel,
                equipamento.image,
                equipamento.id
            ))

            if cursor.rowcount == 0:
                raise ValueError("Equipamento não encontrado")

            cursor.execute("""
                DELETE FROM nexus.equipamentos_especificacoes
                WHERE equipamento_id = %s
            """, (equipamento.id,))

            for especificacao in equipamento.especificacoes:
                if especificacao.strip():
                    cursor.execute("""
                        INSERT INTO nexus.equipamentos_especificacoes
                        (equipamento_id, especificacao)
                        VALUES (%s, %s)
                    """, (equipamento.id, especificacao.strip()))

            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def atualizar_status(equipamento_id, status):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE nexus.equipamentos
                SET status = %s
                WHERE id = %s
            """, (status, equipamento_id))

            if cursor.rowcount == 0:
                raise ValueError("Equipamento não encontrado")

            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
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
                    e.name, 
                    e.categoria, 
                    e.status,
                    e.descricao,
                    e.marca,
                    e.modelo,
                    e.quantidade_disponivel,
                    e.image,
                    STRING_AGG(es.especificacao, ' | ') AS especificacoes
                FROM nexus.equipamentos e
                LEFT JOIN nexus.equipamentos_especificacoes es 
                    ON e.id = es.equipamento_id
                WHERE e.name ILIKE %s
                   OR e.categoria ILIKE %s
                   OR e.descricao ILIKE %s
                GROUP BY e.id
                ORDER BY e.name
            """, (f"%{termo}%", f"%{termo}%", f"%{termo}%"))

            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
    

    

    @staticmethod
    def deletar_equipamento(equipamento_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                DELETE FROM equipamentos
                WHERE id = %s
            """, (equipamento_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

