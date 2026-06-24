import sys
import tempfile
from pathlib import Path
from textwrap import dedent

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from lodestar_veritas.graph import LodestarGraph



def html(markup: str) -> None:
    st.html(dedent(markup))



st.set_page_config(
    page_title="Lodestar Veritas",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed",
)

html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 5%, rgba(37,99,235,0.30), transparent 28%),
        radial-gradient(circle at 85% 15%, rgba(236,72,153,0.22), transparent 30%),
        linear-gradient(135deg, #020617 0%, #07111f 48%, #0f172a 100%);
    color: #f8fafc;
}

.block-container {
    max-width: 1500px;
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

.hero {
    padding: 30px 34px 24px 34px;
    border-radius: 26px;
    border: 1px solid rgba(96,165,250,0.22);
    background:
        radial-gradient(circle at 82% 35%, rgba(236,72,153,0.28), transparent 20%),
        radial-gradient(circle at 12% 20%, rgba(59,130,246,0.22), transparent 20%),
        linear-gradient(90deg, rgba(15,23,42,0.94), rgba(30,27,75,0.70));
    box-shadow: 0 24px 80px rgba(0,0,0,0.42);
    margin-bottom: 16px;
}

.hero-row {
    display: flex;
    align-items: center;
    gap: 26px;
}

.logo-compass {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    display: grid;
    place-items: center;
    position: relative;
    background: radial-gradient(circle, rgba(96,165,250,0.38), transparent 67%);
    filter: drop-shadow(0 0 20px rgba(96,165,250,0.85));
}

.logo-compass::before {
    content: "✦";
    font-size: 5.1rem;
    line-height: 1;
    color: #dbeafe;
    text-shadow:
        0 0 10px #60a5fa,
        0 0 24px #8b5cf6,
        0 0 38px #22d3ee;
}

.logo-compass::after {
    content: "";
    position: absolute;
    width: 92px;
    height: 92px;
    border-radius: 50%;
    border: 1px dashed rgba(96,165,250,0.55);
}

.hero-title {
    font-size: 3.8rem;
    font-weight: 900;
    letter-spacing: -2px;
    background: linear-gradient(90deg, #38bdf8, #818cf8, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    font-size: 1.05rem;
    color: #dbeafe;
    margin-top: -4px;
}

.capability-bar {
    margin-top: 18px;
    padding: 16px 18px;
    border-radius: 18px;
    background: rgba(2,6,23,0.48);
    border: 1px solid rgba(148,163,184,0.18);
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 16px;
}

.capability {
    display: flex;
    align-items: center;
    gap: 11px;
}

.cap-icon {
    font-size: 2rem;
    color: #22d3ee;
    text-shadow: 0 0 14px rgba(34,211,238,0.8);
}

.cap-icon.purple {
    color: #a855f7;
    text-shadow: 0 0 14px rgba(168,85,247,0.8);
}

.cap-icon.pink {
    color: #ec4899;
    text-shadow: 0 0 14px rgba(236,72,153,0.8);
}

.cap-text b {
    color: #22d3ee;
    font-size: 0.82rem;
    display: block;
}

.cap-text span {
    color: #e2e8f0;
    font-size: 0.74rem;
    display: block;
}

.panel {
    border-radius: 20px;
    padding: 20px;
    border: 1px solid rgba(96,165,250,0.22);
    background: rgba(15,23,42,0.76);
    box-shadow: 0 18px 60px rgba(0,0,0,0.32);
    margin-bottom: 16px;
}

.panel-title {
    font-size: 1.3rem;
    font-weight: 850;
    color: #f8fafc;
    margin-bottom: 8px;
}

.panel-subtitle {
    color: #cbd5e1;
    font-size: 0.86rem;
    margin-bottom: 18px;
}

.upload-shell {
    padding: 11px;
    border-radius: 22px;
    background: linear-gradient(145deg, rgba(236,72,153,0.75), rgba(14,165,233,0.85));
}

.upload-inner {
    min-height: 260px;
    border-radius: 18px;
    border: 1.5px dashed rgba(147,197,253,0.58);
    background:
        radial-gradient(circle at 50% 30%, rgba(96,165,250,0.20), transparent 32%),
        rgba(2,6,23,0.83);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    box-shadow: inset 0 0 35px rgba(59,130,246,0.12);
    text-align: center;
    padding: 25px;
}

.upload-icon {
    font-size: 5rem;
    margin-bottom: 12px;
    filter: drop-shadow(0 0 18px rgba(96,165,250,0.9));
}

.upload-title {
    font-size: 1.25rem;
    font-weight: 900;
}

.upload-note {
    color: #cbd5e1;
    font-size: 0.86rem;
    margin-top: 5px;
}

div[data-testid="stFileUploader"] {
    margin-top: -285px;
    opacity: 0.04;
    height: 285px;
}

div[data-testid="stFileUploader"] section {
    min-height: 270px;
}

.uploaded-file {
    padding: 12px 14px;
    border-radius: 13px;
    background: rgba(15,23,42,0.88);
    border: 1px solid rgba(148,163,184,0.20);
    margin-bottom: 8px;
    color: #e2e8f0;
}

.architecture {
    border-radius: 20px;
    padding: 22px;
    border: 1px solid rgba(96,165,250,0.25);
    background:
        radial-gradient(circle at 88% 8%, rgba(168,85,247,0.15), transparent 25%),
        rgba(15,23,42,0.76);
    box-shadow: 0 18px 60px rgba(0,0,0,0.30);
}

.pipeline-stage {
    position: relative;
    border-radius: 18px;
    padding: 34px 14px 20px 14px;
    margin-top: 24px;
    border: 1px solid rgba(14,165,233,0.55);
}

.pipeline-stage.purple {
    border-color: rgba(168,85,247,0.62);
}

.pipeline-stage.pink {
    border-color: rgba(236,72,153,0.62);
}

.stage-label {
    position: absolute;
    top: -16px;
    left: 50%;
    transform: translateX(-50%);
    padding: 8px 18px;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 850;
    color: white;
    background: linear-gradient(90deg, #1d4ed8, #2563eb);
}

.stage-label.purple {
    background: linear-gradient(90deg, #6d28d9, #9333ea);
}

.stage-label.pink {
    background: linear-gradient(90deg, #be185d, #db2777);
}

.pipeline-row {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
}

.node {
    width: 128px;
    min-height: 142px;
    padding: 17px 10px;
    border-radius: 14px;
    text-align: center;
    background: rgba(2,6,23,0.52);
    border: 1px solid rgba(14,165,233,0.65);
}

.node.purple {
    border-color: rgba(168,85,247,0.70);
}

.node.pink {
    border-color: rgba(236,72,153,0.72);
}

.node-icon {
    font-size: 2.55rem;
    line-height: 1;
    margin-bottom: 13px;
    filter: drop-shadow(0 0 8px rgba(96,165,250,0.5));
}

.node-title {
    font-size: 0.83rem;
    font-weight: 900;
    color: #f8fafc;
}

.node-desc {
    margin-top: 7px;
    font-size: 0.72rem;
    color: #cbd5e1;
    line-height: 1.3;
}

.arrow {
    color: #cbd5e1;
    font-size: 1.7rem;
    font-weight: 900;
}

.feedback {
    text-align: center;
    color: #cbd5e1;
    font-size: 0.83rem;
    margin-top: 14px;
}

.info-card {
    position: relative;
    overflow: hidden;
    min-height: 245px;
    border-radius: 18px;
    padding: 20px;
    background:
        radial-gradient(circle at bottom right, rgba(59,130,246,0.16), transparent 38%),
        rgba(15,23,42,0.74);
    border: 1px solid rgba(96,165,250,0.22);
    box-shadow: 0 15px 50px rgba(0,0,0,0.26);
}

.info-card li {
    margin-bottom: 10px;
    color: #e2e8f0;
}

.wave-graphic {
    position: absolute;
    left: 0;
    bottom: 0;
    width: 100%;
    height: 72px;
    opacity: 0.85;
    background:
        radial-gradient(ellipse at 20% 85%, rgba(14,165,233,0.70), transparent 35%),
        radial-gradient(ellipse at 70% 90%, rgba(236,72,153,0.70), transparent 38%);
}

.wave-graphic::before {
    content: "∿∿∿∿∿∿∿∿∿∿∿∿∿";
    position: absolute;
    left: 20px;
    bottom: 12px;
    color: #38bdf8;
    font-size: 2.2rem;
    letter-spacing: 2px;
    text-shadow: 0 0 18px #38bdf8;
}

.shield-graphic {
    position: absolute;
    right: 28px;
    bottom: 18px;
    font-size: 6.8rem;
    color: #60a5fa;
    text-shadow:
        0 0 16px #38bdf8,
        0 0 32px #8b5cf6;
    opacity: 0.85;
}

.chart-graphic {
    position: absolute;
    right: 28px;
    bottom: 22px;
    display: flex;
    align-items: end;
    gap: 10px;
    height: 120px;
}

.bar {
    width: 24px;
    border-radius: 8px 8px 3px 3px;
    background: linear-gradient(180deg, #38bdf8, #7c3aed);
    box-shadow: 0 0 18px rgba(56,189,248,0.65);
}

.bar:nth-child(1) { height: 50px; }
.bar:nth-child(2) { height: 82px; background: linear-gradient(180deg, #fb923c, #ec4899); }
.bar:nth-child(3) { height: 115px; }
.bar:nth-child(4) { height: 68px; background: linear-gradient(180deg, #f59e0b, #8b5cf6); }

.check-list {
    list-style: none;
    padding-left: 0;
}

.check-list li::before {
    content: "✅ ";
    margin-right: 4px;
}

.number-list {
    list-style: none;
    padding-left: 0;
    counter-reset: step;
}

.number-list li {
    counter-increment: step;
}

.number-list li::before {
    content: counter(step);
    display: inline-grid;
    place-items: center;
    width: 22px;
    height: 22px;
    margin-right: 8px;
    border-radius: 50%;
    background: #2563eb;
    color: white;
    font-size: 0.72rem;
    font-weight: 900;
}

.stButton > button {
    width: 100%;
    height: 3.5rem;
    border-radius: 14px;
    border: none;
    font-weight: 900;
    font-size: 1rem;
    color: white;
    background: linear-gradient(90deg, #2563eb, #7c3aed, #db2777);
    box-shadow: 0 18px 40px rgba(124,58,237,0.42);
}

textarea {
    border-radius: 15px !important;
}

div[data-testid="stMetric"] {
    background: rgba(15,23,42,0.78);
    border: 1px solid rgba(96,165,250,0.22);
    border-radius: 18px;
    padding: 18px;
}

.chunk-card {
    padding: 16px;
    border-radius: 16px;
    background: rgba(2,6,23,0.48);
    border: 1px solid rgba(148,163,184,0.20);
    margin-bottom: 12px;
}

.footer {
    text-align: center;
    color: #cbd5e1;
    margin-top: 24px;
    font-size: 0.92rem;
}

.footer span {
    margin: 0 10px;
}

footer {visibility: hidden;}
#MainMenu {visibility: hidden;}
header {background: transparent;}
</style>
""")

html("""
<div class="hero">
    <div class="hero-row">
        <div class="logo-compass"></div>
        <div>
            <div class="hero-title">Lodestar Veritas</div>
            <div class="hero-subtitle">
                Agentic multimodal RAG platform for financial, regulatory, and business documents.
            </div>
        </div>
    </div>

    <div class="capability-bar">
        <div class="capability">
            <div class="cap-icon">▤</div>
            <div class="cap-text"><b>Document Intelligence</b><span>Understand any document</span></div>
        </div>
        <div class="capability">
            <div class="cap-icon">⌕</div>
            <div class="cap-text"><b>Hybrid Retrieval</b><span>Dense + BM25 search</span></div>
        </div>
        <div class="capability">
            <div class="cap-icon">⇄</div>
            <div class="cap-text"><b>RRF Fusion</b><span>Smart result fusion</span></div>
        </div>
        <div class="capability">
            <div class="cap-icon purple">⤨</div>
            <div class="cap-text"><b style="color:#c084fc;">Reranking</b><span>Higher quality answers</span></div>
        </div>
        <div class="capability">
            <div class="cap-icon pink">🔗</div>
            <div class="cap-text"><b style="color:#f472b6;">Citations</b><span>Traceable & reliable</span></div>
        </div>
        <div class="capability">
            <div class="cap-icon pink">🛡</div>
            <div class="cap-text"><b style="color:#f472b6;">Verification</b><span>Fact-checked responses</span></div>
        </div>
    </div>
</div>
""")

left_col, right_col = st.columns([0.32, 0.68], gap="large")

with left_col:
    html('<div class="panel"><div class="panel-title">📁 Upload Documents</div>')

    html("""
    <div class="upload-shell">
        <div class="upload-inner">
            <div class="upload-icon">☁️⬆️</div>
            <div class="upload-title">Drag & drop files here</div>
            <div class="upload-note">or click to browse</div>
            <br>
            <div class="upload-note">
                Supports: PDF, DOCX, PPTX, TXT, MD, CSV, XLSX, PNG, JPG, JPEG<br>
                Max file size: 200MB per file
            </div>
        </div>
    </div>
    """)

    uploaded_files = st.file_uploader(
        "Upload documents",
        type=["txt", "md", "csv", "pdf", "docx", "pptx", "png", "jpg", "jpeg"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

    upload_count = len(uploaded_files) if uploaded_files else 0
    st.markdown(f"#### 📄 Uploaded Files ({upload_count})")

    if uploaded_files:
        for file in uploaded_files:
            html(f'<div class="uploaded-file">✅ {file.name}</div>')
    else:
        html('<div class="uploaded-file">📭 No files uploaded yet</div>')

    html("</div>")

    html('<div class="panel"><div class="panel-title">💬 Ask Your Document</div>')

    query = st.text_area(
        "Question",
        placeholder="Example: What increased in 2024 and what risks were mentioned?",
        height=130,
        max_chars=2000,
        label_visibility="collapsed",
    )

    run_button = st.button("🚀 Run LodeStar Veritas Agentic RAG Pipeline")
    html("</div>")

with right_col:
    html("""
    <div class="architecture">
        <div class="panel-title">🧬 Pipeline Architecture</div>
        <div class="panel-subtitle">
            End-to-end agentic RAG flow from uploaded document to verified answer.
        </div>

        <div class="pipeline-stage">
            <div class="stage-label">Ingestion & Understanding</div>
            <div class="pipeline-row">
                <div class="node"><div class="node-icon">🧠</div><div class="node-title">1. Analyze</div><div class="node-desc">Content<br>intelligence</div></div>
                <div class="arrow">→</div>
                <div class="node"><div class="node-icon">🗂️</div><div class="node-title">2. Plan Chunking</div><div class="node-desc">Adaptive<br>strategy</div></div>
                <div class="arrow">→</div>
                <div class="node"><div class="node-icon">📄</div><div class="node-title">3. Parse</div><div class="node-desc">Extract<br>content</div></div>
                <div class="arrow">→</div>
                <div class="node"><div class="node-icon">🧩</div><div class="node-title">4. Chunk</div><div class="node-desc">Smart<br>segments</div></div>
                <div class="arrow">→</div>
                <div class="node"><div class="node-icon">🏷️</div><div class="node-title">5. Metadata</div><div class="node-desc">Enrich<br>structure</div></div>
                <div class="arrow">→</div>
                <div class="node"><div class="node-icon">🕸️</div><div class="node-title">6. Embed</div><div class="node-desc">Vector<br>representation</div></div>
            </div>
        </div>

        <div class="pipeline-stage purple">
            <div class="stage-label purple">Retrieval & Ranking</div>
            <div class="pipeline-row">
                <div class="node purple"><div class="node-icon">🔍</div><div class="node-title">7. Hybrid Search</div><div class="node-desc">Dense + BM25<br>retrieval</div></div>
                <div class="arrow">→</div>
                <div class="node purple"><div class="node-icon">🔀</div><div class="node-title">8. RRF Fusion</div><div class="node-desc">Reciprocal Rank<br>Fusion</div></div>
                <div class="arrow">→</div>
                <div class="node purple"><div class="node-icon">🏆</div><div class="node-title">9. Rerank</div><div class="node-desc">Quality<br>refinement</div></div>
            </div>
        </div>

        <div class="pipeline-stage pink">
            <div class="stage-label pink">Generation & Verification</div>
            <div class="pipeline-row">
                <div class="node pink"><div class="node-icon">💬</div><div class="node-title">10. Answer</div><div class="node-desc">Generate<br>response</div></div>
                <div class="arrow">→</div>
                <div class="node pink"><div class="node-icon">🛡️</div><div class="node-title">11. Verify</div><div class="node-desc">Grounding<br>check</div></div>
            </div>
        </div>

        <div class="feedback">↔ Feedback loop improves retrieval, answer quality, and verification confidence</div>
    </div>
    """)

info1, info2, info3 = st.columns(3, gap="medium")

with info1:
    html("""
    <div class="info-card">
        <div class="panel-title">🔍 How It Works</div>
        <ol class="number-list">
            <li>Upload supported documents</li>
            <li>Agents analyze content</li>
            <li>Hybrid search finds evidence</li>
            <li>Answer is generated with citations</li>
            <li>Verification checks grounding</li>
        </ol>
        <div class="info-visual-wave"></div>
    </div>
    """)

with info2:
    html("""
    <div class="info-card">
        <div class="panel-title">✨ Key Benefits</div>
        <ul class="check-list">
            <li>Grounded and reliable answers</li>
            <li>Dense + keyword retrieval</li>
            <li>Traceable citations</li>
            <li>Multi-format support</li>
            <li>Production-ready architecture</li>
            <li>Enterprise deployment</li>
        </ul>
        <div class="info-visual-shield"></div>
    </div>
    """)

with info3:
    html("""
    <div class="info-card">
        <div class="panel-title">📊 What You Get</div>
        <ul class="check-list">
            <li>Precise answers</li>
            <li>Retrieved evidence</li>
            <li>Confidence score</li>
            <li>Verification result</li>
            <li>Source traceability</li>
        </ul>
        <div class="info-visual-chart"></div>
    </div>
    """)

html("""
<div class="footer">
    <span>⚡ Built with LangGraph-style orchestration</span>
    <span>•</span>
    <span>🧬 Hybrid Search (Dense + BM25)</span>
    <span>•</span>
    <span>🔀 RRF Fusion</span>
    <span>•</span>
    <span>🏆 Intelligent Reranking</span>
    <span>•</span>
    <span>🔗 Citations</span>
    <span>•</span>
    <span>🛡️ Answer Verification</span>
</div>
""")

if run_button:
    if not uploaded_files:
        st.error("Please upload at least one document.")
        st.stop()

    if not query.strip():
        st.error("Please enter a question.")
        st.stop()

    temp_paths = []

    with st.spinner("Saving uploaded files..."):
        for uploaded_file in uploaded_files:
            suffix = Path(uploaded_file.name).suffix
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                temp_file.write(uploaded_file.getbuffer())
                temp_paths.append(temp_file.name)

    with st.spinner("Running Lodestar Veritas intelligence pipeline..."):
        graph = LodestarGraph()
        state = graph.run(query=query, file_paths=temp_paths)

    st.markdown("---")
    html('<div class="panel-title">📌 Final Answer</div>')
    html('<div class="panel">')
    st.write(state.answer)
    html("</div>")

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric("Documents", len(uploaded_files))
    with m2:
        st.metric("Retrieved Chunks", len(state.retrieved_chunks))
    with m3:
        st.metric("Confidence", state.verification.get("confidence", 0))
    with m4:
        grounded = state.verification.get("is_grounded", False)
        st.metric("Grounded", "Yes" if grounded else "No")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["📚 Evidence", "🔗 Citations", "🛡 Verification", "🧩 Pipeline", "⚠️ Errors"]
    )

    with tab1:
        for index, chunk in enumerate(state.retrieved_chunks, start=1):
            html(f"""
            <div class="chunk-card">
                <b>Chunk {index}</b><br>
                Score: {chunk.get("score")} | Rerank: {chunk.get("rerank_score")}
            </div>
            """)
            st.write(chunk.get("text", ""))
            with st.expander("Metadata"):
                st.json(chunk.get("metadata", {}))

    with tab2:
        st.json(state.citations)

    with tab3:
        st.json(state.verification)

    with tab4:
        st.json(
            {
                "documents_processed": len(state.ingestion_results),
                "retrieved_count": len(state.retrieved_chunks),
                "sources": state.sources,
                "context_used_preview": state.context_used[:1000],
            }
        )

    with tab5:
        if state.errors:
            for error in state.errors:
                st.error(error)
        else:
            st.success("No pipeline errors.")