import streamlit as st

# ─── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Classificador de Pesquisa Científica",
    page_icon="🔬",
    layout="centered",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Source+Sans+3:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Source Sans 3', sans-serif;
    background-color: #0d0d14;
    color: #e0dbd0;
}

.main { background-color: #0d0d14; }
.block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 740px; }

h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: #f0ebe0 !important;
}

/* Botões principais */
.stButton > button {
    background-color: #c9a84c !important;
    color: #0d0d14 !important;
    border: none !important;
    font-family: 'Source Sans 3', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    padding: 0.6rem 2rem !important;
    border-radius: 2px !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background-color: #e0bc5e !important;
    transform: translateY(-1px);
}

/* Radio buttons */
div[data-testid="stRadio"] label {
    font-family: 'Source Sans 3', sans-serif !important;
    color: #c8c4ba !important;
    font-size: 1rem !important;
}
div[data-testid="stRadio"] > div {
    gap: 0.5rem;
}

/* Progress bar */
.stProgress > div > div > div {
    background-color: #c9a84c !important;
}

/* Caixas de texto */
.stTextArea textarea {
    background-color: #1a1a24 !important;
    color: #c8c4ba !important;
    border: 1px solid #3a3530 !important;
    font-family: 'Source Sans 3', sans-serif !important;
    font-size: 0.95rem !important;
    line-height: 1.8 !important;
}

/* Divider */
hr { border-color: #2a2520 !important; }

/* Badges / tags */
.badge {
    display: inline-block;
    padding: 4px 14px;
    border: 1px solid #c9a84c44;
    color: #c9a84c;
    font-size: 0.78rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin: 4px;
    background: #c9a84c11;
    font-family: 'Source Sans 3', sans-serif;
}

.level-badge {
    display: inline-block;
    padding: 3px 10px;
    border: 1px solid #c9a84c44;
    color: #c9a84c;
    font-size: 0.72rem;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    font-family: 'Source Sans 3', sans-serif;
    margin-bottom: 0.5rem;
}

.hint-box {
    border-left: 2px solid #c9a84c33;
    padding: 8px 14px;
    color: #5a5650;
    font-style: italic;
    font-size: 0.87rem;
    margin-bottom: 1.2rem;
    line-height: 1.6;
}

.result-card {
    background: #c9a84c08;
    border: 1px solid #c9a84c22;
    padding: 28px 32px;
    margin: 1rem 0;
}

.methodology-box {
    background: #c9a84c05;
    border: 1px solid #c9a84c18;
    padding: 28px 32px;
    margin: 1rem 0;
    text-align: justify;
    line-height: 1.85;
    color: #c8c4ba;
    font-size: 0.95rem;
}

.section-label {
    font-size: 0.7rem;
    letter-spacing: 0.35em;
    color: #c9a84c;
    text-transform: uppercase;
    font-family: 'Source Sans 3', sans-serif;
    margin-bottom: 0.8rem;
}

.note-text {
    font-size: 0.78rem;
    color: #4a4840;
    font-style: italic;
    text-align: center;
    margin-top: 0.5rem;
}

/* Sidebar escura */
[data-testid="stSidebar"] {
    background-color: #0a0a0f !important;
    border-right: 1px solid #1e1e28;
}
</style>
""", unsafe_allow_html=True)


# ─── Dados das perguntas ─────────────────────────────────────────────────────
QUESTIONS = {
    "q1": {
        "level": "Nível 1", "level_label": "Origem dos Dados",
        "question": "O artigo analisa dados coletados diretamente da realidade pesquisada?",
        "hint": "Exemplos: questionários, entrevistas, observações, experimentos, logs de sistema, tweets coletados, registros institucionais.",
        "options": {"Sim — usa dados originais": "yes", "Não — usa fontes já existentes": "no"},
    },
    "q1_no": {
        "level": "Classificação", "level_label": "Tipo de Fonte",
        "question": "Qual é a natureza principal das fontes utilizadas?",
        "hint": "Selecione a que melhor descreve o corpus do estudo.",
        "options": {
            "Analisa literatura científica / bibliográfica": "bibliografica",
            "Analisa documentos, arquivos, normas ou registros institucionais": "documental",
            "Discute conceitos e autores sem corpus empírico definido": "teorica",
        },
    },
    "q2": {
        "level": "Nível 2", "level_label": "Intervenção",
        "question": "O pesquisador manipula variáveis, cria condições ou introduz uma intervenção deliberada?",
        "hint": "Exemplos: grupo controle/experimental, antes e depois de uma intervenção, teste de ferramenta, aplicação de método didático.",
        "options": {"Sim — há intervenção ou manipulação": "yes", "Não — apenas observa a realidade": "no"},
    },
    "q3": {
        "level": "Nível 3", "level_label": "Finalidade da Intervenção",
        "question": "A intervenção existe para testar efeito causal entre variáveis?",
        "hint": "Ex: 'Avaliar se gamificação aumenta engajamento', 'comparar desempenho entre dois grupos'.",
        "options": {"Sim — testa relação causa-efeito": "yes", "Não — outro propósito": "no"},
    },
    "q4": {
        "level": "Nível 4", "level_label": "Desenvolvimento de Artefato",
        "question": "O estudo desenvolve e avalia um artefato, sistema, modelo, framework, aplicativo ou solução tecnológica?",
        "hint": "Produto, protótipo, ferramenta, plataforma, método computacional...",
        "options": {"Sim — há desenvolvimento de artefato": "yes", "Não — é intervenção sem artefato": "no"},
    },
    "q5": {
        "level": "Nível 5", "level_label": "Caso ou População",
        "question": "O artigo investiga profundamente um caso, contexto, turma, instituição, sistema ou comunidade específica?",
        "hint": "Análise aprofundada de um único caso ou unidade contextual delimitada.",
        "options": {"Sim — foco em caso específico": "yes", "Não — abrangência mais ampla": "no"},
    },
    "q6": {
        "level": "Nível 6", "level_label": "Instrumento de Coleta",
        "question": "O estudo coleta dados padronizados de uma amostra ou população por questionário, formulário ou escala?",
        "hint": "Survey, levantamento com instrumento estruturado aplicado a múltiplos respondentes.",
        "options": {"Sim — usa survey/questionário padronizado": "yes", "Não — outro instrumento": "no"},
    },
    "q7": {
        "level": "Nível 7", "level_label": "Natureza Interpretativa",
        "question": "O estudo busca interpretar sentidos, experiências, percepções, interações ou práticas sociais/culturais?",
        "hint": "Foco em compreensão de significados subjetivos, vivências, discursos.",
        "options": {"Sim — foco interpretativo/qualitativo": "yes", "Não — foco quantitativo/estrutural": "no"},
    },
    "q8": {
        "level": "Nível 8", "level_label": "Imersão no Campo",
        "question": "O pesquisador acompanha o contexto de forma prolongada, com observação participante ou forte inserção no campo?",
        "hint": "Presença contínua, diário de campo, convivência com os sujeitos pesquisados.",
        "options": {"Sim — há imersão prolongada no campo": "yes", "Não — coleta pontual ou sem imersão": "no"},
    },
    "q9": {
        "level": "Nível 9", "level_label": "Geração de Teoria",
        "question": "O artigo afirma construir categorias, modelo teórico ou teoria emergente a partir dos dados?",
        "hint": "Codificação aberta/axial, categorias emergentes, saturação teórica.",
        "options": {"Sim — constrói teoria dos dados": "yes", "Não — descreve ou interpreta sem gerar teoria": "no"},
    },
    "q10": {
        "level": "Nível 10", "level_label": "Correlação Estatística",
        "question": "O estudo analisa correlação, associação, predição ou relação estatística entre variáveis sem manipulação experimental?",
        "hint": "Regressão, correlação de Pearson/Spearman, modelos preditivos, análise fatorial.",
        "options": {"Sim — analisa relações estatísticas": "yes", "Não — não há análise de relação entre variáveis": "no"},
    },
    "q11": {
        "level": "Nível 11", "level_label": "Dimensão Temporal",
        "question": "Os dados foram coletados em vários momentos temporais?",
        "hint": "Coleta em dois ou mais pontos no tempo, acompanhamento longitudinal, painéis.",
        "options": {"Sim — coleta longitudinal": "yes", "Não — coleta em único momento": "no"},
    },
    "qA": {
        "level": "Dimensão A", "level_label": "Paradigma Metodológico",
        "question": "Qual é a natureza predominante dos dados e análise?",
        "hint": "Considere como os dados são coletados e como são analisados.",
        "options": {
            "Dados numéricos analisados estatisticamente": "quantitativa",
            "Falas, textos, observações e interpretações": "qualitativa",
            "Ambos os tipos com integração analítica": "mista",
        },
    },
    "qB": {
        "level": "Dimensão B", "level_label": "Profundidade",
        "question": "Qual é a profundidade pretendida pelo estudo?",
        "hint": "Considere o objetivo principal declarado pelos autores.",
        "options": {
            "Explorar tema pouco conhecido": "exploratoria",
            "Descrever características, perfis ou padrões": "descritiva",
            "Explicar fatores, relações, efeitos ou causas": "explicativa",
        },
    },
    "qC": {
        "level": "Dimensão C", "level_label": "Finalidade",
        "question": "Qual é a finalidade principal da pesquisa?",
        "hint": "Considere o que motiva o estudo.",
        "options": {
            "Resolver problema prático, desenvolver ferramenta ou apoiar decisão": "aplicada",
            "Ampliar teoria, conceito ou compreensão fundamental": "basica",
        },
    },
}

# ─── Fluxo de decisão ────────────────────────────────────────────────────────
FLOW = {
    "q1":    {"yes": "q2",           "no": "q1_no"},
    "q1_no": {"bibliografica": None, "documental": None, "teorica": None},
    "q2":    {"yes": "q3",           "no": "q5"},
    "q3":    {"yes": "RESULT_EXP",   "no": "q4"},
    "q4":    {"yes": "RESULT_DSR",   "no": "RESULT_ACT"},
    "q5":    {"yes": "RESULT_CASE",  "no": "q6"},
    "q6":    {"yes": "RESULT_SURVEY","no": "q7"},
    "q7":    {"yes": "q8",           "no": "q10"},
    "q8":    {"yes": "RESULT_ETNO",  "no": "q9"},
    "q9":    {"yes": "RESULT_GT",    "no": "RESULT_QUAL"},
    "q10":   {"yes": "RESULT_CORR",  "no": "q11"},
    "q11":   {"yes": "RESULT_LONG",  "no": "RESULT_TRANS"},
}

STRATEGIES = {
    "bibliografica":  {"title": "Pesquisa Bibliográfica",                    "icon": "📚"},
    "documental":     {"title": "Pesquisa Documental",                        "icon": "🗂️"},
    "teorica":        {"title": "Pesquisa Teórica / Ensaio Teórico",          "icon": "🧠"},
    "RESULT_EXP":     {"title": "Pesquisa Experimental",                      "icon": "⚗️"},
    "RESULT_DSR":     {"title": "Design Science Research (DSR)",              "icon": "🔧"},
    "RESULT_ACT":     {"title": "Pesquisa-Ação",                              "icon": "🤝"},
    "RESULT_CASE":    {"title": "Estudo de Caso",                             "icon": "🔍"},
    "RESULT_SURVEY":  {"title": "Survey / Levantamento",                      "icon": "📊"},
    "RESULT_ETNO":    {"title": "Pesquisa Etnográfica",                       "icon": "🏕️"},
    "RESULT_GT":      {"title": "Grounded Theory / Teoria Fundamentada",      "icon": "🌱"},
    "RESULT_QUAL":    {"title": "Pesquisa Qualitativa Empírica",              "icon": "💬"},
    "RESULT_CORR":    {"title": "Pesquisa Correlacional",                     "icon": "📈"},
    "RESULT_LONG":    {"title": "Pesquisa Longitudinal",                      "icon": "⏳"},
    "RESULT_TRANS":   {"title": "Pesquisa Transversal",                       "icon": "📷"},
}

STRATEGY_TEXTS = {
    "Pesquisa Bibliográfica": "A presente pesquisa adota a estratégia de pesquisa bibliográfica, caracterizada pela análise sistemática e crítica da produção científica previamente publicada sobre o tema investigado. A coleta de dados foi realizada por meio de levantamento em bases de dados acadêmicas, com seleção e análise de publicações relevantes para o referencial teórico.",
    "Pesquisa Documental": "Esta pesquisa utiliza a estratégia documental, que se distingue da pesquisa bibliográfica por tratar fontes que ainda não receberam tratamento analítico adequado — como documentos oficiais, relatórios institucionais, legislações e registros organizacionais. A análise documental constitui o corpus principal deste estudo.",
    "Pesquisa Teórica / Ensaio Teórico": "O presente trabalho configura-se como pesquisa teórica, na modalidade de ensaio, dedicando-se à discussão, articulação e elaboração de conceitos, categorias e perspectivas teóricas sem recorrer a corpus empírico definido. O objetivo central é contribuir para o avanço do conhecimento por via da reflexão conceitual e revisão crítica de fundamentos teóricos.",
    "Pesquisa Experimental": "Este estudo adota o delineamento experimental, no qual o pesquisador manipula deliberadamente variáveis independentes e controla condições do ambiente a fim de observar e mensurar os efeitos sobre variáveis dependentes. O controle experimental permite estabelecer relações de causalidade entre os fenômenos investigados.",
    "Design Science Research (DSR)": "A pesquisa segue a abordagem do Design Science Research (DSR), paradigma orientado à criação e avaliação de artefatos — como sistemas, modelos, frameworks, algoritmos ou aplicações — que representem soluções inovadoras para problemas práticos identificados. O ciclo de pesquisa compreende as etapas de identificação do problema, definição de requisitos, design, desenvolvimento, avaliação e comunicação dos resultados.",
    "Pesquisa-Ação": "O estudo adota a pesquisa-ação como estratégia metodológica, caracterizada pela participação ativa do pesquisador no contexto investigado e pela busca simultânea de compreensão e transformação da realidade. A produção de conhecimento ocorre de forma colaborativa com os atores envolvidos, em ciclos iterativos de planejamento, ação, observação e reflexão.",
    "Estudo de Caso": "A estratégia metodológica adotada é o estudo de caso, que permite a investigação aprofundada e contextualizada de um fenômeno dentro de seus limites reais. Esta abordagem é especialmente adequada quando as fronteiras entre o fenômeno e seu contexto não são claramente evidentes, possibilitando a compreensão holística e detalhada da unidade de análise.",
    "Survey / Levantamento": "A pesquisa utiliza o método de survey (levantamento), que consiste na coleta sistemática de dados padronizados junto a uma amostra ou população, por meio de questionários ou escalas estruturadas. Esse método permite descrever e analisar características, opiniões, atitudes ou comportamentos de grupos, com possibilidade de generalização estatística dos resultados.",
    "Pesquisa Etnográfica": "O estudo fundamenta-se na abordagem etnográfica, que pressupõe a imersão prolongada do pesquisador no contexto investigado, com o objetivo de compreender culturas, práticas, significados e interações sociais a partir de dentro. A coleta de dados se dá prioritariamente por observação participante, registros em diário de campo e entrevistas aprofundadas.",
    "Grounded Theory / Teoria Fundamentada": "Esta pesquisa utiliza a Grounded Theory (Teoria Fundamentada nos Dados), método qualitativo orientado à construção indutiva de teoria a partir de dados empíricos. O processo analítico envolve codificação aberta, codificação axial e codificação seletiva, até a identificação de categorias centrais e saturação teórica, com o objetivo de produzir teoria substantiva sobre o fenômeno estudado.",
    "Pesquisa Qualitativa Empírica": "A pesquisa adota a abordagem qualitativa empírica, voltada à compreensão e interpretação de significados, experiências, percepções e práticas sociais dos sujeitos pesquisados. A análise é predominantemente interpretativa, orientada pela riqueza e profundidade dos dados, em detrimento da representatividade estatística.",
    "Pesquisa Correlacional": "O delineamento utilizado é o correlacional, que visa identificar e mensurar relações, associações ou correlações entre variáveis, sem que o pesquisador manipule qualquer uma delas. Os procedimentos estatísticos utilizados permitem verificar a existência, direção e magnitude das relações entre as variáveis investigadas.",
    "Pesquisa Longitudinal": "O estudo adota o delineamento longitudinal, com coleta de dados em múltiplos momentos temporais sobre os mesmos sujeitos ou unidades de análise. Este delineamento permite rastrear mudanças, trajetórias e tendências ao longo do tempo, sendo especialmente adequado para investigar processos de desenvolvimento ou transformação.",
    "Pesquisa Transversal": "O estudo adota o delineamento transversal, com coleta de dados em único momento temporal, fornecendo uma fotografia da realidade investigada em um ponto específico no tempo. Este delineamento é eficiente para descrição de características de populações e identificação de associações entre variáveis em um corte temporal definido.",
}

PARADIGM_TEXTS = {
    "quantitativa": "Do ponto de vista da abordagem, a pesquisa é de natureza quantitativa, utilizando instrumentos e procedimentos que permitem a quantificação dos dados e sua análise por meio de técnicas estatísticas descritivas e/ou inferenciais.",
    "qualitativa":  "Quanto à abordagem, o estudo é de natureza qualitativa, priorizando a interpretação aprofundada de dados não numéricos — como discursos, narrativas, observações e interações — sem a pretensão de generalização estatística.",
    "mista":        "Em relação à abordagem metodológica, o estudo caracteriza-se como de método misto, integrando procedimentos quantitativos e qualitativos de forma complementar, visando uma compreensão mais abrangente e robusta do fenômeno investigado.",
}
DEPTH_TEXTS = {
    "exploratoria": "Quanto aos objetivos, a pesquisa é exploratória, buscando ampliar a familiaridade com um fenômeno ainda pouco estudado, levantar hipóteses e identificar variáveis relevantes para investigações futuras.",
    "descritiva":   "Em relação aos objetivos, a pesquisa é descritiva, com foco na caracterização detalhada das propriedades, perfis, frequências ou padrões do fenômeno investigado, sem necessariamente estabelecer relações causais.",
    "explicativa":  "Quanto aos objetivos, a pesquisa é explicativa, buscando identificar fatores determinantes e estabelecer relações causais ou explicativas entre variáveis, contribuindo para a compreensão aprofundada dos mecanismos que governam o fenômeno.",
}
PURPOSE_TEXTS = {
    "aplicada": "No que diz respeito à sua finalidade, trata-se de pesquisa aplicada, orientada à geração de conhecimento com vistas à resolução de problemas práticos, melhoria de processos ou apoio à tomada de decisão em contextos reais.",
    "basica":   "Quanto à sua finalidade, configura-se como pesquisa básica (ou fundamental), voltada à ampliação do conhecimento científico, à elaboração de conceitos e ao desenvolvimento teórico, sem aplicação imediata prevista.",
}

PARADIGM_LABELS = {"quantitativa": "Quantitativa", "qualitativa": "Qualitativa", "mista": "Método Misto"}
DEPTH_LABELS    = {"exploratoria": "Exploratória", "descritiva": "Descritiva", "explicativa": "Explicativa"}
PURPOSE_LABELS  = {"aplicada": "Aplicada", "basica": "Básica"}

# ─── Session state init ──────────────────────────────────────────────────────
if "step" not in st.session_state:
    st.session_state.step = "intro"
if "history" not in st.session_state:
    st.session_state.history = []   # list of (q_id, answer_value, answer_label)
if "result_key" not in st.session_state:
    st.session_state.result_key = None
if "main_strategy" not in st.session_state:
    st.session_state.main_strategy = None
if "current_q" not in st.session_state:
    st.session_state.current_q = "q1"

def reset():
    st.session_state.step = "intro"
    st.session_state.history = []
    st.session_state.result_key = None
    st.session_state.main_strategy = None
    st.session_state.current_q = "q1"

def next_question(q_id, answer_value, answer_label):
    st.session_state.history.append((q_id, answer_value, answer_label))
    next_key = FLOW.get(q_id, {}).get(answer_value)

    # Terminal nodes from q1_no
    if q_id == "q1_no":
        st.session_state.main_strategy = answer_value
        st.session_state.result_key = answer_value
        st.session_state.current_q = "qA"
        return

    if next_key is None or next_key.startswith("RESULT"):
        if next_key:
            st.session_state.result_key = next_key
        st.session_state.current_q = "qA"
        return

    st.session_state.current_q = next_key

def go_back():
    if not st.session_state.history:
        st.session_state.step = "intro"
        return
    last_q, _, _ = st.session_state.history.pop()
    st.session_state.current_q = last_q
    st.session_state.result_key = None
    st.session_state.step = "quiz"

def build_methodology(answers_dict, strategy_title):
    parts = []
    parts.append(STRATEGY_TEXTS.get(strategy_title, ""))
    parts.append(PARADIGM_TEXTS.get(answers_dict.get("qA", ""), ""))
    parts.append(DEPTH_TEXTS.get(answers_dict.get("qB", ""), ""))
    parts.append(PURPOSE_TEXTS.get(answers_dict.get("qC", ""), ""))
    return "\n\n    ".join([p for p in parts if p])

# ─── INTRO ───────────────────────────────────────────────────────────────────
if st.session_state.step == "intro":
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="section-label" style="text-align:center">Ferramenta Metodológica</p>', unsafe_allow_html=True)
    st.markdown("""
    <h1 style='text-align:center; font-size:2.6rem; line-height:1.15; margin-bottom:0.4rem'>
        Classificador de<br><em style='color:#c9a84c'>Pesquisa Científica</em>
    </h1>
    """, unsafe_allow_html=True)
    st.markdown("""
    <p style='text-align:center; color:#7a7670; font-size:1.05rem; line-height:1.8; max-width:520px; margin:0 auto 2rem'>
        Responda às perguntas e receba automaticamente a classificação metodológica
        do seu estudo e a redação do parágrafo de metodologia.
    </p>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="badge">🎯 Estratégia principal</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="badge">🔬 Abordagem metodológica</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="badge">📝 Redação automática</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_btn = st.columns([1, 2, 1])[1]
    with col_btn:
        if st.button("Iniciar Classificação →", use_container_width=True):
            st.session_state.step = "quiz"
            st.rerun()

    st.markdown("""
    <p class='note-text' style='margin-top:1.5rem'>
        Baseado na Árvore de Decisão para Classificação de Artigos Científicos
    </p>
    """, unsafe_allow_html=True)

# ─── QUIZ ────────────────────────────────────────────────────────────────────
elif st.session_state.step == "quiz":
    cq = st.session_state.current_q

    # Check if we're in complementary dimensions
    complementary = ["qA", "qB", "qC"]
    main_done = st.session_state.result_key is not None

    # Get answers dict for complementary tracking
    answers_dict = {q: v for q, v, _ in st.session_state.history}

    # If all complementary answered → show result
    if main_done and all(q in answers_dict for q in complementary):
        st.session_state.step = "result"
        st.rerun()

    q_data = QUESTIONS.get(cq)
    if not q_data:
        st.session_state.step = "result"
        st.rerun()

    # Progress
    total_steps = 14
    progress_val = len(st.session_state.history) / total_steps
    st.progress(progress_val)

    # Header row
    col_back, col_prog = st.columns([1, 3])
    with col_back:
        if st.button("← Voltar"):
            go_back()
            st.rerun()
    with col_prog:
        st.markdown(f'<p style="text-align:right; color:#4a4840; font-size:0.8rem; letter-spacing:0.15em; margin-top:0.4rem">{len(st.session_state.history) + 1} / {total_steps}</p>', unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Level badge
    st.markdown(f'<span class="level-badge">{q_data["level"]}</span> <span style="color:#6a6660; font-size:0.85rem">{q_data["level_label"]}</span>', unsafe_allow_html=True)

    # Question
    st.markdown(f'<h2 style="font-size:1.55rem; line-height:1.35; margin-bottom:0.5rem">{q_data["question"]}</h2>', unsafe_allow_html=True)

    # Hint
    st.markdown(f'<div class="hint-box">{q_data["hint"]}</div>', unsafe_allow_html=True)

    # Options as radio
    option_labels = list(q_data["options"].keys())
    choice = st.radio("", option_labels, index=None, label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    col_confirm = st.columns([2, 1])[0]
    with col_confirm:
        if st.button("Confirmar resposta →", use_container_width=True, disabled=(choice is None)):
            answer_value = q_data["options"][choice]

            # Route to complementary after result key set
            if cq in ["qA", "qB", "qC"]:
                answers_dict[cq] = answer_value
                st.session_state.history.append((cq, answer_value, choice))
                if cq == "qA":
                    st.session_state.current_q = "qB"
                elif cq == "qB":
                    st.session_state.current_q = "qC"
                elif cq == "qC":
                    st.session_state.step = "result"
                st.rerun()
            else:
                next_question(cq, answer_value, choice)
                st.rerun()

# ─── RESULT ──────────────────────────────────────────────────────────────────
elif st.session_state.step == "result":
    answers_dict = {q: v for q, v, _ in st.session_state.history}

    # Determine strategy
    rk = st.session_state.result_key
    if rk in STRATEGIES:
        strat = STRATEGIES[rk]
    elif rk in ["bibliografica", "documental", "teorica"]:
        strat = STRATEGIES[rk]
    else:
        strat = {"title": "Não identificado", "icon": "❓"}

    strategy_title = strat["title"]
    strategy_icon  = strat["icon"]

    # Tags
    paradigm_label = PARADIGM_LABELS.get(answers_dict.get("qA", ""), "")
    depth_label    = DEPTH_LABELS.get(answers_dict.get("qB", ""), "")
    purpose_label  = PURPOSE_LABELS.get(answers_dict.get("qC", ""), "")

    # Methodology text
    methodology = build_methodology(answers_dict, strategy_title)

    # ── Display ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<p style="text-align:center; font-size:3rem; margin-bottom:0">{strategy_icon}</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-label" style="text-align:center">Estratégia Principal Identificada</p>', unsafe_allow_html=True)
    st.markdown(f'<h1 style="text-align:center; font-size:2.2rem; margin-bottom:0.5rem">{strategy_title}</h1>', unsafe_allow_html=True)

    # Badges
    badges_html = " ".join([f'<span class="badge">{t}</span>' for t in [paradigm_label, depth_label, purpose_label] if t])
    st.markdown(f'<div style="text-align:center; margin:0.5rem 0 1.5rem">{badges_html}</div>', unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<p class="section-label">Redação da Metodologia</p>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="methodology-box">
        {methodology.replace(chr(10), '<br><br>')}
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="note-text">* Revise e adapte o texto conforme as especificidades do seu estudo antes de utilizá-lo.</p>', unsafe_allow_html=True)

    # Copy area
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="section-label">Copiar Texto</p>', unsafe_allow_html=True)
    st.text_area("", value=methodology, height=220, label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("↺ Nova Classificação", use_container_width=True):
            reset()
            st.rerun()
    with col2:
        st.download_button(
            label="⬇️ Baixar como .txt",
            data=f"CLASSIFICAÇÃO METODOLÓGICA\n{'='*40}\n\nEstratégia: {strategy_title}\nAbordagem: {paradigm_label}\nProfundidade: {depth_label}\nFinalidade: {purpose_label}\n\n{'='*40}\nREDAÇÃO DA METODOLOGIA\n{'='*40}\n\n{methodology}",
            file_name="metodologia.txt",
            mime="text/plain",
            use_container_width=True,
        )
