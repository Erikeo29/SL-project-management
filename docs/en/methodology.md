# Methodology

## Risk score calculation

The delay risk score is automatically computed for each project using the formula:

$$\text{risk} = \min\left(\max\left((\text{elapsed time \%} - \text{progress \%}) \times 1.5,\ 0\right),\ 100\right)$$

Where:
- **Elapsed time (%)**: proportion of total project duration already elapsed at today's date
- **Progress (%)**: declared project progress

### Interpretation

| Score | Status | Meaning |
|-------|--------|---------|
| 0 | Completed | Project at 100% progress |
| 1-24 | On track | Progress matches or exceeds schedule |
| 25-49 | At risk | Significant delay vs. schedule |
| 50-100 | Late | Critical delay requiring immediate action |

### Limitations

- The score is based solely on the time/progress ratio and does not account for remaining complexity
- Progress is declarative: it depends on reporting quality
- Budget is not integrated into the risk calculation (improvement track)

---

## Reallocation suggestions

Overload detection uses a threshold of **1.4x the average** number of projects per responsible. A responsible is considered:
- **Overloaded**: project count > 1.4x average, or average risk > 50
- **Available**: project count < 0.6x average
- **Balanced**: between both thresholds

---

## AI report generation

Reports are generated via the Groq API (LLaMA 3.3 70B model). The prompt includes:
- Tracking data for all selected projects
- Desired format (executive summary or detailed report)
- Response language

Detailed reports include risk analysis, corrective action recommendations, and prioritization.
