import streamlit as st
import sqlite3
import pandas as pd
from datetime import date
import urllib.parse

# Configuração da página
st.set_page_config(page_title="Caprichos da Vânia", page_icon="✂️", layout="wide")

# Estilização CSS personalizada
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #ff4b4b;
        margin-bottom: 5px;
    }
    .sub-header {
        text-align: center;
        color: #6c757d;
        margin-bottom: 25px;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #ff4b4b;
        margin-bottom: 10px;
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

# --- GERENCIAMENTO DE ESTADO DA NAVEGAÇÃO ---
if 'pagina' not in st.session_state:
    st.session_state.pagina = "🏠 Início"

# --- MENU LATERAL (SIDEBAR) ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/sewing-machine.png", width=80)
    st.title("✂️ Caprichos da Vânia")
    st.markdown("_Ateliê de Costura & Sob Medida_")
    st.markdown("---")
    
    opcoes_menu = ["🏠 Início", "📝 Cadastrar Cliente", "🔍 Consultar Fichas & WhatsApp"]
    
    # Garantir sincronização caso altere via botão na Capa
    index_atual = opcoes_menu.index(st.session_state.pagina) if st.session_state.pagina in opcoes_menu else 0
    
    escolha = st.radio("📌 **Navegação**", opcoes_menu, index=index_atual)
    st.session_state.pagina = escolha
    
    st.markdown("---")
    st.caption("Desenvolvido para o Ateliê Caprichos da Vânia v2.0")

# ==============================================================================
# 🏠 TELA 1: CAPA (INÍCIO / DASHBOARD)
# ==============================================================================
if st.session_state.pagina == "🏠 Início":
    st.markdown("<h1 class='main-header'>✂️ Ateliê Caprichos da Vânia</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Bem-vinda ao seu sistema de gestão de clientes e medidas!</p>", unsafe_allow_html=True)
    
    # --- MÉTRICAS NO TOPO ---
    conn = get_connection()
    df_total = pd.read_sql_query("SELECT * FROM clientes", conn)
    conn.close()

    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.metric(label="👥 Clientes Cadastrados", value=len(df_total))
    with col_m2:
        st.metric(label="✂️ Atendimentos Salvos", value=len(df_total))
    with col_m3:
        st.metric(label="✨ Status do App", value="Online 🟢")

    st.markdown("---")
    st.markdown("### 🎯 O que você deseja fazer hoje?")
    st.write("Clique em um dos blocos abaixo para ir direto à tela desejada:")

    # --- BLOCOS / CARTÕES CLICÁVEIS ---
    col_card1, col_card2 = st.columns(2)

    with col_card1:
        with st.container(border=True):
            st.markdown("## 📝 **Novo Cadastro**")
            st.markdown("Preencha a ficha completa com as **17 medidas**, prazos (entrega/evento), orçamento e observações do modelo.")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("➕ Ir para Cadastrar Cliente", type="primary", use_container_width=True):
                st.session_state.pagina = "📝 Cadastrar Cliente"
                st.rerun()

    with col_card2:
        with st.container(border=True):
            st.markdown("## 🔍 **Consultar Fichas**")
            st.markdown("Busque por nome de cliente, veja orçamentos acordados, datas e envie o relatório completo direto no **WhatsApp**.")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔎 Ir para Consultar Fichas", type="primary", use_container_width=True):
                st.session_state.pagina = "🔍 Consultar Fichas & WhatsApp"
                st.rerun()

# ==============================================================================
# 📝 TELA 2: CADASTRAR CLIENTE
# ==============================================================================
elif st.session_state.pagina == "📝 Cadastrar Cliente":
    st.markdown("## 📝 Cadastrar Nova Ficha de Cliente")
    st.write("Preencha as informações do cliente abaixo:")
    st.markdown("---")
    
    st.markdown("### 👤 Dados Gerais & Prazos")
    nome = st.text_input("Nome do Cliente *")
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        telefone = st.text_input("Telefone (WhatsApp)")
    with col_t2:
        orcamento = st.text_input("Valor do Orçamento (R$)", placeholder="Ex: 250,00")
    
    col_dt1, col_dt2 = st.columns(2)
    with col_dt1:
        data_entrega = st.date_input("📦 Data da Entrega", value=date.today())
    with col_dt2:
        data_evento = st.date_input("🎉 Data do Evento", value=date.today())

    st.markdown("---")
    st.markdown("### 📏 Ficha Geral de Medidas")
    
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
    observacoes = st.text_area("📝 Observações Gerais / Detalhes do Modelo")

    if st.button("💾 Salvar Ficha do Cliente", type="primary", use_container_width=True):
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
    st.markdown("## 🔍 Consultar & Gerenciar Fichas")
    st.markdown("---")
    
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM clientes ORDER BY id DESC", conn)
    conn.close()

    if df.empty:
        st.info("Nenhum cliente cadastrado ainda.")
    else:
        busca = st.text_input("🔎 Digite um nome para filtrar")
        if busca:
            df = df[df['nome'].str.contains(busca, case=False, na=False)]

        for _, row in df.iterrows():
            valor_orc = f"R$ {row['orcamento']}" if row['orcamento'] else "Não informado"
            
            with st.expander(f"👤 {row['nome']} | 📦 Entrega: {row['data_entrega']} | 💰 Orçamento: {valor_orc}"):
                
                st.markdown(f"""
                <div class='metric-card'>
                    <h4>👤 <b>{row['nome']}</b></h4>
                    <p><b>📱 Telefone:</b> {row['telefone']} | <b>💰 Orçamento:</b> {valor_orc}</p>
                    <p><b>📦 Data da Entrega:</b> {row['data_entrega']} | <b>🎉 Data do Evento:</b> {row['data_evento']}</p>
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
                    st.info(f"📝 **Observações:** {row['observacoes']}")

                # --- MENSAGEM DO WHATSAPP ---
                msg = f"✨ *CAPRICHOS DA VÂNIA* ✨\n"
                msg += f"✂️ _Ateliê de Costura & Sob Medida_\n\n"
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
                
                msg += f"\nAgradecemos a confiança! Qualquer dúvida estamos à disposição. 💖"

                texto_url = urllib.parse.quote(msg)
                num_tel = "".join(filter(str.isdigit, str(row['telefone'])))
                link_wa = f"https://wa.me/55{num_tel}?text={texto_url}" if num_tel else f"https://wa.me/?text={texto_url}"

                st.link_button("📲 Enviar Ficha Completa via WhatsApp", link_wa, use_container_width=True)
