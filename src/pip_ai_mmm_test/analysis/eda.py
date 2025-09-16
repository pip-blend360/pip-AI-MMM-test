"""
Exploratory Data Analysis functions for MMM project.

This module provides reusable functions for EDA that can be
used both in notebooks and scripts.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Optional, Tuple
import warnings

# Set plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# XKCD style setup
plt.rcParams['font.family'] = 'xkcd'
plt.rcParams['font.size'] = 12


def enable_xkcd_style():
    """
    Enable XKCD hand-drawn style globally for all plots.
    
    This function sets matplotlib to use XKCD-style rendering
    for all subsequent plots.
    """
    plt.xkcd()
    print("🎨 XKCD style enabled! All plots will now have a hand-drawn appearance.")


def disable_xkcd_style():
    """
    Disable XKCD style and return to normal matplotlib styling.
    """
    plt.rcdefaults()
    print("📊 XKCD style disabled. Back to normal matplotlib styling.")


def plot_time_series(df: pd.DataFrame, 
                    date_col: str, 
                    value_cols: List[str],
                    title: str = "Time Series Plot",
                    figsize: Tuple[int, int] = (12, 6),
                    xkcd_style: bool = False) -> plt.Figure:
    """
    Create time series plots for MMM data.
    
    Args:
        df: DataFrame with time series data
        date_col: Name of date column
        value_cols: List of value columns to plot
        title: Plot title
        figsize: Figure size
        xkcd_style: Whether to use XKCD hand-drawn style
        
    Returns:
        Matplotlib figure
    """
    if xkcd_style:
        with plt.xkcd():
            fig, axes = plt.subplots(len(value_cols), 1, figsize=figsize, sharex=True)
            if len(value_cols) == 1:
                axes = [axes]
            
            for i, col in enumerate(value_cols):
                axes[i].plot(df[date_col], df[col], linewidth=3, color='xkcd:blue')
                axes[i].set_title(f"{col} Over Time", fontsize=14, fontweight='bold')
                axes[i].set_ylabel(col, fontsize=12)
                axes[i].grid(True, alpha=0.3)
                # Add some fun annotations
                max_val = df[col].max()
                max_date = df[df[col] == max_val][date_col].iloc[0]
                axes[i].annotate(f'Peak: {max_val:,.0f}', 
                               xy=(max_date, max_val), 
                               xytext=(10, 10), 
                               textcoords='offset points',
                               bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7),
                               arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
            
            plt.suptitle(title, fontsize=16, fontweight='bold')
            plt.tight_layout()
    else:
        fig, axes = plt.subplots(len(value_cols), 1, figsize=figsize, sharex=True)
        if len(value_cols) == 1:
            axes = [axes]
        
        for i, col in enumerate(value_cols):
            axes[i].plot(df[date_col], df[col], linewidth=2)
            axes[i].set_title(f"{col} Over Time", fontsize=12, fontweight='bold')
            axes[i].set_ylabel(col)
            axes[i].grid(True, alpha=0.3)
        
        plt.suptitle(title, fontsize=14, fontweight='bold')
        plt.tight_layout()
    
    return fig


def plot_channel_spend_distribution(df: pd.DataFrame,
                                  channel_col: str,
                                  spend_col: str,
                                  title: str = "Marketing Spend by Channel",
                                  figsize: Tuple[int, int] = (10, 6),
                                  xkcd_style: bool = False) -> plt.Figure:
    """
    Plot marketing spend distribution across channels.
    
    Args:
        df: DataFrame with marketing data
        channel_col: Name of channel column
        spend_col: Name of spend column
        title: Plot title
        figsize: Figure size
        xkcd_style: Whether to use XKCD hand-drawn style
        
    Returns:
        Matplotlib figure
    """
    # Calculate channel spend
    channel_spend = df.groupby(channel_col)[spend_col].sum().sort_values(ascending=False)
    
    if xkcd_style:
        with plt.xkcd():
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
            
            # Bar plot with XKCD style
            bars = ax1.bar(range(len(channel_spend)), channel_spend.values, 
                          color='xkcd:sky blue', edgecolor='black', linewidth=2)
            ax1.set_title('Total Spend by Channel', fontweight='bold', fontsize=14)
            ax1.set_xlabel('Channel', fontsize=12)
            ax1.set_ylabel('Total Spend', fontsize=12)
            ax1.set_xticks(range(len(channel_spend)))
            ax1.set_xticklabels(channel_spend.index, rotation=45, ha='right')
            
            # Add fun annotations
            max_channel = channel_spend.index[0]
            max_spend = channel_spend.iloc[0]
            ax1.annotate(f'Biggest Spender!\n{max_channel}: ${max_spend:,.0f}', 
                        xy=(0, max_spend), 
                        xytext=(20, 20), 
                        textcoords='offset points',
                        bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.8),
                        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2'))
            
            # Pie chart with XKCD style
            colors = ['xkcd:red', 'xkcd:blue', 'xkcd:green', 'xkcd:orange', 'xkcd:purple', 'xkcd:pink']
            wedges, texts, autotexts = ax2.pie(channel_spend.values, 
                                              labels=channel_spend.index,
                                              autopct='%1.1f%%', 
                                              startangle=90,
                                              colors=colors[:len(channel_spend)])
            ax2.set_title('Spend Distribution', fontweight='bold', fontsize=14)
            
            # Make percentage text bold
            for autotext in autotexts:
                autotext.set_fontweight('bold')
                autotext.set_fontsize(10)
            
            plt.suptitle(title, fontsize=16, fontweight='bold')
            plt.tight_layout()
    else:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
        
        # Bar plot
        channel_spend.plot(kind='bar', ax=ax1, color='skyblue', edgecolor='black')
        ax1.set_title('Total Spend by Channel', fontweight='bold')
        ax1.set_xlabel('Channel')
        ax1.set_ylabel('Total Spend')
        ax1.tick_params(axis='x', rotation=45)
        
        # Pie chart
        channel_spend.plot(kind='pie', ax=ax2, autopct='%1.1f%%', startangle=90)
        ax2.set_title('Spend Distribution', fontweight='bold')
        ax2.set_ylabel('')
        
        plt.suptitle(title, fontsize=14, fontweight='bold')
        plt.tight_layout()
    
    return fig


def plot_correlation_heatmap(df: pd.DataFrame,
                           numeric_cols: Optional[List[str]] = None,
                           title: str = "Correlation Heatmap",
                           figsize: Tuple[int, int] = (10, 8),
                           xkcd_style: bool = False) -> plt.Figure:
    """
    Create correlation heatmap for numeric columns.
    
    Args:
        df: DataFrame
        numeric_cols: List of numeric columns (if None, auto-detect)
        title: Plot title
        figsize: Figure size
        xkcd_style: Whether to use XKCD hand-drawn style
        
    Returns:
        Matplotlib figure
    """
    if numeric_cols is None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Calculate correlation matrix
    corr_matrix = df[numeric_cols].corr()
    
    if xkcd_style:
        with plt.xkcd():
            fig, ax = plt.subplots(figsize=figsize)
            mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
            
            # Create heatmap with XKCD colors
            im = ax.imshow(corr_matrix, cmap='xkcd:rainbow', aspect='auto')
            
            # Add correlation values as text
            for i in range(len(corr_matrix.columns)):
                for j in range(len(corr_matrix.columns)):
                    if not mask[i, j]:  # Only show lower triangle
                        text = ax.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                                     ha="center", va="center", color="black", fontweight='bold')
            
            # Set ticks and labels
            ax.set_xticks(range(len(corr_matrix.columns)))
            ax.set_yticks(range(len(corr_matrix.columns)))
            ax.set_xticklabels(corr_matrix.columns, rotation=45, ha='right')
            ax.set_yticklabels(corr_matrix.columns)
            
            # Add colorbar
            cbar = plt.colorbar(im, ax=ax, shrink=0.8)
            cbar.set_label('Correlation', fontweight='bold')
            
            # Add fun title
            ax.set_title(f'{title}\n(Hand-drawn correlation magic!)', 
                        fontsize=16, fontweight='bold', pad=20)
            
            plt.tight_layout()
    else:
        # Create heatmap
        fig, ax = plt.subplots(figsize=figsize)
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        
        sns.heatmap(corr_matrix, 
                    mask=mask,
                    annot=True, 
                    cmap='coolwarm', 
                    center=0,
                    square=True,
                    fmt='.2f',
                    cbar_kws={"shrink": .8})
        
        plt.title(title, fontsize=14, fontweight='bold')
        plt.tight_layout()
    
    return fig


def plot_missing_data_patterns(df: pd.DataFrame,
                              title: str = "Missing Data Patterns",
                              figsize: Tuple[int, int] = (12, 6),
                              xkcd_style: bool = False) -> plt.Figure:
    """
    Visualize missing data patterns.
    
    Args:
        df: DataFrame
        title: Plot title
        figsize: Figure size
        xkcd_style: Whether to use XKCD hand-drawn style
        
    Returns:
        Matplotlib figure
    """
    if xkcd_style:
        with plt.xkcd():
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
            
            # Missing data by column
            missing_data = df.isnull().sum().sort_values(ascending=False)
            missing_pct = (missing_data / len(df)) * 100
            
            # Only show columns with missing data
            missing_cols = missing_pct[missing_pct > 0]
            
            if len(missing_cols) > 0:
                bars = ax1.bar(range(len(missing_cols)), missing_cols.values, 
                              color='xkcd:red', edgecolor='black', linewidth=2)
                ax1.set_title('Missing Data by Column', fontweight='bold', fontsize=14)
                ax1.set_ylabel('Missing Percentage', fontsize=12)
                ax1.set_xticks(range(len(missing_cols)))
                ax1.set_xticklabels(missing_cols.index, rotation=45, ha='right')
                
                # Add fun annotation
                max_missing = missing_cols.max()
                max_col = missing_cols.idxmax()
                ax1.annotate(f'Most Missing!\n{max_col}: {max_missing:.1f}%', 
                            xy=(0, max_missing), 
                            xytext=(20, 20), 
                            textcoords='offset points',
                            bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.8),
                            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2'))
            else:
                ax1.text(0.5, 0.5, 'No Missing Data!\n🎉', 
                        ha='center', va='center', fontsize=20, fontweight='bold',
                        transform=ax1.transAxes)
                ax1.set_title('Missing Data by Column', fontweight='bold', fontsize=14)
            
            # Missing data pattern matrix (sample)
            sample_size = min(1000, len(df))
            df_sample = df.sample(n=sample_size) if len(df) > sample_size else df
            
            # Create a simple missing data visualization
            missing_matrix = df_sample.isnull().astype(int)
            im = ax2.imshow(missing_matrix.T, cmap='xkcd:red', aspect='auto')
            ax2.set_title('Missing Data Pattern\n(Sample)', fontweight='bold', fontsize=14)
            ax2.set_xlabel('Row Index', fontsize=12)
            ax2.set_ylabel('Columns', fontsize=12)
            
            # Set y-axis labels
            ax2.set_yticks(range(len(df.columns)))
            ax2.set_yticklabels(df.columns)
            
            plt.suptitle(f'{title}\n(Hand-drawn data detective work!)', 
                        fontsize=16, fontweight='bold')
            plt.tight_layout()
    else:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
        
        # Missing data by column
        missing_data = df.isnull().sum().sort_values(ascending=False)
        missing_pct = (missing_data / len(df)) * 100
        
        missing_pct[missing_pct > 0].plot(kind='bar', ax=ax1, color='coral')
        ax1.set_title('Missing Data by Column', fontweight='bold')
        ax1.set_ylabel('Missing Percentage')
        ax1.tick_params(axis='x', rotation=45)
        
        # Missing data pattern matrix (sample)
        sample_size = min(1000, len(df))
        df_sample = df.sample(n=sample_size) if len(df) > sample_size else df
        
        sns.heatmap(df_sample.isnull(), 
                    yticklabels=False, 
                    cbar=True, 
                    ax=ax2,
                    cmap='viridis')
        ax2.set_title('Missing Data Pattern (Sample)', fontweight='bold')
        
        plt.suptitle(title, fontsize=14, fontweight='bold')
        plt.tight_layout()
    
    return fig


def analyze_channel_performance(df: pd.DataFrame,
                               channel_col: str,
                               spend_col: str,
                               revenue_col: str,
                               date_col: str) -> Dict[str, any]:
    """
    Analyze channel performance metrics.
    
    Args:
        df: DataFrame with marketing and revenue data
        channel_col: Name of channel column
        spend_col: Name of spend column
        revenue_col: Name of revenue column
        date_col: Name of date column
        
    Returns:
        Dictionary with channel performance metrics
    """
    # Calculate ROI by channel
    channel_metrics = df.groupby(channel_col).agg({
        spend_col: ['sum', 'mean', 'std'],
        revenue_col: ['sum', 'mean', 'std']
    }).round(2)
    
    # Flatten column names
    channel_metrics.columns = ['_'.join(col).strip() for col in channel_metrics.columns]
    
    # Calculate ROI
    channel_metrics['roi'] = (channel_metrics[f'{revenue_col}_sum'] / 
                             channel_metrics[f'{spend_col}_sum']).round(2)
    
    # Calculate efficiency (revenue per dollar spent)
    channel_metrics['efficiency'] = (channel_metrics[f'{revenue_col}_sum'] / 
                                    channel_metrics[f'{spend_col}_sum']).round(2)
    
    # Sort by ROI
    channel_metrics = channel_metrics.sort_values('roi', ascending=False)
    
    return {
        'channel_metrics': channel_metrics,
        'summary': {
            'total_channels': len(channel_metrics),
            'avg_roi': channel_metrics['roi'].mean(),
            'best_channel': channel_metrics.index[0],
            'worst_channel': channel_metrics.index[-1]
        }
    }


def detect_seasonality(df: pd.DataFrame,
                      date_col: str,
                      value_col: str,
                      period: str = 'M') -> Dict[str, any]:
    """
    Detect seasonality patterns in time series data.
    
    Args:
        df: DataFrame with time series data
        date_col: Name of date column
        value_col: Name of value column
        period: Aggregation period ('D', 'W', 'M', 'Q')
        
    Returns:
        Dictionary with seasonality analysis
    """
    # Ensure date column is datetime
    df_analysis = df.copy()
    df_analysis[date_col] = pd.to_datetime(df_analysis[date_col])
    
    # Set date as index
    df_analysis = df_analysis.set_index(date_col)
    
    # Resample to specified period
    df_resampled = df_analysis[value_col].resample(period).sum()
    
    # Calculate seasonal decomposition
    from statsmodels.tsa.seasonal import seasonal_decompose
    
    decomposition = seasonal_decompose(df_resampled, model='additive', period=12)
    
    # Calculate seasonality strength
    seasonal_strength = np.var(decomposition.seasonal) / np.var(df_resampled)
    
    return {
        'seasonal_strength': seasonal_strength,
        'decomposition': decomposition,
        'monthly_patterns': df_resampled.groupby(df_resampled.index.month).mean().to_dict(),
        'is_seasonal': seasonal_strength > 0.1  # Threshold for seasonality
    }
