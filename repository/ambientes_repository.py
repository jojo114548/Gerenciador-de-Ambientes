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


class AmbientesRepository:

    @staticmethod
    def listar():
        """Lista todos os ambientes com seus recursos"""
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute("""
                SELECT 
                    a.id,
                    a.name,
                    a.capacidade,
                    a.status,
                    a.descricao,
                    a.localizacao,
                    a.area,
                    a.image,
                    STRING_AGG(r.recursos, ' | ') AS recursos
                FROM nexus.ambientes a
                LEFT JOIN nexus.recursos_ambientes r 
                    ON r.recursos_id = a.id
                GROUP BY a.id, a.name, a.capacidade, a.status, a.descricao, a.localizacao, a.area, a.image
                ORDER BY a.name
            """)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def inserir_ambiente(ambiente):
        """Insere um novo ambiente"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            
            cursor.execute("""
                INSERT INTO nexus.ambientes 
                (name, type, capacidade, status, descricao, localizacao, area, image)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (
                ambiente.name,
                ambiente.type,
                ambiente.capacidade,
                ambiente.status,
                ambiente.descricao,
                ambiente.localizacao,
                ambiente.area,
                ambiente.image
            ))

            ambiente_id = cursor.fetchone()[0]
            conn.commit()
            return ambiente_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def inserir_recursos(ambiente_id, recursos):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            for recurso in recursos:
                cursor.execute("""
                    INSERT INTO nexus.recursos_ambientes (recursos_id, recursos)
                    VALUES (%s, %s)
                """, (ambiente_id, recurso))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def deletar_ambiente(ambiente_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # 1️⃣ remove dependências
            cursor.execute("""
                DELETE FROM nexus.recursos_ambientes
                WHERE recursos_id = %s
            """, (ambiente_id,))

            # 2️⃣ remove o ambiente
            cursor.execute("""
                DELETE FROM nexus.ambientes
                WHERE id = %s
            """, (ambiente_id,))

            if cursor.rowcount == 0:
                raise ValueError("Ambiente não encontrado")

            conn.commit()

        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def atualizar_ambiente(ambiente):
        """Atualiza um ambiente existente"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # 1️⃣ Atualiza os dados do ambiente
            cursor.execute("""
                UPDATE nexus.ambientes
                SET name = %s,
                    type = %s,
                    capacidade = %s,
                    status = %s,
                    descricao = %s,
                    localizacao = %s,
                    area = %s,
                    image = %s
                WHERE id = %s
            """, (
                ambiente.name,
                ambiente.type,
                ambiente.capacidade,
                ambiente.status,
                ambiente.descricao,
                ambiente.localizacao,
                ambiente.area,
                ambiente.image,
                ambiente.id
            ))

            if cursor.rowcount == 0:
                raise ValueError("Ambiente não encontrado")

            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def atualizar_recursos(ambiente_id, recursos):
        """Atualiza os recursos de um ambiente"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # 1️⃣ Remove recursos antigos
            cursor.execute("""
                DELETE FROM nexus.recursos_ambientes
                WHERE recursos_id = %s
            """, (ambiente_id,))

            # 2️⃣ Insere novos recursos
            for recurso in recursos:
                cursor.execute("""
                    INSERT INTO nexus.recursos_ambientes (recursos_id, recursos)
                    VALUES (%s, %s)
                """, (ambiente_id, recurso))

            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
        
    @staticmethod
    def buscar(termo):
        """Busca ambientes por nome ou descrição"""
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute("""
                SELECT 
                    id,
                    name,
                    descricao,
                    status
                FROM nexus.ambientes
                WHERE name ILIKE %s
                   OR descricao ILIKE %s
                ORDER BY name
            """, (f"%{termo}%", f"%{termo}%"))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()