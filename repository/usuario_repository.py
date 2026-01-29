import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="jojo4548",
        database="nexus"
    )


class UsuarioRepository:

    @staticmethod
    def listar():
        """Lista todos os usuários"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT 
                    id, name, email, cpf, rg, data_nascimento,
                    telefone, endereco, departamento, funcao,
                    role, image, status, created_at
                FROM users
                ORDER BY name
            """)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def buscar_por_id(user_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT 
                    id, name, email, senha,
                    cpf, rg, data_nascimento,
                    telefone, endereco, departamento, funcao,
                    role, image, status, created_at, updated_at
                FROM users
                WHERE id = %s
            """, (user_id,))
            
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    

    @staticmethod
    def buscar_por_email(email):
        """Busca um usuário por email (com senha para autenticação)"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT * 
                FROM users 
                WHERE email = %s
            """, (email,))
            
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()


    @staticmethod
    def adicionar(users):
        """Adiciona um novo usuário"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO users (
                    id, name, email, cpf, rg, data_nascimento,
                    telefone, endereco, departamento, funcao,
                    role, image, status, senha
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                users.id,
                users.name,
                users.email,
                users.cpf,
                users.rg,
                users.data_nascimento,
                users.telefone,
                users.endereco,
                users.departamento,
                users.funcao,
                users.role,
                users.image,
                users.status,
                users.senha
            ))

            conn.commit()
            return users.id

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def atualizar(usuario_id, dados):
        """Atualiza dados de um usuário"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
           

            cursor.execute("""
                UPDATE users
                SET name = %s,
                    email = %s,
                    cpf = %s,
                    rg = %s,
                    data_nascimento = %s,
                    telefone = %s,
                    endereco = %s,
                    departamento = %s,
                    funcao = %s,
                    role = %s,
                    image = %s,
                    status = %s
                WHERE id = %s
            """, (
                dados["name"],
                dados["email"],
                dados["cpf"],
                dados.get("rg"),
                dados.get("data_nascimento"),
                dados.get("telefone"),
                dados.get("endereco"),
                dados.get("departamento"),
                dados.get("funcao"),
                dados["role"],
                dados.get("image"),
                dados["status"],
                usuario_id
            ))

            conn.commit()

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cursor.close()
            conn.close()



    @staticmethod
    def deletar(usuario_id):
        """Remove um usuário (CASCADE deleta dependências automaticamente)"""
        conn = get_connection()
        cursor = conn.cursor()
        try:

            
            cursor.execute("""
                DELETE FROM users WHERE id = %s
            """, (usuario_id,))


            conn.commit()

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def _existe(usuario_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT 1 FROM users WHERE id = %s",
                (str(usuario_id),)
            )
            return cursor.fetchone() is not None
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def atualizar_senha(usuario_id, senha_hash):
        """Atualiza apenas a senha de um usuário"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE users
                SET senha = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            """, (senha_hash, usuario_id))

            conn.commit()
            
        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cursor.close()
            conn.close()
    