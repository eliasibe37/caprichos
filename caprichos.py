import streamlit as st
import sqlite3
import pandas as pd
from datetime import date
import urllib.parse

# Configuração da página
st.set_page_config(
    page_title="Caprichos da Vânia", 
    page_icon="✂️", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- ESTILIZAÇÃO FEMININA (CSS PERSONALIZADO) ---
st.markdown("""
    <style>
    /* Estilo geral */
    .stApp {
        background-color: #FAFAFA;
    }
    
    /* Títulos e Cabeçalhos */
    h1, h2, h3 {
        color: #7A3043 !important;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    .slogan {
        text-align: center;
        color: #A3586D;
        font-size: 1.15rem;
        font-weight: 500;
        margin-top: -10px;
        margin-bottom: 25px;
    }

    /* Cartões Personalizados da Tela Inicial */
    .card-feminino {
        background-color: #FFF0F3;
        border: 2px solid #F4C2C2;
        border-radius: 15px 15px 0px 0px;
        padding: 20px;
        text-align: center;
        margin-bottom: 0px;
    }
    
    .card-feminino h3 {
        color: #8C3A52 !important;
        margin-bottom: 8px;
    }
    
    .card-feminino p {
        color: #666;
        font-size: 0.95rem;
    }

    /* Ajuste de Botões para tom Rosa Chá */
    div.stButton > button {
        background-color: #D87080 !important;
        color: white !important;
        border-radius: 0px 0px 15px 15px !important;
        border: none !important;
        font-weight: bold !important;
        padding: 0.6rem 1rem !important;
        transition: all 0.3s ease;
    }

    div.stButton > button:hover {
        background-color: #B55262 !important;
        box-shadow: 0 4px 10px rgba(181, 82, 98, 0.3);
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

# --- CONTROLE DE NAVEGAÇÃO ---
if "menu_selecionado" not in st.session_state:
    st.session_state["menu_selecionado"] = "🏠 Início"

def ir_para_pagina(nome_pagina):
    st.session_state["menu_selecionado"] = nome_pagina

# Sidebar
st.sidebar.title("🪡 Ateliê")
st.sidebar.markdown("**Caprichos da Vânia**")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navegação",
    ["🏠 Início", "📝 Cadastrar Ficha", "🔍 Consultar Clientes"],
    key="menu_selecionado"
)

# --- TELA 1: CAPA / INÍCIO ---
if st.session_state["menu_selecionado"] == "🏠 Início":
    st.markdown("<h1 style='text-align: center;'>🪡 Caprichos da Vânia</h1>", unsafe_allow_html=True)
    st.markdown("<p class='slogan'>Você Sonha, Nós Realizamos</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("""
    ### 👋 Olá, Vânia! Seja bem-vinda.
    Este é o seu sistema exclusivo para registrar e organizar as medidas de suas clientes com facilidade e elegância, Lembre-se Você é a melhor ARRAZA.
    """)
    
    st.markdown("<br>", unsafe_allow_html=True)

    col_card1, col_card2 = st.columns(2)
    
    # Cartão 1: Nova Ficha
    with col_card1:
        st.markdown("""
            <div class="card-feminino">
                <h3>📝 Nova Ficha</h3>
                <p>Cadastre uma nova cliente com todas as 17 medidas e datas do evento/entrega.</p>
            </div>
        """, unsafe_allow_html=True)
        st.button("✨ Abrir Nova Ficha", key="btn_nova_ficha", on_click=ir_para_pagina, args=("📝 Cadastrar Ficha",), use_container_width=True)
    
    # Cartão 2: Consultar
    with col_card2:
        st.markdown("""
            <div class="card-feminino">
                <h3>🔍 Consultar</h3>
                <p>Busque fichas salvas, veja os detalhes e envie tudo formatado pelo WhatsApp.</p>
            </div>
        """, unsafe_allow_html=True)
        st.button("🌸 Consultar Clientes", key="btn_consultar", on_click=ir_para_pagina, args=("🔍 Consultar Clientes",), use_container_width=True)

    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.caption("👈 Você também pode usar o menu na lateral esquerda para navegar!")

# --- TELA 2: CADASTRO / EDIÇÃO ---
elif st.session_state["menu_selecionado"] == "📝 Cadastrar Ficha":
    st.title("📝 Cadastrar Nova Ficha")
    
    st.markdown("### Dados do Cliente")
    nome = st.text_input("Nome do Cliente *")
    telefone = st.text_input("Telefone (WhatsApp)")
    
    col_dt1, col_dt2 = st.columns(2)
    with col_dt1:
        data_entrega = st.date_input("Data da Entrega", value=date.today())
    with col_dt2:
        data_evento = st.date_input("Data do Evento", value=date.today())

    st.markdown("---")
    st.markdown("### 📏 Medidas Gerais")
    
    col1, col2 = st.columns(2)
    
    with col1:
        ombro = st.text_input("Ombro")
        cava_frente = st.text_input("Cava frente")
        cava_costas = st.text_input("Cava costas")
        altura_busto = st.text_input("Altura do busto")
        busto = st.text_input("Busto")
        separacao_busto = st.text_input("Separação do busto")
        altura_cintura = st.text_input("Altura da cintura")
        cintura_alta = st.text_input("Cintura alta")
        cintura_baixa = st.text_input("Cintura baixa")

    with col2:
        altura_quadril = st.text_input("Altura do quadril")
        quadril = st.text_input("Quadril")
        tamanho_vestido = st.text_input("Tamanho vestido")
        tamanho_saia = st.text_input("Tamanho saia")
        tamanho_blusa = st.text_input("Tamanho blusa")
        tamanho_manga = st.text_input("Tamanho manga")
        largura_manga = st.text_input("Largura manga")
        colarinho = st.text_input("Colarinho")

    st.markdown("---")
    observacoes = st.text_area("Observações Gerais / Detalhes do Modelo")

    if st.button("💾 Salvar Ficha de Medidas", type="primary", use_container_width=True):
        if not nome.strip():
            st.error("Por favor, preencha pelo menos o nome do cliente!")
        else:
            conn = get_connection()
            c = conn.cursor()
            c.execute('''
                INSERT INTO clientes (
                    nome, telefone, data_entrega, data_evento, ombro, cava_frente, cava_costas, 
                    altura_busto, busto, separacao_busto, altura_cintura, cintura_alta, cintura_baixa, 
                    altura_quadril, quadril, tamanho_vestido, tamanho_saia, tamanho_blusa, tamanho_manga, 
                    largura_manga, colarinho, observacoes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                nome, telefone, data_entrega.strftime("%d/%m/%Y"), data_evento.strftime("%d/%m/%Y"), 
                ombro, cava_frente, cava_costas, altura_busto, busto, separacao_busto, 
                altura_cintura, cintura_alta, cintura_baixa, altura_quadril, quadril, 
                tamanho_vestido, tamanho_saia, tamanho_blusa, tamanho_manga, largura_manga, 
                colarinho, observacoes
            ))
            conn.commit()
            conn.close()
            st.success(f"Ficha de **{nome}** salva com sucesso!")

# --- TELA 3: CONSULTA E WHATSAPP ---
elif st.session_state["menu_selecionado"] == "🔍 Consultar Clientes":
    st.title("🔍 Consultar Clientes")
    
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM clientes ORDER BY id DESC", conn)
    conn.close()

    if df.empty:
        st.info("Nenhum cliente cadastrado ainda.")
    else:
        busca = st.text_input("🔎 Filtrar por Nome")
        if busca:
            df = df[df['nome'].str.contains(busca, case=False, na=False)]

        for _, row in df.iterrows():
            with st.expander(f"👤 {row['nome']} | 📦 Entrega: {row['data_entrega']}"):
                st.markdown(f"**Telefone:** {row['telefone']}")
                st.markdown(f"🗓️ **Data da Entrega:** {row['data_entrega']} | 🎉 **Data do Evento:** {row['data_evento']}")
                st.markdown("---")
                
                c_m1, c_m2 = st.columns(2)
                with c_m1:
                    st.write(f"• **Ombro:** {row['ombro']}")
                    st.write(f"• **Cava frente:** {row['cava_frente']}")
                    st.write(f"• **Cava costas:** {row['cava_costas']}")
                    st.write(f"• **Altura do busto:** {row['altura_busto']}")
                    st.write(f"• **Busto:** {row['busto']}")
                    st.write(f"• **Separação do busto:** {row['separacao_busto']}")
                    st.write(f"• **Altura da cintura:** {row['altura_cintura']}")
                    st.write(f"• **Cintura alta:** {row['cintura_alta']}")
                    st.write(f"• **Cintura baixa:** {row['cintura_baixa']}")

                with c_m2:
                    st.write(f"• **Altura do quadril:** {row['altura_quadril']}")
                    st.write(f"• **Quadril:** {row['quadril']}")
                    st.write(f"• **Tamanho vestido:** {row['tamanho_vestido']}")
                    st.write(f"• **Tamanho saia:** {row['tamanho_saia']}")
                    st.write(f"• **Tamanho blusa:** {row['tamanho_blusa']}")
                    st.write(f"• **Tamanho manga:** {row['tamanho_manga']}")
                    st.write(f"• **Largura manga:** {row['largura_manga']}")
                    st.write(f"• **Colarinho:** {row['colarinho']}")

                if row['observacoes']:
                    st.markdown(f"**Obs:** {row['observacoes']}")

                # Gerar mensagem tratada para WhatsApp
                msg = f"*FICHA DE MEDIDAS - CAPRICHOS DA VÂNIA*\n"
                msg += f"👤 *Cliente:* {row['nome']}\n"
                msg += f"📦 *Data Entrega:* {row['data_entrega']}\n"
                msg += f"🎉 *Data Evento:* {row['data_evento']}\n\n"
                msg += f"*MEDIDAS:*\n"
                
                medidas_dict = {
                    "Ombro": row['ombro'], "Cava frente": row['cava_frente'], "Cava costas": row['cava_costas'],
                    "Altura busto": row['altura_busto'], "Busto": row['busto'], "Separação busto": row['separacao_busto'],
                    "Altura cintura": row['altura_cintura'], "Cintura alta": row['cintura_alta'], "Cintura baixa": row['cintura_baixa'],
                    "Altura quadril": row['altura_quadril'], "Quadril": row['quadril'], "Tam. vestido": row['tamanho_vestido'],
                    "Tam. saia": row['tamanho_saia'], "Tam. blusa": row['tamanho_blusa'], "Tam. manga": row['tamanho_manga'],
                    "Largura manga": row['largura_manga'], "Colarinho": row['colarinho']
                }

                for chave, val in medidas_dict.items():
                    if val and str(val).strip():
                        msg += f"• {chave}: {val}\n"

                if row['observacoes']:
                    msg += f"\n*Obs:* {row['observacoes']}"

                texto_url = urllib.parse.quote(msg)
                num_tel = "".join(filter(str.isdigit, str(row['telefone'])))
                link_wa = f"https://wa.me/55{num_tel}?text={texto_url}" if num_tel else f"https://wa.me/?text={texto_url}"

                st.link_button("📲 Enviar Medidas via WhatsApp", link_wa, use_container_width=True)
