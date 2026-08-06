import streamlit as st
import sqlite3
import pandas as pd
from datetime import date, datetime
import urllib.parse

# Configuração da página
st.set_page_config(
    page_title="Caprichos da Vânia", 
    page_icon="✂️", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- ESTILIZAÇÃO FIXA E CENTRALIZADA ---
st.markdown("""
    <style>
    /* Estilo geral */
    .stApp {
        background-color: #FAFAFA;
    }
    
    .block-container {
        padding-top: 2.5rem !important;
        padding-bottom: 1rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
        max-width: 480px !important;
        margin: 0 auto !important;
    }

    /* Menu lateral estreito */
    [data-testid="stSidebar"] {
        width: 220px !important;
        max-width: 60vw !important;
    }

    /* Título e Slogan */
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
        margin-bottom: 14px !important;
        line-height: 1.25 !important;
        text-align: center;
    }

    /* GRID FLEXBOX FIXO */
    .grid-menu {
        display: flex !important;
        flex-direction: row !important;
        justify-content: center !important;
        gap: 10px !important;
        width: 100% !important;
        box-sizing: border-box !important;
    }

    /* CARD INTEGRADO (BALÃO + BOTÃO) */
    .card-opcao {
        flex: 1 1 50% !important;
        max-width: 200px !important;
        background-color: #FFF0F3;
        border: 1px solid #F4C2C2;
        border-radius: 10px;
        overflow: hidden;
        text-align: center;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.04);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .card-corpo {
        padding: 10px 6px;
    }

    .card-opcao h3 {
        color: #8C3A52 !important;
        font-size: 0.8rem !important;
        margin-bottom: 3px !important;
        margin-top: 0px !important;
        font-weight: bold;
    }

    .card-opcao p {
        color: #666;
        font-size: 0.62rem !important;
        line-height: 1.1 !important;
        margin: 0 !important;
    }

    /* BOTÃO INTEGRADO DENTRO DO CARD */
    .btn-card {
        display: block !important;
        background-color: #D87080 !important;
        color: white !important;
        text-decoration: none !important;
        font-weight: bold !important;
        font-size: 0.72rem !important;
        padding: 6px 0px !important;
        border: none !important;
        width: 100% !important;
        text-align: center !important;
        transition: 0.2s;
    }

    .btn-card:hover {
        background-color: #B55262 !important;
        color: white !important;
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

def deletar_cliente(cliente_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
    conn.commit()
    conn.close()

def converter_data(data_str):
    try:
        return datetime.strptime(data_str, "%d/%m/%Y").date()
    except:
        return date.today()

init_db()

# --- CONTROLE DE NAVEGAÇÃO VIA URL PARAMS ---
query_params = st.query_params
pagina_atual = query_params.get("p", "inicio")

# Sidebar Compacta
st.sidebar.title("🪡 Ateliê")
st.sidebar.markdown("**Caprichos da Vânia**")
st.sidebar.markdown("---")

opcoes_menu = {
    "🏠 Início": "inicio",
    "📝 Cadastrar Nova Medida": "cadastrar",
    "🔍 Consultar Clientes": "consultar"
}

# Sincroniza sidebar
idx_sel = 0
if pagina_atual == "cadastrar":
    idx_sel = 1
elif pagina_atual == "consultar":
    idx_sel = 2

menu_sb = st.sidebar.radio(
    "Navegação",
    list(opcoes_menu.keys()),
    index=idx_sel
)

if opcoes_menu[menu_sb] != pagina_atual:
    st.query_params["p"] = opcoes_menu[menu_sb]
    st.rerun()

# --- TELA 1: CAPA / INÍCIO ---
if pagina_atual == "inicio":
    st.markdown("<div class='titulo-principal'>🪡 Caprichos da Vânia</div>", unsafe_allow_html=True)
    st.markdown("<div class='slogan'>Você Sonha, Nós Realizamos</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='boas-vindas'>👋 <b>Olá, Vânia!</b> Registre e organize as medidas das suas clientes com praticidade. Lembre-se: Você é a melhor, ARRASA!</div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="grid-menu">
        <div class="card-opcao">
            <div class="card-corpo">
                <h3>📝 Nova Medida</h3>
                <p>Cadastre 17 medidas.</p>
            </div>
            <a href="?p=cadastrar" target="_self" class="btn-card">✨ Cadastrar</a>
        </div>
        <div class="card-opcao">
            <div class="card-corpo">
                <h3>🔍 Consultar</h3>
                <p>Envie no WhatsApp.</p>
            </div>
            <a href="?p=consultar" target="_self" class="btn-card">🌸 Consultar</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='margin-top:20px; margin-bottom:8px;'>", unsafe_allow_html=True)
    st.caption("👈 Abra o menu lateral no canto superior para navegar.")

# --- TELA 2: CADASTRO / EDIÇÃO ---
elif pagina_atual == "cadastrar":
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

# --- TELA 3: CONSULTA, EDIÇÃO, EXCLUSÃO E WHATSAPP ---
elif pagina_atual == "consultar":
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
            cliente_id = row['id']
            valor_orcamento = f"R$ {row['orcamento']}" if row.get('orcamento') else "A combinar"
            
            with st.expander(f"👤 {row['nome']} | 📦 Entrega: {row['data_entrega']}"):
                
                # --- VERIFICA SE ESTÁ EM MODO DE EDIÇÃO PARA ESTE CLIENTE ---
                if st.session_state.get(f"editando_{cliente_id}", False):
                    st.markdown("### ✏️ Editar Ficha de Medidas")
                    
                    edit_nome = st.text_input("👤 Nome", value=row['nome'], key=f"e_nome_{cliente_id}")
                    
                    c_e1, c_e2 = st.columns(2)
                    with c_e1:
                        edit_tel = st.text_input("📱 Telefone", value=row['telefone'] or "", key=f"e_tel_{cliente_id}")
                    with c_e2:
                        edit_orc = st.text_input("💰 Orçamento (R$)", value=row['orcamento'] or "", key=f"e_orc_{cliente_id}")
                        
                    c_ed1, c_ed2 = st.columns(2)
                    with c_ed1:
                        edit_dt_ent = st.date_input("📦 Data Entrega", value=converter_data(row['data_entrega']), key=f"e_dt_ent_{cliente_id}")
                    with c_ed2:
                        edit_dt_eve = st.date_input("🎉 Data Evento", value=converter_data(row['data_evento']), key=f"e_dt_eve_{cliente_id}")

                    st.markdown("---")
                    ce1, ce2 = st.columns(2)
                    with ce1:
                        edit_ombro = st.text_input("📐 Ombro", value=row['ombro'] or "", key=f"e_omb_{cliente_id}")
                        edit_cf = st.text_input("✂️ Cava frente", value=row['cava_frente'] or "", key=f"e_cf_{cliente_id}")
                        edit_cc = st.text_input("✂️ Cava costas", value=row['cava_costas'] or "", key=f"e_cc_{cliente_id}")
                        edit_ab = st.text_input("📏 Altura busto", value=row['altura_busto'] or "", key=f"e_ab_{cliente_id}")
                        edit_busto = st.text_input("💖 Busto", value=row['busto'] or "", key=f"e_bus_{cliente_id}")
                        edit_sb = st.text_input("↔️ Separação busto", value=row['separacao_busto'] or "", key=f"e_sb_{cliente_id}")
                        edit_ac = st.text_input("📏 Altura cintura", value=row['altura_cintura'] or "", key=f"e_ac_{cliente_id}")
                        edit_ca = st.text_input("🎀 Cintura alta", value=row['cintura_alta'] or "", key=f"e_ca_{cliente_id}")
                        edit_cb = st.text_input("🎀 Cintura baixa", value=row['cintura_baixa'] or "", key=f"e_cb_{cliente_id}")

                    with ce2:
                        edit_aq = st.text_input("📏 Altura quadril", value=row['altura_quadril'] or "", key=f"e_aq_{cliente_id}")
                        edit_quadril = st.text_input("✨ Quadril", value=row['quadril'] or "", key=f"e_qua_{cliente_id}")
                        edit_tv = st.text_input("👗 Tam. vestido", value=row['tamanho_vestido'] or "", key=f"e_tv_{cliente_id}")
                        edit_ts = st.text_input("👗 Tam. saia", value=row['tamanho_saia'] or "", key=f"e_ts_{cliente_id}")
                        edit_tbl = st.text_input("👚 Tam. blusa", value=row['tamanho_blusa'] or "", key=f"e_tbl_{cliente_id}")
                        edit_tm = st.text_input("🧵 Tam. manga", value=row['tamanho_manga'] or "", key=f"e_tm_{cliente_id}")
                        edit_lm = st.text_input("🧵 Largura manga", value=row['largura_manga'] or "", key=f"e_lm_{cliente_id}")
                        edit_col = st.text_input("👔 Colarinho", value=row['colarinho'] or "", key=f"e_col_{cliente_id}")

                    edit_obs = st.text_area("📝 Observações", value=row['observacoes'] or "", key=f"e_obs_{cliente_id}")

                    btn_salvar, btn_cancelar = st.columns(2)
                    with btn_salvar:
                        if st.button("💾 Salvar Alterações", key=f"btn_salvar_{cliente_id}", type="primary", use_container_width=True):
                            conn = get_connection()
                            c = conn.cursor()
                            c.execute('''
                                UPDATE clientes SET
                                    nome=?, telefone=?, data_entrega=?, data_evento=?, orcamento=?,
                                    ombro=?, cava_frente=?, cava_costas=?, altura_busto=?, busto=?,
                                    separacao_busto=?, altura_cintura=?, cintura_alta=?, cintura_baixa=?,
                                    altura_quadril=?, quadril=?, tamanho_vestido=?, tamanho_saia=?,
                                    tamanho_blusa=?, tamanho_manga=?, largura_manga=?, colarinho=?, observacoes=?
                                WHERE id=?
                            ''', (
                                edit_nome, edit_tel, edit_dt_ent.strftime("%d/%m/%Y"), edit_dt_eve.strftime("%d/%m/%Y"), edit_orc,
                                edit_ombro, edit_cf, edit_cc, edit_ab, edit_busto, edit_sb, edit_ac, edit_ca, edit_cb,
                                edit_aq, edit_quadril, edit_tv, edit_ts, edit_tbl, edit_tm, edit_lm, edit_col, edit_obs,
                                cliente_id
                            ))
                            conn.commit()
                            conn.close()
                            st.session_state[f"editando_{cliente_id}"] = False
                            st.success("Ficha atualizada!")
                            st.rerun()

                    with btn_cancelar:
                        if st.button("❌ Cancelar", key=f"btn_canc_{cliente_id}", use_container_width=True):
                            st.session_state[f"editando_{cliente_id}"] = False
                            st.rerun()

                # --- EXIBIÇÃO NORMAL DA FICHA ---
                else:
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

                    # 🌸 MENSAGEM WHATSAPP 🌸
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

                    # --- BOTÕES DE AÇÃO: EDITAR E EXCLUIR ---
                    st.markdown("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)
                    col_btn_edit, col_btn_del = st.columns(2)
                    
                    with col_btn_edit:
                        if st.button("✏️ Editar", key=f"btn_edit_trigger_{cliente_id}", use_container_width=True):
                            st.session_state[f"editando_{cliente_id}"] = True
                            st.rerun()

                    with col_btn_del:
                        if st.button("🗑️ Excluir", key=f"btn_del_trigger_{cliente_id}", use_container_width=True):
                            st.session_state[f"confirmar_del_{cliente_id}"] = True

                    # Confirmação de exclusão
                    if st.session_state.get(f"confirmar_del_{cliente_id}", False):
                        st.warning(f"⚠️ Tem certeza que deseja excluir **{row['nome']}**?")
                        c_conf1, c_conf2 = st.columns(2)
                        with c_conf1:
                            if st.button("✔️ Sim, Excluir", key=f"sim_del_{cliente_id}", type="primary", use_container_width=True):
                                deletar_cliente(cliente_id)
                                st.session_state[f"confirmar_del_{cliente_id}"] = False
                                st.success("Cliente excluído com sucesso!")
                                st.rerun()
                        with c_conf2:
                            if st.button("❌ Não", key=f"nao_del_{cliente_id}", use_container_width=True):
                                st.session_state[f"confirmar_del_{cliente_id}"] = False
                                st.rerun()
