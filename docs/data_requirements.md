# Data Requirements Checklist for MMM Project

## Required Data Files

### 1. Marketing Spend Data (`data/raw/marketing_spend.csv`)

**Required Columns:**
- `date` - Date of spend (daily/weekly/monthly)
- `channel` - Marketing channel (TV, Digital, Print, Radio, Events, etc.)
- `spend` - Spend amount in USD

**Optional Columns:**
- `region` - Geographic region
- `product` - Product/brand
- `campaign_type` - Type of campaign
- `target_audience` - Target audience segment

**Data Quality Requirements:**
- ✅ 24+ months of historical data
- ✅ Maximum 5% missing values per channel
- ✅ Consistent date format
- ✅ Valid currency amounts
- ✅ Complete channel coverage

### 2. Business Performance Data (`data/raw/business_metrics.csv`)

**Required Columns:**
- `date` - Date of metrics (should match spend data)
- `revenue` - Sales revenue in USD

**Optional Columns:**
- `prescriptions` - Prescription volume
- `market_share` - Market share percentage
- `brand_awareness` - Brand awareness scores
- `customer_acquisition_cost` - CAC metrics
- `customer_lifetime_value` - CLV metrics

**Data Quality Requirements:**
- ✅ Same date range as spend data
- ✅ Maximum 5% missing values
- ✅ Consistent currency and units
- ✅ Validated against financial records

### 3. External Factors Data (`data/raw/external_factors.csv`) - Optional

**Potential Columns:**
- `date` - Date
- `competitor_spend` - Estimated competitor spend
- `seasonal_factor` - Seasonal adjustment factor
- `economic_indicator` - Economic indicators
- `regulatory_change` - Regulatory impact scores

## Data Validation Checklist

### Marketing Spend Data
- [ ] Date column is datetime format
- [ ] Channel names are consistent
- [ ] Spend amounts are positive numbers
- [ ] No duplicate rows for same date/channel
- [ ] Date range covers required period
- [ ] All required channels present

### Business Metrics Data
- [ ] Date column matches spend data
- [ ] Revenue amounts are positive numbers
- [ ] No missing values in critical periods
- [ ] Metrics align with business cycles
- [ ] Data quality validated against sources

### Data Integration
- [ ] Date ranges overlap between datasets
- [ ] Same date granularity (daily/weekly/monthly)
- [ ] Consistent time zones
- [ ] No data gaps in critical periods

## Next Steps After Data Validation

1. **Feature Engineering**
   - Create lag features for marketing spend
   - Add seasonality indicators
   - Calculate rolling averages
   - Create interaction terms

2. **Model Development**
   - Set up Bayesian MMM framework
   - Define saturation curves
   - Implement adstock effects
   - Add hierarchical structure

3. **Validation**
   - Cross-validation setup
   - Holdout testing
   - Business validation
   - Sensitivity analysis

## Sample Data Structure

If you don't have real data yet, we can create sample data for testing:

```python
# Run this to create sample data
python scripts/test_data_pipeline.py
```

This will create sample marketing spend and business metrics data that follows the required structure.
