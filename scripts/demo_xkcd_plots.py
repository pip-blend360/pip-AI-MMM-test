#!/usr/bin/env python3
"""
XKCD Style Plotting Demo for MMM Project

This script demonstrates the XKCD hand-drawn style plotting capabilities
added to the EDA functions.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from pip_ai_mmm_test.analysis.eda import (
    plot_time_series,
    plot_channel_spend_distribution,
    plot_correlation_heatmap,
    plot_missing_data_patterns,
    enable_xkcd_style,
    disable_xkcd_style
)


def create_sample_data():
    """Create sample MMM data for demonstration."""
    print("Creating sample MMM data...")
    
    # Create date range
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    channels = ['TV', 'Digital', 'Print', 'Radio', 'Events']
    
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Create marketing spend data
    spend_data = []
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
            
            spend_data.append({
                'date': date,
                'channel': channel,
                'spend': spend
            })
    
    spend_df = pd.DataFrame(spend_data)
    
    # Create business metrics data
    daily_spend = spend_df.groupby('date')['spend'].sum()
    revenue = daily_spend * np.random.uniform(2.5, 4.0, len(daily_spend))
    
    metrics_df = pd.DataFrame({
        'date': daily_spend.index,
        'revenue': revenue.values,
        'prescriptions': (revenue * np.random.uniform(0.8, 1.2, len(revenue))).astype(int)
    })
    
    print(f"✅ Created sample data:")
    print(f"   - Marketing spend: {len(spend_df)} rows")
    print(f"   - Business metrics: {len(metrics_df)} rows")
    
    return spend_df, metrics_df


def demo_xkcd_plots(spend_df, metrics_df):
    """Demonstrate XKCD style plotting."""
    print("\n🎨 Demonstrating XKCD Style Plots...")
    
    # 1. Channel spend distribution
    print("1. Channel Spend Distribution (XKCD Style)")
    fig1 = plot_channel_spend_distribution(
        spend_df,
        channel_col='channel',
        spend_col='spend',
        title="XKCD Style - Marketing Spend by Channel",
        xkcd_style=True
    )
    plt.show()
    
    # 2. Time series plot
    print("2. Time Series Plot (XKCD Style)")
    daily_spend = spend_df.groupby('date')['spend'].sum().reset_index()
    fig2 = plot_time_series(
        daily_spend,
        date_col='date',
        value_cols=['spend'],
        title="XKCD Style - Daily Marketing Spend Over Time",
        xkcd_style=True
    )
    plt.show()
    
    # 3. Missing data patterns (with some missing data)
    print("3. Missing Data Patterns (XKCD Style)")
    spend_df_with_missing = spend_df.copy()
    # Add some missing data
    missing_indices = spend_df_with_missing.sample(200).index
    spend_df_with_missing.loc[missing_indices, 'spend'] = np.nan
    
    fig3 = plot_missing_data_patterns(
        spend_df_with_missing,
        title="XKCD Style - Missing Data Detective Work",
        xkcd_style=True
    )
    plt.show()
    
    # 4. Correlation heatmap
    print("4. Correlation Heatmap (XKCD Style)")
    # Create correlation data
    pivot_df = spend_df.pivot_table(
        index='date',
        columns='channel',
        values='spend',
        fill_value=0
    )
    pivot_df = pivot_df.join(metrics_df.set_index('date'))
    
    fig4 = plot_correlation_heatmap(
        pivot_df,
        title="XKCD Style - Channel Correlation Magic",
        xkcd_style=True
    )
    plt.show()


def demo_global_xkcd():
    """Demonstrate global XKCD style."""
    print("\n🌍 Demonstrating Global XKCD Style...")
    
    # Enable global XKCD style
    enable_xkcd_style()
    
    # Create a simple plot
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.linspace(0, 10, 100)
    y = np.sin(x) * np.exp(-x/5)
    
    ax.plot(x, y, linewidth=3, color='xkcd:blue')
    ax.set_title('Global XKCD Style - Sinusoidal Decay', fontsize=16, fontweight='bold')
    ax.set_xlabel('Time', fontsize=12)
    ax.set_ylabel('Amplitude', fontsize=12)
    ax.grid(True, alpha=0.3)
    
    # Add fun annotation
    ax.annotate('Peak Value!', 
               xy=(x[np.argmax(y)], np.max(y)), 
               xytext=(20, 20), 
               textcoords='offset points',
               bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.8),
               arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2'))
    
    plt.tight_layout()
    plt.show()
    
    # Disable global XKCD style
    disable_xkcd_style()


def main():
    """Main demonstration function."""
    print("🎨 XKCD Style Plotting Demo for MMM Project")
    print("=" * 50)
    
    # Create sample data
    spend_df, metrics_df = create_sample_data()
    
    # Demonstrate XKCD plots
    demo_xkcd_plots(spend_df, metrics_df)
    
    # Demonstrate global XKCD style
    demo_global_xkcd()
    
    print("\n✅ XKCD Style Demo Complete!")
    print("\nKey Features:")
    print("- Hand-drawn appearance for presentations")
    print("- Fun annotations and callouts")
    print("- XKCD color palette")
    print("- Individual plot control or global style")
    print("- Perfect for stakeholder presentations!")


if __name__ == "__main__":
    main()
