import streamlit as st
import sqlite3
import pandas as pd
from datetime import date
import urllib.parse

# Configuração da página
st.set_page_config(page_title="Caprichos da Vânia - Vania Leonardo", page_icon="✂️", layout="wide")

# --- ESTILIZAÇÃO FEMININA & ELEGANTE (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;1,400&family=Poppins:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background-color: #fdfbf7;
    }

    .atelier-title {
        font-family: 'Playfair Display', serif;
        color: #b0526e;
        text-align: center;
        font-size: 2.8rem;
        font-weight: 600;
        margin-bottom: 0px;
    }

    .atelier-subtitle {
        text-align: center;
        color: #8c7366;
        font-size: 1.1rem;
        font-weight: 500;
        margin-top: 5px;
        margin-bottom: 5px;
    }

    .atelier-slogan {
        font-family: 'Playfair Display', serif;
        font-style: italic;
        color: #b0526e;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 25px;
    }

    /* Cartões de Métricas */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #f2d6dc;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0px 4px 10px rgba(176, 82, 110, 0.05);
        text-align: center;
    }
    
    div[data-testid="stMetricLabel"] {
        color: #8c7366 !important;
        font-weight: 500;
    }

    /* Cartões de Clientes / Resumo */
    .client-card {
        background: linear-gradient(135deg, #ffffff 0%, #fff8f9 100%);
        border-left: 6px solid #b0526e;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 15px;
        box-shadow: 0px 3px 12px rgba(0,0,0,0.04);
        border-top: 1px solid #fce4e9;
        border-right: 1px solid #fce4e9;
        border-bottom: 1px solid #fce4e9;
    }

    .stButton > button {
        border-radius: 25px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button[kind="primary"] {
        background-color: #b0526e !important;
        border-color: #b0526e !important;
        color: white !important;
    }

    .stButton > button[kind="primary"]:hover {
        background-color: #923f58 !important;
        border-color: #923f58 !important;
        box-shadow: 0px 4px 12px rgba(176, 82, 110, 0.3);
    }

    hr {
        border-color: #f2d6dc;
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

# --- GERENCIAMENTO DE NAVEGAÇÃO ---
if 'pagina' not in st.session_state:
    st.session_state.pagina = "🌸 Início / Capa"

# --- MENU LATERAL (SIDEBAR) ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #b0526e;'>✂️ Vania Leonardo</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8c7366; font-size: 0.95rem; margin-top: -10px;'><b>Designer de Moda</b></p>", unsafe_allow_html=True)
    st.markdown("---")
    
    opcoes_menu = ["🌸 Início / Capa", "📝 Cadastrar Cliente", "🔍 Consultar Fichas & WhatsApp"]
    index_atual = opcoes_menu.index(st.session_state.pagina) if st.session_state.pagina in opcoes_menu else 0
    
    escolha = st.radio("✨ **Navegação**", opcoes_menu, index=index_atual)
    st.session_state.pagina = escolha
    
    st.markdown("---")
    st.markdown("""
        <div style='background-color: #fff0f3; padding: 12px; border-radius: 10px; border: 1px solid #fce4e9; text-align: center;'>
            <p style='margin:0; color: #b0526e; font-size: 0.85rem;'>✨ <i>"Você sonha, nós Realizamos!"</i></p>
            <p style='margin:5px 0 0 0; color: #8c7366; font-size: 0.8rem;'><b>Costura sob medida ✂️</b></p>
        </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 🌸 TELA 1: CAPA (INÍCIO)
# ==============================================================================
if st.session_state.pagina == "🌸 Início / Capa":
    st.markdown("<h1 class='atelier-title'>✂️ Caprichos da Vânia</h1>", unsafe_allow_html=True)
    st.markdown("<p class='atelier-subtitle'>Vania Leonardo | Designer de Moda & Costura Sob Medida ✂️</p>", unsafe_allow_html=True)
    st.markdown("<p class='atelier-slogan'>\"Quando ama o que se faz, se faz com capricho. 🥰\"</p>", unsafe_allow_html=True)
    
    # --- MÉTRICAS DE RESUMO ---
    conn = get_connection()
    df_total = pd.read_sql_query("SELECT * FROM clientes", conn)
    conn.close()

    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.metric(label="👥 Clientes Cadastradas", value=len(df_total))
    with col_m2:
        st.metric(label="🪡 Fichas de Medidas", value=len(df_total))
    with col_m3:
        st.metric(label="✨ Ateliê", value="Aberto 🟢")

    st.markdown("---")
    st.markdown("<h3 style='color: #b0526e; text-align: center;'>✨ Você sonha, nós Realizamos!</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8c7366;'>Selecione o que deseja realizar agora:</p>", unsafe_allow_html=True)
    st.write("")

    # --- BLOCOS / CARTÕES CLICÁVEIS ---
    col_card1, col_card2 = st.columns(2)

    with col_card1:
        with st.container(border=True):
            st.markdown("<h3 style='color: #b0526e;'>📝 <b>Nova Ficha de Medidas</b></h3>", unsafe_allow_html=True)
            st.markdown("Cadastre os dados da cliente, insira as **17 medidas**, defina datas de entrega/evento, valor do orçamento e observações do modelo.")
            st.write("")
            if st.button("✨ Ir para Cadastrar Cliente", type="primary", use_container_width=True):
                st.session_state.pagina = "📝 Cadastrar Cliente"
                st.rerun()

    with col_card2:
        with st.container(border=True):
            st.markdown("<h3 style='color: #b0526e;'>🔍 <b>Consultar & Enviar WhatsApp</b></h3>", unsafe_allow_html=True)
            st.markdown("Busque por clientes salvas, consulte orçamentos e envie a **ficha de medidas completa formatada direto no WhatsApp**.")
            st.write("")
            if st.button("📲 Ir para Consultar Fichas", type="primary", use_container_width=True):
                st.session_state.pagina = "🔍 Consultar Fichas & WhatsApp"
                st.rerun()

# ==============================================================================
# 📝 TELA 2: CADASTRAR CLIENTE
# ==============================================================================
elif st.session_state.pagina == "📝 Cadastrar Cliente":
    st.markdown("<h2 style='color: #b0526e;'>📝 Cadastrar Ficha de Medidas</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #8c7366;'>Preencha as informações da cliente para salvar no sistema do ateliê:</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("<h4 style='color: #b0526e;'>👤 Dados da Cliente & Prazos</h4>", unsafe_allow_html=True)
    nome = st.text_input("Nome da Cliente *")
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        telefone = st.text_input("Telefone (WhatsApp)")
    with col_t2:
        orcamento = st.text_input("Valor do Orçamento (R$)", placeholder="Ex: 350,00")
    
    col_dt1, col_dt2 = st.columns(2)
    with col_dt1:
        data_entrega = st.date_input("📦 Data da Entrega", value=date.today())
    with col_dt2:
        data_evento = st.date_input("🎉 Data do Evento", value=date.today())

    st.markdown("---")
    st.markdown("<h4 style='color: #b0526e;'>📏 Ficha Geral de Medidas (em cm)</h4>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        ombro = st.text_input("📏 Ombro")
        cava_frente = st.text_input("📐 Cava frente")
        cava_costas = st.text_input("📐 Cava costas")
        altura_busto = st.text_input("🪡 Altura do busto")
        busto = st.text_input("👗 Busto")
        separacao_busto = st.text_input("↔️ Separação do busto")
        altura_cintura = st.text_input("🪡 Altura da cintura")
        cintura_alta = st.text_input("⏳ Cintura alta")
        cintura_baixa = st.text_input("⏳ Cintura baixa")

    with col2:
        altura_quadril = st.text_input("🪡 Altura do quadril")
        quadril = st.text_input("🧵 Quadril")
        tamanho_vestido = st.text_input("👗 Tamanho vestido")
        tamanho_saia = st.text_input("🥻 Tamanho saia")
        tamanho_blusa = st.text_input("👔 Tamanho blusa")
        tamanho_manga = st.text_input("📏 Tamanho manga")
        largura_manga = st.text_input("📐 Largura manga")
        colarinho = st.text_input("👔 Colarinho")

    st.markdown("---")
    observacoes = st.text_area("📝 Observações Gerais / Detalhes do Modelo & Tecido")

    if st.button("💖 Salvar Ficha no Ateliê", type="primary", use_container_width=True):
        if not nome.strip():
            st.error("Por favor, informe o nome da cliente!")
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
            st.success(f"🎉 Ficha de **{nome}** cadastrada com sucesso!")

# ==============================================================================
# 🔍 TELA 3: CONSULTAR FICHAS & WHATSAPP
# ==============================================================================
elif st.session_state.pagina == "🔍 Consultar Fichas & WhatsApp":
    st.markdown("<h2 style='color: #b0526e;'>🔍 Consultar Fichas & WhatsApp</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM clientes ORDER BY id DESC", conn)
    conn.close()

    if df.empty:
        st.info("Nenhuma cliente cadastrada ainda.")
    else:
        busca = st.text_input("🔎 Digite o nome para buscar no ateliê")
        if busca:
            df = df[df['nome'].str.contains(busca, case=False, na=False)]

        for _, row in df.iterrows():
            valor_orc = f"R$ {row['orcamento']}" if row['orcamento'] else "A combinar"
            
            with st.expander(f"💖 {row['nome']} | 📦 Entrega: {row['data_entrega']} | 💰 {valor_orc}"):
                
                st.markdown(f"""
                <div class='client-card'>
                    <h3 style='color: #b0526e; margin-top:0;'>👤 <b>{row['nome']}</b></h3>
                    <p style='color: #555; margin-bottom: 5px;'><b>📱 Telefone:</b> {row['telefone']} | <b>💰 Orçamento:</b> {valor_orc}</p>
                    <p style='color: #555; margin-bottom: 0;'><b>📦 Data da Entrega:</b> {row['data_entrega']} | <b>🎉 Data do Evento:</b> {row['data_evento']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                c_m1, c_m2 = st.columns(2)
                with c_m1:
                    st.write(f"📏 **Ombro:** {row['ombro']}")
                    st.write(f"📐 **Cava frente:** {row['cava_frente']}")
                    st.write(f"📐 **Cava costas:** {row['cava_costas']}")
                    st.write(f"🪡 **Altura do busto:** {row['altura_busto']}")
                    st.write(f"👗 **Busto:** {row['busto']}")
                    st.write(f"↔️ **Separação do busto:** {row['separacao_busto']}")
                    st.write(f"🪡 **Altura da cintura:** {row['altura_cintura']}")
                    st.write(f"⏳ **Cintura alta:** {row['cintura_alta']}")
                    st.write(f"⏳ **Cintura baixa:** {row['cintura_baixa']}")

                with c_m2:
                    st.write(f"🪡 **Altura do quadril:** {row['altura_quadril']}")
                    st.write(f"🧵 **Quadril:** {row['quadril']}")
                    st.write(f"👗 **Tamanho vestido:** {row['tamanho_vestido']}")
                    st.write(f"🥻 **Tamanho saia:** {row['tamanho_saia']}")
                    st.write(f"👔 **Tamanho blusa:** {row['tamanho_blusa']}")
                    st.write(f"📏 **Tamanho manga:** {row['tamanho_manga']}")
                    st.write(f"📐 **Largura manga:** {row['largura_manga']}")
                    st.write(f"👔 **Colarinho:** {row['colarinho']}")

                if row['observacoes']:
                    st.info(f"📝 **Observações do Modelo:** {row['observacoes']}")

                # --- MENSAGEM DO WHATSAPP COM SLOGANS OFICIAIS ---
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
                msg += f"Agradecemos pela confiança! Qualquer dúvida estou à disposição. 💖"

                texto_url = urllib.parse.quote(msg)
                num_tel = "".join(filter(str.isdigit, str(row['telefone'])))
                link_wa = f"https://wa.me/55{num_tel}?text={texto_url}" if num_tel else f"https://wa.me/?text={texto_url}"

                st.link_button("📲 Enviar Ficha Completa via WhatsApp", link_wa, use_container_width=True)
