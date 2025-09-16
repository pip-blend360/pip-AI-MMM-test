#!/usr/bin/env python3
"""
HCP-Level Data Analysis for MMM Project

Based on the Mock_HCPlevel.csv structure, this script provides
a comprehensive analysis and MMM transformation plan.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

# Set up plotting
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")


def analyze_hcp_data_structure():
    """Analyze the HCP-level data structure."""
    print("🏥 HCP-Level Data Analysis for MMM Project")
    print("=" * 60)
    
    # Load the data
    data_file = Path("data/raw/Mock_HCPlevel.csv")
    df = pd.read_csv(data_file)
    
    print(f"📊 Dataset Overview:")
    print(f"   Shape: {df.shape}")
    print(f"   Columns: {list(df.columns)}")
    print(f"   Date range: {df['month'].min()} to {df['month'].max()}")
    print(f"   Unique HCPs: {df['HCP_ID'].nunique()}")
    print(f"   Unique DMAs: {df['DMA_Code'].nunique()}")
    
    return df


def identify_mmm_components(df):
    """Identify MMM-relevant components in the HCP data."""
    print(f"\n🎯 MMM Component Identification")
    print("=" * 50)
    
    components = {
        'date_column': 'month',
        'geographic_column': 'DMA_Code',
        'hcp_identifier': 'HCP_ID',
        'spend_columns': {
            'Display_HCP': 'SPEND_display_hcp',
            'Display_DTC': 'SPEND_display_dtc', 
            'Paid_Search_HCP': 'COST_paidsearch_hcp_google',
            'Meetings': 'Total_meetings',
            'TeleDetails': 'TeleDetails'
        },
        'impression_columns': {
            'Display_HCP': 'IMPRESSIONS_display_hcp',
            'Display_DTC': 'IMPRESSIONS_display_dtc',
            'Paid_Search_HCP': 'IMPRESSIONS_paidsearch_hcp_google'
        },
        'click_columns': {
            'Display_HCP': 'CLICKS_display_hcp',
            'Display_DTC': 'CLICKS_display_dtc', 
            'Paid_Search_HCP': 'CLICKS_paidsearch_hcp_google'
        },
        'business_metrics': {
            'TRX': 'TRX',
            'NRX': 'NRX', 
            'PDE': 'PDE',
            'ZELAPAR_SELEGILINE': 'ZELAPAR-SELEGILINE_trx'
        },
        'other_metrics': {
            'Emails': 'total emails',
            'Specialty_Group': 'spec_GROUP'
        }
    }
    
    print(f"✅ Identified MMM Components:")
    print(f"   Date Column: {components['date_column']}")
    print(f"   Geographic Column: {components['geographic_column']}")
    print(f"   HCP Identifier: {components['hcp_identifier']}")
    
    print(f"\n💰 Marketing Spend Channels:")
    for channel, column in components['spend_columns'].items():
        total_spend = df[column].sum()
        print(f"   {channel}: ${total_spend:,.2f} total")
    
    print(f"\n📈 Business Metrics:")
    for metric, column in components['business_metrics'].items():
        total_value = df[column].sum()
        print(f"   {metric}: {total_value:,.2f} total")
    
    return components


def create_aggregated_mmm_data(df, components):
    """Create aggregated datasets for MMM modeling."""
    print(f"\n🔄 Creating Aggregated MMM Datasets")
    print("=" * 50)
    
    # Convert month to proper date format
    df['date'] = pd.to_datetime(df['month'], format='%Y%m')
    
    # 1. DMA-level aggregated data
    print(f"📊 Creating DMA-level aggregation...")
    
    dma_agg = df.groupby(['DMA_Code', 'date']).agg({
        # Marketing spend
        'SPEND_display_hcp': 'sum',
        'SPEND_display_dtc': 'sum',
        'COST_paidsearch_hcp_google': 'sum',
        'Total_meetings': 'sum',
        'TeleDetails': 'sum',
        
        # Impressions
        'IMPRESSIONS_display_hcp': 'sum',
        'IMPRESSIONS_display_dtc': 'sum',
        'IMPRESSIONS_paidsearch_hcp_google': 'sum',
        
        # Clicks
        'CLICKS_display_hcp': 'sum',
        'CLICKS_display_dtc': 'sum',
        'CLICKS_paidsearch_hcp_google': 'sum',
        
        # Business metrics
        'TRX': 'sum',
        'NRX': 'sum',
        'PDE': 'sum',
        'ZELAPAR-SELEGILINE_trx': 'sum',
        
        # Other metrics
        'total emails': 'sum',
        'HCP_ID': 'nunique'  # Count of unique HCPs
    }).reset_index()
    
    # Rename columns for clarity
    dma_agg.columns = [
        'DMA_Code', 'date',
        'spend_display_hcp', 'spend_display_dtc', 'spend_paidsearch_hcp',
        'spend_meetings', 'spend_teledetails',
        'impressions_display_hcp', 'impressions_display_dtc', 'impressions_paidsearch_hcp',
        'clicks_display_hcp', 'clicks_display_dtc', 'clicks_paidsearch_hcp',
        'trx', 'nrx', 'pde', 'zelapar_selegiline_trx',
        'total_emails', 'unique_hcps'
    ]
    
    print(f"   DMA-level data shape: {dma_agg.shape}")
    print(f"   Date range: {dma_agg['date'].min()} to {dma_agg['date'].max()}")
    print(f"   Unique DMAs: {dma_agg['DMA_Code'].nunique()}")
    
    # 2. National-level aggregated data
    print(f"\n🌍 Creating national-level aggregation...")
    
    national_agg = df.groupby('date').agg({
        # Marketing spend
        'SPEND_display_hcp': 'sum',
        'SPEND_display_dtc': 'sum',
        'COST_paidsearch_hcp_google': 'sum',
        'Total_meetings': 'sum',
        'TeleDetails': 'sum',
        
        # Impressions
        'IMPRESSIONS_display_hcp': 'sum',
        'IMPRESSIONS_display_dtc': 'sum',
        'IMPRESSIONS_paidsearch_hcp_google': 'sum',
        
        # Clicks
        'CLICKS_display_hcp': 'sum',
        'CLICKS_display_dtc': 'sum',
        'CLICKS_paidsearch_hcp_google': 'sum',
        
        # Business metrics
        'TRX': 'sum',
        'NRX': 'sum',
        'PDE': 'sum',
        'ZELAPAR-SELEGILINE_trx': 'sum',
        
        # Other metrics
        'total emails': 'sum',
        'HCP_ID': 'nunique'  # Count of unique HCPs
    }).reset_index()
    
    # Rename columns for clarity
    national_agg.columns = [
        'date',
        'spend_display_hcp', 'spend_display_dtc', 'spend_paidsearch_hcp',
        'spend_meetings', 'spend_teledetails',
        'impressions_display_hcp', 'impressions_display_dtc', 'impressions_paidsearch_hcp',
        'clicks_display_hcp', 'clicks_display_dtc', 'clicks_paidsearch_hcp',
        'trx', 'nrx', 'pde', 'zelapar_selegiline_trx',
        'total_emails', 'unique_hcps'
    ]
    
    print(f"   National-level data shape: {national_agg.shape}")
    print(f"   Date range: {national_agg['date'].min()} to {national_agg['date'].max()}")
    
    return dma_agg, national_agg


def analyze_marketing_channels(df):
    """Analyze marketing channel performance."""
    print(f"\n📊 Marketing Channel Analysis")
    print("=" * 50)
    
    # Calculate total spend by channel
    channel_spend = {
        'Display_HCP': df['SPEND_display_hcp'].sum(),
        'Display_DTC': df['SPEND_display_dtc'].sum(),
        'Paid_Search_HCP': df['COST_paidsearch_hcp_google'].sum(),
        'Meetings': df['Total_meetings'].sum() * 100,  # Assuming $100 per meeting
        'TeleDetails': df['TeleDetails'].sum() * 50,    # Assuming $50 per tele detail
        'Emails': df['total emails'].sum() * 0.1       # Assuming $0.10 per email
    }
    
    print(f"💰 Total Spend by Channel:")
    total_spend = sum(channel_spend.values())
    for channel, spend in channel_spend.items():
        pct = (spend / total_spend) * 100
        print(f"   {channel}: ${spend:,.2f} ({pct:.1f}%)")
    
    print(f"\n📈 Total Marketing Spend: ${total_spend:,.2f}")
    
    return channel_spend


def create_mmm_ready_datasets(dma_agg, national_agg):
    """Create MMM-ready datasets with proper channel structure."""
    print(f"\n🏗️ Creating MMM-Ready Datasets")
    print("=" * 50)
    
    # Create channel-level spend data for MMM
    channels = ['display_hcp', 'display_dtc', 'paidsearch_hcp', 'meetings', 'teledetails']
    
    # DMA-level channel data
    dma_channels = []
    for _, row in dma_agg.iterrows():
        for channel in channels:
            dma_channels.append({
                'date': row['date'],
                'DMA_Code': row['DMA_Code'],
                'channel': channel,
                'spend': row[f'spend_{channel}'],
                'impressions': row[f'impressions_{channel}'] if f'impressions_{channel}' in row else 0,
                'clicks': row[f'clicks_{channel}'] if f'clicks_{channel}' in row else 0
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
                'impressions': row[f'impressions_{channel}'] if f'impressions_{channel}' in row else 0,
                'clicks': row[f'clicks_{channel}'] if f'clicks_{channel}' in row else 0
            })
    
    national_channels_df = pd.DataFrame(national_channels)
    
    print(f"✅ MMM-Ready Datasets Created:")
    print(f"   DMA-level channels: {dma_channels_df.shape}")
    print(f"   National-level channels: {national_channels_df.shape}")
    
    return dma_channels_df, national_channels_df


def save_processed_data(dma_agg, national_agg, dma_channels_df, national_channels_df):
    """Save processed data for MMM modeling."""
    print(f"\n💾 Saving Processed Data")
    print("=" * 50)
    
    # Create processed data directory
    processed_dir = Path("data/processed")
    processed_dir.mkdir(exist_ok=True)
    
    # Save aggregated data
    dma_agg.to_csv(processed_dir / "dma_aggregated_data.csv", index=False)
    national_agg.to_csv(processed_dir / "national_aggregated_data.csv", index=False)
    
    # Save channel-level data
    dma_channels_df.to_csv(processed_dir / "dma_channel_data.csv", index=False)
    national_channels_df.to_csv(processed_dir / "national_channel_data.csv", index=False)
    
    print(f"✅ Data saved to data/processed/:")
    print(f"   dma_aggregated_data.csv")
    print(f"   national_aggregated_data.csv") 
    print(f"   dma_channel_data.csv")
    print(f"   national_channel_data.csv")


def create_summary_report(df, dma_agg, national_agg, channel_spend):
    """Create a summary report of the data transformation."""
    print(f"\n📋 MMM Data Transformation Summary")
    print("=" * 60)
    
    print(f"📊 Original HCP-Level Data:")
    print(f"   Records: {len(df):,}")
    print(f"   Unique HCPs: {df['HCP_ID'].nunique():,}")
    print(f"   Unique DMAs: {df['DMA_Code'].nunique():,}")
    print(f"   Date Range: {df['month'].min()} to {df['month'].max()}")
    
    print(f"\n🔄 Aggregated Data:")
    print(f"   DMA-level records: {len(dma_agg):,}")
    print(f"   National-level records: {len(national_agg):,}")
    print(f"   Date Range: {dma_agg['date'].min()} to {dma_agg['date'].max()}")
    
    print(f"\n💰 Marketing Channels:")
    total_spend = sum(channel_spend.values())
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
    """Main function to analyze and transform HCP data for MMM."""
    # Analyze original data
    df = analyze_hcp_data_structure()
    
    # Identify MMM components
    components = identify_mmm_components(df)
    
    # Create aggregated datasets
    dma_agg, national_agg = create_aggregated_mmm_data(df, components)
    
    # Analyze marketing channels
    channel_spend = analyze_marketing_channels(df)
    
    # Create MMM-ready datasets
    dma_channels_df, national_channels_df = create_mmm_ready_datasets(dma_agg, national_agg)
    
    # Save processed data
    save_processed_data(dma_agg, national_agg, dma_channels_df, national_channels_df)
    
    # Create summary report
    create_summary_report(df, dma_agg, national_agg, channel_spend)
    
    print(f"\n🎉 HCP Data Analysis Complete!")
    print(f"   Ready for MMM model development!")


if __name__ == "__main__":
    main()
