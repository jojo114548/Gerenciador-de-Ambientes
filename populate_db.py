"""
Script para popular o banco de dados com dados de exemplo
Não precisa reinicializar o banco - apenas adiciona os dados
"""

import psycopg2
from psycopg2.extras import execute_values
import os
from dotenv import load_dotenv
import bcrypt
import uuid
from datetime import datetime, date, time

# Carregar variáveis de ambiente
load_dotenv()

def get_db_connection():
    """Estabelece conexão com o PostgreSQL"""
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5432'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'postgres')
    )

def hash_password(password):
    """Gera hash bcrypt de uma senha"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def insert_users(cursor):
    """Insere usuários de exemplo"""
    print("📝 Inserindo usuários...")
    
    users = [
        (
            str(uuid.uuid4()),
            'João da Silva',
            'joao.silva@exemplo.com',
            '12345678901',
            'MG1234567',
            date(1990, 5, 15),
            '82987654321',
            'Rua das Flores, 123',
            'Tecnologia',
            'Desenvolvedor',
            'admin',
            None,
            'ativo',
            hash_password('senha123')
        ),
        (
            str(uuid.uuid4()),
            'Maria Santos',
            'maria.santos@exemplo.com',
            '98765432109',
            'MG9876543',
            date(1992, 8, 20),
            '82976543210',
            'Av. Principal, 456',
            'Marketing',
            'Analista',
            'user',
            None,
            'ativo',
            hash_password('senha123')
        ),
        (
            str(uuid.uuid4()),
            'Carlos Oliveira',
            'carlos.oliveira@exemplo.com',
            '11122233344',
            'MG1112223',
            date(1988, 3, 10),
            '82965432109',
            'Rua do Comércio, 789',
            'Gestão',
            'Moderador',
            'user',
            None,
            'ativo',
            hash_password('senha123')
        ),
        (
            str(uuid.uuid4()),
            'Ana Costa',
            'ana.costa@exemplo.com',
            '55566677788',
            'MG5556667',
            date(1995, 11, 25),
            '82954321098',
            'Praça Central, 321',
            'Design',
            'Designer',
            'user',
            None,
            'ativo',
            hash_password('senha123')
        ),
        (
            str(uuid.uuid4()),
            'Pedro Almeida',
            'pedro.almeida@exemplo.com',
            '99988877766',
            'MG9998887',
            date(1987, 7, 5),
            '82943210987',
            'Rua Nova, 654',
            'Vendas',
            'Gerente',
            'user',
            None,
            'inativo',
            hash_password('senha123')
        )
    ]
    
    insert_query = """
        INSERT INTO nexus.users 
        (id, name, email, cpf, rg, data_nascimento, telefone, endereco, 
         departamento, funcao, role, image, status, senha)
        VALUES %s
        ON CONFLICT (email) DO NOTHING
    """
    
    execute_values(cursor, insert_query, users)
    print(f"✅ {len(users)} usuários inseridos")

def insert_ambientes(cursor):
    """Insere ambientes de exemplo"""
    print("📝 Inserindo ambientes...")
    
    ambientes = [
        (
            'Sala de Reuniões A',
            'sala',
            12,
            'Disponivel',
            'Sala moderna equipada com TV de 55 polegadas, sistema de videoconferência profissional, quadro branco interativo e ar-condicionado. Perfeita para reuniões corporativas, apresentações e workshops.',
            '2º andar',
            '35m²',
            'https://images.unsplash.com/photo-1497366216548-37526070297c?w=800'
        ),
        (
            'Laboratório de Informática',
            'laboratorio',
            30,
            'Disponivel',
            'Laboratório completo com computadores de última geração, monitores de alta resolução e software especializado para desenvolvimento, design e análise de dados. Ambiente climatizado e confortável.',
            '1º andar',
            '120m²',
            'https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=800'
        ),
        (
            'Auditório Principal',
            'auditorio',
            100,
            'Disponivel',
            'Auditório moderno com assentos confortáveis, sistema de som profissional, iluminação cênica e recursos audiovisuais de ponta. Ideal para palestras, apresentações e eventos corporativos de grande porte.',
            'Térreo',
            '250m²',
            'https://images.unsplash.com/photo-1475721027785-f74eccf877e2?w=800'
        ),
        (
            'Sala de Criação',
            'sala',
            8,
            'Disponivel',
            'Espaço criativo e descontraído, ideal para brainstorming, sessões de design thinking e trabalho colaborativo. Ambiente flexível com mobiliário modulável.',
            '3º andar',
            '45m²',
            'https://images.unsplash.com/photo-1497366811353-6870744d04b2?w=800'
        ),
        (
            'Estúdio Multimídia',
            'estudio',
            15,
            'ocupado',
            'Estúdio profissional para gravação de vídeos, podcasts e produção de conteúdo digital. Equipado com isolamento acústico e equipamentos de áudio e vídeo de alta qualidade.',
            '2º andar',
            '60m²',
            'https://images.unsplash.com/photo-1598488035139-bdbb2231ce04?w=800'
        ),
        (
            'Sala de Treinamento',
            'sala',
            25,
            'Disponivel',
            'Sala versátil projetada para treinamentos, cursos e capacitações. Layout flexível que pode ser adaptado para diferentes necessidades pedagógicas.',
            '1º andar',
            '80m²',
            'https://images.unsplash.com/photo-1524178232363-1fb2b075b655?w=800'
        )
    ]
    
    insert_query = """
        INSERT INTO nexus.ambientes 
        (name, type, capacidade, status, descricao, localizacao, area, image)
        VALUES %s
        RETURNING id
    """
    
    cursor.execute("SELECT COUNT(*) FROM nexus.ambientes")
    if cursor.fetchone()[0] > 0:
        print("⚠️  Ambientes já existem, pulando inserção...")
        return
    
    execute_values(cursor, insert_query, ambientes)
    ambiente_ids = [row[0] for row in cursor.fetchall()]
    print(f"✅ {len(ambientes)} ambientes inseridos")
    
    # Inserir recursos dos ambientes
    insert_recursos_ambientes(cursor, ambiente_ids)

def insert_recursos_ambientes(cursor, ambiente_ids):
    """Insere recursos de cada ambiente"""
    print("📝 Inserindo recursos dos ambientes...")
    
    recursos_por_ambiente = [
        [  # Sala de Reuniões A
            "TV 55 polegadas", "Sistema de videoconferência", "Quadro branco",
            "Ar condicionado", "Wi-Fi de alta velocidade", "Mesa de reunião executiva",
            "Cadeiras ergonômicas", "Tomadas em todos os lugares"
        ],
        [  # Laboratório de Informática
            "30 computadores", "Projetor 4K", "Software especializado",
            "Rede de alta velocidade", "Estações de trabalho individuais",
            "Ar condicionado duplo", "Iluminação ajustável", "Sistema de som ambiente"
        ],
        [  # Auditório Principal
            "Sistema de som profissional", "Projetor de alta resolução", "Palco amplo",
            "Iluminação cênica", "Assentos estofados", "Telão de 5 metros",
            "Microfones sem fio", "Camarim anexo"
        ],
        [  # Sala de Criação
            "Móveis modulares", "Quadros brancos nas paredes", "Post-its e materiais",
            "Almofadas e puffs", "Iluminação natural", "TV para apresentações",
            "Coffee point", "Decoração inspiradora"
        ],
        [  # Estúdio Multimídia
            "Isolamento acústico", "Câmeras profissionais", "Microfones de estúdio",
            "Iluminação de três pontos", "Chroma key verde", "Mesa de edição",
            "Monitores de referência", "Computador para edição"
        ],
        [  # Sala de Treinamento
            "Mesas e cadeiras móveis", "Projetor interativo", "Sistema de áudio",
            "Câmera para gravação", "Quadro flip chart", "Material didático",
            "Ar condicionado", "Acesso para PCD"
        ]
    ]
    
    recursos_data = []
    for i, ambiente_id in enumerate(ambiente_ids[:len(recursos_por_ambiente)]):
        for recurso in recursos_por_ambiente[i]:
            recursos_data.append((ambiente_id, recurso))
    
    insert_query = """
        INSERT INTO nexus.recursos_ambientes (recursos_id, recursos)
        VALUES %s
    """
    
    execute_values(cursor, insert_query, recursos_data)
    print(f"✅ {len(recursos_data)} recursos inseridos")

def insert_equipamentos(cursor):
    """Insere equipamentos de exemplo"""
    print("📝 Inserindo equipamentos...")
    
    equipamentos = [
        (
            'Projetor 4K Sony',
            'Audiovisual',
            'Disponivel',
            'Projetor de alta definição 4K da Sony, com 3500 lumens de brilho, ideal para apresentações profissionais em ambientes com iluminação ambiente. Suporta HDMI, USB e conexão wireless.',
            'Sony',
            'VPL-VW270ES',
            'Excelente',
            'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=800',
            3
        ),
        (
            'Câmera Canon EOS R5',
            'Fotografia',
            'Disponivel',
            'Câmera profissional full-frame com sensor de 45MP e gravação de vídeo 8K. Perfeita para produções de alta qualidade, eventos e conteúdo digital premium.',
            'Canon',
            'EOS R5',
            'Novo',
            'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=800',
            2
        ),
        (
            'Notebook Dell XPS 15',
            'Informática',
            'Disponivel',
            'Notebook de alto desempenho com processador Intel Core i9, 32GB de RAM e placa de vídeo dedicada NVIDIA RTX 4060. Ideal para edição de vídeo, modelagem 3D e desenvolvimento.',
            'Dell',
            'XPS 15 9530',
            'Excelente',
            'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=800',
            5
        ),
        (
            'Microfone Shure SM7B',
            'Áudio',
            'ocupado',
            'Microfone dinâmico profissional usado em estúdios do mundo todo. Excelente para gravação de voz, podcasts e transmissões ao vivo. Rejeição superior de ruídos externos.',
            'Shure',
            'SM7B',
            'Excelente',
            'https://images.unsplash.com/photo-1590602847861-f357a9332bbc?w=800',
            4
        ),
        (
            'Tablet iPad Pro 12.9',
            'Informática',
            'Disponivel',
            'iPad Pro com tela Liquid Retina XDR de 12.9 polegadas e chip M2. Perfeito para design, ilustração, anotações e apresentações. Inclui Apple Pencil e Magic Keyboard.',
            'Apple',
            'iPad Pro 6ª geração',
            'Novo',
            'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=800',
            6
        ),
        (
            'Kit Iluminação LED',
            'Iluminação',
            'Disponivel',
            'Kit completo de iluminação profissional com três painéis LED ajustáveis, suportes de tripé e case de transporte. Ideal para gravações de vídeo e fotografia.',
            'Godox',
            'LED500LRC',
            'Excelente',
            'https://images.unsplash.com/photo-1492619375914-88005aa9e8fb?w=800',
            3
        )
    ]
    
    insert_query = """
        INSERT INTO nexus.equipamentos 
        (name, categoria, status, descricao, marca, modelo, condicao, image, quantidade_disponivel)
        VALUES %s
        RETURNING id
    """
    
    cursor.execute("SELECT COUNT(*) FROM nexus.equipamentos")
    if cursor.fetchone()[0] > 0:
        print("⚠️  Equipamentos já existem, pulando inserção...")
        return
    
    execute_values(cursor, insert_query, equipamentos)
    equipamento_ids = [row[0] for row in cursor.fetchall()]
    print(f"✅ {len(equipamentos)} equipamentos inseridos")
    
    # Inserir especificações
    insert_especificacoes(cursor, equipamento_ids)

def insert_especificacoes(cursor, equipamento_ids):
    """Insere especificações dos equipamentos"""
    print("📝 Inserindo especificações dos equipamentos...")
    
    especificacoes_por_equipamento = [
        [  # Projetor 4K Sony
            "Resolução 4K (3840 x 2160)", "Brilho: 3500 lumens", "Contraste: 10.000:1",
            "HDMI, USB, WiFi", "Correção trapezoidal", "Zoom óptico 1.5x",
            "Alto-falantes integrados 10W", "Controle remoto incluído"
        ],
        [  # Câmera Canon EOS R5
            "Sensor Full-Frame 45MP", "Vídeo 8K a 30fps", "IBIS de 8 stops",
            "Autofoco Dual Pixel", "Tela touch articulada", "WiFi e Bluetooth",
            "Dois slots de cartão", "Bateria de longa duração"
        ],
        [  # Notebook Dell XPS 15
            "Intel Core i9 13ª geração", "32GB RAM DDR5", "SSD 1TB NVMe",
            "NVIDIA RTX 4060 8GB", "Tela 15.6\" 4K OLED", "Thunderbolt 4",
            "Webcam Full HD", "Teclado retroiluminado"
        ],
        [  # Microfone Shure SM7B
            "Tipo: Dinâmico", "Padrão: Cardióide", "Resposta: 50-20.000 Hz",
            "Conexão: XLR", "Filtro pop integrado", "Suporte anti-choque",
            "Filtros de graves e agudos", "Construção metálica robusta"
        ],
        [  # Tablet iPad Pro
            "Chip Apple M2", "Tela 12.9\" Liquid Retina XDR", "256GB de armazenamento",
            "12MP câmera ultra-wide", "5G integrado", "Apple Pencil (2ª geração)",
            "Magic Keyboard incluído", "Bateria para o dia todo"
        ],
        [  # Kit Iluminação LED
            "3 painéis LED 60W", "Temperatura de cor ajustável", "2800K a 6500K",
            "Controle de intensidade", "CRI > 95", "Tripés incluídos",
            "Difusores e filtros", "Case de transporte"
        ]
    ]
    
    especificacoes_data = []
    for i, equipamento_id in enumerate(equipamento_ids[:len(especificacoes_por_equipamento)]):
        for especificacao in especificacoes_por_equipamento[i]:
            especificacoes_data.append((equipamento_id, especificacao))
    
    insert_query = """
        INSERT INTO nexus.equipamentos_especificacoes (equipamento_id, especificacao)
        VALUES %s
    """
    
    execute_values(cursor, insert_query, especificacoes_data)
    print(f"✅ {len(especificacoes_data)} especificações inseridas")

def insert_eventos(cursor):
    """Insere eventos de exemplo"""
    print("📝 Inserindo eventos...")
    
    # Buscar IDs dos ambientes
    cursor.execute("SELECT id, name FROM nexus.ambientes")
    ambientes_map = {row[1]: row[0] for row in cursor.fetchall()}
    
    eventos = [
        (
            'Workshop de UX Design',
            date(2024, 12, 15),
            time(14, 0),
            'Sala de Reuniões A',
            'Workshop completo sobre princípios de User Experience Design, incluindo práticas de prototipagem e testes com usuários.',
            24,
            30,
            'Maria Silva',
            'workshop',
            'https://images.unsplash.com/photo-1531403009284-440f080d1e12?w=800',
            ambientes_map.get('Sala de Reuniões A')
        ),
        (
            'Hackathon 2024',
            date(2024, 12, 20),
            time(9, 0),
            'Laboratório de Informática',
            'Evento de inovação tecnológica onde equipes desenvolvem soluções criativas para problemas reais em 48 horas.',
            45,
            60,
            'João Santos',
            'hackathon',
            'https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=800',
            ambientes_map.get('Laboratório de Informática')
        ),
        (
            'Palestra: Inteligência Artificial',
            date(2024, 12, 18),
            time(16, 0),
            'Auditório Principal',
            'Palestra sobre os últimos avanços em IA e suas aplicações práticas no mercado de trabalho.',
            80,
            100,
            'Dr. Carlos Mendes',
            'palestra',
            'https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=800',
            ambientes_map.get('Auditório Principal')
        )
    ]
    
    insert_query = """
        INSERT INTO nexus.eventos 
        (titulo, data_evento, hora_evento, localizacao, descricao, participantes, 
         capacidade, instrutor, tipo, image, ambiente_id)
        VALUES %s
        ON CONFLICT DO NOTHING
    """
    
    cursor.execute("SELECT COUNT(*) FROM nexus.eventos")
    if cursor.fetchone()[0] > 0:
        print("⚠️  Eventos já existem, pulando inserção...")
        return
    
    execute_values(cursor, insert_query, eventos)
    print(f"✅ {len(eventos)} eventos inseridos")

def insert_notificacoes(cursor):
    """Insere notificações de exemplo"""
    print("📝 Inserindo notificações...")
    
    # Buscar primeiro usuário
    cursor.execute("SELECT id FROM nexus.users LIMIT 1")
    result = cursor.fetchone()
    if not result:
        print("⚠️  Nenhum usuário encontrado, pulando notificações...")
        return
    
    user_id = result[0]
    
    notificacoes = [
        (
            user_id,
            'Agendamento confirmado',
            'Sua reserva da Sala de Reuniões A foi aprovada',
            'sucesso',
            False
        ),
        (
            user_id,
            'Novo evento disponível',
            'Workshop de UX Design começa em 2 dias',
            'info',
            False
        ),
        (
            user_id,
            'Lembrete de agendamento',
            'Seu agendamento do Projetor 4K é amanhã às 10:00',
            'aviso',
            True
        )
    ]
    
    insert_query = """
        INSERT INTO nexus.notificacoes 
        (user_id, titulo, mensagem, tipo, lida)
        VALUES %s
    """
    
    execute_values(cursor, insert_query, notificacoes)
    print(f"✅ {len(notificacoes)} notificações inseridas")

def populate_database():
    """Função principal para popular o banco de dados"""
    
    conn = None
    cursor = None
    
    try:
        # Conectar ao banco
        conn = get_db_connection()
        cursor = conn.cursor()
        
        print("🔄 Iniciando população do banco de dados...")
        print("=" * 60)
        
        # Inserir dados
        insert_users(cursor)
        insert_ambientes(cursor)
        insert_equipamentos(cursor)
        insert_eventos(cursor)
        insert_notificacoes(cursor)
        
        # Commit das transações
        conn.commit()
        
        print("=" * 60)
        print("✅ Banco de dados populado com sucesso!")
        print("\n📊 Resumo:")
        
        # Mostrar estatísticas
        cursor.execute("SELECT COUNT(*) FROM nexus.users")
        print(f"  👥 Usuários: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM nexus.ambientes")
        print(f"  🏢 Ambientes: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM nexus.equipamentos")
        print(f"  📦 Equipamentos: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM nexus.eventos")
        print(f"  📅 Eventos: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM nexus.notificacoes")
        print(f"  🔔 Notificações: {cursor.fetchone()[0]}")
        
        print("\n💡 Credenciais de teste:")
        print("  Email: joao.silva@exemplo.com")
        print("  Senha: senha123")
        print("  Role: admin")
        
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"❌ Erro ao popular banco de dados: {e}")
        raise
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    populate_database()