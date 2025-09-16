#!/usr/bin/env python3
"""
Interactive EDA Dashboard for MMM Data
=====================================

A Streamlit dashboard for exploring marketing mix modeling data with:
- Channel selection (Display_HCP, Display_DTC, Paid_Search_HCP, Meetings, TeleDetails, Emails)
- DMA selection (including National option)
- Time series visualization with XKCD style option
- Data summary statistics
- Channel performance metrics

Usage:
    streamlit run scripts/eda_dashboard.py

Author: AI Assistant
Date: 2024
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
import sys

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from pip_ai_mmm_test.analysis.eda import (
    plot_time_series, 
    plot_channel_spend_distribution,
    enable_xkcd_style, 
    disable_xkcd_style
)

# Page configuration
st.set_page_config(
    page_title="MMM EDA Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load all processed data files with caching."""
    try:
        # Load processed data
        dma_aggregated = pd.read_csv('data/processed/dma_aggregated_data.csv')
        national_aggregated = pd.read_csv('data/processed/national_aggregated_data.csv')
        dma_channel = pd.read_csv('data/processed/dma_channel_data.csv')
        national_channel = pd.read_csv('data/processed/national_channel_data.csv')
        
        # Convert date columns to datetime and standardize column names
        for df in [dma_aggregated, national_aggregated, dma_channel, national_channel]:
            if 'date' in df.columns:
                df['month'] = pd.to_datetime(df['date'])
            elif 'month' in df.columns:
                df['month'] = pd.to_datetime(df['month'])
        
        # Standardize DMA column names
        if 'DMA_Code' in dma_aggregated.columns:
            dma_aggregated['dma'] = dma_aggregated['DMA_Code'].astype(str)
        if 'DMA_Code' in dma_channel.columns:
            dma_channel['dma'] = dma_channel['DMA_Code'].astype(str)
        
        # Add 'dma' column to national data
        national_aggregated['dma'] = 'National'
        national_channel['dma'] = 'National'
        
        return dma_aggregated, national_aggregated, dma_channel, national_channel
    except FileNotFoundError as e:
        st.error(f"Data files not found: {e}")
        st.info("Please run the data transformation script first: `python scripts/run_data_transformation.py`")
        return None, None, None, None

def get_available_channels(df):
    """Extract available marketing channels from dataframe."""
    if df is None:
        return []
    
    # Marketing channels are columns that contain spend data
    spend_columns = [col for col in df.columns if 'spend' in col.lower()]
    return sorted(spend_columns)

def get_available_dmas(df):
    """Extract available DMAs from dataframe."""
    if df is None:
        return ['National']
    
    # Check if we have DMA data
    if 'DMA_Code' in df.columns:
        dmas = sorted(df['DMA_Code'].unique().tolist())
        return ['National'] + [str(dma) for dma in dmas]
    elif 'dma' in df.columns:
        dmas = sorted(df['dma'].unique().tolist())
        return ['National'] + dmas
    else:
        return ['National']


def create_single_channel_plot(data, channel, dma, xkcd_style=False):
    """Create a single channel plot for selected DMA."""
    if data is None or data.empty:
        return None
    
    # Filter data
    if dma == 'National':
        plot_data = data[data['dma'] == 'National'].copy()
        title_suffix = "National"
    else:
        plot_data = data[data['dma'] == dma].copy()
        title_suffix = f"DMA: {dma}"
    
    if plot_data.empty or channel not in plot_data.columns:
        return None
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(12, 6))
    
    if xkcd_style:
        enable_xkcd_style()
    
    # Plot the time series
    ax.plot(plot_data['month'], plot_data[channel], 
            marker='o', linewidth=2, markersize=6, color='#1f77b4')
    
    # Format channel name for display
    channel_display = channel.replace('spend_', '').replace('_', ' ').title()
    
    ax.set_title(f'{channel_display} Spend Over Time - {title_suffix}', 
                fontsize=16, fontweight='bold')
    ax.set_xlabel('Month', fontsize=12)
    ax.set_ylabel(f'{channel_display} Spend ($)', fontsize=12)
    ax.grid(True, alpha=0.3)
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    if xkcd_style:
        disable_xkcd_style()
    
    return fig

def calculate_metrics(data, channel, dma):
    """Calculate key metrics for selected channel and DMA."""
    if data is None or data.empty:
        return {}
    
    # Filter data
    if dma == 'National':
        plot_data = data[data['dma'] == 'National'].copy()
    else:
        plot_data = data[data['dma'] == dma].copy()
    
    if plot_data.empty or channel not in plot_data.columns:
        return {}
    
    channel_data = plot_data[channel]
    
    metrics = {
        'Total Spend': f"${channel_data.sum():,.0f}",
        'Average Monthly Spend': f"${channel_data.mean():,.0f}",
        'Max Monthly Spend': f"${channel_data.max():,.0f}",
        'Min Monthly Spend': f"${channel_data.min():,.0f}",
        'Spend Variance': f"${channel_data.std():,.0f}",
        'Data Points': len(channel_data)
    }
    
    return metrics

def main():
    """Main dashboard application."""
    
    # Header
    st.markdown('<h1 class="main-header">📊 MMM EDA Dashboard</h1>', 
                unsafe_allow_html=True)
    
    # Load data
    with st.spinner("Loading data..."):
        dma_aggregated, national_aggregated, dma_channel, national_channel = load_data()
    
    if dma_aggregated is None:
        st.stop()
    
    # Sidebar controls
    st.sidebar.header("🎛️ Dashboard Controls")
    
    # Use aggregated data (has all spend columns)
    data = dma_aggregated
    available_channels = get_available_channels(data)
    
    # Channel selection (first, so it's prominent)
    if available_channels:
        selected_channel = st.sidebar.selectbox(
            "Select Channel:",
            available_channels,
            index=0,  # Default to first channel
            help="Choose a marketing channel to analyze"
        )
    else:
        st.sidebar.error("No channels found in data")
        st.stop()
    
    # DMA selection
    available_dmas = get_available_dmas(data)
    selected_dma = st.sidebar.selectbox(
        "Select DMA:",
        available_dmas,
        help="Choose a specific DMA or National for aggregated view"
    )
    
    # Visualization options
    st.sidebar.header("🎨 Visualization Options")
    xkcd_style = st.sidebar.checkbox(
        "Enable XKCD Style", 
        value=False,
        help="Use hand-drawn, comic-style plots"
    )
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Format channel name for display
        channel_display = selected_channel.replace('spend_', '').replace('_', ' ').title()
        st.header(f"📈 {channel_display} Analysis")
        
        # Single channel plot
        fig = create_single_channel_plot(data, selected_channel, selected_dma, xkcd_style)
        if fig:
            st.pyplot(fig)
        else:
            st.warning(f"No data available for {channel_display} in {selected_dma}")
    
    with col2:
        st.header("📊 Key Metrics")
        
        # Calculate and display metrics
        metrics = calculate_metrics(data, selected_channel, selected_dma)
        if metrics:
            for metric_name, metric_value in metrics.items():
                st.metric(metric_name, metric_value)
        else:
            st.warning("No metrics available")
    
    # Data summary section
    st.header("📋 Data Summary")
    
    # Filter data for summary
    if selected_dma == 'National':
        summary_data = data[data['dma'] == 'National'].copy()
    else:
        summary_data = data[data['dma'] == selected_dma].copy()
    
    if not summary_data.empty:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("📅 Time Range")
            st.write(f"**Start:** {summary_data['month'].min().strftime('%Y-%m')}")
            st.write(f"**End:** {summary_data['month'].max().strftime('%Y-%m')}")
            st.write(f"**Months:** {len(summary_data)}")
        
        with col2:
            st.subheader("💰 Spend Summary")
            total_spend = summary_data[available_channels].sum().sum()
            avg_monthly = summary_data[available_channels].sum(axis=1).mean()
            st.write(f"**Total Spend:** ${total_spend:,.0f}")
            st.write(f"**Avg Monthly:** ${avg_monthly:,.0f}")
        
        with col3:
            st.subheader("📊 Data Quality")
            missing_data = summary_data[available_channels].isnull().sum().sum()
            total_cells = len(summary_data) * len(available_channels)
            completeness = (1 - missing_data/total_cells) * 100
            st.write(f"**Completeness:** {completeness:.1f}%")
            st.write(f"**Missing Values:** {missing_data}")
        
        # Raw data preview
        st.subheader("🔍 Data Preview")
        st.dataframe(summary_data.head(10), use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "**Dashboard Info:** Built with Streamlit | "
        "Data: Processed MMM datasets | "
        "Visualization: Matplotlib with XKCD style option"
    )

if __name__ == "__main__":
    main()
