--
-- PostgreSQL database dump
--

\restrict fJ3snmeEH4eQuSMXuewt87TTAhy6oSaIPVUhTJLNSzNTjUo55I9roflMHq91MPE

-- Dumped from database version 18.1
-- Dumped by pg_dump version 18.0

-- Started on 2026-02-01 23:11:18

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 6 (class 2615 OID 16469)
-- Name: nexus; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA nexus;


ALTER SCHEMA nexus OWNER TO postgres;

--
-- TOC entry 904 (class 1247 OID 16471)
-- Name: role_usuario; Type: TYPE; Schema: nexus; Owner: postgres
--

CREATE TYPE nexus.role_usuario AS ENUM (
    'admin',
    'user'
);


ALTER TYPE nexus.role_usuario OWNER TO postgres;

--
-- TOC entry 925 (class 1247 OID 16555)
-- Name: status_agendamento; Type: TYPE; Schema: nexus; Owner: postgres
--

CREATE TYPE nexus.status_agendamento AS ENUM (
    'pendente',
    'confirmado',
    'rejeitado',
    'cancelado'
);


ALTER TYPE nexus.status_agendamento OWNER TO postgres;

--
-- TOC entry 928 (class 1247 OID 16564)
-- Name: status_agendamento_eq; Type: TYPE; Schema: nexus; Owner: postgres
--

CREATE TYPE nexus.status_agendamento_eq AS ENUM (
    'pendente',
    'Confirmado',
    'Rejeitado'
);


ALTER TYPE nexus.status_agendamento_eq OWNER TO postgres;

--
-- TOC entry 919 (class 1247 OID 16532)
-- Name: status_ambiente; Type: TYPE; Schema: nexus; Owner: postgres
--

CREATE TYPE nexus.status_ambiente AS ENUM (
    'Disponivel',
    'ocupado',
    'manutencao'
);


ALTER TYPE nexus.status_ambiente OWNER TO postgres;

--
-- TOC entry 934 (class 1247 OID 16596)
-- Name: status_equipamento; Type: TYPE; Schema: nexus; Owner: postgres
--

CREATE TYPE nexus.status_equipamento AS ENUM (
    'Disponivel',
    'ocupado'
);


ALTER TYPE nexus.status_equipamento OWNER TO postgres;

--
-- TOC entry 955 (class 1247 OID 16704)
-- Name: status_historico; Type: TYPE; Schema: nexus; Owner: postgres
--

CREATE TYPE nexus.status_historico AS ENUM (
    'Confirmado',
    'Rejeitado',
    'Concluido',
    'Cancelado'
);


ALTER TYPE nexus.status_historico OWNER TO postgres;

--
-- TOC entry 961 (class 1247 OID 16738)
-- Name: status_historico_eq; Type: TYPE; Schema: nexus; Owner: postgres
--

CREATE TYPE nexus.status_historico_eq AS ENUM (
    'Confirmado',
    'Rejeitado',
    'Concluido',
    'Cancelado'
);


ALTER TYPE nexus.status_historico_eq OWNER TO postgres;

--
-- TOC entry 910 (class 1247 OID 16497)
-- Name: status_usuario; Type: TYPE; Schema: nexus; Owner: postgres
--

CREATE TYPE nexus.status_usuario AS ENUM (
    'ativo',
    'inativo'
);


ALTER TYPE nexus.status_usuario OWNER TO postgres;

--
-- TOC entry 916 (class 1247 OID 16522)
-- Name: tipo_ambiente; Type: TYPE; Schema: nexus; Owner: postgres
--

CREATE TYPE nexus.tipo_ambiente AS ENUM (
    'sala',
    'laboratorio',
    'auditorio',
    'estudio'
);


ALTER TYPE nexus.tipo_ambiente OWNER TO postgres;

--
-- TOC entry 943 (class 1247 OID 16632)
-- Name: tipo_evento; Type: TYPE; Schema: nexus; Owner: postgres
--

CREATE TYPE nexus.tipo_evento AS ENUM (
    'workshop',
    'hackathon',
    'palestra',
    'outro'
);


ALTER TYPE nexus.tipo_evento OWNER TO postgres;

--
-- TOC entry 907 (class 1247 OID 16476)
-- Name: tipo_notificacao; Type: TYPE; Schema: nexus; Owner: postgres
--

CREATE TYPE nexus.tipo_notificacao AS ENUM (
    'info',
    'aviso',
    'sucesso'
);


ALTER TYPE nexus.tipo_notificacao OWNER TO postgres;

--
-- TOC entry 251 (class 1255 OID 32793)
-- Name: fn_criar_historico_equipamento(); Type: FUNCTION; Schema: nexus; Owner: postgres
--

CREATE FUNCTION nexus.fn_criar_historico_equipamento() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Inserir no histórico apenas quando status for Confirmado, Rejeitado ou Cancelado
    IF NEW.status IN ('Confirmado', 'Rejeitado', 'Cancelado') AND 
       (OLD.status IS NULL OR OLD.status != NEW.status) THEN
        
        INSERT INTO nexus.historico_equipamentos (
            agendamento_id,
            equipamento_id,
            user_id,
            equipamento_nome,
            data_equip,
            hora_inicio,
            hora_fim,
            finalidade,
            status
        )
        SELECT 
            ae.id,
            ae.equipamento_id,
            ae.user_id,
            e.name,
            ae.data,
            ae.hora_inicio,
            ae.hora_fim,
            ae.finalidade,
            NEW.status::nexus.status_historico
        FROM nexus.agendamentos_equipamentos ae
        JOIN nexus.equipamentos e ON ae.equipamento_id = e.id
        WHERE ae.id = NEW.agendamento_id;
    END IF;
    
    RETURN NEW;
END;
$$;


ALTER FUNCTION nexus.fn_criar_historico_equipamento() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 224 (class 1259 OID 16572)
-- Name: agendamentos; Type: TABLE; Schema: nexus; Owner: postgres
--

CREATE TABLE nexus.agendamentos (
    id integer NOT NULL,
    ambiente_id integer NOT NULL,
    data date NOT NULL,
    hora_inicio time without time zone NOT NULL,
    hora_fim time without time zone NOT NULL,
    finalidade text,
    status nexus.status_agendamento DEFAULT 'pendente'::nexus.status_agendamento,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE nexus.agendamentos OWNER TO postgres;

--
-- TOC entry 240 (class 1259 OID 16802)
-- Name: agendamentos_equipamentos; Type: TABLE; Schema: nexus; Owner: postgres
--

CREATE TABLE nexus.agendamentos_equipamentos (
    id integer NOT NULL,
    user_id uuid NOT NULL,
    equipamento_id integer NOT NULL,
    data date NOT NULL,
    hora_inicio time without time zone NOT NULL,
    hora_fim time without time zone NOT NULL,
    finalidade character varying(255),
    status character varying(20) DEFAULT 'Pendente'::character varying,
    criado_em timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE nexus.agendamentos_equipamentos OWNER TO postgres;

--
-- TOC entry 239 (class 1259 OID 16801)
-- Name: agendamentos_equipamentos_id_seq; Type: SEQUENCE; Schema: nexus; Owner: postgres
--

CREATE SEQUENCE nexus.agendamentos_equipamentos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE nexus.agendamentos_equipamentos_id_seq OWNER TO postgres;

--
-- TOC entry 5266 (class 0 OID 0)
-- Dependencies: 239
-- Name: agendamentos_equipamentos_id_seq; Type: SEQUENCE OWNED BY; Schema: nexus; Owner: postgres
--

ALTER SEQUENCE nexus.agendamentos_equipamentos_id_seq OWNED BY nexus.agendamentos_equipamentos.id;


--
-- TOC entry 223 (class 1259 OID 16571)
-- Name: agendamentos_id_seq; Type: SEQUENCE; Schema: nexus; Owner: postgres
--

CREATE SEQUENCE nexus.agendamentos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE nexus.agendamentos_id_seq OWNER TO postgres;

--
-- TOC entry 5267 (class 0 OID 0)
-- Dependencies: 223
-- Name: agendamentos_id_seq; Type: SEQUENCE OWNED BY; Schema: nexus; Owner: postgres
--

ALTER SEQUENCE nexus.agendamentos_id_seq OWNED BY nexus.agendamentos.id;


--
-- TOC entry 222 (class 1259 OID 16540)
-- Name: ambientes; Type: TABLE; Schema: nexus; Owner: postgres
--

CREATE TABLE nexus.ambientes (
    id integer NOT NULL,
    name character varying(150) NOT NULL,
    type nexus.tipo_ambiente NOT NULL,
    capacidade integer NOT NULL,
    status nexus.status_ambiente DEFAULT 'Disponivel'::nexus.status_ambiente,
    descricao text,
    localizacao character varying(50),
    area character varying(20),
    image character varying(255),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE nexus.ambientes OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16539)
-- Name: ambientes_id_seq; Type: SEQUENCE; Schema: nexus; Owner: postgres
--

CREATE SEQUENCE nexus.ambientes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE nexus.ambientes_id_seq OWNER TO postgres;

--
-- TOC entry 5268 (class 0 OID 0)
-- Dependencies: 221
-- Name: ambientes_id_seq; Type: SEQUENCE OWNED BY; Schema: nexus; Owner: postgres
--

ALTER SEQUENCE nexus.ambientes_id_seq OWNED BY nexus.ambientes.id;


--
-- TOC entry 226 (class 1259 OID 16602)
-- Name: equipamentos; Type: TABLE; Schema: nexus; Owner: postgres
--

CREATE TABLE nexus.equipamentos (
    id integer NOT NULL,
    name character varying(150) NOT NULL,
    categoria character varying(50) NOT NULL,
    status nexus.status_equipamento DEFAULT 'Disponivel'::nexus.status_equipamento,
    descricao text,
    marca character varying(50),
    modelo character varying(100),
    condicao character varying(30),
    image character varying(255),
    quantidade_disponivel integer NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE nexus.equipamentos OWNER TO postgres;

--
-- TOC entry 228 (class 1259 OID 16617)
-- Name: equipamentos_especificacoes; Type: TABLE; Schema: nexus; Owner: postgres
--

CREATE TABLE nexus.equipamentos_especificacoes (
    id integer NOT NULL,
    equipamento_id integer NOT NULL,
    especificacao character varying(255) NOT NULL
);


ALTER TABLE nexus.equipamentos_especificacoes OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 16616)
-- Name: equipamentos_especificacoes_id_seq; Type: SEQUENCE; Schema: nexus; Owner: postgres
--

CREATE SEQUENCE nexus.equipamentos_especificacoes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE nexus.equipamentos_especificacoes_id_seq OWNER TO postgres;

--
-- TOC entry 5269 (class 0 OID 0)
-- Dependencies: 227
-- Name: equipamentos_especificacoes_id_seq; Type: SEQUENCE OWNED BY; Schema: nexus; Owner: postgres
--

ALTER SEQUENCE nexus.equipamentos_especificacoes_id_seq OWNED BY nexus.equipamentos_especificacoes.id;


--
-- TOC entry 225 (class 1259 OID 16601)
-- Name: equipamentos_id_seq; Type: SEQUENCE; Schema: nexus; Owner: postgres
--

CREATE SEQUENCE nexus.equipamentos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE nexus.equipamentos_id_seq OWNER TO postgres;

--
-- TOC entry 5270 (class 0 OID 0)
-- Dependencies: 225
-- Name: equipamentos_id_seq; Type: SEQUENCE OWNED BY; Schema: nexus; Owner: postgres
--

ALTER SEQUENCE nexus.equipamentos_id_seq OWNED BY nexus.equipamentos.id;


--
-- TOC entry 230 (class 1259 OID 16642)
-- Name: eventos; Type: TABLE; Schema: nexus; Owner: postgres
--

CREATE TABLE nexus.eventos (
    id integer NOT NULL,
    titulo character varying(150) NOT NULL,
    data_evento date NOT NULL,
    hora_evento time without time zone NOT NULL,
    localizacao character varying(150) NOT NULL,
    descricao text,
    participantes integer DEFAULT 0,
    capacidade integer NOT NULL,
    instrutor character varying(100),
    tipo nexus.tipo_evento NOT NULL,
    image character varying(255),
    ambiente_id integer,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE nexus.eventos OWNER TO postgres;

--
-- TOC entry 232 (class 1259 OID 16665)
-- Name: eventos_equipamentos; Type: TABLE; Schema: nexus; Owner: postgres
--

CREATE TABLE nexus.eventos_equipamentos (
    id integer NOT NULL,
    evento_id integer,
    equipamento_id integer,
    quantidade integer DEFAULT 1
);


ALTER TABLE nexus.eventos_equipamentos OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 16664)
-- Name: eventos_equipamentos_id_seq; Type: SEQUENCE; Schema: nexus; Owner: postgres
--

CREATE SEQUENCE nexus.eventos_equipamentos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE nexus.eventos_equipamentos_id_seq OWNER TO postgres;

--
-- TOC entry 5271 (class 0 OID 0)
-- Dependencies: 231
-- Name: eventos_equipamentos_id_seq; Type: SEQUENCE OWNED BY; Schema: nexus; Owner: postgres
--

ALTER SEQUENCE nexus.eventos_equipamentos_id_seq OWNED BY nexus.eventos_equipamentos.id;


--
-- TOC entry 229 (class 1259 OID 16641)
-- Name: eventos_id_seq; Type: SEQUENCE; Schema: nexus; Owner: postgres
--

CREATE SEQUENCE nexus.eventos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE nexus.eventos_id_seq OWNER TO postgres;

--
-- TOC entry 5272 (class 0 OID 0)
-- Dependencies: 229
-- Name: eventos_id_seq; Type: SEQUENCE OWNED BY; Schema: nexus; Owner: postgres
--

ALTER SEQUENCE nexus.eventos_id_seq OWNED BY nexus.eventos.id;


--
-- TOC entry 236 (class 1259 OID 16714)
-- Name: historico; Type: TABLE; Schema: nexus; Owner: postgres
--

CREATE TABLE nexus.historico (
    id integer NOT NULL,
    user_id uuid,
    agendamento_id integer NOT NULL,
    type character varying(20),
    name character varying(100),
    historico_date date,
    start_time time without time zone,
    end_time time without time zone,
    purpose text,
    status nexus.status_historico NOT NULL
);


ALTER TABLE nexus.historico OWNER TO postgres;

--
-- TOC entry 242 (class 1259 OID 16827)
-- Name: historico_equipamentos; Type: TABLE; Schema: nexus; Owner: postgres
--

CREATE TABLE nexus.historico_equipamentos (
    id integer NOT NULL,
    agendamento_id integer NOT NULL,
    equipamento_id integer NOT NULL,
    user_id uuid NOT NULL,
    equipamento_nome character varying(255) NOT NULL,
    data_equip date NOT NULL,
    hora_inicio time without time zone NOT NULL,
    hora_fim time without time zone NOT NULL,
    finalidade character varying(255) NOT NULL,
    status nexus.status_historico NOT NULL,
    criado_em timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE nexus.historico_equipamentos OWNER TO postgres;

--
-- TOC entry 241 (class 1259 OID 16826)
-- Name: historico_equipamentos_id_seq; Type: SEQUENCE; Schema: nexus; Owner: postgres
--

CREATE SEQUENCE nexus.historico_equipamentos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE nexus.historico_equipamentos_id_seq OWNER TO postgres;

--
-- TOC entry 5273 (class 0 OID 0)
-- Dependencies: 241
-- Name: historico_equipamentos_id_seq; Type: SEQUENCE OWNED BY; Schema: nexus; Owner: postgres
--

ALTER SEQUENCE nexus.historico_equipamentos_id_seq OWNED BY nexus.historico_equipamentos.id;


--
-- TOC entry 235 (class 1259 OID 16713)
-- Name: historico_id_seq; Type: SEQUENCE; Schema: nexus; Owner: postgres
--

CREATE SEQUENCE nexus.historico_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE nexus.historico_id_seq OWNER TO postgres;

--
-- TOC entry 5274 (class 0 OID 0)
-- Dependencies: 235
-- Name: historico_id_seq; Type: SEQUENCE OWNED BY; Schema: nexus; Owner: postgres
--

ALTER SEQUENCE nexus.historico_id_seq OWNED BY nexus.historico.id;


--
-- TOC entry 246 (class 1259 OID 16891)
-- Name: inscricoes_eventos; Type: TABLE; Schema: nexus; Owner: postgres
--

CREATE TABLE nexus.inscricoes_eventos (
    id integer NOT NULL,
    evento_id integer NOT NULL,
    user_id uuid NOT NULL,
    status character varying(20) DEFAULT 'Inscrito'::character varying,
    data_inscricao timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE nexus.inscricoes_eventos OWNER TO postgres;

--
-- TOC entry 245 (class 1259 OID 16890)
-- Name: inscricoes_eventos_id_seq; Type: SEQUENCE; Schema: nexus; Owner: postgres
--

CREATE SEQUENCE nexus.inscricoes_eventos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE nexus.inscricoes_eventos_id_seq OWNER TO postgres;

--
-- TOC entry 5275 (class 0 OID 0)
-- Dependencies: 245
-- Name: inscricoes_eventos_id_seq; Type: SEQUENCE OWNED BY; Schema: nexus; Owner: postgres
--

ALTER SEQUENCE nexus.inscricoes_eventos_id_seq OWNED BY nexus.inscricoes_eventos.id;


--
-- TOC entry 234 (class 1259 OID 16686)
-- Name: notificacoes; Type: TABLE; Schema: nexus; Owner: postgres
--

CREATE TABLE nexus.notificacoes (
    id integer NOT NULL,
    user_id uuid,
    titulo character varying(100) NOT NULL,
    mensagem character varying(255) NOT NULL,
    tipo nexus.tipo_notificacao DEFAULT 'info'::nexus.tipo_notificacao,
    lida boolean DEFAULT false,
    data_criacao timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE nexus.notificacoes OWNER TO postgres;

--
-- TOC entry 233 (class 1259 OID 16685)
-- Name: notificacoes_id_seq; Type: SEQUENCE; Schema: nexus; Owner: postgres
--

CREATE SEQUENCE nexus.notificacoes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE nexus.notificacoes_id_seq OWNER TO postgres;

--
-- TOC entry 5276 (class 0 OID 0)
-- Dependencies: 233
-- Name: notificacoes_id_seq; Type: SEQUENCE OWNED BY; Schema: nexus; Owner: postgres
--

ALTER SEQUENCE nexus.notificacoes_id_seq OWNED BY nexus.notificacoes.id;


--
-- TOC entry 238 (class 1259 OID 16768)
-- Name: pendentes_ambientes; Type: TABLE; Schema: nexus; Owner: postgres
--

CREATE TABLE nexus.pendentes_ambientes (
    id integer NOT NULL,
    agendamento_id integer NOT NULL,
    user_id uuid NOT NULL,
    status character varying(20) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE nexus.pendentes_ambientes OWNER TO postgres;

--
-- TOC entry 237 (class 1259 OID 16767)
-- Name: pendentes_ambientes_id_seq; Type: SEQUENCE; Schema: nexus; Owner: postgres
--

CREATE SEQUENCE nexus.pendentes_ambientes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE nexus.pendentes_ambientes_id_seq OWNER TO postgres;

--
-- TOC entry 5277 (class 0 OID 0)
-- Dependencies: 237
-- Name: pendentes_ambientes_id_seq; Type: SEQUENCE OWNED BY; Schema: nexus; Owner: postgres
--

ALTER SEQUENCE nexus.pendentes_ambientes_id_seq OWNED BY nexus.pendentes_ambientes.id;


--
-- TOC entry 244 (class 1259 OID 16857)
-- Name: pendentes_equipamentos; Type: TABLE; Schema: nexus; Owner: postgres
--

CREATE TABLE nexus.pendentes_equipamentos (
    id integer NOT NULL,
    agendamento_id integer NOT NULL,
    user_id uuid NOT NULL,
    status character varying(20) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE nexus.pendentes_equipamentos OWNER TO postgres;

--
-- TOC entry 243 (class 1259 OID 16856)
-- Name: pendentes_equipamentos_id_seq; Type: SEQUENCE; Schema: nexus; Owner: postgres
--

CREATE SEQUENCE nexus.pendentes_equipamentos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE nexus.pendentes_equipamentos_id_seq OWNER TO postgres;

--
-- TOC entry 5278 (class 0 OID 0)
-- Dependencies: 243
-- Name: pendentes_equipamentos_id_seq; Type: SEQUENCE OWNED BY; Schema: nexus; Owner: postgres
--

ALTER SEQUENCE nexus.pendentes_equipamentos_id_seq OWNED BY nexus.pendentes_equipamentos.id;


--
-- TOC entry 250 (class 1259 OID 32769)
-- Name: recursos_ambientes; Type: TABLE; Schema: nexus; Owner: postgres
--

CREATE TABLE nexus.recursos_ambientes (
    id integer NOT NULL,
    recursos_id integer NOT NULL,
    recursos character varying(255) NOT NULL
);


ALTER TABLE nexus.recursos_ambientes OWNER TO postgres;

--
-- TOC entry 249 (class 1259 OID 32768)
-- Name: recursos_ambientes_id_seq; Type: SEQUENCE; Schema: nexus; Owner: postgres
--

CREATE SEQUENCE nexus.recursos_ambientes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE nexus.recursos_ambientes_id_seq OWNER TO postgres;

--
-- TOC entry 5279 (class 0 OID 0)
-- Dependencies: 249
-- Name: recursos_ambientes_id_seq; Type: SEQUENCE OWNED BY; Schema: nexus; Owner: postgres
--

ALTER SEQUENCE nexus.recursos_ambientes_id_seq OWNED BY nexus.recursos_ambientes.id;


--
-- TOC entry 220 (class 1259 OID 16501)
-- Name: users; Type: TABLE; Schema: nexus; Owner: postgres
--

CREATE TABLE nexus.users (
    id uuid NOT NULL,
    name character varying(100) NOT NULL,
    email character varying(150) NOT NULL,
    cpf character varying(14) NOT NULL,
    rg character varying(20),
    data_nascimento date,
    telefone character varying(20),
    endereco character varying(255),
    departamento character varying(100),
    funcao character varying(100),
    role nexus.role_usuario DEFAULT 'user'::nexus.role_usuario NOT NULL,
    image character varying(255),
    status nexus.status_usuario DEFAULT 'ativo'::nexus.status_usuario NOT NULL,
    senha character varying(255) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE nexus.users OWNER TO postgres;

--
-- TOC entry 4991 (class 2604 OID 16575)
-- Name: agendamentos id; Type: DEFAULT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.agendamentos ALTER COLUMN id SET DEFAULT nextval('nexus.agendamentos_id_seq'::regclass);


--
-- TOC entry 5011 (class 2604 OID 16805)
-- Name: agendamentos_equipamentos id; Type: DEFAULT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.agendamentos_equipamentos ALTER COLUMN id SET DEFAULT nextval('nexus.agendamentos_equipamentos_id_seq'::regclass);


--
-- TOC entry 4988 (class 2604 OID 16543)
-- Name: ambientes id; Type: DEFAULT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.ambientes ALTER COLUMN id SET DEFAULT nextval('nexus.ambientes_id_seq'::regclass);


--
-- TOC entry 4995 (class 2604 OID 16605)
-- Name: equipamentos id; Type: DEFAULT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.equipamentos ALTER COLUMN id SET DEFAULT nextval('nexus.equipamentos_id_seq'::regclass);


--
-- TOC entry 4998 (class 2604 OID 16620)
-- Name: equipamentos_especificacoes id; Type: DEFAULT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.equipamentos_especificacoes ALTER COLUMN id SET DEFAULT nextval('nexus.equipamentos_especificacoes_id_seq'::regclass);


--
-- TOC entry 4999 (class 2604 OID 16645)
-- Name: eventos id; Type: DEFAULT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.eventos ALTER COLUMN id SET DEFAULT nextval('nexus.eventos_id_seq'::regclass);


--
-- TOC entry 5002 (class 2604 OID 16668)
-- Name: eventos_equipamentos id; Type: DEFAULT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.eventos_equipamentos ALTER COLUMN id SET DEFAULT nextval('nexus.eventos_equipamentos_id_seq'::regclass);


--
-- TOC entry 5008 (class 2604 OID 16717)
-- Name: historico id; Type: DEFAULT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.historico ALTER COLUMN id SET DEFAULT nextval('nexus.historico_id_seq'::regclass);


--
-- TOC entry 5014 (class 2604 OID 16830)
-- Name: historico_equipamentos id; Type: DEFAULT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.historico_equipamentos ALTER COLUMN id SET DEFAULT nextval('nexus.historico_equipamentos_id_seq'::regclass);


--
-- TOC entry 5018 (class 2604 OID 16894)
-- Name: inscricoes_eventos id; Type: DEFAULT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.inscricoes_eventos ALTER COLUMN id SET DEFAULT nextval('nexus.inscricoes_eventos_id_seq'::regclass);


--
-- TOC entry 5004 (class 2604 OID 16689)
-- Name: notificacoes id; Type: DEFAULT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.notificacoes ALTER COLUMN id SET DEFAULT nextval('nexus.notificacoes_id_seq'::regclass);


--
-- TOC entry 5009 (class 2604 OID 16771)
-- Name: pendentes_ambientes id; Type: DEFAULT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.pendentes_ambientes ALTER COLUMN id SET DEFAULT nextval('nexus.pendentes_ambientes_id_seq'::regclass);


--
-- TOC entry 5016 (class 2604 OID 16860)
-- Name: pendentes_equipamentos id; Type: DEFAULT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.pendentes_equipamentos ALTER COLUMN id SET DEFAULT nextval('nexus.pendentes_equipamentos_id_seq'::regclass);


--
-- TOC entry 5021 (class 2604 OID 32772)
-- Name: recursos_ambientes id; Type: DEFAULT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.recursos_ambientes ALTER COLUMN id SET DEFAULT nextval('nexus.recursos_ambientes_id_seq'::regclass);


--
-- TOC entry 5236 (class 0 OID 16572)
-- Dependencies: 224
-- Data for Name: agendamentos; Type: TABLE DATA; Schema: nexus; Owner: postgres
--

COPY nexus.agendamentos (id, ambiente_id, data, hora_inicio, hora_fim, finalidade, status, created_at, updated_at) FROM stdin;
11	22	2026-01-31	11:27:00	12:27:00	            teste	pendente	2026-01-31 11:27:29.031545	2026-01-31 11:27:29.031545
12	24	2026-01-31	13:29:00	14:29:00	            teste	pendente	2026-01-31 11:29:54.079747	2026-01-31 11:29:54.079747
13	27	2026-01-31	19:27:00	22:27:00	            teste	pendente	2026-01-31 13:28:03.257158	2026-01-31 13:28:03.257158
14	22	2026-02-06	19:16:00	21:16:00	            teste	pendente	2026-01-31 17:16:37.420699	2026-01-31 17:16:37.420699
\.


--
-- TOC entry 5252 (class 0 OID 16802)
-- Dependencies: 240
-- Data for Name: agendamentos_equipamentos; Type: TABLE DATA; Schema: nexus; Owner: postgres
--

COPY nexus.agendamentos_equipamentos (id, user_id, equipamento_id, data, hora_inicio, hora_fim, finalidade, status, criado_em) FROM stdin;
17	88f7f338-b402-404f-986a-069606f51499	6	2026-01-31	14:45:00	16:45:00	      teste	Confirmado	2026-01-31 13:45:16.338673
\.


--
-- TOC entry 5234 (class 0 OID 16540)
-- Dependencies: 222
-- Data for Name: ambientes; Type: TABLE DATA; Schema: nexus; Owner: postgres
--

COPY nexus.ambientes (id, name, type, capacidade, status, descricao, localizacao, area, image, created_at) FROM stdin;
21	Laboratório de Informática	laboratorio	30	Disponivel	Laboratório completo com computadores de última geração, monitores de alta resolução e software especializado para desenvolvimento, design e análise de dados. Ambiente climatizado e confortável.	1º andar	120m²	https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=800	2026-01-31 03:34:50.340979
22	Auditório Principal	auditorio	100	Disponivel	Auditório moderno com assentos confortáveis, sistema de som profissional, iluminação cênica e recursos audiovisuais de ponta. Ideal para palestras, apresentações e eventos corporativos de grande porte.	Térreo	250m²	https://images.unsplash.com/photo-1475721027785-f74eccf877e2?w=800	2026-01-31 03:34:50.340979
23	Sala de Criação	sala	8	Disponivel	Espaço criativo e descontraído, ideal para brainstorming, sessões de design thinking e trabalho colaborativo. Ambiente flexível com mobiliário modulável.	3º andar	45m²	https://images.unsplash.com/photo-1497366811353-6870744d04b2?w=800	2026-01-31 03:34:50.340979
24	Estúdio Multimídia	estudio	15	ocupado	Estúdio profissional para gravação de vídeos, podcasts e produção de conteúdo digital. Equipado com isolamento acústico e equipamentos de áudio e vídeo de alta qualidade.	2º andar	60m²	https://images.unsplash.com/photo-1598488035139-bdbb2231ce04?w=800	2026-01-31 03:34:50.340979
25	Sala de Treinamento	sala	25	Disponivel	Sala versátil projetada para treinamentos, cursos e capacitações. Layout flexível que pode ser adaptado para diferentes necessidades pedagógicas.	1º andar	80m²	https://images.unsplash.com/photo-1524178232363-1fb2b075b655?w=800	2026-01-31 03:34:50.340979
26	Sala de Reuniões A	sala	12	Disponivel	Sala moderna equipada com TV de 55 polegadas, sistema de videoconferência profissional, quadro branco interativo e ar-condicionado. Perfeita para reuniões corporativas, apresentações e workshops.	2º andar	35m²	https://images.unsplash.com/photo-1497366216548-37526070297c?w=800	2026-01-31 04:00:34.270794
27	testePostam	sala	20	Disponivel	teste	2	30	\N	2026-01-31 13:27:29.734366
\.


--
-- TOC entry 5238 (class 0 OID 16602)
-- Dependencies: 226
-- Data for Name: equipamentos; Type: TABLE DATA; Schema: nexus; Owner: postgres
--

COPY nexus.equipamentos (id, name, categoria, status, descricao, marca, modelo, condicao, image, quantidade_disponivel, created_at) FROM stdin;
5	Projetor 4K Sony	Audiovisual	Disponivel	Projetor de alta definição 4K da Sony, com 3500 lumens de brilho, ideal para apresentações profissionais em ambientes com iluminação ambiente. Suporta HDMI, USB e conexão wireless.	Sony	VPL-VW270ES	Excelente	https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=800	3	2026-01-31 03:37:28.844486
6	Câmera Canon EOS R5	Fotografia	Disponivel	Câmera profissional full-frame com sensor de 45MP e gravação de vídeo 8K. Perfeita para produções de alta qualidade, eventos e conteúdo digital premium.	Canon	EOS R5	Novo	https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=800	2	2026-01-31 03:37:28.844486
7	Notebook Dell XPS 15	Informática	Disponivel	Notebook de alto desempenho com processador Intel Core i9, 32GB de RAM e placa de vídeo dedicada NVIDIA RTX 4060. Ideal para edição de vídeo, modelagem 3D e desenvolvimento.	Dell	XPS 15 9530	Excelente	https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=800	5	2026-01-31 03:37:28.844486
8	Microfone Shure SM7B	Áudio	ocupado	Microfone dinâmico profissional usado em estúdios do mundo todo. Excelente para gravação de voz, podcasts e transmissões ao vivo. Rejeição superior de ruídos externos.	Shure	SM7B	Excelente	https://images.unsplash.com/photo-1590602847861-f357a9332bbc?w=800	4	2026-01-31 03:37:28.844486
9	Tablet iPad Pro 12.9	Informática	Disponivel	iPad Pro com tela Liquid Retina XDR de 12.9 polegadas e chip M2. Perfeito para design, ilustração, anotações e apresentações. Inclui Apple Pencil e Magic Keyboard.	Apple	iPad Pro 6ª geração	Novo	https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=800	6	2026-01-31 03:37:28.844486
10	Kit Iluminação LED	Iluminação	Disponivel	Kit completo de iluminação profissional com três painéis LED ajustáveis, suportes de tripé e case de transporte. Ideal para gravações de vídeo e fotografia.	Godox	LED500LRC	Excelente	https://images.unsplash.com/photo-1492619375914-88005aa9e8fb?w=800	3	2026-01-31 03:37:28.844486
\.


--
-- TOC entry 5240 (class 0 OID 16617)
-- Dependencies: 228
-- Data for Name: equipamentos_especificacoes; Type: TABLE DATA; Schema: nexus; Owner: postgres
--

COPY nexus.equipamentos_especificacoes (id, equipamento_id, especificacao) FROM stdin;
21	5	Resolução 4K (3840 x 2160)
22	5	Brilho: 3500 lumens
23	5	Contraste: 10.000:1
24	5	HDMI, USB, WiFi
25	5	Correção trapezoidal
26	5	Zoom óptico 1.5x
27	5	Alto-falantes integrados 10W
28	5	Controle remoto incluído
29	6	Sensor Full-Frame 45MP
30	6	Vídeo 8K a 30fps
31	6	IBIS de 8 stops
32	6	Autofoco Dual Pixel
33	6	Tela touch articulada
34	6	WiFi e Bluetooth
35	6	Dois slots de cartão
36	6	Bateria de longa duração
37	7	Intel Core i9 13ª geração
38	7	32GB RAM DDR5
39	7	SSD 1TB NVMe
40	7	NVIDIA RTX 4060 8GB
41	7	Tela 15.6" 4K OLED
42	7	Thunderbolt 4
43	7	Webcam Full HD
44	7	Teclado retroiluminado
45	8	Tipo: Dinâmico
46	8	Padrão: Cardióide
47	8	Resposta: 50-20.000 Hz
48	8	Conexão: XLR
49	8	Filtro pop integrado
50	8	Suporte anti-choque
51	8	Filtros de graves e agudos
52	8	Construção metálica robusta
53	8	Chip Apple M2
54	8	Tela 12.9" Liquid Retina XDR
55	8	256GB de armazenamento
56	8	12MP câmera ultra-wide
57	8	5G integrado
58	8	Apple Pencil (2ª geração)
59	8	Magic Keyboard incluído
60	8	Bateria para o dia todo
61	10	3 painéis LED 60W
62	10	Temperatura de cor ajustável
63	10	2800K a 6500K
64	10	Controle de intensidade
65	10	CRI > 95
66	10	Tripés incluídos
67	10	Difusores e filtros
68	10	Case de transporte
\.


--
-- TOC entry 5242 (class 0 OID 16642)
-- Dependencies: 230
-- Data for Name: eventos; Type: TABLE DATA; Schema: nexus; Owner: postgres
--

COPY nexus.eventos (id, titulo, data_evento, hora_evento, localizacao, descricao, participantes, capacidade, instrutor, tipo, image, ambiente_id, created_at) FROM stdin;
6	Hackathon 2024	2024-12-20	09:00:00	Laboratório de Informática	Evento de inovação tecnológica onde equipes desenvolvem soluções criativas para problemas reais em 48 horas.	46	60	João Santos	hackathon	https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=800	21	2026-01-31 04:01:13.00638
7	Palestra: Inteligência Artificial	2024-12-18	16:00:00	Auditório Principal	Palestra sobre os últimos avanços em IA e suas aplicações práticas no mercado de trabalho.	81	100	Dr. Carlos Mendes	palestra	https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=800	22	2026-01-31 04:01:13.00638
8	Workshop de UX Design	2024-12-15	14:00:00	Sala de Reuniões A	Workshop completo sobre princípios de User Experience Design, incluindo práticas de prototipagem e testes com usuários.	25	30	Maria Silva	workshop	https://images.unsplash.com/photo-1531403009284-440f080d1e12?w=800	26	2026-01-31 04:01:13.00638
\.


--
-- TOC entry 5244 (class 0 OID 16665)
-- Dependencies: 232
-- Data for Name: eventos_equipamentos; Type: TABLE DATA; Schema: nexus; Owner: postgres
--

COPY nexus.eventos_equipamentos (id, evento_id, equipamento_id, quantidade) FROM stdin;
\.


--
-- TOC entry 5248 (class 0 OID 16714)
-- Dependencies: 236
-- Data for Name: historico; Type: TABLE DATA; Schema: nexus; Owner: postgres
--

COPY nexus.historico (id, user_id, agendamento_id, type, name, historico_date, start_time, end_time, purpose, status) FROM stdin;
9	88f7f338-b402-404f-986a-069606f51499	13	Ambientes	testePostam	2026-01-31	19:27:00	22:27:00	            teste	Confirmado
6	88f7f338-b402-404f-986a-069606f51499	11	Ambientes	Auditório Principal	2026-01-31	11:27:00	12:27:00	            teste	Cancelado
7	88f7f338-b402-404f-986a-069606f51499	11	Ambientes	Auditório Principal	2026-01-31	11:27:00	12:27:00	            teste	Concluido
8	88f7f338-b402-404f-986a-069606f51499	12	Ambientes	Estúdio Multimídia	2026-01-31	13:29:00	14:29:00	            teste	Concluido
\.


--
-- TOC entry 5254 (class 0 OID 16827)
-- Dependencies: 242
-- Data for Name: historico_equipamentos; Type: TABLE DATA; Schema: nexus; Owner: postgres
--

COPY nexus.historico_equipamentos (id, agendamento_id, equipamento_id, user_id, equipamento_nome, data_equip, hora_inicio, hora_fim, finalidade, status, criado_em) FROM stdin;
11	17	6	88f7f338-b402-404f-986a-069606f51499	Câmera Canon EOS R5	2026-01-31	14:45:00	16:45:00	      teste	Cancelado	2026-01-31 13:45:29.643695
\.


--
-- TOC entry 5258 (class 0 OID 16891)
-- Dependencies: 246
-- Data for Name: inscricoes_eventos; Type: TABLE DATA; Schema: nexus; Owner: postgres
--

COPY nexus.inscricoes_eventos (id, evento_id, user_id, status, data_inscricao) FROM stdin;
2	6	88f7f338-b402-404f-986a-069606f51499	Inscrito	2026-01-31 04:14:58.316137
3	7	88f7f338-b402-404f-986a-069606f51499	Inscrito	2026-01-31 04:18:35.213935
4	8	88f7f338-b402-404f-986a-069606f51499	Inscrito	2026-01-31 18:43:10.521306
\.


--
-- TOC entry 5246 (class 0 OID 16686)
-- Dependencies: 234
-- Data for Name: notificacoes; Type: TABLE DATA; Schema: nexus; Owner: postgres
--

COPY nexus.notificacoes (id, user_id, titulo, mensagem, tipo, lida, data_criacao) FROM stdin;
1	88f7f338-b402-404f-986a-069606f51499	Agendamento solicitado	Agendamento solicitado para dia 2026-01-30, Ambiente 1.	aviso	f	2026-01-30 00:03:19.558528
2	88f7f338-b402-404f-986a-069606f51499	O evento foi criado	O evento foi  'teste' criado	aviso	f	2026-01-30 00:07:30.647119
3	88f7f338-b402-404f-986a-069606f51499	O evento foi criado	O evento foi  'novo teste' criado	aviso	f	2026-01-30 00:22:05.701382
4	88f7f338-b402-404f-986a-069606f51499	Inscrição confirmada	Você foi inscrito no evento 'novo teste'.	sucesso	f	2026-01-30 00:22:14.542544
5	88f7f338-b402-404f-986a-069606f51499	Agendamento solicitado	Agendamento solicitado para dia '2026-01-31',Equipamentos '1.	aviso	f	2026-01-30 00:48:21.39498
6	88f7f338-b402-404f-986a-069606f51499	Agendamento solicitado	Agendamento solicitado para dia 2026-01-30, Ambiente 4.	aviso	f	2026-01-30 01:07:05.169557
7	88f7f338-b402-404f-986a-069606f51499	Agendamento solicitado	Agendamento solicitado para dia 2026-01-30, Ambiente 4.	aviso	f	2026-01-30 16:51:42.71168
8	88f7f338-b402-404f-986a-069606f51499	Agendamento solicitado	Agendamento solicitado para dia '2026-01-31',Equipamentos '1.	aviso	f	2026-01-30 16:51:59.211473
9	88f7f338-b402-404f-986a-069606f51499	Agendamento solicitado	Agendamento solicitado para dia '2026-01-30',Equipamentos '4.	aviso	f	2026-01-30 17:56:40.119501
10	88f7f338-b402-404f-986a-069606f51499	Agendamento solicitado	Agendamento solicitado para dia '2026-01-31',Equipamentos '4.	aviso	f	2026-01-30 18:18:11.979856
11	88f7f338-b402-404f-986a-069606f51499	Agendamento solicitado	Agendamento solicitado para dia 2026-01-30, Ambiente 5.	aviso	f	2026-01-30 18:47:31.510996
12	88f7f338-b402-404f-986a-069606f51499	Agendamento solicitado	Agendamento solicitado para dia '2026-01-31',Equipamentos '4.	aviso	f	2026-01-30 19:03:29.461176
13	88f7f338-b402-404f-986a-069606f51499	Agendamento solicitado	Agendamento solicitado para dia '2026-02-02',Equipamentos '4.	aviso	f	2026-01-30 19:19:55.99857
14	88f7f338-b402-404f-986a-069606f51499	Agendamento solicitado	Agendamento solicitado para dia 2026-02-03, Ambiente 5.	aviso	f	2026-01-30 20:11:11.161775
15	88f7f338-b402-404f-986a-069606f51499	Agendamento solicitado	Agendamento solicitado para dia '2026-01-30',Equipamentos '4.	aviso	f	2026-01-30 21:31:21.82851
16	88f7f338-b402-404f-986a-069606f51499	Agendamento solicitado	Agendamento solicitado para dia '2026-02-03',Equipamentos '4.	aviso	f	2026-01-30 21:51:17.07343
17	88f7f338-b402-404f-986a-069606f51499	Agendamento solicitado	Agendamento solicitado para dia '2026-01-31',Equipamentos '4.	aviso	f	2026-01-30 22:00:10.853504
18	88f7f338-b402-404f-986a-069606f51499	Agendamento solicitado	Agendamento solicitado para dia '2026-02-05',Equipamentos '4.	aviso	f	2026-01-30 23:01:08.302809
19	88f7f338-b402-404f-986a-069606f51499	Agendamento solicitado	Agendamento solicitado para dia '2026-02-07',Equipamentos '4.	aviso	f	2026-01-30 23:44:57.44429
20	88f7f338-b402-404f-986a-069606f51499	Agendamento solicitado	Agendamento solicitado para dia '2026-02-06',Equipamentos '4.	aviso	f	2026-01-30 23:45:45.299215
21	88f7f338-b402-404f-986a-069606f51499	Agendamento solicitado	Agendamento solicitado para dia 2026-02-08, Ambiente 5.	aviso	f	2026-01-31 02:26:57.846262
22	88f7f338-b402-404f-986a-069606f51499	Agendamento solicitado	Agendamento solicitado para dia '2026-02-08',Equipamentos '4.	aviso	f	2026-01-31 02:32:59.698748
23	88f7f338-b402-404f-986a-069606f51499	Inscrição confirmada	Você foi inscrito no evento 'Hackathon 2024'.	sucesso	f	2026-01-31 04:14:58.564618
24	88f7f338-b402-404f-986a-069606f51499	Inscrição confirmada	Você foi inscrito no evento 'Palestra: Inteligência Artificial'.	sucesso	f	2026-01-31 04:18:35.395799
25	88f7f338-b402-404f-986a-069606f51499	O evento foi criado	O evento foi  'teste' criado	aviso	f	2026-01-31 11:19:21.542349
26	88f7f338-b402-404f-986a-069606f51499	Agendamento solicitado	Agendamento solicitado para dia 2026-01-31, Ambiente 22.	aviso	f	2026-01-31 11:27:29.92263
27	88f7f338-b402-404f-986a-069606f51499	Agendamento solicitado	Agendamento solicitado para dia 2026-01-31, Ambiente 24.	aviso	f	2026-01-31 11:29:54.91881
28	88f7f338-b402-404f-986a-069606f51499	Agendamento solicitado	Agendamento solicitado para dia 2026-01-31, Ambiente 27.	aviso	f	2026-01-31 13:28:03.500159
29	88f7f338-b402-404f-986a-069606f51499	Agendamento solicitado	Agendamento solicitado para dia '2026-01-31',Equipamentos '6.	aviso	f	2026-01-31 13:45:16.600446
30	88f7f338-b402-404f-986a-069606f51499	Agendamento solicitado	Agendamento solicitado para dia 2026-02-06, Ambiente 22.	aviso	f	2026-01-31 17:16:47.410487
31	88f7f338-b402-404f-986a-069606f51499	Inscrição confirmada	Você foi inscrito no evento 'Workshop de UX Design'.	sucesso	f	2026-01-31 18:43:10.676611
\.


--
-- TOC entry 5250 (class 0 OID 16768)
-- Dependencies: 238
-- Data for Name: pendentes_ambientes; Type: TABLE DATA; Schema: nexus; Owner: postgres
--

COPY nexus.pendentes_ambientes (id, agendamento_id, user_id, status, created_at) FROM stdin;
7	11	88f7f338-b402-404f-986a-069606f51499	Confirmado	2026-01-31 11:27:29.485314
8	12	88f7f338-b402-404f-986a-069606f51499	Confirmado	2026-01-31 11:29:54.487078
9	13	88f7f338-b402-404f-986a-069606f51499	Confirmado	2026-01-31 13:28:03.365474
10	14	88f7f338-b402-404f-986a-069606f51499	pendente	2026-01-31 17:16:46.654639
\.


--
-- TOC entry 5256 (class 0 OID 16857)
-- Dependencies: 244
-- Data for Name: pendentes_equipamentos; Type: TABLE DATA; Schema: nexus; Owner: postgres
--

COPY nexus.pendentes_equipamentos (id, agendamento_id, user_id, status, created_at) FROM stdin;
14	17	88f7f338-b402-404f-986a-069606f51499	Confirmado	2026-01-31 13:45:16.480876
\.


--
-- TOC entry 5260 (class 0 OID 32769)
-- Dependencies: 250
-- Data for Name: recursos_ambientes; Type: TABLE DATA; Schema: nexus; Owner: postgres
--

COPY nexus.recursos_ambientes (id, recursos_id, recursos) FROM stdin;
29	21	30 computadores
30	21	Projetor 4K
31	21	Software especializado
32	21	Rede de alta velocidade
33	21	Estações de trabalho individuais
34	21	Ar condicionado duplo
35	21	Iluminação ajustável
36	21	Sistema de som ambiente
37	22	Sistema de som profissional
38	22	Projetor de alta resolução
39	22	Palco amplo
40	22	Iluminação cênica
41	22	Assentos estofados
42	22	Telão de 5 metros
43	22	Microfones sem fio
44	22	Camarim anexo
45	23	Móveis modulares
46	23	Quadros brancos nas paredes
47	23	Post-its e materiais
48	23	Almofadas e puffs
49	23	Iluminação natural
50	23	TV para apresentações
51	23	Coffee point
52	23	Decoração inspiradora
53	24	Isolamento acústico
54	24	Câmeras profissionais
55	24	Microfones de estúdio
56	24	Iluminação de três pontos
57	24	Chroma key verde
58	24	Mesa de edição
59	24	Monitores de referência
60	24	Computador para edição
61	25	Mesas e cadeiras móveis
62	25	Projetor interativo
63	25	Sistema de áudio
64	25	Câmera para gravação
65	25	Quadro flip chart
66	25	Material didático
67	25	Ar condicionado
68	25	Acesso para PCD
69	26	TV 55 polegadas
70	26	Sistema de videoconferência
71	26	Quadro branco
72	26	Ar condicionado
73	26	Wi-Fi de alta velocidade
74	26	Mesa de reunião executiva
75	26	Cadeiras ergonômicas
76	26	Tomadas em todos os lugares
\.


--
-- TOC entry 5232 (class 0 OID 16501)
-- Dependencies: 220
-- Data for Name: users; Type: TABLE DATA; Schema: nexus; Owner: postgres
--

COPY nexus.users (id, name, email, cpf, rg, data_nascimento, telefone, endereco, departamento, funcao, role, image, status, senha, created_at, updated_at) FROM stdin;
88f7f338-b402-404f-986a-069606f51499	jo	jo@gmail.com	23399480440	42594956	2026-01-29	8299999999999	None	TI	dev	admin	/static/imgs/0d97e5ba-32c4-46cc-95e0-4275098d10de_Modelo1.png	ativo	$2b$12$CzMKX292HIp09xiCrpu8we8c2s82oJTP310LF2xZtVi7Tz/.PGvJ.	2026-01-29 21:29:09.887223	2026-01-29 22:45:37.674499
a9dac88c-540e-4270-997f-34cf9603c48e	Administrador	admin@nexus.com	00000000000	34298384	1990-01-01	82987343350	rua telma 	TI	Admin	admin	/static/imgs/a245622e-7e1c-494c-90e6-308d3d1b4f57_Gemini_Generated_Image_xt7s61xt7s61xt7s.png	ativo	$2b$12$O0dC9y8bTUwppgSD/pdqrefUZ.DwQ9ykZarqmOhxQ0dl.oDGYm4Dm	2026-01-29 17:27:13.44894	2026-01-30 22:42:36.889991
\.


--
-- TOC entry 5280 (class 0 OID 0)
-- Dependencies: 239
-- Name: agendamentos_equipamentos_id_seq; Type: SEQUENCE SET; Schema: nexus; Owner: postgres
--

SELECT pg_catalog.setval('nexus.agendamentos_equipamentos_id_seq', 17, true);


--
-- TOC entry 5281 (class 0 OID 0)
-- Dependencies: 223
-- Name: agendamentos_id_seq; Type: SEQUENCE SET; Schema: nexus; Owner: postgres
--

SELECT pg_catalog.setval('nexus.agendamentos_id_seq', 14, true);


--
-- TOC entry 5282 (class 0 OID 0)
-- Dependencies: 221
-- Name: ambientes_id_seq; Type: SEQUENCE SET; Schema: nexus; Owner: postgres
--

SELECT pg_catalog.setval('nexus.ambientes_id_seq', 27, true);


--
-- TOC entry 5283 (class 0 OID 0)
-- Dependencies: 227
-- Name: equipamentos_especificacoes_id_seq; Type: SEQUENCE SET; Schema: nexus; Owner: postgres
--

SELECT pg_catalog.setval('nexus.equipamentos_especificacoes_id_seq', 68, true);


--
-- TOC entry 5284 (class 0 OID 0)
-- Dependencies: 225
-- Name: equipamentos_id_seq; Type: SEQUENCE SET; Schema: nexus; Owner: postgres
--

SELECT pg_catalog.setval('nexus.equipamentos_id_seq', 11, true);


--
-- TOC entry 5285 (class 0 OID 0)
-- Dependencies: 231
-- Name: eventos_equipamentos_id_seq; Type: SEQUENCE SET; Schema: nexus; Owner: postgres
--

SELECT pg_catalog.setval('nexus.eventos_equipamentos_id_seq', 2, true);


--
-- TOC entry 5286 (class 0 OID 0)
-- Dependencies: 229
-- Name: eventos_id_seq; Type: SEQUENCE SET; Schema: nexus; Owner: postgres
--

SELECT pg_catalog.setval('nexus.eventos_id_seq', 9, true);


--
-- TOC entry 5287 (class 0 OID 0)
-- Dependencies: 241
-- Name: historico_equipamentos_id_seq; Type: SEQUENCE SET; Schema: nexus; Owner: postgres
--

SELECT pg_catalog.setval('nexus.historico_equipamentos_id_seq', 11, true);


--
-- TOC entry 5288 (class 0 OID 0)
-- Dependencies: 235
-- Name: historico_id_seq; Type: SEQUENCE SET; Schema: nexus; Owner: postgres
--

SELECT pg_catalog.setval('nexus.historico_id_seq', 9, true);


--
-- TOC entry 5289 (class 0 OID 0)
-- Dependencies: 245
-- Name: inscricoes_eventos_id_seq; Type: SEQUENCE SET; Schema: nexus; Owner: postgres
--

SELECT pg_catalog.setval('nexus.inscricoes_eventos_id_seq', 4, true);


--
-- TOC entry 5290 (class 0 OID 0)
-- Dependencies: 233
-- Name: notificacoes_id_seq; Type: SEQUENCE SET; Schema: nexus; Owner: postgres
--

SELECT pg_catalog.setval('nexus.notificacoes_id_seq', 31, true);


--
-- TOC entry 5291 (class 0 OID 0)
-- Dependencies: 237
-- Name: pendentes_ambientes_id_seq; Type: SEQUENCE SET; Schema: nexus; Owner: postgres
--

SELECT pg_catalog.setval('nexus.pendentes_ambientes_id_seq', 10, true);


--
-- TOC entry 5292 (class 0 OID 0)
-- Dependencies: 243
-- Name: pendentes_equipamentos_id_seq; Type: SEQUENCE SET; Schema: nexus; Owner: postgres
--

SELECT pg_catalog.setval('nexus.pendentes_equipamentos_id_seq', 14, true);


--
-- TOC entry 5293 (class 0 OID 0)
-- Dependencies: 249
-- Name: recursos_ambientes_id_seq; Type: SEQUENCE SET; Schema: nexus; Owner: postgres
--

SELECT pg_catalog.setval('nexus.recursos_ambientes_id_seq', 76, true);


--
-- TOC entry 5053 (class 2606 OID 16815)
-- Name: agendamentos_equipamentos agendamentos_equipamentos_pkey; Type: CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.agendamentos_equipamentos
    ADD CONSTRAINT agendamentos_equipamentos_pkey PRIMARY KEY (id);


--
-- TOC entry 5029 (class 2606 OID 16587)
-- Name: agendamentos agendamentos_pkey; Type: CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.agendamentos
    ADD CONSTRAINT agendamentos_pkey PRIMARY KEY (id);


--
-- TOC entry 5027 (class 2606 OID 16553)
-- Name: ambientes ambientes_pkey; Type: CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.ambientes
    ADD CONSTRAINT ambientes_pkey PRIMARY KEY (id);


--
-- TOC entry 5035 (class 2606 OID 16625)
-- Name: equipamentos_especificacoes equipamentos_especificacoes_pkey; Type: CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.equipamentos_especificacoes
    ADD CONSTRAINT equipamentos_especificacoes_pkey PRIMARY KEY (id);


--
-- TOC entry 5033 (class 2606 OID 16615)
-- Name: equipamentos equipamentos_pkey; Type: CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.equipamentos
    ADD CONSTRAINT equipamentos_pkey PRIMARY KEY (id);


--
-- TOC entry 5039 (class 2606 OID 16674)
-- Name: eventos_equipamentos eventos_equipamentos_evento_id_equipamento_id_key; Type: CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.eventos_equipamentos
    ADD CONSTRAINT eventos_equipamentos_evento_id_equipamento_id_key UNIQUE (evento_id, equipamento_id);


--
-- TOC entry 5041 (class 2606 OID 16672)
-- Name: eventos_equipamentos eventos_equipamentos_pkey; Type: CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.eventos_equipamentos
    ADD CONSTRAINT eventos_equipamentos_pkey PRIMARY KEY (id);


--
-- TOC entry 5037 (class 2606 OID 16658)
-- Name: eventos eventos_pkey; Type: CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.eventos
    ADD CONSTRAINT eventos_pkey PRIMARY KEY (id);


--
-- TOC entry 5055 (class 2606 OID 16845)
-- Name: historico_equipamentos historico_equipamentos_pkey; Type: CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.historico_equipamentos
    ADD CONSTRAINT historico_equipamentos_pkey PRIMARY KEY (id);


--
-- TOC entry 5045 (class 2606 OID 16724)
-- Name: historico historico_pkey; Type: CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.historico
    ADD CONSTRAINT historico_pkey PRIMARY KEY (id);


--
-- TOC entry 5061 (class 2606 OID 16901)
-- Name: inscricoes_eventos inscricoes_eventos_pkey; Type: CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.inscricoes_eventos
    ADD CONSTRAINT inscricoes_eventos_pkey PRIMARY KEY (id);


--
-- TOC entry 5043 (class 2606 OID 16697)
-- Name: notificacoes notificacoes_pkey; Type: CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.notificacoes
    ADD CONSTRAINT notificacoes_pkey PRIMARY KEY (id);


--
-- TOC entry 5049 (class 2606 OID 16780)
-- Name: pendentes_ambientes pendentes_ambientes_agendamento_id_key; Type: CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.pendentes_ambientes
    ADD CONSTRAINT pendentes_ambientes_agendamento_id_key UNIQUE (agendamento_id);


--
-- TOC entry 5051 (class 2606 OID 16778)
-- Name: pendentes_ambientes pendentes_ambientes_pkey; Type: CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.pendentes_ambientes
    ADD CONSTRAINT pendentes_ambientes_pkey PRIMARY KEY (id);


--
-- TOC entry 5057 (class 2606 OID 16869)
-- Name: pendentes_equipamentos pendentes_equipamentos_agendamento_id_key; Type: CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.pendentes_equipamentos
    ADD CONSTRAINT pendentes_equipamentos_agendamento_id_key UNIQUE (agendamento_id);


--
-- TOC entry 5059 (class 2606 OID 16867)
-- Name: pendentes_equipamentos pendentes_equipamentos_pkey; Type: CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.pendentes_equipamentos
    ADD CONSTRAINT pendentes_equipamentos_pkey PRIMARY KEY (id);


--
-- TOC entry 5065 (class 2606 OID 32777)
-- Name: recursos_ambientes recursos_ambientes_pkey; Type: CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.recursos_ambientes
    ADD CONSTRAINT recursos_ambientes_pkey PRIMARY KEY (id);


--
-- TOC entry 5063 (class 2606 OID 16903)
-- Name: inscricoes_eventos uq_evento_usuario; Type: CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.inscricoes_eventos
    ADD CONSTRAINT uq_evento_usuario UNIQUE (evento_id, user_id);


--
-- TOC entry 5023 (class 2606 OID 16520)
-- Name: users users_email_key; Type: CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- TOC entry 5025 (class 2606 OID 16518)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 5030 (class 1259 OID 16593)
-- Name: idx_agendamento_data; Type: INDEX; Schema: nexus; Owner: postgres
--

CREATE INDEX idx_agendamento_data ON nexus.agendamentos USING btree (data);


--
-- TOC entry 5031 (class 1259 OID 16594)
-- Name: idx_agendamento_status; Type: INDEX; Schema: nexus; Owner: postgres
--

CREATE INDEX idx_agendamento_status ON nexus.agendamentos USING btree (status);


--
-- TOC entry 5046 (class 1259 OID 16736)
-- Name: idx_historico_agendamento; Type: INDEX; Schema: nexus; Owner: postgres
--

CREATE INDEX idx_historico_agendamento ON nexus.historico USING btree (agendamento_id);


--
-- TOC entry 5047 (class 1259 OID 16735)
-- Name: idx_historico_user; Type: INDEX; Schema: nexus; Owner: postgres
--

CREATE INDEX idx_historico_user ON nexus.historico USING btree (user_id);


--
-- TOC entry 5084 (class 2620 OID 32794)
-- Name: pendentes_equipamentos trg_historico_equipamento; Type: TRIGGER; Schema: nexus; Owner: postgres
--

CREATE TRIGGER trg_historico_equipamento AFTER UPDATE ON nexus.pendentes_equipamentos FOR EACH ROW EXECUTE FUNCTION nexus.fn_criar_historico_equipamento();


--
-- TOC entry 5066 (class 2606 OID 16588)
-- Name: agendamentos agendamentos_ambiente_id_fkey; Type: FK CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.agendamentos
    ADD CONSTRAINT agendamentos_ambiente_id_fkey FOREIGN KEY (ambiente_id) REFERENCES nexus.ambientes(id) ON DELETE CASCADE;


--
-- TOC entry 5067 (class 2606 OID 16626)
-- Name: equipamentos_especificacoes equipamentos_especificacoes_equipamento_id_fkey; Type: FK CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.equipamentos_especificacoes
    ADD CONSTRAINT equipamentos_especificacoes_equipamento_id_fkey FOREIGN KEY (equipamento_id) REFERENCES nexus.equipamentos(id) ON DELETE CASCADE;


--
-- TOC entry 5068 (class 2606 OID 32788)
-- Name: eventos eventos_ambiente_id_fkey; Type: FK CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.eventos
    ADD CONSTRAINT eventos_ambiente_id_fkey FOREIGN KEY (ambiente_id) REFERENCES nexus.ambientes(id) ON DELETE CASCADE;


--
-- TOC entry 5069 (class 2606 OID 16680)
-- Name: eventos_equipamentos eventos_equipamentos_equipamento_id_fkey; Type: FK CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.eventos_equipamentos
    ADD CONSTRAINT eventos_equipamentos_equipamento_id_fkey FOREIGN KEY (equipamento_id) REFERENCES nexus.equipamentos(id);


--
-- TOC entry 5070 (class 2606 OID 16675)
-- Name: eventos_equipamentos eventos_equipamentos_evento_id_fkey; Type: FK CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.eventos_equipamentos
    ADD CONSTRAINT eventos_equipamentos_evento_id_fkey FOREIGN KEY (evento_id) REFERENCES nexus.eventos(id) ON DELETE CASCADE;


--
-- TOC entry 5075 (class 2606 OID 16821)
-- Name: agendamentos_equipamentos fk_ag_equip_equipamento; Type: FK CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.agendamentos_equipamentos
    ADD CONSTRAINT fk_ag_equip_equipamento FOREIGN KEY (equipamento_id) REFERENCES nexus.equipamentos(id) ON DELETE CASCADE;


--
-- TOC entry 5076 (class 2606 OID 16816)
-- Name: agendamentos_equipamentos fk_ag_equip_user; Type: FK CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.agendamentos_equipamentos
    ADD CONSTRAINT fk_ag_equip_user FOREIGN KEY (user_id) REFERENCES nexus.users(id) ON DELETE CASCADE;


--
-- TOC entry 5082 (class 2606 OID 32783)
-- Name: recursos_ambientes fk_ambiente; Type: FK CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.recursos_ambientes
    ADD CONSTRAINT fk_ambiente FOREIGN KEY (recursos_id) REFERENCES nexus.ambientes(id) ON DELETE CASCADE;


--
-- TOC entry 5077 (class 2606 OID 16846)
-- Name: historico_equipamentos fk_hist_eq_agendamento; Type: FK CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.historico_equipamentos
    ADD CONSTRAINT fk_hist_eq_agendamento FOREIGN KEY (agendamento_id) REFERENCES nexus.agendamentos_equipamentos(id) ON DELETE CASCADE;


--
-- TOC entry 5078 (class 2606 OID 16851)
-- Name: historico_equipamentos fk_hist_eq_equipamento; Type: FK CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.historico_equipamentos
    ADD CONSTRAINT fk_hist_eq_equipamento FOREIGN KEY (equipamento_id) REFERENCES nexus.equipamentos(id) ON DELETE CASCADE;


--
-- TOC entry 5072 (class 2606 OID 16725)
-- Name: historico fk_historico_agendamento; Type: FK CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.historico
    ADD CONSTRAINT fk_historico_agendamento FOREIGN KEY (agendamento_id) REFERENCES nexus.agendamentos(id) ON DELETE CASCADE;


--
-- TOC entry 5073 (class 2606 OID 16730)
-- Name: historico fk_historico_user; Type: FK CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.historico
    ADD CONSTRAINT fk_historico_user FOREIGN KEY (user_id) REFERENCES nexus.users(id) ON DELETE CASCADE;


--
-- TOC entry 5080 (class 2606 OID 16904)
-- Name: inscricoes_eventos fk_inscricao_evento; Type: FK CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.inscricoes_eventos
    ADD CONSTRAINT fk_inscricao_evento FOREIGN KEY (evento_id) REFERENCES nexus.eventos(id) ON DELETE CASCADE;


--
-- TOC entry 5081 (class 2606 OID 16909)
-- Name: inscricoes_eventos fk_inscricao_usuario; Type: FK CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.inscricoes_eventos
    ADD CONSTRAINT fk_inscricao_usuario FOREIGN KEY (user_id) REFERENCES nexus.users(id) ON DELETE CASCADE;


--
-- TOC entry 5074 (class 2606 OID 16781)
-- Name: pendentes_ambientes fk_pendente_amb_agendamento; Type: FK CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.pendentes_ambientes
    ADD CONSTRAINT fk_pendente_amb_agendamento FOREIGN KEY (agendamento_id) REFERENCES nexus.agendamentos(id) ON DELETE CASCADE;


--
-- TOC entry 5079 (class 2606 OID 16870)
-- Name: pendentes_equipamentos fk_pendente_equip_agendamento; Type: FK CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.pendentes_equipamentos
    ADD CONSTRAINT fk_pendente_equip_agendamento FOREIGN KEY (agendamento_id) REFERENCES nexus.agendamentos_equipamentos(id) ON DELETE CASCADE;


--
-- TOC entry 5071 (class 2606 OID 16698)
-- Name: notificacoes notificacoes_user_id_fkey; Type: FK CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.notificacoes
    ADD CONSTRAINT notificacoes_user_id_fkey FOREIGN KEY (user_id) REFERENCES nexus.users(id) ON DELETE CASCADE;


--
-- TOC entry 5083 (class 2606 OID 32778)
-- Name: recursos_ambientes recursos_ambientes_recursos_id_fkey; Type: FK CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.recursos_ambientes
    ADD CONSTRAINT recursos_ambientes_recursos_id_fkey FOREIGN KEY (recursos_id) REFERENCES nexus.ambientes(id) ON DELETE CASCADE;


-- Completed on 2026-02-01 23:11:19

--
-- PostgreSQL database dump complete
--

\unrestrict fJ3snmeEH4eQuSMXuewt87TTAhy6oSaIPVUhTJLNSzNTjUo55I9roflMHq91MPE

