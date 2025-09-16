# HCP-Level Data Analysis and MMM Transformation Plan

## Data Structure Analysis

Based on the `Mock_HCPlevel.csv` file, here's what we have:

### **📊 Dataset Overview**
- **Level**: HCP (Healthcare Professional) level
- **Granularity**: Monthly data
- **Geographic**: DMA-level aggregation
- **Time Period**: 2020-10 to 2021-06 (based on sample data)
- **Records**: ~7,588 rows (HCP-month combinations)

### **📋 Column Structure**
```
HCP_ID, DMA_Code, zip_code, month, TRX, NRX, PDE, Total_meetings, 
TeleDetails, SPEND_display_hcp, IMPRESSIONS_display_hcp, CLICKS_display_hcp,
SPEND_display_dtc, IMPRESSIONS_display_dtc, CLICKS_display_dtc,
COST_paidsearch_hcp_google, IMPRESSIONS_paidsearch_hcp_google, CLICKS_paidsearch_hcp_google,
ZELAPAR-SELEGILINE_trx, total emails, spec_GROUP
```

## MMM Component Identification

### **🎯 Essential Components**

**Date Column:**
- `month` - Monthly period (YYYYMM format)

**Geographic Column:**
- `DMA_Code` - Designated Market Area code

**HCP Identifier:**
- `HCP_ID` - Unique healthcare professional identifier

**Marketing Spend Channels:**
1. **Display_HCP** - `SPEND_display_hcp` (HCP-targeted display advertising)
2. **Display_DTC** - `SPEND_display_dtc` (Direct-to-consumer display)
3. **Paid_Search_HCP** - `COST_paidsearch_hcp_google` (HCP-targeted paid search)
4. **Meetings** - `Total_meetings` (Face-to-face meetings)
5. **TeleDetails** - `TeleDetails` (Telephone detailing)
6. **Emails** - `total emails` (Email marketing)

**Business Metrics:**
1. **TRX** - Total prescriptions
2. **NRX** - New prescriptions  
3. **PDE** - Prescription drug events
4. **ZELAPAR-SELEGILINE_trx** - Product-specific prescriptions

**Additional Metrics:**
- **Impressions** - For display and paid search channels
- **Clicks** - For display and paid search channels
- **Specialty Group** - `spec_GROUP` (e.g., PSY for psychiatry)

## MMM Transformation Plan

### **🔄 Step 1: Data Aggregation**

**DMA-Level Aggregation:**
```python
dma_agg = df.groupby(['DMA_Code', 'month']).agg({
    # Marketing spend
    'SPEND_display_hcp': 'sum',
    'SPEND_display_dtc': 'sum', 
    'COST_paidsearch_hcp_google': 'sum',
    'Total_meetings': 'sum',
    'TeleDetails': 'sum',
    'total emails': 'sum',
    
    # Business metrics
    'TRX': 'sum',
    'NRX': 'sum',
    'PDE': 'sum',
    'ZELAPAR-SELEGILINE_trx': 'sum',
    
    # HCP count
    'HCP_ID': 'nunique'
})
```

**National-Level Aggregation:**
```python
national_agg = df.groupby('month').agg({
    # Same aggregation as DMA but without DMA_Code
})
```

### **🔄 Step 2: Channel Restructuring**

**Create Channel-Level Data:**
```python
channels = ['display_hcp', 'display_dtc', 'paidsearch_hcp', 'meetings', 'teledetails', 'emails']

channel_data = []
for _, row in dma_agg.iterrows():
    for channel in channels:
        channel_data.append({
            'date': row['month'],
            'DMA_Code': row['DMA_Code'],
            'channel': channel,
            'spend': row[f'spend_{channel}'],
            'impressions': row[f'impressions_{channel}'],
            'clicks': row[f'clicks_{channel}']
        })
```

### **🔄 Step 3: Feature Engineering**

**Lag Effects (Adstock):**
- 1-month lag for display channels
- 2-month lag for meetings/teleDetails
- 3-month lag for paid search

**Seasonality:**
- Monthly seasonality indicators
- Quarterly patterns
- Holiday effects

**Saturation Curves:**
- Hill transformation for diminishing returns
- Channel-specific saturation parameters

## MMM Model Architecture

### **🏗️ Bayesian MMM Structure**

**Base Model:**
```python
# Revenue = f(Marketing Channels) + Seasonality + Trend + Noise

revenue ~ Normal(μ, σ)

μ = (
    # Channel effects with saturation
    β_display_hcp * Hill(display_hcp_spend, α_display_hcp, γ_display_hcp) +
    β_display_dtc * Hill(display_dtc_spend, α_display_dtc, γ_display_dtc) +
    β_paidsearch * Hill(paidsearch_spend, α_paidsearch, γ_paidsearch) +
    β_meetings * Hill(meetings_spend, α_meetings, γ_meetings) +
    β_teledetails * Hill(teledetails_spend, α_teledetails, γ_teledetails) +
    
    # Seasonality
    seasonality_component +
    
    # Trend
    trend_component +
    
    # Intercept
    α
)
```

**Hierarchical Structure:**
- DMA-level random effects
- Channel-specific parameters
- Time-varying effects

### **📊 Model Components**

**Saturation Curves:**
```python
def hill_transformation(spend, alpha, gamma):
    return (spend**gamma) / (alpha**gamma + spend**gamma)
```

**Adstock Effects:**
```python
def adstock_transformation(spend, lambda_param):
    # Exponential decay
    return spend * exp(-lambda_param * lag)
```

**Seasonality:**
```python
def fourier_seasonality(date, n_harmonics=6):
    # Fourier decomposition for seasonality
    pass
```

## Implementation Steps

### **🎯 Phase 1: Data Preparation**
1. ✅ Load HCP-level data
2. 🔄 Aggregate to DMA/month level
3. 🔄 Create channel-level datasets
4. 🔄 Validate data quality
5. 🔄 Save processed data

### **🎯 Phase 2: Feature Engineering**
1. 🔄 Create lag features (adstock)
2. 🔄 Add seasonality indicators
3. 🔄 Calculate saturation curves
4. 🔄 Create interaction terms
5. 🔄 Handle missing values

### **🎯 Phase 3: Model Development**
1. 🔄 Set up Bayesian framework (PyMC/Stan)
2. 🔄 Define hierarchical structure
3. 🔄 Implement channel effects
4. 🔄 Add seasonality and trend
5. 🔄 Train model

### **🎯 Phase 4: Validation & Optimization**
1. 🔄 Cross-validation
2. 🔄 Business validation
3. 🔄 Sensitivity analysis
4. 🔄 Budget optimization
5. 🔄 Scenario simulation

## Expected Outcomes

### **📈 Model Performance Targets**
- **R²**: ≥0.80 on training data
- **MAPE**: ≤15% for revenue predictions
- **Cross-validation**: ≥0.75 R² on holdout data

### **💰 Business Impact**
- **ROI Optimization**: 10-15% improvement in marketing ROI
- **Budget Allocation**: Data-driven spend recommendations
- **Scenario Planning**: What-if analysis capabilities

### **🎯 Deliverables**
1. **Trained MMM Model** - Bayesian model with channel effects
2. **Optimization Engine** - Budget allocation recommendations
3. **Simulation Platform** - Scenario planning capabilities
4. **Validation Report** - Model performance and business validation
5. **Implementation Guide** - How to use and maintain the model

## Next Immediate Actions

1. **🔧 Set up Python environment** - Install required packages
2. **📊 Run data transformation** - Create aggregated datasets
3. **🔍 Exploratory analysis** - Understand data patterns
4. **🏗️ Model architecture** - Design Bayesian MMM structure
5. **📈 Implementation** - Build and train the model

This HCP-level data is excellent for MMM modeling - it has all the essential components needed for a robust marketing mix model!
