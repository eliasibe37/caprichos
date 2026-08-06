import sqlite3
import urllib.parse
import streamlit as st

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Caprichos da Vânia",
    page_icon="✂️",
    layout="centered"
)

DB_NAME = "caprichos_vania.db"

# --- BANCO DE DADOS ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL, telefone TEXT, nascimento TEXT,
            busto TEXT, torax TEXT, cintura TEXT, quadril TEXT, ombro TEXT,
            alt_busto TEXT, seio_seio TEXT, comp_corpo TEXT, alt_quadril TEXT,
            comp_saia TEXT, comp_calca TEXT, alt_gancho TEXT, larg_braco TEXT,
            comp_manga TEXT, punho TEXT, obs TEXT
        )
    ''')
    conn.commit()
    conn.close()

def salvar_cliente(dados):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO clientes (
            nome, telefone, nascimento, busto, torax, cintura, quadril, ombro,
            alt_busto, seio_seio, comp_corpo, alt_quadril, comp_saia, comp_calca,
            alt_gancho, larg_braco, comp_manga, punho, obs
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', dados)
    conn.commit()
    conn.close()

def atualizar_cliente(cliente_id, dados):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE clientes SET
            nome=?, telefone=?, nascimento=?, busto=?, torax=?, cintura=?, quadril=?, ombro=?,
            alt_busto=?, seio_seio=?, comp_corpo=?, alt_quadril=?, comp_saia=?, comp_calca=?,
            alt_gancho=?, larg_braco=?, comp_manga=?, punho=?, obs=?
        WHERE id=?
    ''', (*dados, cliente_id))
    conn.commit()
    conn.close()

def buscar_clientes():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes ORDER BY nome ASC")
    dados = cursor.fetchall()
    conn.close()
    return dados

def deletar_cliente(cliente_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
    conn.commit()
    conn.close()

# --- LINK DO WHATSAPP ---
def gerar_link_whatsapp(c):
    (id_c, nome, tel, nasc, busto, torax, cint, quad, ombro, 
     alt_b, seio, comp_c, alt_q, saia, calca, gancho, braco, manga, punho, obs) = c

    msg = f"✂️ *FICHA DE MEDIDAS - CAPRICHOS DA VÂNIA*\n"
    msg += f"----------------------------------------\n"
    msg += f"👤 *Cliente:* {nome or '-'}\n"
    if tel: msg += f"📞 *Tel:* {tel}\n"
    if nasc: msg += f"🎂 *Nascimento:* {nasc}\n"

    msg += f"\n📐 *MEDIDAS SUPERIORES (cm)*\n"
    msg += f"• Busto: {busto or '-'} | Tórax: {torax or '-'}\n"
    msg += f"• Cintura: {cint or '-'} | Ombro: {ombro or '-'}\n"
    msg += f"• Alt. Busto: {alt_b or '-'} | Seio a Seio: {seio or '-'}\n"
    msg += f"• Comp. Corpo: {comp_c or '-'}\n"

    msg += f"\n📏 *MEDIDAS INFERIORES (cm)*\n"
    msg += f"• Quadril: {quad or '-'} | Alt. Quadril: {alt_q or '-'}\n"
    msg += f"• Comp. Saia/Vestido: {saia or '-'}\n"
    msg += f"• Comp. Calça: {calca or '-'}\n"
    msg += f"• Altura Gancho: {gancho or '-'}\n"

    msg += f"\n🧵 *BRAÇO E MANGA (cm)*\n"
    msg += f"• Largura Braço: {braco or '-'} | Comp. Manga: {manga or '-'}\n"
    msg += f"• Punho: {punho or '-'}\n"

    if obs:
        msg += f"\n📝 *OBSERVAÇÕES*\n{obs}\n"

    msg += f"\n_Ateliê Caprichos da Vânia_"

    texto_encoded = urllib.parse.quote(msg)
    
    if tel:
        num_limpo = "".join(filter(str.isdigit, tel))
        if len(num_limpo) in (10, 11) and not num_limpo.startswith("55"):
            num_limpo = "55" + num_limpo
        return f"https://api.whatsapp.com/send?phone={num_limpo}&text={texto_encoded}"
    
    return f"https://api.whatsapp.com/send?text={texto_encoded}"

# Inicializa Banco
init_db()

# Estado da sessão para guardar quem está sendo editado
if 'cliente_em_edicao' not in st.session_state:
    st.session_state.cliente_em_edicao = None

# --- CABEÇALHO ---
st.markdown("<h1 style='text-align: center; color: #D81B60;'>✂️ CAPRICHOS DA VÂNIA</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-weight: bold; color: #555;'>Vania Leonardo • Designer de Moda</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-style: italic; color: #888;'>“Você sonha, nós realizamos!”</p>", unsafe_allow_html=True)
st.divider()

# AVISO DE EDIÇÃO (Aparece no topo para avisar o usuário)
if st.session_state.cliente_em_edicao is not None:
    st.warning(f"✏️ **Você está editando a cliente:** {st.session_state.cliente_em_edicao[1].upper()}. Vá para a primeira aba ('✨ Nova Ficha / Cadastro / Edição') para alterar os dados!")
    if st.button("❌ Cancelar Edição"):
        st.session_state.cliente_em_edicao = None
        st.rerun()

tab1, tab2 = st.tabs(["✨ Nova Ficha / Cadastro / Edição", "📋 Clientes Cadastradas"])

# --- TAB 1: CADASTRO / EDIÇÃO ---
with tab1:
    c_edit = st.session_state.cliente_em_edicao

    if c_edit:
        st.subheader(f"✏️ Editando: {c_edit[1]}")
    else:
        st.subheader("📝 Nova Ficha de Medidas")

    # Usamos uma chave dinâmica no formulário para forçar a atualização dos valores ao clicar em Editar
    form_key = f"form_cliente_{c_edit[0]}" if c_edit else "form_cliente_novo"

    with st.form(key=form_key):
        st.markdown("### 👤 Dados Principais")
        col1, col2 = st.columns(2)
        nome = col1.text_input("Nome Completo *", value=c_edit[1] if c_edit else "")
        tel = col2.text_input("WhatsApp / Telefone (com DDD)", value=c_edit[2] if c_edit else "")
        nasc = st.text_input("Data de Nascimento (DD/MM)", value=c_edit[3] if c_edit else "")

        st.markdown("### 📐 Medidas Superiores (cm)")
        col_s1, col_s2 = st.columns(2)
        busto = col_s1.text_input("Busto", value=c_edit[4] if c_edit else "")
        torax = col_s2.text_input("Tórax", value=c_edit[5] if c_edit else "")
        cintura = col_s1.text_input("Cintura", value=c_edit[6] if c_edit else "")
        ombro = col_s2.text_input("Ombro a Ombro", value=c_edit[8] if c_edit else "")
        alt_busto = col_s1.text_input("Altura do Busto", value=c_edit[9] if c_edit else "")
        seio_seio = col_s2.text_input("Seio a Seio", value=c_edit[10] if c_edit else "")
        comp_corpo = st.text_input("Comprimento do Corpo", value=c_edit[11] if c_edit else "")

        st.markdown("### 📏 Medidas Inferiores (cm)")
        col_i1, col_i2 = st.columns(2)
        quadril = col_i1.text_input("Quadril", value=c_edit[7] if c_edit else "")
        alt_quadril = col_i2.text_input("Altura do Quadril", value=c_edit[12] if c_edit else "")
        comp_saia = col_i1.text_input("Comprimento Saia/Vestido", value=c_edit[13] if c_edit else "")
        comp_calca = col_i2.text_input("Comprimento Calça", value=c_edit[14] if c_edit else "")
        alt_gancho = st.text_input("Altura Gancho/Gavião", value=c_edit[15] if c_edit else "")

        st.markdown("### 🧵 Braço e Manga (cm)")
        col_b1, col_b2 = st.columns(2)
        larg_braco = col_b1.text_input("Largura do Braço", value=c_edit[16] if c_edit else "")
        comp_manga = col_b2.text_input("Comprimento da Manga", value=c_edit[17] if c_edit else "")
        punho = st.text_input("Punho", value=c_edit[18] if c_edit else "")

        st.markdown("### 📝 Observações")
        obs = st.text_area("Ajustes, tecidos, preferências...", value=c_edit[19] if c_edit else "")

        texto_btn = "💾 Salvar Alterações no Banco de Dados" if c_edit else "💾 Salvar Cliente no Banco de Dados"
        submit = st.form_submit_button(texto_btn, use_container_width=True)

        if submit:
            if not nome.strip():
                st.error("⚠️ O campo Nome Completo é obrigatório!")
            else:
                dados = (
                    nome.strip(), tel.strip(), nasc.strip(), busto.strip(), torax.strip(),
                    cintura.strip(), quadril.strip(), ombro.strip(), alt_busto.strip(),
                    seio_seio.strip(), comp_corpo.strip(), alt_quadril.strip(), comp_saia.strip(),
                    comp_calca.strip(), alt_gancho.strip(), larg_braco.strip(), comp_manga.strip(),
                    punho.strip(), obs.strip()
                )
                
                if c_edit:
                    atualizar_cliente(c_edit[0], dados)
                    st.success(f"✅ Ficha de **{nome}** atualizada!")
                    st.session_state.cliente_em_edicao = None
                    st.rerun()
                else:
                    salvar_cliente(dados)
                    st.success(f"✅ Ficha de **{nome}** salva com sucesso!")

# --- TAB 2: CONSULTA / LISTA ---
with tab2:
    st.subheader("📋 Lista de Clientes")
    clientes = buscar_clientes()

    if not clientes:
        st.info("Nenhuma cliente cadastrada ainda.")
    else:
        busca = st.text_input("🔍 Buscar por nome", "")
        clientes_filtrados = [c for c in clientes if busca.lower() in c[1].lower()]

        for c in clientes_filtrados:
            with st.expander(f"👤 **{c[1].upper()}**"):
                st.write(f"📞 **WhatsApp:** {c[2] or 'Não informado'}")
                st.write(f"🎂 **Nascimento:** {c[3] or 'Não informado'}")
                
                col_det1, col_det2 = st.columns(2)
                with col_det1:
                    st.markdown("**📐 Superiores:**")
                    st.write(f"• Busto: {c[4] or '-'} | Tórax: {c[5] or '-'}")
                    st.write(f"• Cintura: {c[6] or '-'} | Ombro: {c[8] or '-'}")
                    st.write(f"• Alt. Busto: {c[9] or '-'} | Seio: {c[10] or '-'}")
                    st.write(f"• Comp. Corpo: {c[11] or '-'}")

                    st.markdown("**🧵 Braço / Manga:**")
                    st.write(f"• Larg. Braço: {c[16] or '-'} | Manga: {c[17] or '-'}")
                    st.write(f"• Punho: {c[18] or '-'}")

                with col_det2:
                    st.markdown("**📏 Inferiores:**")
                    st.write(f"• Quadril: {c[7] or '-'} | Alt. Quadril: {c[12] or '-'}")
                    st.write(f"• Comp. Saia: {c[13] or '-'}")
                    st.write(f"• Comp. Calça: {c[14] or '-'}")
                    st.write(f"• Alt. Gancho: {c[15] or '-'}")

                    st.markdown("**📝 Observações:**")
                    st.write(c[19] or "Nenhuma observação.")

                st.divider()

                link_wp = gerar_link_whatsapp(c)
                st.link_button("📲 Enviar Ficha no WhatsApp", link_wp, use_container_width=True)

                col_btn1, col_btn2 = st.columns(2)
                
                # Botão Editar
                if col_btn1.button("✏️ Editar Cliente", key=f"btn_edit_{c[0]}", use_container_width=True):
                    st.session_state.cliente_em_edicao = c
                    st.rerun()

                # Botão Excluir
                if col_btn2.button("🗑️ Excluir Cliente", key=f"btn_del_{c[0]}", use_container_width=True):
                    deletar_cliente(c[0])
                    st.toast(f"Cliente {c[1]} excluída!")
                    st.rerun()