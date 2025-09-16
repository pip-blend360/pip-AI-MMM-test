# pip-AI-MMM-test

A Python Marketing Mix Modeling (MMM) project, structured for functional programming best practices.

## Structure
- src/: functional core modules
- data/: datasets (ignored in git)
- notebooks/: exploratory work
- scripts/: CLI entry points
- tests/: unit tests
- reports/: generated figures and reports

## Documentation
- **Development Log**: `DEVELOPMENT.md` - Chronological development history
- **Project Context**: `PROJECT_CONTEXT.md` - Current state and ongoing context
- **Architecture Decisions**: `docs/decisions/` - Major technical decisions
- **Requirements**: `docs/requirements/MMM_Requirements_v1.md` - Comprehensive MMM requirements for drug manufacturer
- **Project Docs**: `docs/` - Detailed documentation

## Getting Started
1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd pip-AI-MMM-test
   ```

2. **Set up Python environment**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run data transformation**
   ```bash
   python scripts/run_data_transformation.py
   ```

4. **Launch Interactive Dashboard** 🎯
   ```bash
   # Option 1: Python launcher (recommended)
   python scripts/launch_dashboard.py
   
   # Option 2: Windows batch file
   launch_dashboard.bat
   
   # Option 3: Direct Streamlit command
   streamlit run scripts/eda_dashboard.py
   ```
   
   The dashboard will open at: **http://localhost:8501**

5. **Review project context**
   - Read `PROJECT_CONTEXT.md` for current development state
   - Check `DEVELOPMENT.md` for development history

## 📊 Interactive EDA Dashboard

The project includes a comprehensive Streamlit dashboard for exploring MMM data:

### **Dashboard Features:**
- **🎛️ Interactive Controls**: Select channels and DMAs dynamically
- **📈 Time Series Visualization**: Plot spend patterns over time
- **🎨 XKCD Style Plots**: Toggle hand-drawn, comic-style visualizations
- **📊 Key Metrics**: Real-time calculation of spend statistics
- **🔄 Channel Comparison**: Side-by-side comparison of all channels
- **📋 Data Summary**: Comprehensive data quality and range information

### **Available Channels:**
- Display_HCP, Display_DTC, Paid_Search_HCP
- Meetings, TeleDetails, Emails

### **Data Views:**
- **Channel Level**: Individual channel spend data
- **Aggregated Level**: Total spend and business metrics
- **DMA Selection**: Choose specific DMAs or National view

### **Usage:**
Launch the dashboard and explore your data interactively. Perfect for:
- Understanding spend patterns across channels and geographies
- Identifying seasonal trends and anomalies
- Validating data quality and completeness
- Presenting findings with engaging XKCD-style plots

## AI-Assisted Development Setup

### For New Developers Starting an AI Session

When starting a new AI-assisted development session, follow these steps to initialize the AI with complete project context:

#### 1. **Context Initialization Prompt**
Copy and paste this prompt to initialize your AI session:

```
I'm starting a new AI-assisted development session for the pip-AI-MMM-test project. Please read and understand the project context by reviewing these key files:

1. PROJECT_CONTEXT.md - Current project state and decisions
2. DEVELOPMENT.md - Development history and key decisions  
3. docs/requirements/MMM_Requirements_v1.md - Complete requirements document
4. docs/decisions/README.md - Architecture Decision Records (ADRs)
5. src/pip_ai_mmm_test/analysis/eda.py - EDA functions with XKCD plotting
6. notebooks/templates/eda_template.ipynb - Notebook template with examples

Key project details:
- Drug manufacturer Marketing Mix Modeling (MMM) project
- Functional programming approach with hybrid notebook + code pattern
- Bayesian MMM with hierarchical structure
- XKCD style plotting for presentations
- FDA/EMA compliance requirements

Please confirm you understand the project context and are ready to assist with development.
```

#### 2. **Essential Context Files to Review**
The AI should understand these key aspects:

**Project Overview:**
- Drug manufacturer MMM project using functional programming
- Hybrid approach: functional code (`src/`) + interactive notebooks
- Bayesian modeling with PyMC/Stan framework
- Pharmaceutical compliance requirements (FDA/EMA)

**Current Architecture:**
- `src/pip_ai_mmm_test/data/loaders.py` - Data loading utilities
- `src/pip_ai_mmm_test/analysis/eda.py` - EDA functions with XKCD support
- `notebooks/templates/eda_template.ipynb` - Standardized analysis template
- `data/raw/` → `data/interim/` → `data/processed/` pipeline

**Key Features:**
- XKCD style plotting (`xkcd_style=True` parameter)
- Global style control (`enable_xkcd_style()`)
- Fun annotations and hand-drawn appearance
- Perfect for stakeholder presentations

#### 3. **Development Workflow**
The AI should understand our development pattern:

**Functional Code First:**
- Create pure, testable functions in `src/` modules
- Import functions into notebooks for interactive use
- Maintain separation between logic and visualization

**Notebook Usage:**
- Use `notebooks/templates/eda_template.ipynb` as starting point
- Import functions from `src/` modules
- Choose normal or XKCD style based on audience

**Documentation:**
- Update `PROJECT_CONTEXT.md` for current state
- Add entries to `DEVELOPMENT.md` for major changes
- Create ADRs in `docs/decisions/` for architectural decisions

#### 4. **Current Project State**
As of latest update:
- ✅ Project structure and git setup complete
- ✅ Requirements document created
- ✅ Hybrid development approach implemented
- ✅ XKCD plotting capabilities added
- ⏳ Ready for data loading and model development

**Next Immediate Tasks:**
1. Add CSV data to `data/raw/`
2. Test data loading utilities with real data
3. Create feature engineering pipeline
4. Design MMM model architecture
5. Implement Bayesian modeling framework

#### 5. **AI Session Best Practices**
- **Start with context**: Always initialize with the prompt above
- **Reference decisions**: Check ADRs before making architectural changes
- **Update documentation**: Keep context files current
- **Follow patterns**: Use established functional + notebook approach
- **Test functions**: Write unit tests for new functions in `src/`

#### 6. **Quick Reference Commands**
```bash
# Check current project state
cat PROJECT_CONTEXT.md

# Review development history
cat DEVELOPMENT.md

# See all available EDA functions
python -c "from src.pip_ai_mmm_test.analysis.eda import *; help(plot_time_series)"

# Run XKCD demo
python scripts/demo_xkcd_plots.py

# Start new notebook from template
cp notebooks/templates/eda_template.ipynb notebooks/my_analysis.ipynb
```

This setup ensures the AI has complete context and can provide informed assistance throughout the development process. 
