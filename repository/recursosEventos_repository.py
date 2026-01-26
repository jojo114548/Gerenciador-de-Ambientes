import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="jojo4548",
        database="nexus"
    )


class RecursosRepository:
    
    # ========== AMBIENTES ==========
    
    @staticmethod
    def listar_ambientes():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM ambientes WHERE status = 'Disponivel' ORDER BY name")
        ambientes = cursor.fetchall()
        cursor.close()
        conn.close()
        return ambientes
    
    @staticmethod
    def buscar_ambiente_por_id(id):
        """Busca um ambiente específico por ID"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM ambientes WHERE id = %s", (id,))
        ambiente = cursor.fetchone()
        cursor.close()
        conn.close()
        return ambiente
    
    @staticmethod
    def verificar_disponibilidade_ambiente(ambiente_id, data_evento, hora_evento):
        """Verifica se o ambiente está disponível na data/hora especificada"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT COUNT(*) as total FROM eventos 
            WHERE ambiente_id = %s 
            AND data_evento = %s 
            AND hora_evento = %s
        """, (ambiente_id, data_evento, hora_evento))
        
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        return result['total'] == 0
    
    # ========== EQUIPAMENTOS ==========
    
    @staticmethod
    def listar_equipamentos():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM equipamentos WHERE status = 'Disponivel' ORDER BY name")
        equipamentos = cursor.fetchall()
        cursor.close()
        conn.close()
        return equipamentos
    
    @staticmethod
    def buscar_equipamento_por_id(id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM equipamentos WHERE id = %s", (id,))
        equipamento = cursor.fetchone()
        cursor.close()
        conn.close()
        return equipamento
    
    @staticmethod
    def verificar_disponibilidade_equipamento(equipamento_id, quantidade, data_evento, hora_evento):
        """Verifica se há equipamentos suficientes disponíveis"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Busca a quantidade disponível
        cursor.execute("""
            SELECT quantidade_disponivel FROM equipamentos 
            WHERE id = %s
        """, (equipamento_id,))
        
        equipamento = cursor.fetchone()
        
        if not equipamento:
            cursor.close()
            conn.close()
            return False
        
        # Verifica quanto já está reservado para o mesmo horário
        cursor.execute("""
            SELECT COALESCE(SUM(ee.quantidade), 0) as reservado
            FROM eventos_equipamentos ee
            JOIN eventos e ON ee.evento_id = e.id
            WHERE ee.equipamento_id = %s
            AND e.data_evento = %s
            AND e.hora_evento = %s
        """, (equipamento_id, data_evento, hora_evento))
        
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        disponivel = equipamento['quantidade_disponivel'] - result['reservado']
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
                INSERT INTO eventos_equipamentos 
                (evento_id, equipamento_id, quantidade)
                VALUES (%s, %s, %s)
            """, (evento_id, equip['equipamento_id'], equip['quantidade']))
        
        conn.commit()
        cursor.close()
        conn.close()
    
    @staticmethod
    def listar_equipamentos_evento(evento_id):
        """Lista todos os equipamentos de um evento"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT 
                ee.id,
                ee.quantidade,
                e.id as equipamento_id,
                e.name,
                e.descricao
            FROM eventos_equipamentos ee
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
            DELETE FROM eventos_equipamentos 
            WHERE evento_id = %s
        """, (evento_id,))
        
        conn.commit()
        cursor.close()
        conn.close()