import streamlit as st
import sqlite3
import pandas as pd
from datetime import date
import urllib.parse

# Configuração da página
st.set_page_config(page_title="Caprichos da Vânia - Vania Leonardo", page_icon="✂️", layout="wide")

# --- DESIGN SOFISTICADO & FIX PARA FICAR LADO A LADO NO CELULAR ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    /* Limpeza de margens no topo/lados do celular */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1.5rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
    }

    /* Fundo Rose Suave */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #faf4f5;
        color: #2c1820;
    }

    /* CABEÇALHO DO ATELIÊ */
    .header-box {
        text-align: center;
        padding: 5px 0 10px 0;
    }
    .header-title {
        font-family: 'Cormorant Garamond', serif;
        color: #8c2b4e;
        font-size: 2rem !important;
        font-weight: 700;
        margin: 0;
        line-height: 1.1;
    }
    .header-subtitle {
        color: #613346;
        font-size: 0.8rem !important;
        font-weight: 600;
        margin: 4px 0 2px 0;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    .header-slogan {
        font-family: 'Cormorant Garamond', serif;
        font-style: italic;
        color: #ad3b66;
        font-size: 0.95rem !important;
        margin: 2px 0 0 0;
        font-weight: 600;
    }

    /* 🚨 FORÇAR COLUNAS LADO A LADO NO CELULAR (OVERRIDE DO STREAMLIT) 🚨 */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 8px !important;
        width: 100% !important;
    }

    [data-testid="column"] {
        width: 50% !important;
        flex: 1 1 50% !important;
        min-width: 0 !important;
    }

    /* CARDS DE MÉTRICAS - ROSA CHIC */
    .metric-card {
        background: linear-gradient(145deg, #ffffff, #fff0f3);
        border: 1px solid #eab8c4;
        border-radius: 12px;
        padding: 8px 4px;
        text-align: center;
        box-shadow: 0px 3px 8px rgba(140, 43, 78, 0.06);
    }
    .metric-label {
        color: #613346;
        font-size: 0.75rem;
        font-weight: 700;
        margin-bottom: 2px;
        white-space: nowrap;
    }
    .metric-value {
        color: #8c2b4e;
        font-size: 1.5rem;
        font-weight: 700;
        line-height: 1;
    }

    /* SUBTÍTULO EM DESTAQUE */
    .section-banner {
        text-align: center;
        color: #8c2b4e;
        font-weight: 700;
        font-size: 0.9rem;
        margin: 12px 0 8px 0;
    }

    /* CARDS DE NAVEGAÇÃO LADO A LADO */
    .nav-card-title {
        color: #8c2b4e;
        font-weight: 700;
        font-size: 0.88rem;
        margin-bottom: 3px;
        text-align: center;
        white-space: nowrap;
    }
    .nav-card-desc {
        color: #4a2835;
        font-size: 0.7rem;
        font-weight: 500;
        margin-bottom: 8px;
        line-height: 1.2;
        text-align: center;
        min-height: 32px; /* Garante que os cards tenham a mesma altura */
    }

    /* BOTÕES AJUSTADOS PARA CELULAR */
    .stButton > button {
        background: linear-gradient(135deg, #a8325c 0%, #8c2b4e 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 20px !important;
        font-weight: 600 !important;
        font-size: 0.78rem !important;
        padding: 4px 8px !important;
        min-height: 36px !important;
        width: 100% !important;
        box-shadow: 0px 3px 8px rgba(140, 43, 78, 0.2) !important;
    }

    .stButton > button:active {
        transform: scale(0.96);
    }

    /* INPUTS */
    .stTextInput input, .stTextArea textarea, .stDateInput input {
        border-radius: 10px !important;
        border: 1px solid #e2a8b6 !important;
        color: #2c1820 !important;
        font-weight: 500 !important;
    }

    .stTextInput label, .stTextArea label, .stDateInput label {
        color: #613346 !important;
        font-weight: 600 !important;
        font-size: 0.82rem !important;
    }

    hr {
        border: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, #eab8c4, transparent);
        margin: 12px 0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- BANCO DE DADOS ---
def get_connection():
    return sqlite3.connect('ateliervania.db', check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT,
            data_entrega TEXT,
            data_evento TEXT,
            orcamento TEXT,
            ombro TEXT,
            cava_frente TEXT,
            cava_costas TEXT,
            altura_busto TEXT,
            busto TEXT,
            separacao_busto TEXT,
            altura_cintura TEXT,
            cintura_alta TEXT,
            cintura_baixa TEXT,
            altura_quadril TEXT,
            quadril TEXT,
            tamanho_vestido TEXT,
            tamanho_saia TEXT,
            tamanho_blusa TEXT,
            tamanho_manga TEXT,
            largura_manga TEXT,
            colarinho TEXT,
            observacoes TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# --- NAVEGAÇÃO ---
if 'pagina' not in st.session_state:
    st.session_state.pagina = "🌸 Início / Capa"

# --- MENU LATERAL (SIDEBAR) ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #8c2b4e; font-family: Cormorant Garamond, serif; font-size: 1.8rem; margin-bottom: 0;'>✂️ Vania Leonardo</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #613346; font-size: 0.8rem; font-weight: 600; margin-top: 0;'>DESIGNER DE MODA</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    opcoes_menu = ["🌸 Início / Capa", "📝 Nova Medida", "🔍 Consultar Medidas & WhatsApp"]
    index_atual = opcoes_menu.index(st.session_state.pagina) if st.session_state.pagina in opcoes_menu else 0
    
    escolha = st.radio("✨ **Menu Principal**", opcoes_menu, index=index_atual)
    st.session_state.pagina = escolha
    
    st.markdown("---")
    st.markdown("""
        <div style='background: #fff0f3; padding: 10px; border-radius: 10px; border: 1px solid #f2c2cd; text-align: center;'>
            <p style='margin:0; color: #8c2b4e; font-size: 0.8rem; font-weight: 600;'>✨ <i>"Você sonha, nós Realizamos!"</i></p>
        </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 🌸 TELA 1: CAPA (INÍCIO)
# ==============================================================================
if st.session_state.pagina == "🌸 Início / Capa":
    # Cabeçalho Principal
    st.markdown("""
        <div class="header-box">
            <h1 class="header-title">✂️ Caprichos da Vânia</h1>
            <p class="header-subtitle">Vania Leonardo | Designer de Moda</p>
            <p class="header-slogan">"Quando ama o que se faz, se faz com capricho. 🥰"</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Busca contagem no BD
    conn = get_connection()
    df_total = pd.read_sql_query("SELECT * FROM clientes", conn)
    conn.close()
    qtd = len(df_total)

    # 1. MÉTRICAS LADO A LADO NO CELULAR
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">👥 Clientes</div>
                <div class="metric-value">{qtd}</div>
            </div>
        """, unsafe_allow_html=True)

    with col_m2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">🪡 Medidas Salvas</div>
                <div class="metric-value">{qtd}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<p class='section-banner'>✨ Você sonha, nós Realizamos!</p>", unsafe_allow_html=True)

    # 2. CARDS LADO A LADO NO CELULAR
    col_c1, col_c2 = st.columns(2)

    with col_c1:
        st.markdown("""
            <div class="nav-card-title">📝 Nova Medida</div>
            <div class="nav-card-desc">Cadastre dados e 17 medidas completas.</div>
        """, unsafe_allow_html=True)
        if st.button("✨ Cadastrar", key="btn_cad", use_container_width=True):
            st.session_state.pagina = "📝 Nova Medida"
            st.rerun()

    with col_c2:
        st.markdown("""
            <div class="nav-card-title">🔍 Consultar</div>
            <div class="nav-card-desc">Busque medidas e envie pelo WhatsApp.</div>
        """, unsafe_allow_html=True)
        if st.button("📲 Consultar", key="btn_cons", use_container_width=True):
            st.session_state.pagina = "🔍 Consultar Medidas & WhatsApp"
            st.rerun()

# ==============================================================================
# 📝 TELA 2: NOVA MEDIDA
# ==============================================================================
elif st.session_state.pagina == "📝 Nova Medida":
    st.markdown("<h2 style='color: #8c2b4e; font-family: Cormorant Garamond, serif; font-size: 1.5rem; margin-bottom: 0;'>📝 Cadastrar Nova Medida</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("<h4 style='color: #8c2b4e; font-size: 0.9rem; margin-bottom: 8px;'>👤 Dados da Cliente & Prazos</h4>", unsafe_allow_html=True)
    nome = st.text_input("Nome da Cliente *")
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        telefone = st.text_input("Telefone (WhatsApp)")
    with col_t2:
        orcamento = st.text_input("Orçamento (R$)", placeholder="Ex: 350,00")
    
    col_dt1, col_dt2 = st.columns(2)
    with col_dt1:
        data_entrega = st.date_input("📦 Data Entrega", value=date.today())
    with col_dt2:
        data_evento = st.date_input("🎉 Data Evento", value=date.today())

    st.markdown("---")
    st.markdown("<h4 style='color: #8c2b4e; font-size: 0.9rem; margin-bottom: 8px;'>📏 Medidas (cm)</h4>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        ombro = st.text_input("📏 Ombro")
        cava_frente = st.text_input("📐 Cava frente")
        cava_costas = st.text_input("📐 Cava costas")
        altura_busto = st.text_input("🪡 Altura busto")
        busto = st.text_input("👗 Busto")
        separacao_busto = st.text_input("↔️ Separação busto")
        altura_cintura = st.text_input("🪡 Altura cintura")
        cintura_alta = st.text_input("⏳ Cintura alta")
        cintura_baixa = st.text_input("⏳ Cintura baixa")

    with col2:
        altura_quadril = st.text_input("🪡 Altura quadril")
        quadril = st.text_input("🧵 Quadril")
        tamanho_vestido = st.text_input("👗 Tam. vestido")
        tamanho_saia = st.text_input("🥻 Tam. saia")
        tamanho_blusa = st.text_input("👔 Tam. blusa")
        tamanho_manga = st.text_input("📏 Tam. manga")
        largura_manga = st.text_input("📐 Largura manga")
        colarinho = st.text_input("👔 Colarinho")

    st.markdown("---")
    observacoes = st.text_area("📝 Observações / Detalhes do Modelo")

    if st.button("💖 Salvar Medidas no Ateliê", use_container_width=True):
        if not nome.strip():
            st.error("Por favor, preencha o nome da cliente!")
        else:
            conn = get_connection()
            c = conn.cursor()
            c.execute('''
                INSERT INTO clientes (
                    nome, telefone, data_entrega, data_evento, orcamento, ombro, cava_frente, cava_costas, 
                    altura_busto, busto, separacao_busto, altura_cintura, cintura_alta, cintura_baixa, 
                    altura_quadril, quadril, tamanho_vestido, tamanho_saia, tamanho_blusa, tamanho_manga, 
                    largura_manga, colarinho, observacoes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                nome, telefone, data_entrega.strftime("%d/%m/%Y"), data_evento.strftime("%d/%m/%Y"),
                orcamento, ombro, cava_frente, cava_costas, altura_busto, busto, separacao_busto, 
                altura_cintura, cintura_alta, cintura_baixa, altura_quadril, quadril, 
                tamanho_vestido, tamanho_saia, tamanho_blusa, tamanho_manga, largura_manga, 
                colarinho, observacoes
            ))
            conn.commit()
            conn.close()
            st.success(f"🎉 Medidas de **{nome}** salvas com sucesso!")

# ==============================================================================
# 🔍 TELA 3: CONSULTAR MEDIDAS & WHATSAPP
# ==============================================================================
elif st.session_state.pagina == "🔍 Consultar Medidas & WhatsApp":
    st.markdown("<h2 style='color: #8c2b4e; font-family: Cormorant Garamond, serif; font-size: 1.5rem; margin-bottom: 0;'>🔍 Consultar Medidas & WhatsApp</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM clientes ORDER BY id DESC", conn)
    conn.close()

    if df.empty:
        st.info("Nenhuma cliente cadastrada no momento.")
    else:
        busca = st.text_input("🔎 Buscar por nome da cliente")
        if busca:
            df = df[df['nome'].str.contains(busca, case=False, na=False)]

        for _, row in df.iterrows():
            valor_orc = f"R$ {row['orcamento']}" if row['orcamento'] else "A combinar"
            
            with st.expander(f"💖 {row['nome']} | 📦 Entrega: {row['data_entrega']}"):
                st.write(f"📱 **Tel:** {row['telefone']} | 💰 **Orçamento:** {valor_orc}")
                st.write(f"📦 **Entrega:** {row['data_entrega']} | 🎉 **Evento:** {row['data_evento']}")
                
                c_m1, c_m2 = st.columns(2)
                with c_m1:
                    st.write(f"📏 **Ombro:** {row['ombro']}")
                    st.write(f"📐 **Cava fr.:** {row['cava_frente']}")
                    st.write(f"📐 **Cava cost.:** {row['cava_costas']}")
                    st.write(f"🪡 **Alt. busto:** {row['altura_busto']}")
                    st.write(f"👗 **Busto:** {row['busto']}")
                    st.write(f"↔️ **Sep. busto:** {row['separacao_busto']}")
                    st.write(f"🪡 **Alt. cintura:** {row['altura_cintura']}")
                    st.write(f"⏳ **Cint. alta:** {row['cintura_alta']}")
                    st.write(f"⏳ **Cint. baixa:** {row['cintura_baixa']}")

                with c_m2:
                    st.write(f"🪡 **Alt. quadril:** {row['altura_quadril']}")
                    st.write(f"🧵 **Quadril:** {row['quadril']}")
                    st.write(f"👗 **Tam. vest.:** {row['tamanho_vestido']}")
                    st.write(f"🥻 **Tam. saia:** {row['tamanho_saia']}")
                    st.write(f"👔 **Tam. blusa:** {row['tamanho_blusa']}")
                    st.write(f"📏 **Tam. manga:** {row['tamanho_manga']}")
                    st.write(f"📐 **Larg. manga:** {row['largura_manga']}")
                    st.write(f"👔 **Colarinho:** {row['colarinho']}")

                if row['observacoes']:
                    st.info(f"📝 **Obs:** {row['observacoes']}")

                # Mensagem Formatada WhatsApp
                msg = f"✨ *CAPRICHOS DA VÂNIA* ✨\n"
                msg += f"👗 _Vania Leonardo | Designer de Moda_\n"
                msg += f"✂️ _Costura sob medida_\n"
                msg += f"💖 _\"Você sonha, nós Realizamos!\"_\n\n"
                msg += f"👤 *Cliente:* {row['nome']}\n"
                if row['orcamento']:
                    msg += f"💰 *Valor do Orçamento:* R$ {row['orcamento']}\n"
                msg += f"📦 *Data da Entrega:* {row['data_entrega']}\n"
                msg += f"🎉 *Data do Evento:* {row['data_evento']}\n\n"
                msg += f"📐 *TABELA DE MEDIDAS:*\n"
                
                medidas_dict = {
                    "📏 Ombro": row['ombro'], "📐 Cava frente": row['cava_frente'], "📐 Cava costas": row['cava_costas'],
                    "🪡 Altura busto": row['altura_busto'], "👗 Busto": row['busto'], "↔️ Separação busto": row['separacao_busto'],
                    "🪡 Altura cintura": row['altura_cintura'], "⏳ Cintura alta": row['cintura_alta'], "⏳ Cintura baixa": row['cintura_baixa'],
                    "🪡 Altura quadril": row['altura_quadril'], "🧵 Quadril": row['quadril'], "👗 Tam. vestido": row['tamanho_vestido'],
                    "🥻 Tam. saia": row['tamanho_saia'], "👔 Tam. blusa": row['tamanho_blusa'], "📏 Tam. manga": row['tamanho_manga'],
                    "📐 Largura manga": row['largura_manga'], "👔 Colarinho": row['colarinho']
                }

                for chave, val in medidas_dict.items():
                    if val and str(val).strip():
                        msg += f"• {chave}: {val}\n"

                if row['observacoes']:
                    msg += f"\n📝 *Observações / Detalhes:*\n_{row['observacoes']}_\n"
                
                msg += f"\n🥰 _Quando ama o que se faz, se faz com capricho._\n"

                texto_url = urllib.parse.quote(msg)
                num_tel = "".join(filter(str.isdigit, str(row['telefone'])))
                link_wa = f"https://wa.me/55{num_tel}?text={texto_url}" if num_tel else f"https://wa.me/?text={texto_url}"

                st.link_button("📲 Enviar via WhatsApp", link_wa, use_container_width=True)
