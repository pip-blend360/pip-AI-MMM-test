#!/usr/bin/env python3
"""
HCP-Level Data Analysis Script

This script analyzes the Mock_HCPlevel.csv data and Column Descriptions.xlsx
to understand the data structure for MMM modeling.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import matplotlib.pyplot as plt

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from pip_ai_mmm_test.data.loaders import (
    validate_data_quality,
    get_data_summary
)

from pip_ai_mmm_test.analysis.eda import (
    plot_time_series,
    plot_channel_spend_distribution,
    plot_missing_data_patterns,
    plot_correlation_heatmap
)


def load_hcp_data():
    """Load and examine the HCP-level data."""
    print("🔍 Loading HCP-Level Data")
    print("=" * 50)
    
    # Load the main data file
    data_file = Path("data/raw/Mock_HCPlevel.csv")
    print(f"📊 Loading data from: {data_file}")
    
    try:
        # Load CSV data
        df = pd.read_csv(data_file)
        print(f"✅ Data loaded successfully!")
        print(f"   Shape: {df.shape}")
        print(f"   Columns: {list(df.columns)}")
        
        return df
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None


def load_column_descriptions():
    """Load and examine the column descriptions."""
    print(f"\n📋 Loading Column Descriptions")
    print("=" * 50)
    
    # Load the Excel file with column descriptions
    desc_file = Path("data/raw/Column Desriptions.xlsx")
    print(f"📖 Loading descriptions from: {desc_file}")
    
    try:
        # Load Excel file
        desc_df = pd.read_excel(desc_file)
        print(f"✅ Column descriptions loaded successfully!")
        print(f"   Shape: {desc_df.shape}")
        print(f"   Columns: {list(desc_df.columns)}")
        
        # Display the descriptions
        print(f"\n📝 Column Descriptions:")
        for idx, row in desc_df.iterrows():
            print(f"   {row.iloc[0]}: {row.iloc[1] if len(row) > 1 else 'No description'}")
        
        return desc_df
        
    except Exception as e:
        print(f"❌ Error loading descriptions: {e}")
        return None


def analyze_data_structure(df):
    """Analyze the structure of the HCP data."""
    print(f"\n🔍 Data Structure Analysis")
    print("=" * 50)
    
    # Basic info
    print(f"📊 Dataset Overview:")
    print(f"   Total rows: {len(df):,}")
    print(f"   Total columns: {len(df.columns)}")
    print(f"   Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    # Data types
    print(f"\n📋 Data Types:")
    dtype_counts = df.dtypes.value_counts()
    for dtype, count in dtype_counts.items():
        print(f"   {dtype}: {count} columns")
    
    # Missing values
    print(f"\n❓ Missing Values:")
    missing_data = df.isnull().sum()
    missing_pct = (missing_data / len(df)) * 100
    
    for col in df.columns:
        if missing_data[col] > 0:
            print(f"   {col}: {missing_data[col]:,} ({missing_pct[col]:.1f}%)")
    
    # Unique values per column
    print(f"\n🔢 Unique Values per Column:")
    for col in df.columns:
        unique_count = df[col].nunique()
        print(f"   {col}: {unique_count:,} unique values")
        
        # Show sample values for categorical columns
        if unique_count <= 20 and df[col].dtype == 'object':
            print(f"      Sample values: {list(df[col].unique()[:5])}")
    
    return {
        'shape': df.shape,
        'dtypes': df.dtypes,
        'missing_data': missing_data,
        'unique_counts': {col: df[col].nunique() for col in df.columns}
    }


def identify_mmm_columns(df):
    """Identify columns relevant for MMM modeling."""
    print(f"\n🎯 MMM-Relevant Column Identification")
    print("=" * 50)
    
    mmm_columns = {
        'date_columns': [],
        'spend_columns': [],
        'channel_columns': [],
        'geographic_columns': [],
        'business_metrics': [],
        'hcp_identifiers': []
    }
    
    # Look for date columns
    for col in df.columns:
        col_lower = col.lower()
        if any(keyword in col_lower for keyword in ['date', 'time', 'period', 'month', 'year']):
            mmm_columns['date_columns'].append(col)
    
    # Look for spend/marketing columns
    for col in df.columns:
        col_lower = col.lower()
        if any(keyword in col_lower for keyword in ['spend', 'cost', 'budget', 'investment', 'marketing']):
            mmm_columns['spend_columns'].append(col)
    
    # Look for channel columns
    for col in df.columns:
        col_lower = col.lower()
        if any(keyword in col_lower for keyword in ['channel', 'media', 'platform', 'campaign', 'touchpoint']):
            mmm_columns['channel_columns'].append(col)
    
    # Look for geographic columns
    for col in df.columns:
        col_lower = col.lower()
        if any(keyword in col_lower for keyword in ['region', 'state', 'city', 'territory', 'geography']):
            mmm_columns['geographic_columns'].append(col)
    
    # Look for business metrics
    for col in df.columns:
        col_lower = col.lower()
        if any(keyword in col_lower for keyword in ['revenue', 'sales', 'prescription', 'volume', 'conversion']):
            mmm_columns['business_metrics'].append(col)
    
    # Look for HCP identifiers
    for col in df.columns:
        col_lower = col.lower()
        if any(keyword in col_lower for keyword in ['hcp', 'doctor', 'physician', 'id', 'name']):
            mmm_columns['hcp_identifiers'].append(col)
    
    # Display findings
    for category, columns in mmm_columns.items():
        if columns:
            print(f"   {category.replace('_', ' ').title()}: {columns}")
        else:
            print(f"   {category.replace('_', ' ').title()}: None identified")
    
    return mmm_columns


def create_mmm_data_summary(df, mmm_columns):
    """Create a summary for MMM modeling."""
    print(f"\n📈 MMM Data Summary")
    print("=" * 50)
    
    # Check if we have the essential components
    has_date = len(mmm_columns['date_columns']) > 0
    has_spend = len(mmm_columns['spend_columns']) > 0
    has_channels = len(mmm_columns['channel_columns']) > 0
    has_metrics = len(mmm_columns['business_metrics']) > 0
    
    print(f"✅ Essential Components:")
    print(f"   Date columns: {'✅' if has_date else '❌'} {mmm_columns['date_columns']}")
    print(f"   Spend columns: {'✅' if has_spend else '❌'} {mmm_columns['spend_columns']}")
    print(f"   Channel columns: {'✅' if has_channels else '❌'} {mmm_columns['channel_columns']}")
    print(f"   Business metrics: {'✅' if has_metrics else '❌'} {mmm_columns['business_metrics']}")
    
    # Data aggregation recommendations
    print(f"\n🔄 Data Aggregation Recommendations:")
    if has_date and has_spend:
        print(f"   Aggregate spend data by date and channel")
        if mmm_columns['geographic_columns']:
            print(f"   Consider geographic aggregation")
        if mmm_columns['hcp_identifiers']:
            print(f"   Aggregate HCP-level data to market level")
    
    # Next steps
    print(f"\n🎯 Next Steps:")
    if has_date and has_spend and has_channels:
        print(f"   1. ✅ Data structure suitable for MMM")
        print(f"   2. 🔄 Create aggregated datasets")
        print(f"   3. 📊 Run exploratory data analysis")
        print(f"   4. 🏗️ Design MMM model architecture")
    else:
        print(f"   1. ❌ Missing essential components")
        print(f"   2. 🔍 Review column descriptions")
        print(f"   3. 📋 Identify required transformations")
        print(f"   4. 🔄 Create derived columns if needed")


def main():
    """Main function to analyze HCP data."""
    print("🏥 HCP-Level Data Analysis for MMM Project")
    print("=" * 60)
    
    # Load data
    df = load_hcp_data()
    if df is None:
        return
    
    # Load column descriptions
    desc_df = load_column_descriptions()
    
    # Analyze data structure
    structure_info = analyze_data_structure(df)
    
    # Identify MMM-relevant columns
    mmm_columns = identify_mmm_columns(df)
    
    # Create MMM summary
    create_mmm_data_summary(df, mmm_columns)
    
    # Save analysis results
    print(f"\n💾 Saving Analysis Results")
    print("=" * 50)
    
    # Save column mapping
    column_mapping = pd.DataFrame([
        {'category': category, 'columns': ', '.join(columns)}
        for category, columns in mmm_columns.items()
        if columns
    ])
    column_mapping.to_csv('reports/hcp_column_mapping.csv', index=False)
    print(f"   ✅ Column mapping saved to reports/hcp_column_mapping.csv")
    
    # Save data summary
    summary_df = pd.DataFrame([
        {'column': col, 'dtype': str(dtype), 'unique_count': structure_info['unique_counts'][col], 
         'missing_count': structure_info['missing_data'][col]}
        for col, dtype in structure_info['dtypes'].items()
    ])
    summary_df.to_csv('reports/hcp_data_summary.csv', index=False)
    print(f"   ✅ Data summary saved to reports/hcp_data_summary.csv")
    
    print(f"\n🎉 Analysis Complete!")
    print(f"   Review the reports/ directory for detailed results")
    print(f"   Next: Create aggregated datasets for MMM modeling")


if __name__ == "__main__":
    main()
