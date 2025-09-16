"""
Data loading utilities for MMM project.

This module provides pure functions for loading and validating
marketing mix modeling data.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_csv_data(file_path: str, **kwargs) -> pd.DataFrame:
    """
    Load CSV data with standard MMM configurations.
    
    Args:
        file_path: Path to CSV file
        **kwargs: Additional arguments for pd.read_csv
        
    Returns:
        DataFrame with loaded data
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If data loading fails
    """
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {file_path}")
    
    try:
        # Default configurations for MMM data
        default_kwargs = {
            'parse_dates': True,
            'infer_datetime_format': True,
            'low_memory': False
        }
        default_kwargs.update(kwargs)
        
        df = pd.read_csv(file_path, **default_kwargs)
        logger.info(f"Loaded {len(df)} rows from {file_path}")
        
        return df
        
    except Exception as e:
        raise ValueError(f"Failed to load data from {file_path}: {str(e)}")


def load_marketing_spend_data(file_path: str) -> pd.DataFrame:
    """
    Load marketing spend data with MMM-specific preprocessing.
    
    Args:
        file_path: Path to marketing spend CSV
        
    Returns:
        DataFrame with marketing spend data
    """
    df = load_csv_data(file_path)
    
    # Standardize column names
    column_mapping = {
        'date': 'date',
        'Date': 'date',
        'DATE': 'date',
        'spend': 'spend',
        'Spend': 'spend',
        'SPEND': 'spend',
        'channel': 'channel',
        'Channel': 'channel',
        'CHANNEL': 'channel',
        'media': 'channel',
        'Media': 'channel'
    }
    
    df = df.rename(columns=column_mapping)
    
    # Ensure date column is datetime
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    
    return df


def load_business_metrics_data(file_path: str) -> pd.DataFrame:
    """
    Load business performance metrics data.
    
    Args:
        file_path: Path to business metrics CSV
        
    Returns:
        DataFrame with business metrics
    """
    df = load_csv_data(file_path)
    
    # Standardize column names
    column_mapping = {
        'date': 'date',
        'Date': 'date',
        'DATE': 'date',
        'revenue': 'revenue',
        'Revenue': 'revenue',
        'REVENUE': 'revenue',
        'sales': 'revenue',
        'Sales': 'revenue',
        'prescriptions': 'prescriptions',
        'Prescriptions': 'prescriptions',
        'PRESCRIPTIONS': 'prescriptions'
    }
    
    df = df.rename(columns=column_mapping)
    
    # Ensure date column is datetime
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    
    return df


def validate_data_quality(df: pd.DataFrame, 
                         required_columns: List[str],
                         date_column: str = 'date') -> Dict[str, any]:
    """
    Validate data quality for MMM analysis.
    
    Args:
        df: DataFrame to validate
        required_columns: List of required column names
        date_column: Name of date column
        
    Returns:
        Dictionary with validation results
    """
    validation_results = {
        'is_valid': True,
        'issues': [],
        'summary': {}
    }
    
    # Check required columns
    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        validation_results['is_valid'] = False
        validation_results['issues'].append(f"Missing columns: {missing_columns}")
    
    # Check data types
    if date_column in df.columns:
        if not pd.api.types.is_datetime64_any_dtype(df[date_column]):
            validation_results['issues'].append(f"Date column '{date_column}' is not datetime type")
    
    # Check for missing values
    missing_pct = df.isnull().sum() / len(df) * 100
    high_missing = missing_pct[missing_pct > 10]
    if len(high_missing) > 0:
        validation_results['issues'].append(f"High missing values (>10%): {high_missing.to_dict()}")
    
    # Check for duplicates
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        validation_results['issues'].append(f"Found {duplicates} duplicate rows")
    
    # Summary statistics
    validation_results['summary'] = {
        'shape': df.shape,
        'date_range': {
            'start': df[date_column].min() if date_column in df.columns else None,
            'end': df[date_column].max() if date_column in df.columns else None
        },
        'missing_values': missing_pct.to_dict(),
        'duplicates': duplicates
    }
    
    if validation_results['issues']:
        validation_results['is_valid'] = False
    
    return validation_results


def get_data_summary(df: pd.DataFrame) -> Dict[str, any]:
    """
    Generate comprehensive data summary for EDA.
    
    Args:
        df: DataFrame to summarize
        
    Returns:
        Dictionary with data summary
    """
    summary = {
        'shape': df.shape,
        'columns': list(df.columns),
        'dtypes': df.dtypes.to_dict(),
        'missing_values': df.isnull().sum().to_dict(),
        'numeric_summary': df.describe().to_dict() if len(df.select_dtypes(include=[np.number]).columns) > 0 else {},
        'categorical_summary': {}
    }
    
    # Categorical columns summary
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    for col in categorical_cols:
        summary['categorical_summary'][col] = {
            'unique_values': df[col].nunique(),
            'top_values': df[col].value_counts().head().to_dict()
        }
    
    return summary
