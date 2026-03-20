import streamlit as st

# ─── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Classificador de Pesquisa Científica",
    page_icon="🔬",
    layout="centered",
)

# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Source+Sans+3:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Source Sans 3', sans-serif;
    background-color: #0d0d14;
    color: #e0dbd0;
}
.main { background-color: #0d0d14; }
.block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 760px; }
h1, h2, h3 { font-family: 'Playfair Display', serif !important; color: #f0ebe0 !important; }

.stButton > button {
    background-color: #c9a84c !important; color: #0d0d14 !important;
    border: none !important; font-family: 'Source Sans 3', sans-serif !important;
    font-weight: 600 !important; letter-spacing: 0.1em !important;
    text-transform: uppercase !important; padding: 0.6rem 2rem !important;
    border-radius: 2px !important;
}
.stButton > button:hover { background-color: #e0bc5e !important; }
.stButton > button:disabled { background-color: #3a3530 !important; color: #6a6660 !important; }

div[data-testid="stRadio"] label { color: #c8c4ba !important; font-size: 1rem !important; }
.stProgress > div > div > div { background-color: #c9a84c !important; }

.stTextArea textarea {
    background-color: #1a1a24 !important; color: #c8c4ba !important;
    border: 1px solid #3a3530 !important; font-size: 0.93rem !important; line-height: 1.8 !important;
}
hr { border-color: #2a2520 !important; }

.badge {
    display: inline-block; padding: 4px 14px;
    border: 1px solid #c9a84c44; color: #c9a84c;
    font-size: 0.76rem; letter-spacing: 0.12em; text-transform: uppercase;
    margin: 3px; background: #c9a84c11;
}
.badge-sec {
    display: inline-block; padding: 3px 11px;
    border: 1px solid #4a7a9b44; color: #6aabcb;
    font-size: 0.74rem; letter-spacing: 0.1em; text-transform: uppercase;
    margin: 3px; background: #4a7a9b11;
}
.level-badge {
    display: inline-block; padding: 3px 10px;
    border: 1px solid #c9a84c44; color: #c9a84c;
    font-size: 0.7rem; letter-spacing: 0.3em; text-transform: uppercase;
}
.hint-box {
    border-left: 2px solid #c9a84c33; padding: 8px 14px;
    color: #5a5650; font-style: italic; font-size: 0.87rem;
    margin-bottom: 1.2rem; line-height: 1.6;
}
.methodology-box {
    background: #c9a84c05; border: 1px solid #c9a84c18;
    padding: 28px 32px; margin: 0.5rem 0 1rem;
    line-height: 1.85; color: #c8c4ba; font-size: 0.95rem;
}
.section-label {
    font-size: 0.7rem; letter-spacing: 0.35em;
    color: #c9a84c; text-transform: uppercase; margin-bottom: 0.6rem;
}
.note-text { font-size: 0.78rem; color: #4a4840; font-style: italic; text-align: center; }
.info-box {
    background: #1a2030; border: 1px solid #2a3a50;
    padding: 12px 18px; margin: 0.5rem 0;
    font-size: 0.85rem; color: #6aabcb; line-height: 1.6;
}
.warn-box {
    background: #201a10; border: 1px solid #5a4010;
    padding: 10px 16px; margin: 0.4rem 0;
    font-size: 0.83rem; color: #c9a84c; line-height: 1.6;
}
[data-testid="stSidebar"] { background-color: #0a0a0f !important; border-right: 1px solid #1e1e28; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# BLOCOS DE PERGUNTAS
# ══════════════════════════════════════════════════════════════════════════════

BLOCOS = [
    {
        "id": "corpus",
        "nivel": "Bloco 1", "titulo": "Corpus e Fontes de Dados",
        "pergunta": "Qual é a principal fonte de dados ou corpus utilizado no estudo?",
        "hint": "Marque todas as que se aplicam — um estudo pode combinar fontes.",
        "tipo": "multi",
        "opcoes": [
            {"label": "Dados coletados diretamente pelo pesquisador (entrevistas, questionários, observações, experimentos, logs, registros)", "value": "empirico"},
            {"label": "Literatura científica já publicada (artigos, livros, teses, revisões)", "value": "bibliografico"},
            {"label": "Documentos, arquivos, normas, atas ou registros institucionais", "value": "documental"},
            {"label": "Apenas reflexão/discussão conceitual e teórica, sem corpus empírico definido", "value": "teorico"},
        ],
    },
    {
        "id": "intervencao",
        "nivel": "Bloco 2", "titulo": "Intervenção do Pesquisador",
        "pergunta": "O pesquisador realiza algum tipo de intervenção deliberada?",
        "hint": "Selecione a opção que melhor descreve a relação do pesquisador com o campo.",
        "tipo": "single",
        "opcoes": [
            {"label": "Sim — manipula variáveis ou aplica intervenção controlada (grupo controle/experimental, pré-pós)", "value": "experimental"},
            {"label": "Sim — desenvolve e avalia um artefato, sistema, framework, aplicativo ou solução tecnológica (DSR)", "value": "dsr"},
            {"label": "Sim — intervém colaborativamente no contexto real junto com os participantes (pesquisa-ação)", "value": "pesquisa_acao"},
            {"label": "Não — observa, descreve ou analisa a realidade sem intervenção direta", "value": "nao"},
        ],
    },
    {
        "id": "estrategia",
        "nivel": "Bloco 3", "titulo": "Estratégia de Investigação",
        "pergunta": "Como o estudo organiza a investigação? (Marque todas que se aplicam)",
        "hint": "Múltiplas estratégias podem coexistir, como Survey + Correlacional ou Estudo de Caso + Longitudinal.",
        "tipo": "multi",
        "opcoes": [
            {"label": "Investiga em profundidade um caso, turma, empresa, sistema ou contexto específico (Estudo de Caso)", "value": "estudo_caso"},
            {"label": "Aplica questionário ou escala padronizados a uma amostra ou população (Survey / Levantamento)", "value": "survey"},
            {"label": "Analisa relações, correlações ou predições estatísticas entre variáveis (Correlacional)", "value": "correlacional"},
            {"label": "Coleta dados em múltiplos momentos temporais sobre os mesmos sujeitos (Longitudinal)", "value": "longitudinal"},
            {"label": "Coleta dados em único momento temporal (Transversal)", "value": "transversal"},
            {"label": "Imersão prolongada no campo com observação participante (Etnografia)", "value": "etnografica"},
            {"label": "Constrói teoria emergente sistematicamente a partir dos dados (Grounded Theory)", "value": "grounded"},
            {"label": "Não se aplica — estudo sem coleta primária estruturada", "value": "nenhuma"},
        ],
    },
    {
        "id": "abordagem",
        "nivel": "Bloco 4", "titulo": "Abordagem Metodológica",
        "pergunta": "Qual é a natureza predominante dos dados e da análise?",
        "hint": "Selecione uma ou ambas — se ambas, o estudo é de método misto.",
        "tipo": "multi",
        "opcoes": [
            {"label": "Quantitativa — dados numéricos, métricas e análise estatística", "value": "quantitativa"},
            {"label": "Qualitativa — falas, textos, observações, interpretação de sentidos e significados", "value": "qualitativa"},
        ],
    },
    {
        "id": "profundidade",
        "nivel": "Bloco 5", "titulo": "Profundidade / Objetivo do Estudo",
        "pergunta": "Qual é o principal objetivo declarado pelo estudo?",
        "hint": "Escolha o que melhor reflete a intenção central dos autores.",
        "tipo": "single",
        "opcoes": [
            {"label": "Explorar tema pouco estudado, levantar hipóteses ou mapear variáveis relevantes", "value": "exploratoria"},
            {"label": "Descrever características, perfis, frequências ou padrões do fenômeno", "value": "descritiva"},
            {"label": "Explicar causas, efeitos ou relações entre variáveis", "value": "explicativa"},
        ],
    },
    {
        "id": "finalidade",
        "nivel": "Bloco 6", "titulo": "Finalidade da Pesquisa",
        "pergunta": "O que motiva principalmente o estudo?",
        "hint": "Uma revisão bibliográfica orientada à prática pode ser aplicada; um ensaio conceitual sem aplicação imediata é básica.",
        "tipo": "single",
        "opcoes": [
            {"label": "Aplicada — resolver problema prático, melhorar processo, desenvolver ferramenta ou apoiar decisão", "value": "aplicada"},
            {"label": "Básica — ampliar teoria, conceitos ou compreensão fundamental sem aplicação imediata prevista", "value": "basica"},
        ],
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# LÓGICA DE CLASSIFICAÇÃO
# ══════════════════════════════════════════════════════════════════════════════

def classificar(r):
    corpus      = r.get("corpus", [])
    intervencao = r.get("intervencao", "nao")
    estrategia  = r.get("estrategia", [])
    abordagem   = r.get("abordagem", [])
    profund     = r.get("profundidade", "")
    finalidade  = r.get("finalidade", "")

    principais   = []
    secundarias  = []
    dim_temporal = ""

    # ── Intervenção define estratégia principal ───────────────────────────────
    if intervencao == "experimental":
        principais.append("Pesquisa Experimental")
    elif intervencao == "dsr":
        principais.append("Design Science Research (DSR)")
    elif intervencao == "pesquisa_acao":
        principais.append("Pesquisa-Ação")

    # ── Corpus sem intervenção ────────────────────────────────────────────────
    if not principais:
        if "bibliografico" in corpus and "empirico" not in corpus:
            principais.append("Pesquisa Bibliográfica")
        if "documental" in corpus and "empirico" not in corpus:
            principais.append("Pesquisa Documental")
        if "teorico" in corpus and "empirico" not in corpus:
            principais.append("Pesquisa Teórica / Ensaio Teórico")

    # ── Estratégias empíricas de investigação ─────────────────────────────────
    tem_principal_nao_empirica = bool(principais)  # já classificado por corpus/intervenção

    for v, nome in [
        ("estudo_caso",  "Estudo de Caso"),
        ("survey",       "Survey / Levantamento"),
        ("etnografica",  "Pesquisa Etnográfica"),
        ("grounded",     "Grounded Theory / Teoria Fundamentada"),
    ]:
        if v in estrategia:
            if tem_principal_nao_empirica:
                secundarias.append(nome)
            else:
                if nome not in principais:
                    principais.append(nome)

    # Correlacional é sempre complementar à estratégia de coleta
    if "correlacional" in estrategia:
        secundarias.append("Pesquisa Correlacional")

    # ── Corpus complementar (quando há empírico + outro) ─────────────────────
    if "empirico" in corpus and "bibliografico" in corpus:
        secundarias.append("Revisão de Literatura (complementar)")
    if "empirico" in corpus and "documental" in corpus:
        secundarias.append("Análise Documental (complementar)")

    # ── Temporal ──────────────────────────────────────────────────────────────
    if "longitudinal" in estrategia:
        dim_temporal = "Longitudinal"
    elif "transversal" in estrategia:
        dim_temporal = "Transversal"

    # ── Paradigma ─────────────────────────────────────────────────────────────
    if "quantitativa" in abordagem and "qualitativa" in abordagem:
        paradigma = "Método Misto"
    elif "quantitativa" in abordagem:
        paradigma = "Quantitativa"
    elif "qualitativa" in abordagem:
        paradigma = "Qualitativa"
    else:
        paradigma = ""

    # Fallback
    if not principais:
        principais.append("Pesquisa Empírica")

    return {
        "principais": principais,
        "secundarias": list(dict.fromkeys(secundarias)),  # dedup mantendo ordem
        "paradigma": paradigma,
        "profundidade": profund,
        "finalidade": finalidade,
        "dim_temporal": dim_temporal,
    }


# ══════════════════════════════════════════════════════════════════════════════
# TEXTOS DE METODOLOGIA
# ══════════════════════════════════════════════════════════════════════════════

T_ESTRATEGIA = {
    "Pesquisa Bibliográfica":
        "A presente pesquisa adota a estratégia de pesquisa bibliográfica, caracterizada pela análise sistemática e crítica da produção científica previamente publicada sobre o tema investigado. A coleta de dados foi realizada por meio de levantamento em bases de dados acadêmicas, com seleção e análise de publicações pertinentes à construção do referencial teórico.",
    "Pesquisa Documental":
        "Este estudo recorre à pesquisa documental, que se distingue da pesquisa bibliográfica por tratar fontes primárias que ainda não receberam tratamento analítico sistemático — como documentos oficiais, relatórios institucionais, legislações, atas e registros organizacionais. A análise documental constitui o corpus principal da investigação.",
    "Pesquisa Teórica / Ensaio Teórico":
        "O presente trabalho configura-se como pesquisa teórica na modalidade de ensaio, dedicando-se à discussão, articulação e elaboração crítica de conceitos, categorias e perspectivas teóricas sem recorrer a corpus empírico. O objetivo central é contribuir para o avanço do conhecimento por via da reflexão conceitual e revisão crítica de fundamentos.",
    "Pesquisa Experimental":
        "Este estudo adota o delineamento experimental, no qual o pesquisador manipula deliberadamente variáveis independentes e controla as condições do ambiente, a fim de observar e mensurar os efeitos sobre variáveis dependentes. O controle experimental permite estabelecer relações de causalidade entre os fenômenos investigados com alto grau de rigor metodológico.",
    "Design Science Research (DSR)":
        "A pesquisa segue a abordagem do Design Science Research (DSR), paradigma orientado à criação e avaliação rigorosa de artefatos — sistemas, modelos, frameworks, algoritmos ou aplicações — que representem soluções inovadoras para problemas práticos identificados. O ciclo metodológico compreende as etapas de identificação do problema, definição de objetivos, design, desenvolvimento, avaliação e comunicação dos resultados.",
    "Pesquisa-Ação":
        "O estudo adota a pesquisa-ação como estratégia central, caracterizada pela participação ativa do pesquisador no contexto investigado e pela busca simultânea de compreensão e transformação da realidade. A produção de conhecimento ocorre de forma colaborativa com os atores envolvidos, em ciclos iterativos de planejamento, ação, observação e reflexão crítica.",
    "Estudo de Caso":
        "A estratégia metodológica adotada é o estudo de caso, que permite a investigação aprofundada e contextualizada de um fenômeno dentro de seus limites reais. Esta abordagem é especialmente adequada quando as fronteiras entre o fenômeno e seu contexto não são claramente evidentes, possibilitando a compreensão holística e detalhada da unidade de análise.",
    "Survey / Levantamento":
        "A pesquisa utiliza o método de survey (levantamento), que consiste na coleta sistemática de dados padronizados junto a uma amostra ou população, por meio de questionários ou escalas estruturadas. Esse método permite descrever e analisar características, opiniões, atitudes ou comportamentos de grupos, com possibilidade de generalização estatística dos resultados.",
    "Pesquisa Etnográfica":
        "O estudo fundamenta-se na abordagem etnográfica, que pressupõe a imersão prolongada do pesquisador no contexto investigado, com o objetivo de compreender culturas, práticas, significados e interações sociais a partir de dentro. A coleta de dados se dá prioritariamente por observação participante, registros em diário de campo e entrevistas aprofundadas.",
    "Grounded Theory / Teoria Fundamentada":
        "Esta pesquisa utiliza a Grounded Theory (Teoria Fundamentada nos Dados), método qualitativo orientado à construção indutiva de teoria a partir de dados empíricos. O processo analítico envolve codificação aberta, codificação axial e codificação seletiva, até a identificação de categorias centrais e saturação teórica, produzindo teoria substantiva sobre o fenômeno.",
    "Pesquisa Correlacional":
        "No que se refere ao tratamento dos dados, o estudo emprega análise correlacional, buscando identificar e mensurar relações, associações ou correlações entre variáveis, sem que o pesquisador manipule qualquer uma delas. Os procedimentos estatísticos adotados permitem verificar existência, direção e magnitude das relações entre as variáveis investigadas.",
    "Revisão de Literatura (complementar)":
        "Complementarmente à coleta primária de dados, o estudo realiza revisão da literatura científica pertinente ao tema, fundamentando teoricamente as análises e contextualizando os achados no estado da arte da área.",
    "Análise Documental (complementar)":
        "Complementarmente à coleta primária de dados, o estudo recorre à análise de documentos e registros institucionais como fonte secundária de evidências, ampliando a triangulação dos achados.",
    "Pesquisa Empírica":
        "A pesquisa adota abordagem empírica, com coleta e análise de dados produzidos ou obtidos diretamente no campo de investigação, orientando-se pela busca de evidências observáveis para responder às questões propostas.",
}

T_PARADIGMA = {
    "Quantitativa":   "Do ponto de vista da abordagem, a pesquisa é de natureza quantitativa, utilizando instrumentos e procedimentos que permitem a quantificação dos dados e sua análise por meio de técnicas estatísticas descritivas e/ou inferenciais.",
    "Qualitativa":    "Quanto à abordagem, o estudo é de natureza qualitativa, priorizando a interpretação aprofundada de dados não numéricos — como discursos, narrativas, observações e interações — sem a pretensão de generalização estatística.",
    "Método Misto":   "Em relação à abordagem metodológica, o estudo caracteriza-se como de método misto, integrando procedimentos quantitativos e qualitativos de forma complementar, visando uma compreensão mais abrangente e robusta do fenômeno investigado.",
}
T_PROFUNDIDADE = {
    "exploratoria": "Quanto aos objetivos, a pesquisa é exploratória, buscando ampliar a familiaridade com um fenômeno ainda pouco estudado, levantar hipóteses e identificar variáveis relevantes para investigações futuras.",
    "descritiva":   "Em relação aos objetivos, a pesquisa é descritiva, com foco na caracterização detalhada das propriedades, perfis, frequências ou padrões do fenômeno investigado.",
    "explicativa":  "Quanto aos objetivos, a pesquisa é explicativa, buscando identificar fatores determinantes e estabelecer relações causais ou explicativas entre variáveis, contribuindo para a compreensão dos mecanismos que governam o fenômeno.",
}
T_FINALIDADE = {
    "aplicada": "No que diz respeito à sua finalidade, trata-se de pesquisa aplicada, orientada à geração de conhecimento com vistas à resolução de problemas práticos, melhoria de processos ou apoio à tomada de decisão em contextos reais.",
    "basica":   "Quanto à sua finalidade, configura-se como pesquisa básica (ou fundamental), voltada à ampliação do conhecimento científico, à elaboração de conceitos e ao desenvolvimento teórico, sem aplicação imediata prevista.",
}
T_TEMPORAL = {
    "Longitudinal": "Do ponto de vista do delineamento temporal, o estudo é longitudinal, com coleta de dados em múltiplos momentos sobre os mesmos sujeitos ou unidades de análise, permitindo rastrear mudanças e tendências ao longo do tempo.",
    "Transversal":  "Quanto ao corte temporal, o estudo é transversal, com coleta de dados em único momento, fornecendo uma fotografia da realidade investigada em um ponto específico no tempo.",
}

def gerar_metodologia(res):
    partes = []
    for e in res["principais"]:
        t = T_ESTRATEGIA.get(e, "")
        if t: partes.append(t)
    if res["paradigma"]:
        t = T_PARADIGMA.get(res["paradigma"], "")
        if t: partes.append(t)
    if res["profundidade"]:
        t = T_PROFUNDIDADE.get(res["profundidade"], "")
        if t: partes.append(t)
    if res["finalidade"]:
        t = T_FINALIDADE.get(res["finalidade"], "")
        if t: partes.append(t)
    if res["dim_temporal"]:
        t = T_TEMPORAL.get(res["dim_temporal"], "")
        if t: partes.append(t)
    for e in res["secundarias"]:
        t = T_ESTRATEGIA.get(e, "")
        if t: partes.append(t)
    return "\n\n".join(partes)


# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════

if "passo" not in st.session_state:
    st.session_state.passo = 0
if "respostas" not in st.session_state:
    st.session_state.respostas = {}
if "tela" not in st.session_state:
    st.session_state.tela = "intro"

def resetar():
    st.session_state.passo = 0
    st.session_state.respostas = {}
    st.session_state.tela = "intro"


# ══════════════════════════════════════════════════════════════════════════════
# TELA: INTRO
# ══════════════════════════════════════════════════════════════════════════════

if st.session_state.tela == "intro":
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="section-label" style="text-align:center">Ferramenta Metodológica</p>', unsafe_allow_html=True)
    st.markdown("""
    <h1 style='text-align:center; font-size:2.6rem; line-height:1.15; margin-bottom:0.4rem'>
        Classificador de<br><em style='color:#c9a84c'>Pesquisa Científica</em>
    </h1>
    """, unsafe_allow_html=True)
    st.markdown("""
    <p style='text-align:center; color:#7a7670; font-size:1rem; line-height:1.8; max-width:580px; margin:0 auto 1.5rem'>
        Responda 6 blocos de perguntas e receba a classificação metodológica completa
        e a redação automática do parágrafo de metodologia do seu estudo.
    </p>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
    ℹ️ <strong>Este classificador reconhece combinações reais:</strong> uma pesquisa pode ser
    simultaneamente DSR + qualitativa + estudo de caso, ou bibliográfica + quantitativa + exploratória,
    ou survey + correlacional + método misto. Marque todas as opções que se aplicam.
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    col = st.columns([1, 2, 1])[1]
    with col:
        if st.button("Iniciar Classificação →", use_container_width=True):
            st.session_state.tela = "quiz"
            st.rerun()
    st.markdown('<p class="note-text" style="margin-top:1.5rem">Baseado na Árvore de Decisão para Classificação de Artigos Científicos</p>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TELA: QUIZ
# ══════════════════════════════════════════════════════════════════════════════

elif st.session_state.tela == "quiz":
    passo = st.session_state.passo
    total = len(BLOCOS)

    if passo >= total:
        st.session_state.tela = "result"
        st.rerun()

    bloco = BLOCOS[passo]
    st.progress(passo / total)

    col_back, col_prog = st.columns([1, 3])
    with col_back:
        if st.button("← Voltar"):
            if passo == 0:
                st.session_state.tela = "intro"
            else:
                st.session_state.passo -= 1
                bid = BLOCOS[passo - 1]["id"]
                st.session_state.respostas.pop(bid, None)
            st.rerun()
    with col_prog:
        st.markdown(f'<p style="text-align:right; color:#4a4840; font-size:0.8rem; letter-spacing:0.15em; margin-top:0.4rem">Bloco {passo + 1} de {total}</p>', unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f'<span class="level-badge">{bloco["nivel"]}</span>&nbsp;&nbsp;<span style="color:#6a6660; font-size:0.85rem">{bloco["titulo"]}</span>', unsafe_allow_html=True)
    st.markdown(f'<h2 style="font-size:1.45rem; line-height:1.35; margin:0.5rem 0 0.3rem">{bloco["pergunta"]}</h2>', unsafe_allow_html=True)
    st.markdown(f'<div class="hint-box">{bloco["hint"]}</div>', unsafe_allow_html=True)

    opcoes_labels  = [o["label"] for o in bloco["opcoes"]]
    opcoes_values  = {o["label"]: o["value"] for o in bloco["opcoes"]}
    escolha = None
    valido  = False

    if bloco["tipo"] == "single":
        escolha_label = st.radio("", opcoes_labels, index=None, label_visibility="collapsed")
        if escolha_label:
            escolha = opcoes_values[escolha_label]
            valido = True

    elif bloco["tipo"] == "multi":
        selecionados = []
        for label in opcoes_labels:
            if st.checkbox(label, key=f"{bloco['id']}_{opcoes_values[label]}"):
                selecionados.append(opcoes_values[label])
        escolha = selecionados
        valido  = len(selecionados) > 0

        # Alertas de consistência
        if bloco["id"] == "corpus":
            if "teorico" in selecionados and len(selecionados) > 1:
                st.markdown('<div class="warn-box">⚠️ "Apenas discussão teórica" foi marcado junto com outras fontes. Se houver coleta empírica, desmarque a opção teórica.</div>', unsafe_allow_html=True)

        if bloco["id"] == "estrategia":
            if "nenhuma" in selecionados and len(selecionados) > 1:
                st.markdown('<div class="warn-box">⚠️ "Não se aplica" foi marcado junto com outras estratégias. Revise sua seleção.</div>', unsafe_allow_html=True)
            if "longitudinal" in selecionados and "transversal" in selecionados:
                st.markdown('<div class="warn-box">⚠️ Longitudinal e transversal são excludentes. Selecione apenas um.</div>', unsafe_allow_html=True)

        if bloco["id"] == "abordagem" and len(selecionados) == 0:
            st.markdown('<div class="info-box">ℹ️ Selecione pelo menos uma abordagem.</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_btn = st.columns([2, 1])[0]
    with col_btn:
        if st.button("Próximo →", use_container_width=True, disabled=not valido):
            st.session_state.respostas[bloco["id"]] = escolha
            st.session_state.passo += 1
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# TELA: RESULTADO
# ══════════════════════════════════════════════════════════════════════════════

elif st.session_state.tela == "result":
    resultado   = classificar(st.session_state.respostas)
    metodologia = gerar_metodologia(resultado)

    ICONS = {
        "Pesquisa Bibliográfica": "📚", "Pesquisa Documental": "🗂️",
        "Pesquisa Teórica / Ensaio Teórico": "🧠", "Pesquisa Experimental": "⚗️",
        "Design Science Research (DSR)": "🔧", "Pesquisa-Ação": "🤝",
        "Estudo de Caso": "🔍", "Survey / Levantamento": "📊",
        "Pesquisa Etnográfica": "🏕️", "Grounded Theory / Teoria Fundamentada": "🌱",
        "Pesquisa Empírica": "🔬", "Revisão de Literatura (complementar)": "📖",
        "Análise Documental (complementar)": "📄", "Pesquisa Correlacional": "📈",
    }

    LBL_P = {"exploratoria": "Exploratória", "descritiva": "Descritiva", "explicativa": "Explicativa"}
    LBL_F = {"aplicada": "Aplicada", "basica": "Básica"}

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="section-label" style="text-align:center">Classificação Identificada</p>', unsafe_allow_html=True)

    icones = " ".join([ICONS.get(e, "🔬") for e in resultado["principais"]])
    titulos = " + ".join(resultado["principais"])
    st.markdown(f'<p style="text-align:center; font-size:2.2rem; margin-bottom:0.2rem">{icones}</p>', unsafe_allow_html=True)
    st.markdown(f'<h1 style="text-align:center; font-size:1.85rem; line-height:1.25; margin-bottom:0.8rem">{titulos}</h1>', unsafe_allow_html=True)

    badges = ""
    if resultado["paradigma"]:      badges += f'<span class="badge">{resultado["paradigma"]}</span>'
    if resultado["profundidade"]:   badges += f'<span class="badge">{LBL_P.get(resultado["profundidade"],"")}</span>'
    if resultado["finalidade"]:     badges += f'<span class="badge">{LBL_F.get(resultado["finalidade"],"")}</span>'
    if resultado["dim_temporal"]:   badges += f'<span class="badge">{resultado["dim_temporal"]}</span>'
    if badges:
        st.markdown(f'<div style="text-align:center; margin-bottom:0.8rem">{badges}</div>', unsafe_allow_html=True)

    if resultado["secundarias"]:
        sec = " ".join([f'<span class="badge-sec">{ICONS.get(e,"📌")} {e}</span>' for e in resultado["secundarias"]])
        st.markdown('<p class="section-label" style="text-align:center; margin-top:0.6rem">Complementares / Procedimentos analíticos</p>', unsafe_allow_html=True)
        st.markdown(f'<div style="text-align:center; margin-bottom:1rem">{sec}</div>', unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<p class="section-label">Redação da Metodologia</p>', unsafe_allow_html=True)
    st.markdown(f'<div class="methodology-box">{"<br><br>".join(metodologia.split(chr(10)+chr(10)))}</div>', unsafe_allow_html=True)
    st.markdown('<p class="note-text">* Revise e adapte o texto às especificidades do seu estudo antes de utilizá-lo em publicações.</p>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="section-label">Texto para cópia</p>', unsafe_allow_html=True)
    st.text_area("", value=metodologia, height=200, label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("↺ Nova Classificação", use_container_width=True):
            resetar()
            st.rerun()

    resumo_download = f"""CLASSIFICAÇÃO METODOLÓGICA
{'='*50}

Estratégia(s) principal(is) : {' + '.join(resultado['principais'])}
Complementares               : {', '.join(resultado['secundarias']) if resultado['secundarias'] else '—'}
Abordagem                    : {resultado['paradigma'] or '—'}
Profundidade                 : {LBL_P.get(resultado['profundidade'], '—')}
Finalidade                   : {LBL_F.get(resultado['finalidade'], '—')}
Corte temporal               : {resultado['dim_temporal'] or '—'}

{'='*50}
REDAÇÃO DA METODOLOGIA
{'='*50}

{metodologia}
"""
    with col2:
        st.download_button(
            label="⬇️ Baixar como .txt",
            data=resumo_download,
            file_name="classificacao_metodologica.txt",
            mime="text/plain",
            use_container_width=True,
        )
