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


class RecursosRepository:
    
    # ========== AMBIENTES ==========
    
    @staticmethod
    def listar_ambientes():
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT * FROM nexus.ambientes 
            WHERE status = 'Disponivel' 
            ORDER BY name
        """)
        ambientes = cursor.fetchall()
        cursor.close()
        conn.close()
        return ambientes
    
    @staticmethod
    def buscar_ambiente_por_id(id):
        """Busca um ambiente específico por ID"""
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(
            "SELECT * FROM nexus.ambientes WHERE id = %s",
            (id,)
        )
        ambiente = cursor.fetchone()
        cursor.close()
        conn.close()
        return ambiente
    
    @staticmethod
    def verificar_disponibilidade_ambiente(ambiente_id, data_evento, hora_evento):
        """Verifica se o ambiente está disponível na data/hora especificada"""
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT COUNT(*) AS total 
            FROM nexus.eventos 
            WHERE ambiente_id = %s 
              AND data_evento = %s 
              AND hora_evento = %s
        """, (ambiente_id, data_evento, hora_evento))
        
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        return result["total"] == 0
    
    # ========== EQUIPAMENTOS ==========
    
    @staticmethod
    def listar_equipamentos():
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT * FROM nexus.equipamentos 
            WHERE status = 'Disponivel' 
            ORDER BY name
        """)
        equipamentos = cursor.fetchall()
        cursor.close()
        conn.close()
        return equipamentos
    
    @staticmethod
    def buscar_equipamento_por_id(id):
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(
            "SELECT * FROM nexus.equipamentos WHERE id = %s",
            (id,)
        )
        equipamento = cursor.fetchone()
        cursor.close()
        conn.close()
        return equipamento
    
    @staticmethod
    def verificar_disponibilidade_equipamento(equipamento_id, quantidade, data_evento, hora_evento):
        """Verifica se há equipamentos suficientes disponíveis"""
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Busca a quantidade disponível
        cursor.execute("""
            SELECT quantidade_disponivel 
            FROM nexus.equipamentos 
            WHERE id = %s
        """, (equipamento_id,))
        
        equipamento = cursor.fetchone()
        
        if not equipamento:
            cursor.close()
            conn.close()
            return False
        
        # Verifica quanto já está reservado para o mesmo horário
        cursor.execute("""
            SELECT COALESCE(SUM(ee.quantidade), 0) AS reservado
            FROM nexus.eventos_equipamentos ee
            JOIN nexus.eventos e ON ee.evento_id = e.id
            WHERE ee.equipamento_id = %s
              AND e.data_evento = %s
              AND e.hora_evento = %s
        """, (equipamento_id, data_evento, hora_evento))
        
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        disponivel = equipamento["quantidade_disponivel"] - result["reservado"]
        return disponivel >= quantidade
    
    @staticmethod
    def adicionar_equipamentos_evento(evento_id, equipamentos):
        """Adiciona equipamentos a um evento
        equipamentos: lista de dicts com {equipamento_id, quantidade}
        """
        conn = get_connection()
        cursor = conn.cursor()
        
        for equip in equipamentos:
            cursor.execute("""
                INSERT INTO nexus.eventos_equipamentos 
                (evento_id, equipamento_id, quantidade)
                VALUES (%s, %s, %s)
            """, (
                evento_id,
                equip["equipamento_id"],
                equip["quantidade"]
            ))
        
        conn.commit()
        cursor.close()
        conn.close()
    
    @staticmethod
    def listar_equipamentos_evento(evento_id):
        """Lista todos os equipamentos de um evento"""
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT 
                ee.id,
                ee.quantidade,
                e.id AS equipamento_id,
                e.name,
                e.descricao
            FROM nexus.eventos_equipamentos ee
            JOIN equipamentos e ON ee.equipamento_id = e.id
            WHERE ee.evento_id = %s
        """, (evento_id,))
        
        equipamentos = cursor.fetchall()
        cursor.close()
        conn.close()
        return equipamentos
    
    @staticmethod
    def remover_equipamentos_evento(evento_id):
        """Remove todos os equipamentos de um evento"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            DELETE FROM nexus.eventos_equipamentos 
            WHERE evento_id = %s
        """, (evento_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
