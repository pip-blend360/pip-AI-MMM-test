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
        
        # Convert month columns to datetime
        for df in [dma_aggregated, national_aggregated, dma_channel, national_channel]:
            if 'month' in df.columns:
                df['month'] = pd.to_datetime(df['month'])
        
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
    spend_columns = [col for col in df.columns if 'spend' in col.lower() or col in [
        'Display_HCP', 'Display_DTC', 'Paid_Search_HCP', 
        'Meetings', 'TeleDetails', 'Emails'
    ]]
    return sorted(spend_columns)

def get_available_dmas(df):
    """Extract available DMAs from dataframe."""
    if df is None or 'dma' not in df.columns:
        return ['National']
    
    dmas = sorted(df['dma'].unique().tolist())
    return ['National'] + dmas

def create_time_series_plot(data, channel, dma, xkcd_style=False):
    """Create time series plot for selected channel and DMA."""
    if data is None or data.empty:
        return None
    
    # Filter data
    if dma == 'National':
        plot_data = data[data['dma'] == 'National'].copy()
        title_suffix = "National"
    else:
        plot_data = data[data['dma'] == dma].copy()
        title_suffix = f"DMA: {dma}"
    
    if plot_data.empty:
        return None
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(12, 6))
    
    if xkcd_style:
        enable_xkcd_style()
    
    # Plot the time series
    ax.plot(plot_data['month'], plot_data[channel], 
            marker='o', linewidth=2, markersize=6)
    
    ax.set_title(f'{channel} Spend Over Time - {title_suffix}', 
                fontsize=16, fontweight='bold')
    ax.set_xlabel('Month', fontsize=12)
    ax.set_ylabel(f'{channel} Spend ($)', fontsize=12)
    ax.grid(True, alpha=0.3)
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    if xkcd_style:
        disable_xkcd_style()
    
    return fig

def create_channel_comparison_plot(data, dma, xkcd_style=False):
    """Create channel comparison plot for selected DMA."""
    if data is None or data.empty:
        return None
    
    # Filter data
    if dma == 'National':
        plot_data = data[data['dma'] == 'National'].copy()
        title_suffix = "National"
    else:
        plot_data = data[data['dma'] == dma].copy()
        title_suffix = f"DMA: {dma}"
    
    if plot_data.empty:
        return None
    
    # Get channel columns
    channels = get_available_channels(data)
    if not channels:
        return None
    
    # Create subplot for each channel
    n_channels = len(channels)
    n_cols = 3
    n_rows = (n_channels + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 4*n_rows))
    if n_rows == 1:
        axes = [axes] if n_cols == 1 else axes
    else:
        axes = axes.flatten()
    
    if xkcd_style:
        enable_xkcd_style()
    
    for i, channel in enumerate(channels):
        if i < len(axes):
            ax = axes[i]
            ax.plot(plot_data['month'], plot_data[channel], 
                   marker='o', linewidth=2, markersize=4)
            ax.set_title(f'{channel}', fontsize=12, fontweight='bold')
            ax.set_xlabel('Month', fontsize=10)
            ax.set_ylabel('Spend ($)', fontsize=10)
            ax.grid(True, alpha=0.3)
            ax.tick_params(axis='x', rotation=45)
    
    # Hide unused subplots
    for i in range(len(channels), len(axes)):
        axes[i].set_visible(False)
    
    fig.suptitle(f'All Channels Comparison - {title_suffix}', 
                fontsize=16, fontweight='bold')
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
    
    # Data level selection
    data_level = st.sidebar.selectbox(
        "Select Data Level:",
        ["Channel Level", "Aggregated Level"],
        help="Channel Level: Individual channel spend data\nAggregated Level: Total spend and business metrics"
    )
    
    # Choose appropriate dataset
    if data_level == "Channel Level":
        data = dma_channel
        available_channels = get_available_channels(dma_channel)
    else:
        data = dma_aggregated
        available_channels = get_available_channels(dma_aggregated)
    
    # DMA selection
    available_dmas = get_available_dmas(data)
    selected_dma = st.sidebar.selectbox(
        "Select DMA:",
        available_dmas,
        help="Choose a specific DMA or National for aggregated view"
    )
    
    # Channel selection
    if available_channels:
        selected_channel = st.sidebar.selectbox(
            "Select Channel:",
            available_channels,
            help="Choose a marketing channel to analyze"
        )
    else:
        st.sidebar.error("No channels found in data")
        st.stop()
    
    # Visualization options
    st.sidebar.header("🎨 Visualization Options")
    xkcd_style = st.sidebar.checkbox(
        "Enable XKCD Style", 
        value=False,
        help="Use hand-drawn, comic-style plots"
    )
    
    show_comparison = st.sidebar.checkbox(
        "Show All Channels Comparison",
        value=False,
        help="Display comparison plot of all channels"
    )
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header(f"📈 {selected_channel} Analysis")
        
        # Time series plot
        fig = create_time_series_plot(data, selected_channel, selected_dma, xkcd_style)
        if fig:
            st.pyplot(fig)
        else:
            st.warning(f"No data available for {selected_channel} in {selected_dma}")
    
    with col2:
        st.header("📊 Key Metrics")
        
        # Calculate and display metrics
        metrics = calculate_metrics(data, selected_channel, selected_dma)
        if metrics:
            for metric_name, metric_value in metrics.items():
                st.metric(metric_name, metric_value)
        else:
            st.warning("No metrics available")
    
    # Channel comparison section
    if show_comparison:
        st.header("🔄 All Channels Comparison")
        comparison_fig = create_channel_comparison_plot(data, selected_dma, xkcd_style)
        if comparison_fig:
            st.pyplot(comparison_fig)
        else:
            st.warning(f"No comparison data available for {selected_dma}")
    
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
