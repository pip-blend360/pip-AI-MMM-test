#!/usr/bin/env python3
"""
Data Pipeline Test Script

This script tests our data loading utilities with real CSV data
and validates the data structure for MMM modeling.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from pip_ai_mmm_test.data.loaders import (
    load_marketing_spend_data,
    load_business_metrics_data,
    validate_data_quality,
    get_data_summary
)

from pip_ai_mmm_test.analysis.eda import (
    plot_time_series,
    plot_channel_spend_distribution,
    plot_missing_data_patterns,
    get_data_summary
)


def test_data_pipeline():
    """Test the complete data pipeline with real data."""
    print("🔍 Testing Data Pipeline for MMM Project")
    print("=" * 50)
    
    # Check if data files exist
    raw_data_dir = Path("data/raw")
    spend_file = raw_data_dir / "marketing_spend.csv"
    metrics_file = raw_data_dir / "business_metrics.csv"
    
    print(f"📁 Raw data directory: {raw_data_dir}")
    print(f"📊 Marketing spend file: {spend_file}")
    print(f"📈 Business metrics file: {metrics_file}")
    
    # Test marketing spend data
    if spend_file.exists():
        print(f"\n✅ Loading marketing spend data from {spend_file}")
        try:
            spend_df = load_marketing_spend_data(str(spend_file))
            print(f"   Shape: {spend_df.shape}")
            print(f"   Columns: {list(spend_df.columns)}")
            print(f"   Date range: {spend_df['date'].min()} to {spend_df['date'].max()}")
            print(f"   Channels: {spend_df['channel'].unique()}")
            
            # Validate data quality
            validation = validate_data_quality(
                spend_df, 
                required_columns=['date', 'channel', 'spend'],
                date_column='date'
            )
            print(f"   Data quality valid: {validation['is_valid']}")
            if validation['issues']:
                print(f"   Issues: {validation['issues']}")
                
        except Exception as e:
            print(f"❌ Error loading marketing spend data: {e}")
    else:
        print(f"❌ Marketing spend file not found: {spend_file}")
        print("   Please add your marketing spend CSV to data/raw/")
    
    # Test business metrics data
    if metrics_file.exists():
        print(f"\n✅ Loading business metrics data from {metrics_file}")
        try:
            metrics_df = load_business_metrics_data(str(metrics_file))
            print(f"   Shape: {metrics_df.shape}")
            print(f"   Columns: {list(metrics_df.columns)}")
            print(f"   Date range: {metrics_df['date'].min()} to {metrics_df['date'].max()}")
            
            # Validate data quality
            validation = validate_data_quality(
                metrics_df,
                required_columns=['date', 'revenue'],
                date_column='date'
            )
            print(f"   Data quality valid: {validation['is_valid']}")
            if validation['issues']:
                print(f"   Issues: {validation['issues']}")
                
        except Exception as e:
            print(f"❌ Error loading business metrics data: {e}")
    else:
        print(f"❌ Business metrics file not found: {metrics_file}")
        print("   Please add your business metrics CSV to data/raw/")
    
    # Check data requirements compliance
    print(f"\n📋 Checking Requirements Compliance:")
    print(f"   Required: 24+ months of data")
    print(f"   Required: Marketing spend by channel")
    print(f"   Required: Business performance metrics")
    print(f"   Required: Date, channel, spend columns")
    
    return spend_df if 'spend_df' in locals() else None, metrics_df if 'metrics_df' in locals() else None


def create_sample_data_if_needed():
    """Create sample data if real data is not available."""
    print("\n🎲 Creating sample data for testing...")
    
    # Create sample marketing spend data
    dates = pd.date_range(start='2022-01-01', end='2023-12-31', freq='D')
    channels = ['TV', 'Digital', 'Print', 'Radio', 'Events']
    
    sample_data = []
    for date in dates:
        for channel in channels:
            # Different spend patterns per channel
            if channel == 'TV':
                spend = np.random.exponential(2000)
            elif channel == 'Digital':
                spend = np.random.exponential(1500)
            elif channel == 'Print':
                spend = np.random.exponential(800)
            elif channel == 'Radio':
                spend = np.random.exponential(600)
            else:  # Events
                spend = np.random.exponential(1000)
            
            sample_data.append({
                'date': date,
                'channel': channel,
                'spend': spend
            })
    
    spend_df = pd.DataFrame(sample_data)
    
    # Create sample business metrics
    daily_spend = spend_df.groupby('date')['spend'].sum()
    revenue = daily_spend * np.random.uniform(2.5, 4.0, len(daily_spend))
    
    metrics_df = pd.DataFrame({
        'date': daily_spend.index,
        'revenue': revenue.values,
        'prescriptions': (revenue * np.random.uniform(0.8, 1.2, len(revenue))).astype(int)
    })
    
    # Save sample data
    spend_df.to_csv('data/raw/marketing_spend_sample.csv', index=False)
    metrics_df.to_csv('data/raw/business_metrics_sample.csv', index=False)
    
    print(f"✅ Created sample data:")
    print(f"   Marketing spend: {len(spend_df)} rows")
    print(f"   Business metrics: {len(metrics_df)} rows")
    print(f"   Date range: {dates[0]} to {dates[-1]}")
    
    return spend_df, metrics_df


def main():
    """Main function to test data pipeline."""
    # Test with real data first
    spend_df, metrics_df = test_data_pipeline()
    
    # If no real data, create sample data
    if spend_df is None or metrics_df is None:
        spend_df, metrics_df = create_sample_data_if_needed()
    
    # Run basic EDA if we have data
    if spend_df is not None and metrics_df is not None:
        print(f"\n📊 Running Basic EDA...")
        
        # Channel spend distribution
        print("   Creating channel spend distribution plot...")
        fig = plot_channel_spend_distribution(
            spend_df,
            channel_col='channel',
            spend_col='spend',
            title="Marketing Spend by Channel",
            xkcd_style=True  # Use XKCD style for fun!
        )
        
        # Save plot
        import matplotlib.pyplot as plt
        plt.savefig('reports/figures/channel_spend_distribution.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✅ Data pipeline test complete!")
        print("\nNext steps:")
        print("1. Review the data quality validation results")
        print("2. Check the channel spend distribution plot")
        print("3. Proceed with feature engineering")
        print("4. Design the MMM model architecture")


if __name__ == "__main__":
    main()
