import streamlit as st
import base64
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from groq import Groq

# --- Configuration de la page ---
st.set_page_config(
    page_title="Project Management",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Chemins ---
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DOC_PATH = os.path.join(ROOT_DIR, "docs")
DATA_PATH = os.path.join(ROOT_DIR, "data")
ASSETS_PATH = os.path.join(ROOT_DIR, "assets")
CSS_PATH = os.path.join(ASSETS_PATH, "style.css")

# --- Version ---
VERSION = "1.0.0"
VERSION_DATE = "Feb 2026"

# --- Dictionnaire de Traduction UI ---
TRANSLATIONS = {
    "fr": {
        "title": "Gestion de projet augmentee",
        "sidebar_title": "Gestion de projet",
        "nav_header": "Navigation",
        "gen_header": "General",
        "study_header": "Etudes",
        "annex_header": "Annexes",
        "gen_pages": ["Accueil", "Dashboard projets"],
        "study_pages": [
            "Allocation ressources",
            "Status reports IA",
        ],
        "annex_pages": ["Methodologie", "A propos"],
        # Dashboard
        "dashboard_title": "Dashboard projets",
        "metric_total": "Projets",
        "metric_on_track": "En bonne voie",
        "metric_at_risk": "A risque",
        "metric_late": "En retard",
        "metric_completed": "Termines",
        "gantt_title": "Diagramme de Gantt interactif",
        "risk_title": "Score de risque de retard",
        "risk_col_project": "Projet",
        "risk_col_score": "Score risque",
        "risk_col_progress": "Avancement",
        "risk_col_status": "Statut",
        "risk_col_responsible": "Responsable",
        "filter_status": "Filtrer par statut",
        "filter_responsible": "Filtrer par responsable",
        "filter_all": "Tous",
        "status_on_track": "En bonne voie",
        "status_at_risk": "A risque",
        "status_late": "En retard",
        "status_completed": "Termine",
        # Resources
        "resources_title": "Allocation des ressources",
        "resources_workload": "Charge par responsable",
        "resources_suggestion": "Suggestions de reallocation",
        "resources_overloaded": "Surcharge : {} projets actifs",
        "resources_available": "Disponible : {} projets actifs",
        "resources_balanced": "Charge equilibree",
        # Reports
        "reports_title": "Synthese status reports",
        "reports_generate": "GENERER LE RAPPORT",
        "reports_generating": "Generation en cours...",
        "reports_select": "Selectionner les projets",
        "reports_format": "Format du rapport",
        "reports_format_summary": "Resume executif",
        "reports_format_detailed": "Rapport detaille",
        "reports_copy": "Copier",
        # Upload
        "upload_title": "Charger des donnees projets",
        "upload_help": "Glissez votre fichier CSV ou Excel ici",
        "upload_success": "Donnees chargees avec succes",
        "upload_columns": "Colonnes attendues : project, start_date, end_date, progress, responsible, budget, status",
        "upload_use_sample": "Utiliser les donnees d'exemple",
        # About
        "about_title": "A propos",
        # Chatbot
        "chat_title": "Assistant IA",
        "chat_welcome": "Bonjour ! Je suis votre assistant pour la gestion de projet. Posez-moi vos questions sur le suivi, les risques, l'allocation des ressources ou les bonnes pratiques.",
        "chat_placeholder": "Posez votre question...",
        "chat_error": "Erreur de connexion a l'API. Verifiez votre cle API.",
        "chat_close": "Fermer",
        "chat_clear": "Effacer",
        "chat_api_missing": "Cle API manquante. Configurez GROQ_API_KEY.",
        "chat_toggle": "Assistant IA",
        # Version
        "version_info": f"""**Version {VERSION}** -- {VERSION_DATE}

**Fonctionnalites :**
- Gantt interactif avec score de risque
- Allocation des ressources
- Synthese status reports par IA
- Support bilingue FR/EN
- Assistant IA""",
        # Errors
        "data_not_found": "Donnees non trouvees",
        "no_data": "Aucune donnee chargee. Utilisez les donnees d'exemple ou chargez un fichier.",
    },
    "en": {
        "title": "Augmented project management",
        "sidebar_title": "Project Management",
        "nav_header": "Navigation",
        "gen_header": "General",
        "study_header": "Studies",
        "annex_header": "Appendices",
        "gen_pages": ["Home", "Project dashboard"],
        "study_pages": [
            "Resource allocation",
            "AI status reports",
        ],
        "annex_pages": ["Methodology", "About"],
        # Dashboard
        "dashboard_title": "Project dashboard",
        "metric_total": "Projects",
        "metric_on_track": "On track",
        "metric_at_risk": "At risk",
        "metric_late": "Late",
        "metric_completed": "Completed",
        "gantt_title": "Interactive Gantt chart",
        "risk_title": "Delay risk score",
        "risk_col_project": "Project",
        "risk_col_score": "Risk score",
        "risk_col_progress": "Progress",
        "risk_col_status": "Status",
        "risk_col_responsible": "Responsible",
        "filter_status": "Filter by status",
        "filter_responsible": "Filter by responsible",
        "filter_all": "All",
        "status_on_track": "On track",
        "status_at_risk": "At risk",
        "status_late": "Late",
        "status_completed": "Completed",
        # Resources
        "resources_title": "Resource allocation",
        "resources_workload": "Workload per responsible",
        "resources_suggestion": "Reallocation suggestions",
        "resources_overloaded": "Overloaded: {} active projects",
        "resources_available": "Available: {} active projects",
        "resources_balanced": "Balanced workload",
        # Reports
        "reports_title": "Status reports synthesis",
        "reports_generate": "GENERATE REPORT",
        "reports_generating": "Generating...",
        "reports_select": "Select projects",
        "reports_format": "Report format",
        "reports_format_summary": "Executive summary",
        "reports_format_detailed": "Detailed report",
        "reports_copy": "Copy",
        # Upload
        "upload_title": "Upload project data",
        "upload_help": "Drop your CSV or Excel file here",
        "upload_success": "Data loaded successfully",
        "upload_columns": "Expected columns: project, start_date, end_date, progress, responsible, budget, status",
        "upload_use_sample": "Use sample data",
        # About
        "about_title": "About",
        # Chatbot
        "chat_title": "AI Assistant",
        "chat_welcome": "Hello! I'm your project management assistant. Ask me about tracking, risks, resource allocation, or best practices.",
        "chat_placeholder": "Ask your question...",
        "chat_error": "API connection error. Check your API key.",
        "chat_close": "Close",
        "chat_clear": "Clear",
        "chat_api_missing": "API key missing. Configure GROQ_API_KEY.",
        "chat_toggle": "AI Assistant",
        # Version
        "version_info": f"""**Version {VERSION}** -- {VERSION_DATE}

**Features:**
- Interactive Gantt with risk score
- Resource allocation
- AI-powered status reports
- Bilingual support FR/EN
- AI assistant""",
        # Errors
        "data_not_found": "Data not found",
        "no_data": "No data loaded. Use sample data or upload a file.",
    },
}


# ─────────────────────────── Helpers ───────────────────────────


def t(key: str) -> str:
    """Retourne la traduction pour la langue courante."""
    lang = st.session_state.get("lang", "fr")
    return TRANSLATIONS.get(lang, TRANSLATIONS["fr"]).get(key, key)


@st.cache_data(ttl=3600)
def load_custom_css(path: str) -> str:
    """Charge le fichier CSS avec cache."""
    with open(path) as f:
        return f.read()


@st.cache_data(ttl=600)
def load_file_content(path: str) -> str:
    """Charge un fichier markdown avec cache."""
    with open(path, encoding="utf-8") as f:
        return f.read()


@st.cache_data(ttl=600)
def load_csv_data(path: str) -> pd.DataFrame:
    """Charge un fichier CSV avec cache."""
    return pd.read_csv(path, sep=";")


def compute_risk_score(row: pd.Series) -> float:
    """Calcule un score de risque de retard (0-100).

    Logique :
    - Temps ecoule (%) vs avancement (%) : ecart = risque
    - Budget consomme pris en compte si disponible
    """
    today = datetime.now().date()
    try:
        start = pd.to_datetime(row["start_date"]).date()
        end = pd.to_datetime(row["end_date"]).date()
    except Exception:
        return 50.0

    total_days = (end - start).days
    if total_days <= 0:
        return 0.0

    elapsed_days = (today - start).days
    elapsed_pct = min(max(elapsed_days / total_days * 100, 0), 100)
    progress = float(row.get("progress", 0))

    # Ecart temps vs avancement
    gap = elapsed_pct - progress  # positif = en retard
    risk = max(min(gap * 1.5, 100), 0)

    # Bonus si termine
    if progress >= 100:
        risk = 0.0

    return round(risk, 1)


def get_status_label(risk: float) -> str:
    """Retourne le label de statut en fonction du risque."""
    if risk == 0:
        return t("status_completed")
    elif risk < 25:
        return t("status_on_track")
    elif risk < 50:
        return t("status_at_risk")
    else:
        return t("status_late")


def get_status_color(risk: float) -> str:
    """Retourne la couleur associee au risque."""
    if risk == 0:
        return "#2ecc71"
    elif risk < 25:
        return "#27ae60"
    elif risk < 50:
        return "#f39c12"
    else:
        return "#e74c3c"


def load_sample_data() -> pd.DataFrame:
    """Charge les donnees d'exemple depuis data/sample_projects.csv."""
    path = os.path.join(DATA_PATH, "sample_projects.csv")
    if os.path.exists(path):
        df = pd.read_csv(path, sep=";")
        return df
    return pd.DataFrame()


# ─────────────────────────── CSS ───────────────────────────

try:
    css = load_custom_css(CSS_PATH)
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

# ─────────────────────────── Session State ───────────────────────────

if "lang" not in st.session_state:
    st.session_state.lang = "fr"
if "nav_gen_idx" not in st.session_state:
    st.session_state.nav_gen_idx = 0
if "nav_study_idx" not in st.session_state:
    st.session_state.nav_study_idx = None
if "nav_annex_idx" not in st.session_state:
    st.session_state.nav_annex_idx = None
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "project_data" not in st.session_state:
    st.session_state.project_data = None
if "report_text" not in st.session_state:
    st.session_state.report_text = ""


# ─────────────────────────── Navigation callbacks ───────────────────────────


def set_nav(section: str, idx: int):
    """Met a jour la navigation."""
    if section == "gen":
        st.session_state.nav_gen_idx = idx
        st.session_state.nav_study_idx = None
        st.session_state.nav_annex_idx = None
    elif section == "study":
        st.session_state.nav_gen_idx = None
        st.session_state.nav_study_idx = idx
        st.session_state.nav_annex_idx = None
    elif section == "annex":
        st.session_state.nav_gen_idx = None
        st.session_state.nav_study_idx = None
        st.session_state.nav_annex_idx = idx


# ─────────────────────────── Sidebar ───────────────────────────

with st.sidebar:
    st.title(t("sidebar_title"))
    st.markdown("---")

    # Langue
    lang_cols = st.columns(2)
    with lang_cols[0]:
        if st.button("Francais", use_container_width=True,
                      type="primary" if st.session_state.lang == "fr" else "secondary"):
            if st.session_state.lang != "fr":
                st.session_state.lang = "fr"
                st.rerun()
    with lang_cols[1]:
        if st.button("English", use_container_width=True,
                      type="primary" if st.session_state.lang == "en" else "secondary"):
            if st.session_state.lang != "en":
                st.session_state.lang = "en"
                st.rerun()

    st.markdown("---")

    # Navigation - General
    st.subheader(t("gen_header"))
    gen_pages = t("gen_pages")
    for i, page in enumerate(gen_pages):
        is_active = st.session_state.nav_gen_idx == i
        if st.button(
            f"{'▸ ' if is_active else ''}{page}",
            key=f"gen_{i}",
            use_container_width=True,
            type="primary" if is_active else "secondary",
        ):
            set_nav("gen", i)
            st.rerun()

    st.markdown("---")

    # Navigation - Etudes
    st.subheader(t("study_header"))
    study_pages = t("study_pages")
    for i, page in enumerate(study_pages):
        is_active = st.session_state.nav_study_idx == i
        if st.button(
            f"{'▸ ' if is_active else ''}{page}",
            key=f"study_{i}",
            use_container_width=True,
            type="primary" if is_active else "secondary",
        ):
            set_nav("study", i)
            st.rerun()

    st.markdown("---")

    # Navigation - Annexes
    st.subheader(t("annex_header"))
    annex_pages = t("annex_pages")
    for i, page in enumerate(annex_pages):
        is_active = st.session_state.nav_annex_idx == i
        if st.button(
            f"{'▸ ' if is_active else ''}{page}",
            key=f"annex_{i}",
            use_container_width=True,
            type="primary" if is_active else "secondary",
        ):
            set_nav("annex", i)
            st.rerun()

    st.markdown("---")

    # Upload rapide
    uploaded = st.file_uploader(
        t("upload_title"),
        type=["csv", "xlsx"],
        help=t("upload_columns"),
    )
    if uploaded is not None:
        try:
            if uploaded.name.endswith(".csv"):
                df_up = pd.read_csv(uploaded, sep=";")
            else:
                df_up = pd.read_excel(uploaded)
            st.session_state.project_data = df_up
            st.success(t("upload_success"))
        except Exception as e:
            st.error(f"{t('data_not_found')}: {str(e)[:80]}")

    if st.session_state.project_data is None:
        if st.button(t("upload_use_sample"), use_container_width=True):
            sample = load_sample_data()
            if not sample.empty:
                st.session_state.project_data = sample
                st.rerun()

    st.markdown("---")
    st.markdown(t("version_info"))
    st.caption("MIT License")

# ─────────────────────────── Chatbot (popover) ───────────────────────────

SYSTEM_PROMPT = """Tu es un assistant specialise en gestion de projet industriel.
Tu maitrises : planification (Gantt, PERT, chemin critique), gestion des risques,
allocation des ressources, methodologies (Agile, Waterfall, hybride), KPIs projet
(SPI, CPI, EAC, ETC), et reporting executif.
Reponds de maniere concise et actionnable. Utilise des listes et tableaux quand pertinent.
Langue de reponse : celle de l'utilisateur."""

try:
    api_key = st.secrets["GROQ_API_KEY"]
except (FileNotFoundError, KeyError):
    api_key = os.environ.get("GROQ_API_KEY")

with st.popover(t("chat_toggle"), use_container_width=False):
    if not api_key:
        st.warning(t("chat_api_missing"))
    else:
        # Historique
        for msg in st.session_state.chat_messages[-20:]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if not st.session_state.chat_messages:
            st.info(t("chat_welcome"))

        user_input = st.chat_input(t("chat_placeholder"))
        if user_input and api_key:
            st.session_state.chat_messages.append(
                {"role": "user", "content": user_input}
            )
            try:
                client = Groq(api_key=api_key)
                messages = [{"role": "system", "content": SYSTEM_PROMPT}]
                messages += st.session_state.chat_messages[-20:]
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages,
                    temperature=0.3,
                    max_tokens=1024,
                )
                reply = response.choices[0].message.content
                st.session_state.chat_messages.append(
                    {"role": "assistant", "content": reply}
                )
                st.rerun()
            except Exception as e:
                st.error(f"{t('chat_error')} {str(e)[:50]}")

        col_clear, _ = st.columns([1, 2])
        with col_clear:
            if st.button(t("chat_clear"), key="chat_clear_btn"):
                st.session_state.chat_messages = []
                st.rerun()


# ═══════════════════════════ PAGES ═══════════════════════════


def get_df() -> pd.DataFrame | None:
    """Retourne le DataFrame courant avec colonnes de risque calculees."""
    df = st.session_state.project_data
    if df is None or df.empty:
        return None
    if "risk_score" not in df.columns:
        df["risk_score"] = df.apply(compute_risk_score, axis=1)
        df["status_label"] = df["risk_score"].apply(get_status_label)
        df["status_color"] = df["risk_score"].apply(get_status_color)
    return df


# ─────────────────────────── Accueil ───────────────────────────


def page_home():
    """Page d'accueil."""
    lang = st.session_state.lang
    doc_path = os.path.join(DOC_PATH, lang, "accueil.md")
    st.title(t("title"))
    try:
        content = load_file_content(doc_path)
        st.markdown(content)
    except FileNotFoundError:
        st.info(t("no_data"))


# ─────────────────────────── Dashboard ───────────────────────────


def page_dashboard():
    """Dashboard projets avec Gantt et metriques."""
    st.title(t("dashboard_title"))

    df = get_df()
    if df is None:
        st.warning(t("no_data"))
        return

    # --- Filtres ---
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        statuses = [t("filter_all")] + sorted(df["status_label"].unique().tolist())
        sel_status = st.selectbox(t("filter_status"), statuses)
    with col_f2:
        responsibles = [t("filter_all")] + sorted(df["responsible"].unique().tolist())
        sel_resp = st.selectbox(t("filter_responsible"), responsibles)

    df_filtered = df.copy()
    if sel_status != t("filter_all"):
        df_filtered = df_filtered[df_filtered["status_label"] == sel_status]
    if sel_resp != t("filter_all"):
        df_filtered = df_filtered[df_filtered["responsible"] == sel_resp]

    # --- Metriques ---
    total = len(df_filtered)
    on_track = len(df_filtered[df_filtered["risk_score"] < 25])
    at_risk = len(df_filtered[(df_filtered["risk_score"] >= 25) & (df_filtered["risk_score"] < 50)])
    late = len(df_filtered[df_filtered["risk_score"] >= 50])
    completed = len(df_filtered[df_filtered["progress"] >= 100])

    cols = st.columns(5)
    cols[0].metric(t("metric_total"), total, border=True)
    cols[1].metric(t("metric_on_track"), on_track, border=True)
    cols[2].metric(t("metric_at_risk"), at_risk, border=True)
    cols[3].metric(t("metric_late"), late, border=True)
    cols[4].metric(t("metric_completed"), completed, border=True)

    st.markdown("---")

    # --- Gantt ---
    st.subheader(t("gantt_title"))
    df_gantt = df_filtered.copy()
    df_gantt["start_date"] = pd.to_datetime(df_gantt["start_date"])
    df_gantt["end_date"] = pd.to_datetime(df_gantt["end_date"])

    fig = px.timeline(
        df_gantt,
        x_start="start_date",
        x_end="end_date",
        y="project",
        color="risk_score",
        color_continuous_scale=["#27ae60", "#f39c12", "#e74c3c"],
        range_color=[0, 100],
        hover_data=["responsible", "progress", "risk_score"],
    )
    fig.update_layout(
        yaxis_title="",
        xaxis_title="",
        coloraxis_colorbar_title="Risque",
        height=max(300, len(df_gantt) * 45),
        margin=dict(l=10, r=10, t=10, b=10),
    )
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # --- Tableau de risque ---
    st.subheader(t("risk_title"))
    risk_cols = ["project", "responsible", "progress", "risk_score", "status_label"]
    display_names = {
        "project": t("risk_col_project"),
        "responsible": t("risk_col_responsible"),
        "progress": t("risk_col_progress"),
        "risk_score": t("risk_col_score"),
        "status_label": t("risk_col_status"),
    }
    df_risk = df_filtered[risk_cols].rename(columns=display_names)
    df_risk = df_risk.sort_values(
        by=t("risk_col_score"), ascending=False
    )

    st.dataframe(
        df_risk,
        use_container_width=True,
        hide_index=True,
        column_config={
            t("risk_col_score"): st.column_config.ProgressColumn(
                min_value=0,
                max_value=100,
                format="%.0f",
            ),
            t("risk_col_progress"): st.column_config.ProgressColumn(
                min_value=0,
                max_value=100,
                format="%.0f %%",
            ),
        },
    )

    # --- Download CSV ---
    csv_data = df_filtered.to_csv(index=False, sep=";")
    st.download_button(
        "Download CSV",
        data=csv_data,
        file_name="project_status.csv",
        mime="text/csv",
    )


# ─────────────────────────── Ressources ───────────────────────────


def page_resources():
    """Allocation des ressources."""
    st.title(t("resources_title"))

    df = get_df()
    if df is None:
        st.warning(t("no_data"))
        return

    # Projets actifs (non termines)
    df_active = df[df["progress"] < 100].copy()

    # --- Charge par responsable ---
    st.subheader(t("resources_workload"))
    workload = (
        df_active.groupby("responsible")
        .agg(
            projects=("project", "count"),
            avg_risk=("risk_score", "mean"),
            total_progress=("progress", "mean"),
        )
        .reset_index()
        .sort_values("projects", ascending=False)
    )

    fig_bar = px.bar(
        workload,
        x="responsible",
        y="projects",
        color="avg_risk",
        color_continuous_scale=["#27ae60", "#f39c12", "#e74c3c"],
        range_color=[0, 100],
        text="projects",
    )
    fig_bar.update_layout(
        xaxis_title="",
        yaxis_title="",
        coloraxis_colorbar_title="Risque moyen",
        height=350,
        margin=dict(l=10, r=10, t=10, b=10),
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")

    # --- Suggestions reallocation ---
    st.subheader(t("resources_suggestion"))
    avg_projects = workload["projects"].mean() if len(workload) > 0 else 0
    threshold_high = avg_projects * 1.4
    threshold_low = avg_projects * 0.6

    for _, row in workload.iterrows():
        name = row["responsible"]
        n = int(row["projects"])
        risk = row["avg_risk"]

        if n > threshold_high or risk > 50:
            st.error(f"**{name}** -- {t('resources_overloaded').format(n)} (risque moyen: {risk:.0f})")
        elif n < threshold_low:
            st.success(f"**{name}** -- {t('resources_available').format(n)}")
        else:
            st.info(f"**{name}** -- {t('resources_balanced')} ({n} projets, risque: {risk:.0f})")

    st.markdown("---")

    # --- Detail par responsable ---
    for resp in workload["responsible"].tolist():
        with st.expander(f"{resp}"):
            df_resp = df_active[df_active["responsible"] == resp][
                ["project", "progress", "risk_score", "status_label"]
            ]
            st.dataframe(df_resp, hide_index=True, use_container_width=True)


# ─────────────────────────── Status Reports ───────────────────────────


def page_reports():
    """Generation de status reports par LLM."""
    st.title(t("reports_title"))

    df = get_df()
    if df is None:
        st.warning(t("no_data"))
        return

    if not api_key:
        st.warning(t("chat_api_missing"))
        return

    # Selection projets
    projects = df["project"].tolist()
    selected = st.multiselect(t("reports_select"), projects, default=projects)

    col1, col2 = st.columns([1, 2])
    with col1:
        fmt = st.radio(
            t("reports_format"),
            [t("reports_format_summary"), t("reports_format_detailed")],
            horizontal=True,
        )

    if st.button(t("reports_generate"), type="primary", use_container_width=True):
        df_sel = df[df["project"].isin(selected)]
        data_summary = df_sel[
            ["project", "responsible", "progress", "risk_score", "status_label", "start_date", "end_date"]
        ].to_string(index=False)

        lang_label = "francais" if st.session_state.lang == "fr" else "anglais"
        is_detailed = fmt == t("reports_format_detailed")
        detail_instruction = (
            "Fais un rapport detaille avec analyse des risques, recommandations d'actions correctives, "
            "et priorisation."
            if is_detailed
            else "Fais un resume executif concis (10-15 lignes max)."
        )

        prompt = f"""Voici les donnees de suivi projet :

{data_summary}

{detail_instruction}

Langue de reponse : {lang_label}.
Structure avec titres markdown, listes, et tableaux si pertinent.
Mentionne les projets a risque en priorite avec des actions concretes."""

        with st.status(t("reports_generating"), expanded=True) as status:
            try:
                client = Groq(api_key=api_key)
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.3,
                    max_tokens=2048,
                )
                report = response.choices[0].message.content
                st.session_state.report_text = report
                status.update(label="OK", state="complete")
            except Exception as e:
                st.error(f"{t('chat_error')} {str(e)[:80]}")

    # Affichage rapport
    if st.session_state.report_text:
        st.markdown("---")
        st.markdown(st.session_state.report_text)
        st.download_button(
            "Download report (.md)",
            data=st.session_state.report_text,
            file_name="status_report.md",
            mime="text/markdown",
        )


# ─────────────────────────── Methodologie ───────────────────────────


def page_methodology():
    """Page methodologie."""
    lang = st.session_state.lang
    doc_path = os.path.join(DOC_PATH, lang, "methodology.md")
    try:
        content = load_file_content(doc_path)
        st.markdown(content)
    except FileNotFoundError:
        st.info(t("data_not_found"))


# ─────────────────────────── A propos ───────────────────────────


def page_about():
    """Page a propos."""
    lang = st.session_state.lang
    doc_path = os.path.join(DOC_PATH, lang, "about.md")
    st.title(t("about_title"))
    try:
        content = load_file_content(doc_path)
        st.markdown(content)
    except FileNotFoundError:
        st.markdown(f"""
### {t("about_title")}

{t("title")}

- Gantt interactif (Plotly)
- Score de risque automatique
- Allocation des ressources
- Synthese IA (Groq / LLaMA 3.3)
- Bilingue FR/EN

**Version** : {VERSION} ({VERSION_DATE})

MIT License
""")


# ═══════════════════════════ ROUTING ═══════════════════════════

if st.session_state.nav_gen_idx == 0:
    page_home()
elif st.session_state.nav_gen_idx == 1:
    page_dashboard()
elif st.session_state.nav_study_idx == 0:
    page_resources()
elif st.session_state.nav_study_idx == 1:
    page_reports()
elif st.session_state.nav_annex_idx == 0:
    page_methodology()
elif st.session_state.nav_annex_idx == 1:
    page_about()
else:
    page_home()
