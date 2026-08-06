import streamlit as st
import sqlite3
import pandas as pd
from datetime import date
import urllib.parse

# Configuração da página
st.set_page_config(page_title="Caprichos da Vânia - Vania Leonardo", page_icon="✂️", layout="wide")

# --- ESTILIZAÇÃO CUSTOMIZADA PARA MOBILE E DESKTOP (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;1,400&family=Poppins:wght@300;400;500;600&display=swap');

    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
    }

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background-color: #fdfbf7;
    }

    /* Cabeçalho Ateliê */
    .atelier-header {
        text-align: center;
        margin-bottom: 15px;
    }
    .atelier-title {
        font-family: 'Playfair Display', serif;
        color: #a0435d;
        font-size: 1.7rem;
        font-weight: 600;
        margin: 0;
        line-height: 1.1;
    }
    .atelier-subtitle {
        color: #8c7366;
        font-size: 0.8rem;
        margin: 3px 0 2px 0;
        font-weight: 500;
    }
    .atelier-slogan {
        font-family: 'Playfair Display', serif;
        font-style: italic;
        color: #b0526e;
        font-size: 0.85rem;
        margin: 0;
    }

    /* CONTAINER FLEXBOX - FORÇA LADO A LADO NO CELULAR */
    .flex-grid {
        display: flex !important;
        flex-direction: row !important;
        justify-content: space-between !important;
        gap: 10px !important;
        width: 100% !important;
        margin-bottom: 12px !important;
    }

    .flex-card {
        flex: 1 !important;
        background: #ffffff;
        border: 1px solid #f7dce2;
        border-radius: 12px;
        padding: 10px 8px;
        text-align: center;
        box-shadow: 0px 2px 8px rgba(176, 82, 110, 0.04);
    }

    .card-label {
        color: #8c7366;
        font-size: 0.75rem;
        font-weight: 500;
        margin-bottom: 2px;
    }

    .card-value {
        color: #a0435d;
        font-size: 1.4rem;
        font-weight: 600;
        line-height: 1;
    }

    .nav-card {
        flex: 1 !important;
        background: linear-gradient(135deg, #ffffff 0%, #fff7f9 100%);
        border: 1px solid #f2d2d8;
        border-radius: 14px;
        padding: 12px 10px;
        text-align: center;
        box-shadow: 0px 3px 10px rgba(160, 67, 93, 0.05);
    }

    .nav-title {
        color: #a0435d;
        font-size: 0.88rem;
        font-weight: 600;
        margin-bottom: 3px;
    }

    .nav-desc {
        color: #776660;
        font-size: 0.7rem;
        margin-bottom: 10px;
        line-height: 1.2;
    }

    /* Botões Customizados */
    .stButton > button {
        border-radius: 20px !important;
        font-weight: 500 !important;
        font-size: 0.8rem !important;
        padding: 4px 8px !important;
        min-height: 36px !important;
    }
    
    .stButton > button[kind="primary"] {
        background-color: #a0435d !important;
        border-color: #a0435d !important;
        color: white !important;
    }

    hr {
        border: 0;
        height: 1px;
        background: #f2d2d8;
        margin: 12px 0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- CONEXÃO BANCO DE DADOS ---
def get_connection():
    conn = sqlite3.connect('ateliervania.db', check_same_thread=False)
    return conn

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
    st.markdown("<h2 style='text-align: center; color: #a0435d; margin-bottom: 0;'>✂️ Vania Leonardo</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8c7366; font-size: 0.85rem; margin-top: 0;'><b>Designer de Moda</b></p>", unsafe_allow_html=True)
    st.markdown("---")
    
    opcoes_menu = ["🌸 Início / Capa", "📝 Cadastrar Cliente", "🔍 Consultar Fichas & WhatsApp"]
    index_atual = opcoes_menu.index(st.session_state.pagina) if st.session_state.pagina in opcoes_menu else 0
    
    escolha = st.radio("✨ **Navegação**", opcoes_menu, index=index_atual)
    st.session_state.pagina = escolha
    
    st.markdown("---")
    st.markdown("""
        <div style='background-color: #fff0f3; padding: 10px; border-radius: 8px; border: 1px solid #fce4e9; text-align: center;'>
            <p style='margin:0; color: #a0435d; font-size: 0.8rem;'>✨ <i>"Você sonha, nós Realizamos!"</i></p>
        </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 🌸 TELA 1: CAPA (INÍCIO)
# ==============================================================================
if st.session_state.pagina == "🌸 Início / Capa":
    # Cabeçalho Elegante
    st.markdown("""
        <div class="atelier-header">
            <h1 class="atelier-title">✂️ Caprichos da Vânia</h1>
            <p class="atelier-subtitle">Vania Leonardo | Designer de Moda</p>
            <p class="atelier-slogan">"Quando ama o que se faz, se faz com capricho. 🥰"</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Busca contagem no BD
    conn = get_connection()
    df_total = pd.read_sql_query("SELECT * FROM clientes", conn)
    conn.close()
    qtd = len(df_total)

    # METRICAS LADO A LADO NATIVAS EM HTML/CSS
    st.html(f"""
        <div class="flex-grid">
            <div class="flex-card">
                <div class="card-label">👥 Clientes</div>
                <div class="card-value">{qtd}</div>
            </div>
            <div class="flex-card">
                <div class="card-label">🪡 Fichas Salvas</div>
                <div class="card-value">{qtd}</div>
            </div>
        </div>
    """)

    st.markdown("<p style='color: #a0435d; text-align: center; font-weight: 600; font-size: 0.9rem; margin: 5px 0;'>✨ Você sonha, nós Realizamos!</p>", unsafe_allow_html=True)

    # BLOCOS DE AÇÃO LADO A LADO
    st.html("""
        <div class="flex-grid">
            <div class="nav-card">
                <div class="nav-title">📝 Nova Ficha</div>
                <div class="nav-desc">Cadastre dados e 17 medidas.</div>
            </div>
            <div class="nav-card">
                <div class="nav-title">🔍 Consultar</div>
                <div class="nav-desc">Busque e envie pelo Whats.</div>
            </div>
        </div>
    """)

    # BOTÕES DE NAVEGAÇÃO CORRESPONDENTES
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("✨ Cadastrar", type="primary", use_container_width=True):
            st.session_state.pagina = "📝 Cadastrar Cliente"
            st.rerun()
    with btn_col2:
        if st.button("📲 Consultar", type="primary", use_container_width=True):
            st.session_state.pagina = "🔍 Consultar Fichas & WhatsApp"
            st.rerun()

# ==============================================================================
# 📝 TELA 2: CADASTRAR CLIENTE
# ==============================================================================
elif st.session_state.pagina == "📝 Cadastrar Cliente":
    st.markdown("<h2 style='color: #a0435d; font-size: 1.25rem; margin-bottom: 0;'>📝 Cadastrar Ficha de Medidas</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("<h4 style='color: #a0435d; font-size: 0.95rem; margin-bottom: 5px;'>👤 Dados da Cliente & Prazos</h4>", unsafe_allow_html=True)
    nome = st.text_input("Nome da Cliente *")
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        telefone = st.text_input("Telefone (WhatsApp)")
    with col_t2:
        orcamento = st.text_input("Orçamento (R$)", placeholder="Ex: 350,00")
    
    col_dt1, col_dt2 = st.columns(2)
    with col_dt1:
        data_entrega = st.date_input("📦 Entrega", value=date.today())
    with col_dt2:
        data_evento = st.date_input("🎉 Evento", value=date.today())

    st.markdown("---")
    st.markdown("<h4 style='color: #a0435d; font-size: 0.95rem; margin-bottom: 5px;'>📏 Medidas (cm)</h4>", unsafe_allow_html=True)
    
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
    observacoes = st.text_area("📝 Observações / Modelo")

    if st.button("💖 Salvar Ficha no Ateliê", type="primary", use_container_width=True):
        if not nome.strip():
            st.error("Informe o nome da cliente!")
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
            st.success(f"🎉 Ficha de **{nome}** salva com sucesso!")

# ==============================================================================
# 🔍 TELA 3: CONSULTAR FICHAS & WHATSAPP
# ==============================================================================
elif st.session_state.pagina == "🔍 Consultar Fichas & WhatsApp":
    st.markdown("<h2 style='color: #a0435d; font-size: 1.25rem; margin-bottom: 0;'>🔍 Consultar Fichas & WhatsApp</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM clientes ORDER BY id DESC", conn)
    conn.close()

    if df.empty:
        st.info("Nenhuma cliente cadastrada.")
    else:
        busca = st.text_input("🔎 Buscar por nome")
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
                msg += f"📐 *FICHA DE MEDIDAS:*\n"
                
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
