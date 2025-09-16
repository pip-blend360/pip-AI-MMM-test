# Architecture Decision Records (ADRs)

## ADR-001: Project Structure and Organization

**Date:** 2025-01-16  
**Status:** Accepted  
**Context:** Setting up initial project structure for Python MMM project

### Decision
Adopt functional programming approach with clear separation of concerns:
- `src/pip_ai_mmm_test/`: Core functional modules
- `data/`: Organized data pipeline
- `notebooks/`: Exploratory analysis
- `scripts/`: CLI entry points
- `tests/`: Unit tests

### Rationale
- **Maintainability**: Clear module boundaries
- **Testability**: Functional approach enables easier unit testing
- **Scalability**: Modular structure supports growth
- **Reproducibility**: Standard data science organization

### Consequences
- **Positive**: Clean code organization, easier collaboration
- **Negative**: Slightly more complex initial setup
- **Mitigation**: Comprehensive documentation and examples

---

## ADR-002: Data Pipeline Organization

**Date:** 2025-01-16  
**Status:** Accepted  
**Context:** Organizing data flow for MMM project

### Decision
Implement standard data science pipeline:
```
data/raw/ → data/interim/ → data/processed/
```

### Rationale
- **Data Lineage**: Clear traceability from raw to processed
- **Reproducibility**: Standardized data flow
- **Collaboration**: Team members understand data organization
- **Version Control**: Raw data preserved, processed data reproducible

### Consequences
- **Positive**: Clear data flow, reproducible analysis
- **Negative**: Additional directory management
- **Mitigation**: Automated scripts for data movement

---

## ADR-003: Hybrid Development Approach

**Date:** 2025-01-16  
**Status:** Accepted  
**Context:** Balancing functional programming with notebook flexibility

### Decision
Combine functional code modules with interactive notebooks:
- **Functional Code**: Pure functions in `src/` modules
- **Notebooks**: Interactive exploration and visualization
- **Templates**: Standardized notebook structures
- **Import Pattern**: Notebooks import and use functions from `src/`

### Rationale
- **Reusability**: Functions can be used across multiple notebooks
- **Testability**: Unit tests can be written for each function
- **Flexibility**: Notebooks provide interactive exploration
- **Consistency**: Standardized functions ensure consistent analysis

### Consequences
- **Positive**: Best of both worlds, maintainable and flexible
- **Negative**: Requires discipline to keep functions pure
- **Mitigation**: Clear documentation and examples

---

## ADR-004: XKCD Style Plotting

**Date:** 2025-01-16  
**Status:** Accepted  
**Context:** Making presentations more engaging for stakeholders

### Decision
Add hand-drawn XKCD style plotting capabilities:
- **Individual Control**: `xkcd_style=True` parameter for each plot
- **Global Control**: `enable_xkcd_style()` for all subsequent plots
- **Fun Annotations**: Engaging callouts and annotations
- **XKCD Colors**: Hand-drawn color palette

### Rationale
- **Engagement**: More memorable and approachable visualizations
- **Presentations**: Perfect for stakeholder reports and dashboards
- **Flexibility**: Can choose normal or XKCD style per plot
- **Professional**: Maintains data accuracy while improving aesthetics

### Consequences
- **Positive**: More engaging presentations, better stakeholder buy-in
- **Negative**: Additional complexity in plotting functions
- **Mitigation**: Clear documentation and examples
