# Augmented project management

Project tracking and steering application with AI assistance.

---

## Features

### 1. Project dashboard
- **Interactive Gantt chart** with color coding by risk level
- **Automatic risk score** computed in real-time (elapsed time vs progress gap)
- **Key metrics**: on track, at risk, late, completed projects
- **Filters** by status and responsible

### 2. Resource allocation
- **Workload per responsible**: active project count and average risk
- **Reallocation suggestions**: automatic detection of overloads and availability
- **Detail** per responsible with assigned project list

### 3. AI status reports synthesis
- **Automatic generation** of status reports via LLM (LLaMA 3.3)
- **Two formats**: executive summary (concise) or detailed report (risk analysis, recommendations)
- **Export** to markdown

### 4. AI assistant
- Chatbot specialized in project management (Gantt, PERT, critical path, KPIs)
- Accessible via the red button at the bottom of the page

---

## Quick start

1. **Load data**: use the "Use sample data" button in the sidebar, or upload your own CSV/Excel file
2. **Explore the dashboard**: view the Gantt chart and metrics
3. **Analyze resources**: identify overloads
4. **Generate a report**: get an AI synthesis of project status

### Expected CSV format

Separator: semicolon (`;`)

| Column | Type | Description |
|--------|------|-------------|
| project | text | Project name |
| start_date | date (YYYY-MM-DD) | Start date |
| end_date | date (YYYY-MM-DD) | Planned end date |
| progress | number (0-100) | Progress in % |
| responsible | text | Project responsible |
| budget | number | Budget in euros |
