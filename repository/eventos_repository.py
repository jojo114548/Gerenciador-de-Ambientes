import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="jojo4548",
        database="nexus"
    )


class EventosRepository:

    @staticmethod
    def listar():
        """Lista todos os eventos com informações do ambiente"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
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
                FROM eventos e
                LEFT JOIN ambientes a ON e.ambiente_id = a.id
                ORDER BY e.data_evento DESC, e.hora_evento DESC
            """)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def buscar_por_id(id):
        """Busca um evento específico por ID com informações do ambiente"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
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
                FROM eventos e
                LEFT JOIN ambientes a ON e.ambiente_id = a.id
                WHERE e.id = %s
            """, (id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def inserir(dados):
        """Insere um novo evento"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO eventos
                (titulo, data_evento, hora_evento, localizacao, descricao,
                 participantes, capacidade, instrutor, tipo, image, ambiente_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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

            evento_id = cursor.lastrowid
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
        """Atualiza dados de um evento"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE eventos
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
        """Remove um evento"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                DELETE FROM eventos WHERE id = %s
            """, (id,))

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
        """Verifica se usuário já está inscrito no evento"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT id
                FROM inscricoes_eventos
                WHERE evento_id = %s AND user_id = %s
            """, (evento_id, user_id))
            return cursor.fetchone() is not None
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def registrar_inscricao(evento_id, user_id):
        """Registra inscrição de um usuário em um evento"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO inscricoes_eventos (evento_id, user_id)
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
        """Cancela inscrição de um usuário em um evento"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                DELETE FROM inscricoes_eventos
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
        """Incrementa contador de participantes do evento"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE eventos
                SET participantes = participantes + 1
                WHERE id = %s
            """, (evento_id,))

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
    def decrementar_participantes(evento_id):
        """Decrementa contador de participantes do evento"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE eventos
                SET participantes = GREATEST(participantes - 1, 0)
                WHERE id = %s
            """, (evento_id,))

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
    def listar_inscricoes(evento_id):
        """Lista todos os usuários inscritos em um evento"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT 
                    u.id,
                    u.name,
                    u.email,
                    u.departamento,
                    u.funcao,
                    ie.created_at as data_inscricao
                FROM inscricoes_eventos ie
                INNER JOIN users u ON ie.user_id = u.id
                WHERE ie.evento_id = %s
                ORDER BY ie.created_at
            """, (evento_id,))

            return cursor.fetchall()

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def listar_eventos_usuario(user_id):
        """Lista todos os eventos em que o usuário está inscrito"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
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
                    ie.created_at as data_inscricao
                FROM inscricoes_eventos ie
                INNER JOIN eventos e ON ie.evento_id = e.id
                LEFT JOIN ambientes a ON e.ambiente_id = a.id
                WHERE ie.user_id = %s
                ORDER BY e.data_evento DESC, e.hora_evento DESC
            """, (user_id,))

            return cursor.fetchall()

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def listar_por_tipo(tipo):
        """Lista eventos filtrados por tipo"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
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
                FROM eventos e
                LEFT JOIN ambientes a ON e.ambiente_id = a.id
                WHERE e.tipo = %s
                ORDER BY e.data_evento DESC, e.hora_evento DESC
            """, (tipo,))

            return cursor.fetchall()

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def listar_proximos():
        """Lista eventos futuros (data >= hoje)"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
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
                FROM eventos e
                LEFT JOIN ambientes a ON e.ambiente_id = a.id
                WHERE e.data_evento >= CURDATE()
                ORDER BY e.data_evento ASC, e.hora_evento ASC
            """)

            return cursor.fetchall()

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def listar_disponiveis():
        """Lista eventos que ainda têm vagas disponíveis"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
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
                FROM eventos e
                LEFT JOIN ambientes a ON e.ambiente_id = a.id
                WHERE e.participantes < e.capacidade
                  AND e.data_evento >= CURDATE()
                ORDER BY e.data_evento ASC, e.hora_evento ASC
            """)

            return cursor.fetchall()

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def verificar_lotacao(evento_id):
        """Verifica se evento está lotado"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT 
                    participantes,
                    capacidade,
                    (participantes >= capacidade) as lotado
                FROM eventos
                WHERE id = %s
            """, (evento_id,))

            resultado = cursor.fetchone()
            return resultado['lotado'] if resultado else True

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def buscar(termo):
        """Busca eventos por título, descrição ou instrutor"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
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
                FROM eventos e
                LEFT JOIN ambientes a ON e.ambiente_id = a.id
                WHERE e.titulo LIKE %s 
                   OR e.descricao LIKE %s
                   OR e.instrutor LIKE %s
                ORDER BY e.data_evento DESC
            """, (f"%{termo}%", f"%{termo}%", f"%{termo}%"))

            return cursor.fetchall()

        finally:
            cursor.close()
            conn.close()