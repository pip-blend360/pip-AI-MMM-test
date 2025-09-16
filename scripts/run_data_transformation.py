#!/usr/bin/env python3
"""
HCP to MMM Data Transformation Script

This script transforms HCP-level data into MMM-ready aggregated datasets.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# Set up plotting
plt.style.use('default')
sns.set_palette("husl")


def load_hcp_data():
    """Load the HCP-level data."""
    print("📊 Loading HCP-Level Data")
    print("=" * 50)
    
    data_file = Path("data/raw/Mock_HCPlevel.csv")
    
    if not data_file.exists():
        print(f"❌ Data file not found: {data_file}")
        return None
    
    try:
        df = pd.read_csv(data_file)
        print(f"✅ Data loaded successfully!")
        print(f"   Shape: {df.shape}")
        print(f"   Columns: {len(df.columns)}")
        print(f"   Date range: {df['month'].min()} to {df['month'].max()}")
        print(f"   Unique HCPs: {df['HCP_ID'].nunique():,}")
        print(f"   Unique DMAs: {df['DMA_Code'].nunique()}")
        
        return df
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None


def transform_month_to_date(df):
    """Convert month column to proper date format."""
    print("\n📅 Converting month to date format...")
    
    # Convert YYYYMM to datetime
    df['date'] = pd.to_datetime(df['month'], format='%Y%m')
    
    print(f"   Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"   Unique months: {df['date'].dt.to_period('M').nunique()}")
    
    return df


def create_dma_aggregation(df):
    """Create DMA-level aggregated data."""
    print("\n🏢 Creating DMA-level aggregation...")
    
    # Define aggregation dictionary
    agg_dict = {
        # Marketing spend columns
        'SPEND_display_hcp': 'sum',
        'SPEND_display_dtc': 'sum',
        'COST_paidsearch_hcp_google': 'sum',
        'Total_meetings': 'sum',
        'TeleDetails': 'sum',
        'total emails': 'sum',
        
        # Impression columns
        'IMPRESSIONS_display_hcp': 'sum',
        'IMPRESSIONS_display_dtc': 'sum',
        'IMPRESSIONS_paidsearch_hcp_google': 'sum',
        
        # Click columns
        'CLICKS_display_hcp': 'sum',
        'CLICKS_display_dtc': 'sum',
        'CLICKS_paidsearch_hcp_google': 'sum',
        
        # Business metrics
        'TRX': 'sum',
        'NRX': 'sum',
        'PDE': 'sum',
        'ZELAPAR-SELEGILINE_trx': 'sum',
        
        # HCP count
        'HCP_ID': 'nunique'
    }
    
    # Aggregate by DMA and date
    dma_agg = df.groupby(['DMA_Code', 'date']).agg(agg_dict).reset_index()
    
    # Rename columns for clarity
    column_mapping = {
        'SPEND_display_hcp': 'spend_display_hcp',
        'SPEND_display_dtc': 'spend_display_dtc',
        'COST_paidsearch_hcp_google': 'spend_paidsearch_hcp',
        'Total_meetings': 'spend_meetings',
        'TeleDetails': 'spend_teledetails',
        'total emails': 'spend_emails',
        'IMPRESSIONS_display_hcp': 'impressions_display_hcp',
        'IMPRESSIONS_display_dtc': 'impressions_display_dtc',
        'IMPRESSIONS_paidsearch_hcp_google': 'impressions_paidsearch_hcp',
        'CLICKS_display_hcp': 'clicks_display_hcp',
        'CLICKS_display_dtc': 'clicks_display_dtc',
        'CLICKS_paidsearch_hcp_google': 'clicks_paidsearch_hcp',
        'ZELAPAR-SELEGILINE_trx': 'zelapar_selegiline_trx',
        'HCP_ID': 'unique_hcps'
    }
    
    dma_agg = dma_agg.rename(columns=column_mapping)
    
    print(f"   DMA aggregation shape: {dma_agg.shape}")
    print(f"   Unique DMAs: {dma_agg['DMA_Code'].nunique()}")
    print(f"   Date range: {dma_agg['date'].min()} to {dma_agg['date'].max()}")
    
    return dma_agg


def create_national_aggregation(df):
    """Create national-level aggregated data."""
    print("\n🌍 Creating national-level aggregation...")
    
    # Define aggregation dictionary
    agg_dict = {
        # Marketing spend columns
        'SPEND_display_hcp': 'sum',
        'SPEND_display_dtc': 'sum',
        'COST_paidsearch_hcp_google': 'sum',
        'Total_meetings': 'sum',
        'TeleDetails': 'sum',
        'total emails': 'sum',
        
        # Impression columns
        'IMPRESSIONS_display_hcp': 'sum',
        'IMPRESSIONS_display_dtc': 'sum',
        'IMPRESSIONS_paidsearch_hcp_google': 'sum',
        
        # Click columns
        'CLICKS_display_hcp': 'sum',
        'CLICKS_display_dtc': 'sum',
        'CLICKS_paidsearch_hcp_google': 'sum',
        
        # Business metrics
        'TRX': 'sum',
        'NRX': 'sum',
        'PDE': 'sum',
        'ZELAPAR-SELEGILINE_trx': 'sum',
        
        # HCP count
        'HCP_ID': 'nunique'
    }
    
    # Aggregate by date only
    national_agg = df.groupby('date').agg(agg_dict).reset_index()
    
    # Rename columns for clarity
    column_mapping = {
        'SPEND_display_hcp': 'spend_display_hcp',
        'SPEND_display_dtc': 'spend_display_dtc',
        'COST_paidsearch_hcp_google': 'spend_paidsearch_hcp',
        'Total_meetings': 'spend_meetings',
        'TeleDetails': 'spend_teledetails',
        'total emails': 'spend_emails',
        'IMPRESSIONS_display_hcp': 'impressions_display_hcp',
        'IMPRESSIONS_display_dtc': 'impressions_display_dtc',
        'IMPRESSIONS_paidsearch_hcp_google': 'impressions_paidsearch_hcp',
        'CLICKS_display_hcp': 'clicks_display_hcp',
        'CLICKS_display_dtc': 'clicks_display_dtc',
        'CLICKS_paidsearch_hcp_google': 'clicks_paidsearch_hcp',
        'ZELAPAR-SELEGILINE_trx': 'zelapar_selegiline_trx',
        'HCP_ID': 'unique_hcps'
    }
    
    national_agg = national_agg.rename(columns=column_mapping)
    
    print(f"   National aggregation shape: {national_agg.shape}")
    print(f"   Date range: {national_agg['date'].min()} to {national_agg['date'].max()}")
    
    return national_agg


def create_channel_level_data(dma_agg, national_agg):
    """Create channel-level data for MMM modeling."""
    print("\n📊 Creating channel-level data...")
    
    # Define channels
    channels = ['display_hcp', 'display_dtc', 'paidsearch_hcp', 'meetings', 'teledetails', 'emails']
    
    # DMA-level channel data
    dma_channels = []
    for _, row in dma_agg.iterrows():
        for channel in channels:
            dma_channels.append({
                'date': row['date'],
                'DMA_Code': row['DMA_Code'],
                'channel': channel,
                'spend': row[f'spend_{channel}'],
                'impressions': row.get(f'impressions_{channel}', 0),
                'clicks': row.get(f'clicks_{channel}', 0)
            })
    
    dma_channels_df = pd.DataFrame(dma_channels)
    
    # National-level channel data
    national_channels = []
    for _, row in national_agg.iterrows():
        for channel in channels:
            national_channels.append({
                'date': row['date'],
                'channel': channel,
                'spend': row[f'spend_{channel}'],
                'impressions': row.get(f'impressions_{channel}', 0),
                'clicks': row.get(f'clicks_{channel}', 0)
            })
    
    national_channels_df = pd.DataFrame(national_channels)
    
    print(f"   DMA channel data shape: {dma_channels_df.shape}")
    print(f"   National channel data shape: {national_channels_df.shape}")
    
    return dma_channels_df, national_channels_df


def analyze_channel_performance(dma_channels_df):
    """Analyze channel performance."""
    print("\n💰 Channel Performance Analysis")
    print("=" * 50)
    
    # Calculate total spend by channel
    channel_spend = dma_channels_df.groupby('channel')['spend'].sum().sort_values(ascending=False)
    
    print("📊 Total Spend by Channel:")
    total_spend = channel_spend.sum()
    for channel, spend in channel_spend.items():
        pct = (spend / total_spend) * 100
        print(f"   {channel}: ${spend:,.2f} ({pct:.1f}%)")
    
    print(f"\n💵 Total Marketing Spend: ${total_spend:,.2f}")
    
    return channel_spend


def create_visualizations(dma_channels_df, channel_spend):
    """Create visualizations of the transformed data."""
    print("\n📈 Creating visualizations...")
    
    # Create reports directory
    reports_dir = Path("reports/figures")
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Channel spend distribution
    plt.figure(figsize=(12, 8))
    
    plt.subplot(2, 2, 1)
    channel_spend.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title('Total Spend by Channel', fontweight='bold')
    plt.xlabel('Channel')
    plt.ylabel('Total Spend ($)')
    plt.xticks(rotation=45)
    
    # 2. Channel spend pie chart
    plt.subplot(2, 2, 2)
    channel_spend.plot(kind='pie', autopct='%1.1f%%', startangle=90)
    plt.title('Spend Distribution', fontweight='bold')
    plt.ylabel('')
    
    # 3. Time series of total spend
    plt.subplot(2, 2, 3)
    monthly_spend = dma_channels_df.groupby('date')['spend'].sum()
    monthly_spend.plot(linewidth=2, color='green')
    plt.title('Monthly Total Spend Over Time', fontweight='bold')
    plt.xlabel('Date')
    plt.ylabel('Total Spend ($)')
    plt.grid(True, alpha=0.3)
    
    # 4. Channel spend over time
    plt.subplot(2, 2, 4)
    channel_time = dma_channels_df.groupby(['date', 'channel'])['spend'].sum().unstack()
    channel_time.plot(ax=plt.gca(), linewidth=2)
    plt.title('Channel Spend Over Time', fontweight='bold')
    plt.xlabel('Date')
    plt.ylabel('Spend ($)')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout()
    plt.savefig(reports_dir / 'channel_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"   ✅ Visualizations saved to {reports_dir}/channel_analysis.png")


def save_processed_data(dma_agg, national_agg, dma_channels_df, national_channels_df):
    """Save all processed data."""
    print("\n💾 Saving processed data...")
    
    # Create processed data directory
    processed_dir = Path("data/processed")
    processed_dir.mkdir(exist_ok=True)
    
    # Save aggregated data
    dma_agg.to_csv(processed_dir / "dma_aggregated_data.csv", index=False)
    national_agg.to_csv(processed_dir / "national_aggregated_data.csv", index=False)
    
    # Save channel-level data
    dma_channels_df.to_csv(processed_dir / "dma_channel_data.csv", index=False)
    national_channels_df.to_csv(processed_dir / "national_channel_data.csv", index=False)
    
    print(f"✅ Data saved to {processed_dir}/:")
    print(f"   📊 dma_aggregated_data.csv")
    print(f"   🌍 national_aggregated_data.csv")
    print(f"   📈 dma_channel_data.csv")
    print(f"   📈 national_channel_data.csv")


def create_summary_report(df, dma_agg, national_agg, channel_spend):
    """Create a summary report."""
    print("\n📋 MMM Data Transformation Summary")
    print("=" * 60)
    
    print(f"📊 Original HCP-Level Data:")
    print(f"   Records: {len(df):,}")
    print(f"   Unique HCPs: {df['HCP_ID'].nunique():,}")
    print(f"   Unique DMAs: {df['DMA_Code'].nunique():,}")
    print(f"   Date Range: {df['date'].min()} to {df['date'].max()}")
    
    print(f"\n🔄 Aggregated Data:")
    print(f"   DMA-level records: {len(dma_agg):,}")
    print(f"   National-level records: {len(national_agg):,}")
    print(f"   Date Range: {dma_agg['date'].min()} to {dma_agg['date'].max()}")
    
    print(f"\n💰 Marketing Channels:")
    total_spend = channel_spend.sum()
    for channel, spend in channel_spend.items():
        pct = (spend / total_spend) * 100
        print(f"   {channel}: ${spend:,.2f} ({pct:.1f}%)")
    
    print(f"\n🎯 Next Steps for MMM:")
    print(f"   1. ✅ Data aggregation complete")
    print(f"   2. 🔄 Feature engineering (lag effects, seasonality)")
    print(f"   3. 🏗️ Bayesian MMM model setup")
    print(f"   4. 📊 Model training and validation")
    print(f"   5. 🎯 Optimization and simulation")


def main():
    """Main transformation function."""
    print("🔄 HCP to MMM Data Transformation")
    print("=" * 60)
    
    # Load data
    df = load_hcp_data()
    if df is None:
        return False
    
    # Transform month to date
    df = transform_month_to_date(df)
    
    # Create aggregations
    dma_agg = create_dma_aggregation(df)
    national_agg = create_national_aggregation(df)
    
    # Create channel-level data
    dma_channels_df, national_channels_df = create_channel_level_data(dma_agg, national_agg)
    
    # Analyze channel performance
    channel_spend = analyze_channel_performance(dma_channels_df)
    
    # Create visualizations
    create_visualizations(dma_channels_df, channel_spend)
    
    # Save processed data
    save_processed_data(dma_agg, national_agg, dma_channels_df, national_channels_df)
    
    # Create summary report
    create_summary_report(df, dma_agg, national_agg, channel_spend)
    
    print(f"\n🎉 Data transformation complete!")
    print(f"   Ready for MMM model development!")
    
    return True


if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ Transformation successful!")
    else:
        print("\n❌ Transformation failed!")
