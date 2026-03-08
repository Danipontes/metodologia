import { useState, useEffect, useRef } from "react";

const QUESTIONS = [
  {
    id: "q1",
    level: "Nível 1",
    levelLabel: "Origem dos Dados",
    question: "O artigo analisa dados coletados diretamente da realidade pesquisada?",
    hint: "Questionários, entrevistas, observações, experimentos, logs, tweets coletados, registros institucionais...",
    options: [
      { label: "Sim — usa dados originais", value: "yes" },
      { label: "Não — usa fontes já existentes", value: "no" },
    ],
  },
  {
    id: "q1_no",
    level: "Classificação",
    levelLabel: "Tipo de Fonte",
    question: "Qual é a natureza principal das fontes utilizadas?",
    hint: "Selecione a que melhor descreve o corpus do estudo.",
    options: [
      { label: "Analisa literatura científica / bibliográfica", value: "bibliografica" },
      { label: "Analisa documentos, arquivos, normas ou registros institucionais", value: "documental" },
      { label: "Discute conceitos e autores sem corpus empírico definido", value: "teorica" },
    ],
  },
  {
    id: "q2",
    level: "Nível 2",
    levelLabel: "Intervenção",
    question: "O pesquisador manipula variáveis, cria condições ou introduz uma intervenção deliberada?",
    hint: "Grupo controle/experimental, antes e depois, teste de ferramenta, aplicação de método didático...",
    options: [
      { label: "Sim — há intervenção ou manipulação", value: "yes" },
      { label: "Não — apenas observa a realidade", value: "no" },
    ],
  },
  {
    id: "q3",
    level: "Nível 3",
    levelLabel: "Finalidade da Intervenção",
    question: "A intervenção existe para testar efeito causal entre variáveis?",
    hint: "'Avaliar se gamificação aumenta engajamento', 'comparar desempenho entre grupos'...",
    options: [
      { label: "Sim — testa relação causa-efeito", value: "yes" },
      { label: "Não — outro propósito", value: "no" },
    ],
  },
  {
    id: "q4",
    level: "Nível 4",
    levelLabel: "Desenvolvimento de Artefato",
    question: "O estudo desenvolve e avalia um artefato, sistema, modelo, framework, aplicativo ou solução tecnológica?",
    hint: "Produto, protótipo, ferramenta, plataforma, método computacional...",
    options: [
      { label: "Sim — há desenvolvimento de artefato", value: "yes" },
      { label: "Não — é intervenção sem artefato", value: "no" },
    ],
  },
  {
    id: "q5",
    level: "Nível 5",
    levelLabel: "Caso ou População",
    question: "O artigo investiga profundamente um caso, contexto, turma, instituição, sistema ou comunidade específica?",
    hint: "Análise aprofundada de um único caso ou unidade contextual delimitada.",
    options: [
      { label: "Sim — foco em caso específico", value: "yes" },
      { label: "Não — abrangência mais ampla", value: "no" },
    ],
  },
  {
    id: "q6",
    level: "Nível 6",
    levelLabel: "Instrumento de Coleta",
    question: "O estudo coleta dados padronizados de uma amostra ou população por questionário, formulário ou escala?",
    hint: "Survey, levantamento com instrumento estruturado aplicado a múltiplos respondentes.",
    options: [
      { label: "Sim — usa survey/questionário padronizado", value: "yes" },
      { label: "Não — outro instrumento", value: "no" },
    ],
  },
  {
    id: "q7",
    level: "Nível 7",
    levelLabel: "Natureza Interpretativa",
    question: "O estudo busca interpretar sentidos, experiências, percepções, interações ou práticas sociais/culturais?",
    hint: "Foco em compreensão de significados subjetivos, vivências, discursos...",
    options: [
      { label: "Sim — foco interpretativo/qualitativo", value: "yes" },
      { label: "Não — foco quantitativo/estrutural", value: "no" },
    ],
  },
  {
    id: "q8",
    level: "Nível 8",
    levelLabel: "Imersão no Campo",
    question: "O pesquisador acompanha o contexto de forma prolongada, com observação participante ou forte inserção no campo?",
    hint: "Presença contínua, diário de campo, convivência com os sujeitos pesquisados.",
    options: [
      { label: "Sim — há imersão prolongada no campo", value: "yes" },
      { label: "Não — coleta pontual ou sem imersão", value: "no" },
    ],
  },
  {
    id: "q9",
    level: "Nível 9",
    levelLabel: "Geração de Teoria",
    question: "O artigo afirma construir categorias, modelo teórico ou teoria emergente a partir dos dados?",
    hint: "Codificação aberta/axial, categorias emergentes, saturação teórica...",
    options: [
      { label: "Sim — constrói teoria dos dados", value: "yes" },
      { label: "Não — descreve ou interpreta sem gerar teoria", value: "no" },
    ],
  },
  {
    id: "q10",
    level: "Nível 10",
    levelLabel: "Correlação Estatística",
    question: "O estudo analisa correlação, associação, predição ou relação estatística entre variáveis sem manipulação experimental?",
    hint: "Regressão, correlação de Pearson/Spearman, modelos preditivos, análise fatorial...",
    options: [
      { label: "Sim — analisa relações estatísticas", value: "yes" },
      { label: "Não — não há análise de relação entre variáveis", value: "no" },
    ],
  },
  {
    id: "q11",
    level: "Nível 11",
    levelLabel: "Dimensão Temporal",
    question: "Os dados foram coletados em vários momentos temporais?",
    hint: "Coleta em dois ou mais pontos no tempo, acompanhamento longitudinal, painéis...",
    options: [
      { label: "Sim — coleta longitudinal", value: "yes" },
      { label: "Não — coleta em único momento", value: "no" },
    ],
  },
  // Complementary dimensions
  {
    id: "qA",
    level: "Dimensão A",
    levelLabel: "Paradigma Metodológico",
    question: "Qual é a natureza predominante dos dados e análise?",
    hint: "Considere como os dados são coletados e como são analisados.",
    options: [
      { label: "Dados numéricos analisados estatisticamente", value: "quantitativa" },
      { label: "Falas, textos, observações e interpretações", value: "qualitativa" },
      { label: "Ambos os tipos com integração analítica", value: "mista" },
    ],
  },
  {
    id: "qB",
    level: "Dimensão B",
    levelLabel: "Profundidade",
    question: "Qual é a profundidade pretendida pelo estudo?",
    hint: "Considere o objetivo principal declarado pelos autores.",
    options: [
      { label: "Explorar tema pouco conhecido", value: "exploratoria" },
      { label: "Descrever características, perfis ou padrões", value: "descritiva" },
      { label: "Explicar fatores, relações, efeitos ou causas", value: "explicativa" },
    ],
  },
  {
    id: "qC",
    level: "Dimensão C",
    levelLabel: "Finalidade",
    question: "Qual é a finalidade principal da pesquisa?",
    hint: "Considere o que motiva o estudo.",
    options: [
      { label: "Resolver problema prático, desenvolver ferramenta ou apoiar decisão", value: "aplicada" },
      { label: "Ampliar teoria, conceito ou compreensão fundamental", value: "basica" },
    ],
  },
];

const FLOW = {
  q1: { yes: "q2", no: "q1_no" },
  q1_no: { bibliografica: "RESULT", documental: "RESULT", teorica: "RESULT" },
  q2: { yes: "q3", no: "q5" },
  q3: { yes: "RESULT_EXP", no: "q4" },
  q4: { yes: "RESULT_DSR", no: "RESULT_ACT" },
  q5: { yes: "RESULT_CASE", no: "q6" },
  q6: { yes: "RESULT_SURVEY", no: "q7" },
  q7: { yes: "q8", no: "q10" },
  q8: { yes: "RESULT_ETNO", no: "q9" },
  q9: { yes: "RESULT_GT", no: "RESULT_QUAL" },
  q10: { yes: "RESULT_CORR", no: "q11" },
  q11: { yes: "RESULT_LONG", no: "RESULT_TRANS" },
};

function classify(answers) {
  const main = answers.mainStrategy;
  const paradigm = answers.qA;
  const depth = answers.qB;
  const purpose = answers.qC;

  const labels = {
    quantitativa: "Quantitativa",
    qualitativa: "Qualitativa",
    mista: "Método Misto",
    exploratoria: "Exploratória",
    descritiva: "Descritiva",
    explicativa: "Explicativa",
    aplicada: "Aplicada",
    basica: "Básica",
  };

  const p = labels[paradigm] || "";
  const d = labels[depth] || "";
  const f = labels[purpose] || "";

  const strategies = {
    bibliografica: {
      title: "Pesquisa Bibliográfica",
      icon: "📚",
      color: "#4A90D9",
      desc: "Análise sistemática da literatura científica existente sobre o tema.",
    },
    documental: {
      title: "Pesquisa Documental",
      icon: "🗂️",
      color: "#7B68EE",
      desc: "Análise de documentos, arquivos, normas e registros institucionais como fonte primária.",
    },
    teorica: {
      title: "Pesquisa Teórica / Ensaio Teórico",
      icon: "🧠",
      color: "#9B59B6",
      desc: "Discussão conceitual e reflexão teórica sem corpus empírico definido.",
    },
    experimental: {
      title: "Pesquisa Experimental",
      icon: "⚗️",
      color: "#E74C3C",
      desc: "Manipulação controlada de variáveis para testar relações causais.",
    },
    dsr: {
      title: "Design Science Research",
      icon: "🔧",
      color: "#E67E22",
      desc: "Desenvolvimento e avaliação de artefatos, sistemas ou soluções tecnológicas.",
    },
    action: {
      title: "Pesquisa-Ação",
      icon: "🤝",
      color: "#27AE60",
      desc: "Intervenção colaborativa no contexto real com mudança prática e reflexão crítica.",
    },
    case: {
      title: "Estudo de Caso",
      icon: "🔍",
      color: "#16A085",
      desc: "Investigação aprofundada de caso, contexto ou unidade específica.",
    },
    survey: {
      title: "Survey / Levantamento",
      icon: "📊",
      color: "#2980B9",
      desc: "Coleta padronizada de dados de uma amostra ou população via questionário.",
    },
    etnografica: {
      title: "Pesquisa Etnográfica",
      icon: "🏕️",
      color: "#8E44AD",
      desc: "Imersão prolongada no campo com observação participante intensa.",
    },
    grounded: {
      title: "Grounded Theory / Teoria Fundamentada",
      icon: "🌱",
      color: "#1ABC9C",
      desc: "Geração de teoria emergente a partir da análise sistemática dos dados.",
    },
    qualitativa_emp: {
      title: "Pesquisa Qualitativa Empírica",
      icon: "💬",
      color: "#3498DB",
      desc: "Interpretação de significados, experiências e práticas com dados qualitativos.",
    },
    correlacional: {
      title: "Pesquisa Correlacional",
      icon: "📈",
      color: "#E74C3C",
      desc: "Análise de correlações, associações e relações estatísticas entre variáveis.",
    },
    longitudinal: {
      title: "Pesquisa Longitudinal",
      icon: "⏳",
      color: "#F39C12",
      desc: "Coleta de dados em múltiplos momentos temporais para rastrear mudanças.",
    },
    transversal: {
      title: "Pesquisa Transversal",
      icon: "📷",
      color: "#95A5A6",
      desc: "Coleta de dados em único momento para captura da realidade presente.",
    },
  };

  const resultMap = {
    RESULT: strategies[main] || strategies.bibliografica,
    RESULT_EXP: strategies.experimental,
    RESULT_DSR: strategies.dsr,
    RESULT_ACT: strategies.action,
    RESULT_CASE: strategies.case,
    RESULT_SURVEY: strategies.survey,
    RESULT_ETNO: strategies.etnografica,
    RESULT_GT: strategies.grounded,
    RESULT_QUAL: strategies.qualitativa_emp,
    RESULT_CORR: strategies.correlacional,
    RESULT_LONG: strategies.longitudinal,
    RESULT_TRANS: strategies.transversal,
  };

  return { strategy: resultMap[answers.resultKey] || strategies.bibliografica, p, d, f };
}

function generateMethodology(answers, result) {
  const { strategy, p, d, f } = result;

  const strategyTexts = {
    "Pesquisa Bibliográfica": `A presente pesquisa adota a estratégia de pesquisa bibliográfica, caracterizada pela análise sistemática e crítica da produção científica previamente publicada sobre o tema investigado. A coleta de dados foi realizada por meio de levantamento em bases de dados acadêmicas, com seleção e análise de publicações relevantes para o referencial teórico.`,
    "Pesquisa Documental": `Esta pesquisa utiliza a estratégia documental, que se distingue da pesquisa bibliográfica por tratar fontes que ainda não receberam tratamento analítico adequado — como documentos oficiais, relatórios institucionais, legislações e registros organizacionais. A análise documental constitui o corpus principal deste estudo.`,
    "Pesquisa Teórica / Ensaio Teórico": `O presente trabalho configura-se como pesquisa teórica, na modalidade de ensaio, dedicando-se à discussão, articulação e elaboração de conceitos, categorias e perspectivas teóricas sem recorrer a corpus empírico definido. O objetivo central é contribuir para o avanço do conhecimento por via da reflexão conceitual e revisão crítica de fundamentos teóricos.`,
    "Pesquisa Experimental": `Este estudo adota o delineamento experimental, no qual o pesquisador manipula deliberadamente variáveis independentes e controla condições do ambiente a fim de observar e mensurar os efeitos sobre variáveis dependentes. O controle experimental permite estabelecer relações de causalidade entre os fenômenos investigados.`,
    "Design Science Research": `A pesquisa segue a abordagem do Design Science Research (DSR), paradigma orientado à criação e avaliação de artefatos — como sistemas, modelos, frameworks, algoritmos ou aplicações — que representem soluções inovadoras para problemas práticos identificados. O ciclo de pesquisa compreende as etapas de identificação do problema, definição de requisitos, design, desenvolvimento, avaliação e comunicação dos resultados.`,
    "Pesquisa-Ação": `O estudo adota a pesquisa-ação como estratégia metodológica, caracterizada pela participação ativa do pesquisador no contexto investigado e pela busca simultânea de compreensão e transformação da realidade. A produção de conhecimento ocorre de forma colaborativa com os atores envolvidos, em ciclos iterativos de planejamento, ação, observação e reflexão.`,
    "Estudo de Caso": `A estratégia metodológica adotada é o estudo de caso, que permite a investigação aprofundada e contextualizada de um fenômeno dentro de seus limites reais. Esta abordagem é especialmente adequada quando as fronteiras entre o fenômeno e seu contexto não são claramente evidentes, possibilitando a compreensão holística e detalhada da unidade de análise.`,
    "Survey / Levantamento": `A pesquisa utiliza o método de survey (levantamento), que consiste na coleta sistemática de dados padronizados junto a uma amostra ou população, por meio de questionários ou escalas estruturadas. Esse método permite descrever e analisar características, opiniões, atitudes ou comportamentos de grupos, com possibilidade de generalização estatística dos resultados.`,
    "Pesquisa Etnográfica": `O estudo fundamenta-se na abordagem etnográfica, que pressupõe a imersão prolongada do pesquisador no contexto investigado, com o objetivo de compreender culturas, práticas, significados e interações sociais a partir de dentro. A coleta de dados se dá prioritariamente por observação participante, registros em diário de campo e entrevistas aprofundadas.`,
    "Grounded Theory / Teoria Fundamentada": `Esta pesquisa utiliza a Grounded Theory (Teoria Fundamentada nos Dados), método qualitativo orientado à construção indutiva de teoria a partir de dados empíricos. O processo analítico envolve codificação aberta, codificação axial e codificação seletiva, até a identificação de categorias centrais e saturação teórica, com o objetivo de produzir teoria substantiva sobre o fenômeno estudado.`,
    "Pesquisa Qualitativa Empírica": `A pesquisa adota a abordagem qualitativa empírica, voltada à compreensão e interpretação de significados, experiências, percepções e práticas sociais dos sujeitos pesquisados. A análise é predominantemente interpretativa, orientada pela riqueza e profundidade dos dados, em detrimento da representatividade estatística.`,
    "Pesquisa Correlacional": `O delineamento utilizado é o correlacional, que visa identificar e mensurar relações, associações ou correlações entre variáveis, sem que o pesquisador manipule qualquer uma delas. Os procedimentos estatísticos utilizados permitem verificar a existência, direção e magnitude das relações entre as variáveis investigadas.`,
    "Pesquisa Longitudinal": `O estudo adota o delineamento longitudinal, com coleta de dados em múltiplos momentos temporais sobre os mesmos sujeitos ou unidades de análise. Este delineamento permite rastrear mudanças, trajetórias e tendências ao longo do tempo, sendo especialmente adequado para investigar processos de desenvolvimento ou transformação.`,
    "Pesquisa Transversal": `O estudo adota o delineamento transversal, com coleta de dados em único momento temporal, fornecendo uma fotografia da realidade investigada em um ponto específico no tempo. Este delineamento é eficiente para descrição de características de populações e identificação de associações entre variáveis em um corte temporal definido.`,
  };

  const paradigmText = {
    Quantitativa: `Do ponto de vista da abordagem, a pesquisa é de natureza quantitativa, utilizando instrumentos e procedimentos que permitem a quantificação dos dados e sua análise por meio de técnicas estatísticas descritivas e/ou inferenciais.`,
    Qualitativa: `Quanto à abordagem, o estudo é de natureza qualitativa, priorizando a interpretação aprofundada de dados não numéricos — como discursos, narrativas, observações e interações — sem a pretensão de generalização estatística.`,
    "Método Misto": `Em relação à abordagem metodológica, o estudo caracteriza-se como de método misto, integrando procedimentos quantitativos e qualitativos de forma complementar, visando uma compreensão mais abrangente e robusta do fenômeno investigado.`,
  };

  const depthText = {
    Exploratória: `Quanto aos objetivos, a pesquisa é exploratória, buscando ampliar a familiaridade com um fenômeno ainda pouco estudado, levantar hipóteses e identificar variáveis relevantes para investigações futuras.`,
    Descritiva: `Em relação aos objetivos, a pesquisa é descritiva, com foco na caracterização detalhada das propriedades, perfis, frequências ou padrões do fenômeno investigado, sem necessariamente estabelecer relações causais.`,
    Explicativa: `Quanto aos objetivos, a pesquisa é explicativa, buscando identificar fatores determinantes e estabelecer relações causais ou explicativas entre variáveis, contribuindo para a compreensão aprofundada dos mecanismos que governam o fenômeno.`,
  };

  const purposeText = {
    Aplicada: `No que diz respeito à sua finalidade, trata-se de pesquisa aplicada, orientada à geração de conhecimento com vistas à resolução de problemas práticos, melhoria de processos ou apoio à tomada de decisão em contextos reais.`,
    Básica: `Quanto à sua finalidade, configura-se como pesquisa básica (ou fundamental), voltada à ampliação do conhecimento científico, à elaboração de conceitos e ao desenvolvimento teórico, sem aplicação imediata prevista.`,
  };

  const parts = [
    strategyTexts[strategy.title] || "",
    paradigmText[p] || "",
    depthText[d] || "",
    purposeText[f] || "",
  ].filter(Boolean);

  return parts.join("\n\n");
}

export default function App() {
  const [step, setStep] = useState("intro");
  const [currentQ, setCurrentQ] = useState("q1");
  const [answers, setAnswers] = useState({});
  const [history, setHistory] = useState([]);
  const [result, setResult] = useState(null);
  const [methodology, setMethodology] = useState("");
  const [animating, setAnimating] = useState(false);
  const [copied, setCopied] = useState(false);
  const cardRef = useRef(null);

  const progress = history.length;
  const totalSteps = 14;

  const getCurrentQuestion = () => QUESTIONS.find((q) => q.id === currentQ);

  const handleAnswer = (value) => {
    if (animating) return;
    setAnimating(true);

    const newAnswers = { ...answers, [currentQ]: value };
    setAnswers(newAnswers);

    setTimeout(() => {
      const nextKey = FLOW[currentQ]?.[value];

      if (!nextKey) {
        // Complementary dimensions
        if (currentQ === "q1_no") {
          setAnswers({ ...newAnswers, mainStrategy: value });
          setHistory([...history, currentQ]);
          setCurrentQ("qA");
          setAnimating(false);
          return;
        }
        if (currentQ === "qA") {
          setHistory([...history, currentQ]);
          setCurrentQ("qB");
          setAnimating(false);
          return;
        }
        if (currentQ === "qB") {
          setHistory([...history, currentQ]);
          setCurrentQ("qC");
          setAnimating(false);
          return;
        }
        if (currentQ === "qC") {
          // Final result
          const finalAnswers = { ...newAnswers };
          const resultKey = history.includes("RESULT_marker") ? finalAnswers.resultKey : finalAnswers.resultKey;
          const classified = classify(finalAnswers);
          const meth = generateMethodology(finalAnswers, classified);
          setResult(classified);
          setMethodology(meth);
          setStep("result");
          setAnimating(false);
          return;
        }
      }

      if (nextKey && nextKey.startsWith("RESULT")) {
        setHistory([...history, currentQ]);
        const finalAnswers = { ...newAnswers, resultKey: nextKey };
        setAnswers(finalAnswers);
        setCurrentQ("qA");
        setAnimating(false);
        return;
      }

      setHistory([...history, currentQ]);
      setCurrentQ(nextKey || "qA");
      setAnimating(false);
    }, 300);
  };

  const handleBack = () => {
    if (history.length === 0) {
      setStep("intro");
      return;
    }
    const prev = history[history.length - 1];
    const newHistory = history.slice(0, -1);
    setHistory(newHistory);
    setCurrentQ(prev);
    const newAnswers = { ...answers };
    delete newAnswers[prev];
    setAnswers(newAnswers);
  };

  const handleRestart = () => {
    setStep("intro");
    setCurrentQ("q1");
    setAnswers({});
    setHistory([]);
    setResult(null);
    setMethodology("");
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(methodology);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const q = getCurrentQuestion();

  return (
    <div style={{
      minHeight: "100vh",
      background: "#0a0a0f",
      fontFamily: "'Georgia', 'Times New Roman', serif",
      color: "#e8e4dc",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      padding: "0",
      overflowX: "hidden",
    }}>

      {/* Grain overlay */}
      <div style={{
        position: "fixed", inset: 0, zIndex: 0, pointerEvents: "none",
        backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E")`,
        opacity: 0.5,
      }} />

      {/* Subtle grid */}
      <div style={{
        position: "fixed", inset: 0, zIndex: 0, pointerEvents: "none",
        backgroundImage: `linear-gradient(rgba(200,180,120,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(200,180,120,0.03) 1px, transparent 1px)`,
        backgroundSize: "60px 60px",
      }} />

      {step === "intro" && (
        <div style={{
          position: "relative", zIndex: 1, maxWidth: 720, width: "100%",
          padding: "80px 32px", textAlign: "center",
          animation: "fadeIn 0.8s ease",
        }}>
          <div style={{
            fontSize: 11, letterSpacing: "0.4em", color: "#c9a84c",
            textTransform: "uppercase", marginBottom: 32, fontFamily: "'Georgia', serif",
          }}>
            Ferramenta Metodológica
          </div>

          <h1 style={{
            fontSize: "clamp(2.4rem, 6vw, 4rem)",
            fontWeight: 400,
            lineHeight: 1.1,
            marginBottom: 24,
            color: "#f0ebe0",
            letterSpacing: "-0.02em",
          }}>
            Classificador de<br />
            <span style={{ color: "#c9a84c", fontStyle: "italic" }}>Pesquisa Científica</span>
          </h1>

          <p style={{
            fontSize: "1.1rem", lineHeight: 1.8, color: "#9e9a8e",
            maxWidth: 520, margin: "0 auto 48px",
          }}>
            Responda às perguntas sobre o seu estudo e receba automaticamente a classificação metodológica e a redação do parágrafo de metodologia.
          </p>

          <div style={{
            display: "flex", gap: 24, justifyContent: "center",
            flexWrap: "wrap", marginBottom: 56,
          }}>
            {[
              { icon: "🎯", label: "Estratégia principal" },
              { icon: "🔬", label: "Abordagem metodológica" },
              { icon: "📝", label: "Redação automática" },
            ].map((item) => (
              <div key={item.label} style={{
                display: "flex", alignItems: "center", gap: 8,
                fontSize: "0.85rem", color: "#7a7670",
                padding: "8px 16px",
                border: "1px solid rgba(201,168,76,0.15)",
                borderRadius: 2,
              }}>
                <span>{item.icon}</span>
                <span>{item.label}</span>
              </div>
            ))}
          </div>

          <button
            onClick={() => setStep("quiz")}
            style={{
              background: "#c9a84c",
              color: "#0a0a0f",
              border: "none",
              padding: "16px 48px",
              fontSize: "0.95rem",
              letterSpacing: "0.15em",
              textTransform: "uppercase",
              cursor: "pointer",
              fontFamily: "'Georgia', serif",
              transition: "all 0.2s",
              fontWeight: 700,
            }}
            onMouseEnter={e => e.target.style.background = "#e0bc5e"}
            onMouseLeave={e => e.target.style.background = "#c9a84c"}
          >
            Iniciar Classificação →
          </button>

          <p style={{ marginTop: 20, fontSize: "0.78rem", color: "#4a4840" }}>
            Baseado na Árvore de Decisão para Classificação de Artigos Científicos
          </p>
        </div>
      )}

      {step === "quiz" && q && (
        <div style={{
          position: "relative", zIndex: 1, maxWidth: 680, width: "100%",
          padding: "48px 24px",
          animation: animating ? "slideOut 0.3s ease" : "slideIn 0.35s ease",
        }}>
          {/* Header bar */}
          <div style={{
            display: "flex", justifyContent: "space-between", alignItems: "center",
            marginBottom: 40,
          }}>
            <button onClick={handleBack} style={{
              background: "none", border: "1px solid rgba(201,168,76,0.2)",
              color: "#9e9a8e", padding: "6px 16px", fontSize: "0.8rem",
              cursor: "pointer", letterSpacing: "0.1em", fontFamily: "inherit",
              transition: "all 0.2s",
            }}
              onMouseEnter={e => { e.target.style.borderColor = "#c9a84c"; e.target.style.color = "#c9a84c"; }}
              onMouseLeave={e => { e.target.style.borderColor = "rgba(201,168,76,0.2)"; e.target.style.color = "#9e9a8e"; }}
            >
              ← Voltar
            </button>
            <span style={{ fontSize: "0.78rem", color: "#4a4840", letterSpacing: "0.15em" }}>
              {progress + 1} / {totalSteps}
            </span>
          </div>

          {/* Progress bar */}
          <div style={{ height: 2, background: "rgba(201,168,76,0.1)", marginBottom: 48, borderRadius: 1 }}>
            <div style={{
              height: "100%", background: "#c9a84c",
              width: `${((progress) / totalSteps) * 100}%`,
              transition: "width 0.4s ease", borderRadius: 1,
            }} />
          </div>

          {/* Level badge */}
          <div style={{ marginBottom: 12, display: "flex", alignItems: "center", gap: 12 }}>
            <span style={{
              fontSize: 10, letterSpacing: "0.35em", textTransform: "uppercase",
              color: "#c9a84c", border: "1px solid rgba(201,168,76,0.3)",
              padding: "4px 10px",
            }}>
              {q.level}
            </span>
            <span style={{ fontSize: "0.85rem", color: "#6a6660" }}>{q.levelLabel}</span>
          </div>

          {/* Question */}
          <h2 style={{
            fontSize: "clamp(1.3rem, 3.5vw, 1.8rem)",
            fontWeight: 400, lineHeight: 1.35,
            color: "#f0ebe0", marginBottom: 16,
            letterSpacing: "-0.01em",
          }}>
            {q.question}
          </h2>

          {/* Hint */}
          <p style={{
            fontSize: "0.85rem", color: "#5a5650", lineHeight: 1.7,
            marginBottom: 40, fontStyle: "italic",
            borderLeft: "2px solid rgba(201,168,76,0.2)",
            paddingLeft: 14,
          }}>
            {q.hint}
          </p>

          {/* Options */}
          <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
            {q.options.map((opt) => (
              <button
                key={opt.value}
                onClick={() => handleAnswer(opt.value)}
                style={{
                  background: "rgba(201,168,76,0.03)",
                  border: "1px solid rgba(201,168,76,0.15)",
                  color: "#d0cbc0",
                  padding: "18px 24px",
                  textAlign: "left",
                  cursor: "pointer",
                  fontSize: "0.95rem",
                  lineHeight: 1.5,
                  fontFamily: "'Georgia', serif",
                  transition: "all 0.2s",
                  display: "flex", alignItems: "center", justifyContent: "space-between",
                  gap: 16,
                }}
                onMouseEnter={e => {
                  e.currentTarget.style.background = "rgba(201,168,76,0.08)";
                  e.currentTarget.style.borderColor = "rgba(201,168,76,0.5)";
                  e.currentTarget.style.color = "#f0ebe0";
                }}
                onMouseLeave={e => {
                  e.currentTarget.style.background = "rgba(201,168,76,0.03)";
                  e.currentTarget.style.borderColor = "rgba(201,168,76,0.15)";
                  e.currentTarget.style.color = "#d0cbc0";
                }}
              >
                <span>{opt.label}</span>
                <span style={{ color: "#c9a84c", fontSize: "1.2rem", flexShrink: 0 }}>→</span>
              </button>
            ))}
          </div>
        </div>
      )}

      {step === "result" && result && (
        <div style={{
          position: "relative", zIndex: 1, maxWidth: 760, width: "100%",
          padding: "48px 24px",
          animation: "fadeIn 0.6s ease",
        }}>
          {/* Result header */}
          <div style={{ textAlign: "center", marginBottom: 48 }}>
            <div style={{ fontSize: 48, marginBottom: 16 }}>{result.strategy.icon}</div>
            <div style={{
              fontSize: 10, letterSpacing: "0.4em", color: "#c9a84c",
              textTransform: "uppercase", marginBottom: 12,
            }}>
              Estratégia Principal Identificada
            </div>
            <h1 style={{
              fontSize: "clamp(1.8rem, 5vw, 2.8rem)",
              fontWeight: 400, color: "#f0ebe0",
              letterSpacing: "-0.02em", marginBottom: 12,
            }}>
              {result.strategy.title}
            </h1>
            <p style={{ color: "#7a7670", fontSize: "0.95rem", maxWidth: 480, margin: "0 auto" }}>
              {result.strategy.desc}
            </p>
          </div>

          {/* Tags */}
          <div style={{
            display: "flex", flexWrap: "wrap", gap: 10,
            justifyContent: "center", marginBottom: 48,
          }}>
            {[result.p, result.d, result.f].filter(Boolean).map((tag) => (
              <span key={tag} style={{
                padding: "6px 18px",
                border: `1px solid ${result.strategy.color}40`,
                color: result.strategy.color,
                fontSize: "0.8rem",
                letterSpacing: "0.1em",
                background: `${result.strategy.color}10`,
              }}>
                {tag}
              </span>
            ))}
          </div>

          {/* Divider */}
          <div style={{
            display: "flex", alignItems: "center", gap: 16, marginBottom: 32,
          }}>
            <div style={{ flex: 1, height: 1, background: "rgba(201,168,76,0.15)" }} />
            <span style={{ fontSize: 10, letterSpacing: "0.35em", color: "#c9a84c", textTransform: "uppercase" }}>
              Redação da Metodologia
            </span>
            <div style={{ flex: 1, height: 1, background: "rgba(201,168,76,0.15)" }} />
          </div>

          {/* Methodology text */}
          <div style={{
            background: "rgba(201,168,76,0.03)",
            border: "1px solid rgba(201,168,76,0.12)",
            padding: "32px 36px",
            marginBottom: 28,
            position: "relative",
          }}>
            <div style={{
              position: "absolute", top: -1, left: 32,
              background: "#0a0a0f", padding: "0 8px",
              fontSize: 10, letterSpacing: "0.3em", color: "#c9a84c", textTransform: "uppercase",
            }}>
              Parágrafo Gerado
            </div>
            {methodology.split("\n\n").map((para, i) => (
              <p key={i} style={{
                fontSize: "0.95rem", lineHeight: 1.85, color: "#c8c4ba",
                marginBottom: i < methodology.split("\n\n").length - 1 ? 20 : 0,
                textAlign: "justify",
                textIndent: "2em",
              }}>
                {para}
              </p>
            ))}
          </div>

          {/* Note */}
          <p style={{
            fontSize: "0.78rem", color: "#4a4840", lineHeight: 1.7,
            marginBottom: 36, fontStyle: "italic",
            textAlign: "center",
          }}>
            * Revise e adapte o texto conforme as especificidades do seu estudo antes de utilizá-lo.
          </p>

          {/* Buttons */}
          <div style={{ display: "flex", gap: 12, justifyContent: "center", flexWrap: "wrap" }}>
            <button
              onClick={handleCopy}
              style={{
                background: "#c9a84c", color: "#0a0a0f",
                border: "none", padding: "14px 36px",
                fontSize: "0.85rem", letterSpacing: "0.15em",
                textTransform: "uppercase", cursor: "pointer",
                fontFamily: "'Georgia', serif", fontWeight: 700,
                transition: "all 0.2s",
              }}
              onMouseEnter={e => e.target.style.background = "#e0bc5e"}
              onMouseLeave={e => e.target.style.background = "#c9a84c"}
            >
              {copied ? "✓ Copiado!" : "📋 Copiar Texto"}
            </button>
            <button
              onClick={handleRestart}
              style={{
                background: "none",
                border: "1px solid rgba(201,168,76,0.25)",
                color: "#9e9a8e", padding: "14px 36px",
                fontSize: "0.85rem", letterSpacing: "0.15em",
                textTransform: "uppercase", cursor: "pointer",
                fontFamily: "'Georgia', serif",
                transition: "all 0.2s",
              }}
              onMouseEnter={e => { e.target.style.borderColor = "#c9a84c"; e.target.style.color = "#c9a84c"; }}
              onMouseLeave={e => { e.target.style.borderColor = "rgba(201,168,76,0.25)"; e.target.style.color = "#9e9a8e"; }}
            >
              ↺ Nova Classificação
            </button>
          </div>
        </div>
      )}

      <style>{`
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(16px); }
          to { opacity: 1; transform: translateY(0); }
        }
        @keyframes slideIn {
          from { opacity: 0; transform: translateX(24px); }
          to { opacity: 1; transform: translateX(0); }
        }
        @keyframes slideOut {
          from { opacity: 1; transform: translateX(0); }
          to { opacity: 0; transform: translateX(-24px); }
        }
        * { box-sizing: border-box; }
        body { margin: 0; }
      `}</style>
    </div>
  );
}
