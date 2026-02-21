# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run locally
streamlit run app.py

# Install dependencies
pip install -r requirements.txt

# Deploy (auto-deploys on push)
git add . && git commit -m "message" && git push origin main
```

## Architecture

### Overview

Streamlit application for augmented project management with AI-powered insights:
- Interactive Gantt chart with automatic delay risk scoring
- Resource allocation analysis with overload detection
- AI-generated status reports (Groq / LLaMA 3.3)
- Bilingual FR/EN support

### File Structure

```
app.py              # Single-file application (~500 lines)
assets/
  style.css         # Custom CSS (palette #004b87)
data/
  sample_projects.csv  # Sample project data (semicolon-separated)
docs/
  fr/               # French documentation
    accueil.md      # Home page content
    methodology.md  # Risk scoring methodology
    about.md        # About page
  en/               # English documentation (mirror of fr/)
.streamlit/
  config.toml       # Theme and server config
```

### Key Patterns

**Risk Score Calculation** (`compute_risk_score()`):
- Compares elapsed time % vs declared progress %
- Score = (elapsed% - progress%) * 1.5, clamped to [0, 100]
- 0 = completed, <25 = on track, 25-49 = at risk, 50+ = late

**Navigation** (sidebar radio buttons with index-based routing):
- 3 sections: General (Home, Dashboard), Studies (Resources, Reports), Annexes (Methodology, About)
- Callbacks `set_nav()` manage mutual exclusion between sections

**CSV Format**:
- Semicolon separator (`;`)
- Columns: project, start_date, end_date, progress, responsible, budget

**Bilingual Support**:
- TRANSLATIONS dict with FR/EN keys
- `t(key)` function returns translated string
- Language selector in sidebar (two buttons)

**Chatbot** (Groq API):
- System prompt specialized in project management (Gantt, PERT, KPIs)
- History limited to 20 messages
- Popover-based UI

## Common Tasks

### Adding New Sample Projects

Edit `data/sample_projects.csv`:
```csv
New Project;2026-03-01;2026-06-30;0;Responsible;25000
```

### Modifying Risk Thresholds

In `app.py`, function `get_status_label()`:
- `risk < 25` = on track
- `risk < 50` = at risk
- `risk >= 50` = late

### Editing Documentation

1. Edit markdown in `docs/fr/` and `docs/en/`
2. Use KaTeX-compatible LaTeX for equations
3. Changes appear on next load (600s cache TTL)

## Deployment

- Target: Streamlit Community Cloud
- Dependencies: streamlit, pandas, plotly, groq, openpyxl
- Secrets: `GROQ_API_KEY` in `.streamlit/secrets.toml`
