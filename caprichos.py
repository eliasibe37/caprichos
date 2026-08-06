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
    initial_sidebar_state="collapsed"
)

# --- ESTILIZAÇÃO COMPACTA PARA CELULAR ---
st.markdown("""
    <style>
    /* Estilo geral */
    .stApp {
        background-color: #FAFAFA;
    }
    
    /* Espaçamento superior ideal */
    .block-container {
        padding-top: 3.2rem !important;
        padding-bottom: 1rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
    }

    /* REDUZIR A LARGURA DO MENU LATERAL (SIDEBAR) NO MOBILE */
    [data-testid="stSidebar"] {
        width: 240px !important;
        max-width: 65vw !important;
    }

    /* FORÇAR COLUNAS A FICAREM LADO A LADO E DENTRO DA TELA */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 6px !important;
        width: 100% !important;
    }

    [data-testid="column"] {
        width: 50% !important;
        flex: 1 1 50% !important;
        min-width: 0px !important;
    }

    /* Título sem cortar topo nem laterais */
    .titulo-principal {
        text-align: center;
        color: #7A3043;
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 1.35rem;
        font-weight: bold;
        margin-top: 0px;
        margin-bottom: 2px;
        line-height: 1.2;
    }
    
    .slogan {
        text-align: center;
        color: #A3586D;
        font-size: 0.8rem;
        font-weight: 500;
        margin-top: 0px;
        margin-bottom: 10px;
    }

    .boas-vindas {
        font-size: 0.78rem !important;
        color: #444;
        margin-bottom: 12px !important;
        line-height: 1.2 !important;
        text-align: center;
    }

    /* BALÕES COMPACTOS LADO A LADO */
    .card-feminino-box {
        background-color: #FFF0F3;
        border: 1px solid #F4C2C2;
        border-radius: 10px 10px 0px 0px;
        padding: 6px 3px;
        text-align: center;
        box-sizing: border-box;
        min-height: 65px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .card-feminino-box h3 {
        color: #8C3A52 !important;
        font-size: 0.78rem !important;
        margin-bottom: 2px !important;
        margin-top: 0px !important;
        font-weight: bold;
    }

    .card-feminino-box p {
        color: #666;
        font-size: 0.6rem !important;
        line-height: 1.05 !important;
        margin: 0 !important;
    }

    /* Botões dos Balões */
    div.stButton > button {
        background-color: #D87080 !important;
        color: white !important;
        border-radius: 0px 0px 8px 8px !important;
        border: none !important;
        font-weight: bold !important;
        font-size: 0.7rem !important;
        padding: 0.25rem 0.1rem !important;
        width: 100% !important;
        transition: all 0.3s ease;
    }

    div.stButton > button:hover {
        background-color: #B55262 !important;
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
    
    try:
        c.execute("ALTER TABLE clientes ADD COLUMN orcamento TEXT")
    except sqlite3.OperationalError:
        pass
        
    conn.commit()
    conn.close()

init_db()

# --- CONTROLE DE NAVEGAÇÃO ---
if "menu_selecionado" not in st.session_state:
    st.session_state["menu_selecionado"] = "🏠 Início"

def ir_para_pagina(nome_pagina):
    st.session_state["menu_selecionado"] = nome_pagina

# Sidebar Compacta
st.sidebar.title("🪡 Ateliê")
st.sidebar.markdown("**Caprichos da Vânia**")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navegação",
    ["🏠 Início", "📝 Cadastrar Nova Medida", "🔍 Consultar Clientes"],
    key="menu_selecionado"
)

# --- TELA 1: CAPA / INÍCIO ---
if st.session_state["menu_selecionado"] == "🏠 Início":
    st.markdown("<div class='titulo-principal'>🪡 Caprichos da Vânia</div>", unsafe_allow_html=True)
    st.markdown("<div class='slogan'>Você Sonha, Nós Realizamos</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='boas-vindas'>👋 <b>Olá, Vânia!</b> Registre e organize as medidas das suas clientes com praticidade. Lembre-se: Você é a melhor, ARRASA!</div>
    """, unsafe_allow_html=True)

    # COLUNAS LADO A LADO ENCOLHIDAS
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("""
            <div class="card-feminino-box">
                <h3>📝 Nova Medida</h3>
                <p>Cadastre clientes com 17 medidas e prazos.</p>
            </div>
        """, unsafe_allow_html=True)
        st.button("✨ Cadastrar", key="btn_nova_medida", on_click=ir_para_pagina, args=("📝 Cadastrar Nova Medida",), use_container_width=True)

    with c2:
        st.markdown("""
            <div class="card-feminino-box">
                <h3>🔍 Consultar</h3>
                <p>Busque fichas e envie no WhatsApp.</p>
            </div>
        """, unsafe_allow_html=True)
        st.button("🌸 Consultar", key="btn_consultar", on_click=ir_para_pagina, args=("🔍 Consultar Clientes",), use_container_width=True)

    st.markdown("<hr style='margin-top:12px; margin-bottom:8px;'>", unsafe_allow_html=True)
    st.caption("👈 Abra o menu lateral no canto superior para navegar.")

# --- TELA 2: CADASTRO / EDIÇÃO ---
elif st.session_state["menu_selecionado"] == "📝 Cadastrar Nova Medida":
    st.title("📝 Cadastrar Nova Medida")
    
    st.markdown("### 👤 Dados do Cliente")
    nome = st.text_input("👤 Nome do Cliente *")
    
    col_inf1, col_inf2 = st.columns(2)
    with col_inf1:
        telefone = st.text_input("📱 Telefone (WhatsApp)")
    with col_inf2:
        orcamento = st.text_input("💰 Valor do Orçamento (R$)", placeholder="Ex: 350,00")
    
    col_dt1, col_dt2 = st.columns(2)
    with col_dt1:
        data_entrega = st.date_input("📦 Data da Entrega", value=date.today())
    with col_dt2:
        data_evento = st.date_input("🎉 Data do Evento", value=date.today())

    st.markdown("---")
    st.markdown("### 📏 Medidas Gerais")
    
    col1, col2 = st.columns(2)
    
    with col1:
        ombro = st.text_input("📐 Ombro")
        cava_frente = st.text_input("✂️ Cava frente")
        cava_costas = st.text_input("✂️ Cava costas")
        altura_busto = st.text_input("📏 Altura do busto")
        busto = st.text_input("💖 Busto")
        separacao_busto = st.text_input("↔️ Separação do busto")
        altura_cintura = st.text_input("📏 Altura da cintura")
        cintura_alta = st.text_input("🎀 Cintura alta")
        cintura_baixa = st.text_input("🎀 Cintura baixa")

    with col2:
        altura_quadril = st.text_input("📏 Altura do quadril")
        quadril = st.text_input("✨ Quadril")
        tamanho_vestido = st.text_input("👗 Tamanho vestido")
        tamanho_saia = st.text_input("👗 Tamanho saia")
        tamanho_blusa = st.text_input("👚 Tamanho blusa")
        tamanho_manga = st.text_input("🧵 Tamanho manga")
        largura_manga = st.text_input("🧵 Largura manga")
        colarinho = st.text_input("👔 Colarinho")

    st.markdown("---")
    observacoes = st.text_area("📝 Observações Gerais / Detalhes do Modelo")

    if st.button("💾 Salvar Ficha de Medidas", type="primary", use_container_width=True):
        if not nome.strip():
            st.error("Por favor, preencha pelo menos o nome do cliente!")
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
                nome, telefone, data_entrega.strftime("%d/%m/%Y"), data_evento.strftime("%d/%m/%Y"), orcamento,
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
            valor_orcamento = f"R$ {row['orcamento']}" if row.get('orcamento') else "A combinar"
            
            with st.expander(f"👤 {row['nome']} | 📦 Entrega: {row['data_entrega']}"):
                st.markdown(f"📱 **Telefone:** {row['telefone']} | 💰 **Orçamento:** {valor_orcamento}")
                st.markdown(f"📦 **Data da Entrega:** {row['data_entrega']} | 🎉 **Data do Evento:** {row['data_evento']}")
                st.markdown("---")
                
                c_m1, c_m2 = st.columns(2)
                with c_m1:
                    st.write(f"📐 **Ombro:** {row['ombro']}")
                    st.write(f"✂️ **Cava frente:** {row['cava_frente']}")
                    st.write(f"✂️ **Cava costas:** {row['cava_costas']}")
                    st.write(f"📏 **Altura do busto:** {row['altura_busto']}")
                    st.write(f"💖 **Busto:** {row['busto']}")
                    st.write(f"↔️ **Separação do busto:** {row['separacao_busto']}")
                    st.write(f"📏 **Altura da cintura:** {row['altura_cintura']}")
                    st.write(f"🎀 **Cintura alta:** {row['cintura_alta']}")
                    st.write(f"🎀 **Cintura baixa:** {row['cintura_baixa']}")

                with c_m2:
                    st.write(f"📏 **Altura do quadril:** {row['altura_quadril']}")
                    st.write(f"✨ **Quadril:** {row['quadril']}")
                    st.write(f"👗 **Tamanho vestido:** {row['tamanho_vestido']}")
                    st.write(f"👗 **Tamanho saia:** {row['tamanho_saia']}")
                    st.write(f"👚 **Tamanho blusa:** {row['tamanho_blusa']}")
                    st.write(f"🧵 **Tamanho manga:** {row['tamanho_manga']}")
                    st.write(f"🧵 **Largura manga:** {row['largura_manga']}")
                    st.write(f"👔 **Colarinho:** {row['colarinho']}")

                if row['observacoes']:
                    st.markdown(f"📝 **Obs:** {row['observacoes']}")

                # 🌸 MENSAGEM INTERATIVA & FORMATADA PARA WHATSAPP 🌸
                msg = f"✨ *CAPRICHOS DA VÂNIA* ✨\n"
                msg += f"👗 _Vania Leonardo | Designer de Moda_\n"
                msg += f"💖 _\"Você Sonha, Nós Realizamos\"_\n"
                msg += f"──────────────────────\n\n"
                
                msg += f"👤 *Cliente:* {row['nome']}\n"
                if row.get('orcamento'):
                    msg += f"💰 *Orçamento:* R$ {row['orcamento']}\n"
                msg += f"📦 *Data de Entrega:* {row['data_entrega']}\n"
                msg += f"🎉 *Data do Evento:* {row['data_evento']}\n\n"
                
                msg += f"📏 *TABELA DE MEDIDAS (cm):*\n"
                
                medidas_dict = {
                    "📐 Ombro": row['ombro'],
                    "✂️ Cava frente": row['cava_frente'],
                    "✂️ Cava costas": row['cava_costas'],
                    "📏 Altura busto": row['altura_busto'],
                    "💖 Busto": row['busto'],
                    "↔️ Separação busto": row['separacao_busto'],
                    "📏 Altura cintura": row['altura_cintura'],
                    "🎀 Cintura alta": row['cintura_alta'],
                    "🎀 Cintura baixa": row['cintura_baixa'],
                    "📏 Altura quadril": row['altura_quadril'],
                    "✨ Quadril": row['quadril'],
                    "👗 Tam. vestido": row['tamanho_vestido'],
                    "👗 Tam. saia": row['tamanho_saia'],
                    "👚 Tam. blusa": row['tamanho_blusa'],
                    "🧵 Tam. manga": row['tamanho_manga'],
                    "🧵 Largura manga": row['largura_manga'],
                    "👔 Colarinho": row['colarinho']
                }

                tem_medidas = False
                for chave, val in medidas_dict.items():
                    if val and str(val).strip():
                        msg += f"  {chave}: {val}\n"
                        tem_medidas = True

                if not tem_medidas:
                    msg += f"  ▫️ _Ainda não preenchidas_\n"

                if row['observacoes']:
                    msg += f"\n📝 *Detalhes & Observações:*\n_{row['observacoes']}_\n"

                msg += f"\n──────────────────────\n"
                msg += f"🥰 _Quando ama o que se faz, se faz com capricho!_"

                texto_url = urllib.parse.quote(msg)
                num_tel = "".join(filter(str.isdigit, str(row['telefone'])))
                link_wa = f"https://wa.me/55{num_tel}?text={texto_url}" if num_tel else f"https://wa.me/?text={texto_url}"

                st.link_button("📲 Enviar Medidas via WhatsApp", link_wa, use_container_width=True)
