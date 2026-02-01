// Mock data for the application

const eventsData = [
    {
        id: 1,
        title: "Workshop de UX Design",
        date: "2024-12-15",
        time: "14:00",
        location: "Sala de Reuniões A",
        description: "Workshop completo sobre princípios de User Experience Design, incluindo práticas de prototipagem e testes com usuários.",
        attendees: 24,
        capacity: 30,
        instructor: "Maria Silva",
        type: "workshop",
        image: "https://6949b3fa30e1aa8ca4b7eecf.imgix.net/Gemini_Generated_Image_135ut5135ut5135u%201.png"
    },
    {
        id: 2,
        title: "Hackathon 2024",
        date: "2024-12-20",
        time: "09:00",
        location: "Laboratório de Informática",
        description: "Evento de inovação tecnológica onde equipes desenvolvem soluções criativas para problemas reais em 48 horas.",
        attendees: 45,
        capacity: 60,
        instructor: "João Santos",
        type: "hackathon",
        image: "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=800"
    },
    {
        id: 3,
        title: "Palestra: Inteligência Artificial",
        date: "2024-12-18",
        time: "16:00",
        location: "Auditório Principal",
        description: "Palestra sobre os últimos avanços em IA e suas aplicações práticas no mercado de trabalho.",
        attendees: 80,
        capacity: 100,
        instructor: "Dr. Carlos Mendes",
        type: "palestra",
        image: "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=800"
    }
];

const spacesData = [
    {
        id: 1,
        name: "Sala de Reuniões A",
        type: "sala",
        capacity: 12,
        status: "available",
        description: "Sala moderna equipada com TV de 55 polegadas, sistema de videoconferência profissional, quadro branco interativo e ar-condicionado. Perfeita para reuniões corporativas, apresentações e workshops.",
        features: [
            "TV 55 polegadas",
            "Sistema de videoconferência",
            "Quadro branco",
            "Ar condicionado",
            "Wi-Fi de alta velocidade",
            "Mesa de reunião executiva",
            "Cadeiras ergonômicas",
            "Tomadas em todos os lugares"
        ],
        floor: "2º andar",
        area: "35m²",
        image: "https://images.unsplash.com/photo-1497366216548-37526070297c?w=800"
    },
    {
        id: 2,
        name: "Laboratório de Informática",
        type: "laboratorio",
        capacity: 30,
        status: "available",
        description: "Laboratório completo com computadores de última geração, monitores de alta resolução e software especializado para desenvolvimento, design e análise de dados. Ambiente climatizado e confortável.",
        features: [
            "30 computadores",
            "Projetor 4K",
            "Software especializado",
            "Rede de alta velocidade",
            "Estações de trabalho individuais",
            "Ar condicionado duplo",
            "Iluminação ajustável",
            "Sistema de som ambiente"
        ],
        floor: "1º andar",
        area: "120m²",
        image: "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=800"
    },
    {
        id: 3,
        name: "Auditório Principal",
        type: "auditorio",
        capacity: 100,
        status: "available",
        description: "Auditório moderno com assentos confortáveis, sistema de som profissional, iluminação cênica e recursos audiovisuais de ponta. Ideal para palestras, apresentações e eventos corporativos de grande porte.",
        features: [
            "Sistema de som profissional",
            "Projetor de alta resolução",
            "Palco amplo",
            "Iluminação cênica",
            "Assentos estofados",
            "Telão de 5 metros",
            "Microfones sem fio",
            "Camarim anexo"
        ],
        floor: "Térreo",
        area: "250m²",
        image: "https://images.unsplash.com/photo-1475721027785-f74eccf877e2?w=800"
    },
    {
        id: 4,
        name: "Sala de Criação",
        type: "sala",
        capacity: 8,
        status: "available",
        description: "Espaço criativo e descontraído, ideal para brainstorming, sessões de design thinking e trabalho colaborativo. Ambiente flexível com mobiliário modulável.",
        features: [
            "Móveis modulares",
            "Quadros brancos nas paredes",
            "Post-its e materiais",
            "Almofadas e puffs",
            "Iluminação natural",
            "TV para apresentações",
            "Coffee point",
            "Decoração inspiradora"
        ],
        floor: "3º andar",
        area: "45m²",
        image: "https://images.unsplash.com/photo-1497366811353-6870744d04b2?w=800"
    },
    {
        id: 5,
        name: "Estúdio Multimídia",
        type: "estudio",
        capacity: 15,
        status: "occupied",
        description: "Estúdio profissional para gravação de vídeos, podcasts e produção de conteúdo digital. Equipado com isolamento acústico e equipamentos de áudio e vídeo de alta qualidade.",
        features: [
            "Isolamento acústico",
            "Câmeras profissionais",
            "Microfones de estúdio",
            "Iluminação de três pontos",
            "Chroma key verde",
            "Mesa de edição",
            "Monitores de referência",
            "Computador para edição"
        ],
        floor: "2º andar",
        area: "60m²",
        image: "https://images.unsplash.com/photo-1598488035139-bdbb2231ce04?w=800"
    },
    {
        id: 6,
        name: "Sala de Treinamento",
        type: "sala",
        capacity: 25,
        status: "available",
        description: "Sala versátil projetada para treinamentos, cursos e capacitações. Layout flexível que pode ser adaptado para diferentes necessidades pedagógicas.",
        features: [
            "Mesas e cadeiras móveis",
            "Projetor interativo",
            "Sistema de áudio",
            "Câmera para gravação",
            "Quadro flip chart",
            "Material didático",
            "Ar condicionado",
            "Acesso para PCD"
        ],
        floor: "1º andar",
        area: "80m²",
        image: "https://images.unsplash.com/photo-1524178232363-1fb2b075b655?w=800"
    }
];

const equipmentData = [
    {
        id: 1,
        name: "Projetor 4K Sony",
        category: "Audiovisual",
        status: "available",
        description: "Projetor de alta definição 4K da Sony, com 3500 lumens de brilho, ideal para apresentações profissionais em ambientes com iluminação ambiente. Suporta HDMI, USB e conexão wireless.",
        specifications: [
            "Resolução 4K (3840 x 2160)",
            "Brilho: 3500 lumens",
            "Contraste: 10.000:1",
            "HDMI, USB, WiFi",
            "Correção trapezoidal",
            "Zoom óptico 1.5x",
            "Alto-falantes integrados 10W",
            "Controle remoto incluído"
        ],
        brand: "Sony",
        model: "VPL-VW270ES",
        condition: "Excelente",
        image: "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=800"
    },
    {
        id: 2,
        name: "Câmera Canon EOS R5",
        category: "Fotografia",
        status: "available",
        description: "Câmera profissional full-frame com sensor de 45MP e gravação de vídeo 8K. Perfeita para produções de alta qualidade, eventos e conteúdo digital premium.",
        specifications: [
            "Sensor Full-Frame 45MP",
            "Vídeo 8K a 30fps",
            "IBIS de 8 stops",
            "Autofoco Dual Pixel",
            "Tela touch articulada",
            "WiFi e Bluetooth",
            "Dois slots de cartão",
            "Bateria de longa duração"
        ],
        brand: "Canon",
        model: "EOS R5",
        condition: "Novo",
        image: "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=800"
    },
    {
        id: 3,
        name: "Notebook Dell XPS 15",
        category: "Informática",
        status: "available",
        description: "Notebook de alto desempenho com processador Intel Core i9, 32GB de RAM e placa de vídeo dedicada NVIDIA RTX 4060. Ideal para edição de vídeo, modelagem 3D e desenvolvimento.",
        specifications: [
            "Intel Core i9 13ª geração",
            "32GB RAM DDR5",
            "SSD 1TB NVMe",
            "NVIDIA RTX 4060 8GB",
            "Tela 15.6\" 4K OLED",
            "Thunderbolt 4",
            "Webcam Full HD",
            "Teclado retroiluminado"
        ],
        brand: "Dell",
        model: "XPS 15 9530",
        condition: "Excelente",
        image: "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=800"
    },
    {
        id: 4,
        name: "Microfone Shure SM7B",
        category: "Áudio",
        status: "occupied",
        description: "Microfone dinâmico profissional usado em estúdios do mundo todo. Excelente para gravação de voz, podcasts e transmissões ao vivo. Rejeição superior de ruídos externos.",
        specifications: [
            "Tipo: Dinâmico",
            "Padrão: Cardióide",
            "Resposta: 50-20.000 Hz",
            "Conexão: XLR",
            "Filtro pop integrado",
            "Suporte anti-choque",
            "Filtros de graves e agudos",
            "Construção metálica robusta"
        ],
        brand: "Shure",
        model: "SM7B",
        condition: "Excelente",
        image: "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?w=800"
    },
    {
        id: 5,
        name: "Tablet iPad Pro 12.9",
        category: "Informática",
        status: "available",
        description: "iPad Pro com tela Liquid Retina XDR de 12.9 polegadas e chip M2. Perfeito para design, ilustração, anotações e apresentações. Inclui Apple Pencil e Magic Keyboard.",
        specifications: [
            "Chip Apple M2",
            "Tela 12.9\" Liquid Retina XDR",
            "256GB de armazenamento",
            "12MP câmera ultra-wide",
            "5G integrado",
            "Apple Pencil (2ª geração)",
            "Magic Keyboard incluído",
            "Bateria para o dia todo"
        ],
        brand: "Apple",
        model: "iPad Pro 6ª geração",
        condition: "Novo",
        image: "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=800"
    },
    {
        id: 6,
        name: "Kit Iluminação LED",
        category: "Iluminação",
        status: "available",
        description: "Kit completo de iluminação profissional com três painéis LED ajustáveis, suportes de tripé e case de transporte. Ideal para gravações de vídeo e fotografia.",
        specifications: [
            "3 painéis LED 60W",
            "Temperatura de cor ajustável",
            "2800K a 6500K",
            "Controle de intensidade",
            "CRI > 95",
            "Tripés incluídos",
            "Difusores e filtros",
            "Case de transporte"
        ],
        brand: "Godox",
        model: "LED500LRC",
        condition: "Excelente",
        image: "https://6949b3fa30e1aa8ca4b7eecf.imgix.net/Gemini_Generated_Image_135ut5135ut5135u%201.png"
    }
];

const historyData = [
    {
        id: 1,
        type: "space",
        name: "Sala de Reuniões A",
        date: "2024-12-05",
        startTime: "14:00",
        endTime: "16:00",
        purpose: "Reunião com cliente sobre novo projeto de desenvolvimento web",
        status: "completed"
    },
    {
        id: 2,
        type: "equipment",
        name: "Projetor 4K Sony",
        date: "2024-12-03",
        startTime: "09:00",
        endTime: "12:00",
        purpose: "Apresentação de resultados trimestrais",
        status: "completed"
    },
    {
        id: 3,
        type: "space",
        name: "Laboratório de Informática",
        date: "2024-11-28",
        startTime: "13:00",
        endTime: "17:00",
        purpose: "Workshop de Python para iniciantes",
        status: "completed"
    },
    {
        id: 4,
        type: "equipment",
        name: "Câmera Canon EOS R5",
        date: "2024-11-25",
        startTime: "10:00",
        endTime: "15:00",
        purpose: "Gravação de vídeo institucional",
        status: "completed"
    },
    {
        id: 5,
        type: "space",
        name: "Auditório Principal",
        date: "2024-11-20",
        startTime: "14:00",
        endTime: "18:00",
        purpose: "Palestra sobre transformação digital",
        status: "completed"
    },
    {
        id: 6,
        type: "equipment",
        name: "Notebook Dell XPS 15",
        date: "2024-11-18",
        startTime: "08:00",
        endTime: "17:00",
        purpose: "Desenvolvimento de aplicação mobile",
        status: "completed"
    }
];

// Calendar data
const calendarEvents = [
    { date: "2024-12-15", title: "Workshop de UX Design", time: "14:00" },
    { date: "2024-12-18", title: "Palestra: IA", time: "16:00" },
    { date: "2024-12-20", title: "Hackathon 2024", time: "09:00" },
    { date: "2024-12-22", title: "Treinamento Equipe", time: "10:00" }
];

// Users data for admin panel
const usersData = [
    {
        id: 1,
        name: "João da Silva",
        email: "joao.silva@exemplo.com",
        role: "admin",
        status: "active"
    },
    {
        id: 2,
        name: "Maria Santos",
        email: "maria.santos@exemplo.com",
        role: "user",
        status: "active"
    },
    {
        id: 3,
        name: "Carlos Oliveira",
        email: "carlos.oliveira@exemplo.com",
        role: "moderator",
        status: "active"
    },
    {
        id: 4,
        name: "Ana Costa",
        email: "ana.costa@exemplo.com",
        role: "user",
        status: "active"
    },
    {
        id: 5,
        name: "Pedro Almeida",
        email: "pedro.almeida@exemplo.com",
        role: "user",
        status: "inactive"
    }
];

// Pending bookings for admin approval
const pendingBookingsData = [
    {
        id: 1,
        type: "space",
        itemName: "Sala de Reuniões A",
        userName: "Maria Santos",
        userEmail: "maria.santos@exemplo.com",
        date: "2024-12-16",
        startTime: "14:00",
        endTime: "16:00",
        purpose: "Reunião de planejamento trimestral com equipe de marketing",
        status: "pending"
    },
    {
        id: 2,
        type: "equipment",
        itemName: "Projetor 4K Sony",
        userName: "Carlos Oliveira",
        userEmail: "carlos.oliveira@exemplo.com",
        date: "2024-12-17",
        startTime: "10:00",
        endTime: "12:00",
        purpose: "Apresentação de projeto para clientes",
        status: "pending"
    },
    {
        id: 3,
        type: "space",
        itemName: "Laboratório de Informática",
        userName: "Ana Costa",
        userEmail: "ana.costa@exemplo.com",
        date: "2024-12-18",
        startTime: "09:00",
        endTime: "17:00",
        purpose: "Workshop de programação para iniciantes",
        status: "pending"
    }
];

// System settings
const systemSettings = {
    autoApprove: false,
    emailNotifications: true,
    maxBookings: 5,
    minAdvanceHours: 24
};