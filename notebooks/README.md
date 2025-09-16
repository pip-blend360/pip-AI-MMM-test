# Example: Hybrid Notebook + Functional Code Approach

## Benefits of This Approach:

### ✅ **Functional Code (`src/` modules)**
- **Reusable**: Functions can be used across multiple notebooks
- **Testable**: Unit tests can be written for each function
- **Maintainable**: Changes in one place affect all usage
- **Version Control**: Clean diffs and easy code review

### ✅ **Notebooks for Exploration**
- **Interactive**: Immediate feedback and visualization
- **Flexible**: Easy to experiment with different parameters
- **Documentation**: Self-documenting analysis process
- **Sharing**: Easy to share insights with stakeholders

## Usage Pattern:

```python
# In notebook:
from src.pip_ai_mmm_test.data.loaders import load_marketing_spend_data
from src.pip_ai_mmm_test.analysis.eda import plot_time_series

# Load data using reusable function
df = load_marketing_spend_data('data/raw/marketing_spend.csv')

# Create visualization using reusable function
fig = plot_time_series(df, 'date', ['spend'], 'Marketing Spend Over Time')
plt.show()

# Add notebook-specific analysis
df['spend_ma7'] = df['spend'].rolling(7).mean()
```

## File Structure Created:

```
src/pip_ai_mmm_test/
├── data/
│   └── loaders.py          # Pure data loading functions
└── analysis/
    └── eda.py              # Reusable EDA functions

notebooks/
└── templates/
    └── eda_template.ipynb  # Reusable notebook template
```

## Next Steps:

1. **Add your CSV data** to `data/raw/`
2. **Use the template** to create your EDA notebook
3. **Import functions** from `src/` modules
4. **Customize analysis** in notebook cells
5. **Reuse functions** across multiple notebooks

This gives you the best of both worlds: functional, maintainable code with notebook flexibility!
