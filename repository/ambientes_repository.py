import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="jojo4548",
        database="nexus"
    )


class AmbientesRepository:

    @staticmethod
    def listar():
        """Lista todos os ambientes com seus recursos"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

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
                GROUP_CONCAT(r.recursos SEPARATOR ' | ') AS recursos
            FROM Ambientes a
            LEFT JOIN recursos_ambientes r ON r.recursos_id = a.id
            GROUP BY a.id
        """)

        ambientes = cursor.fetchall()
        cursor.close()
        conn.close()
        return ambientes
    @staticmethod
    def inserir_ambiente(ambiente):
        """Insere um novo ambiente"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
    INSERT INTO Ambientes 
    (name, type, capacidade, status, descricao, localizacao, area, image)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
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

        conn.commit()
        ambiente_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return ambiente_id
    

    @staticmethod
    def inserir_recursos(ambiente_id, recursos):
        conn = get_connection()
        cursor = conn.cursor()
        
        for recurso in recursos:
            cursor.execute("""
                INSERT INTO recursos_ambientes (recursos_id, recursos)
                VALUES (%s, %s)
            """, (ambiente_id, recurso))
        
        conn.commit()
        cursor.close()
        conn.close()
    @staticmethod
    def deletar_ambiente(ambiente_id):
      conn = get_connection()
      cursor = conn.cursor()

      cursor.execute(
        "DELETE FROM Ambientes WHERE id = %s",
        (ambiente_id,)
    )

      conn.commit()
      cursor.close()
      conn.close()
    

    @staticmethod
    def deletar_ambiente(ambiente_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM Ambientes WHERE id = %s",
            (ambiente_id,)
        )

        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def atualizar_ambiente(ambiente):
     conn = get_connection()
     cursor = conn.cursor()

     try:
      cursor.execute("""
            UPDATE Ambientes
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
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute("""
        SELECT id, nome, descricao, status
        FROM ambientes
        WHERE nome LIKE %s OR descricao LIKE %s
    """, (f"%{termo}%", f"%{termo}%"))

            return cursor.fetchall()

        finally:
            cursor.close()
            conn.close()
