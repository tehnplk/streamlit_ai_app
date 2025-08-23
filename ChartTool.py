import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import pandas as pd
from io import StringIO
from pydantic_ai.toolsets import FunctionToolset
import matplotlib.font_manager as fm
import os
import numpy as np
from datetime import datetime

# Configure matplotlib to handle Thai characters
plt.rcParams['font.family'] = ['Tahoma', 'DejaVu Sans', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# Try to find and use a system font that supports Thai characters
def find_thai_font():
    # Common Thai font names
    thai_fonts = [
        'Tahoma', 'Microsoft Sans Serif', 'Arial Unicode MS',
        'DejaVu Sans', 'Liberation Sans', 'Noto Sans Thai'
    ]
    
    # Get all available fonts
    available_fonts = {f.name for f in fm.fontManager.ttflist}
    
    # Find the first matching Thai font
    for font in thai_fonts:
        if font in available_fonts:
            return font
    
    # If no Thai font found, return None
    return None

# Set Thai font if available
thai_font = find_thai_font()
if thai_font:
    plt.rcParams['font.family'] = [thai_font, 'DejaVu Sans', 'sans-serif']


def save_chart(fig, filename):
    """
    Save chart to file and return relative file path
    
    Args:
        fig: matplotlib figure object
        filename: name of the file to save
    
    Returns:
        str: relative file path to the saved chart (./temp/charts/filename.png)
    """
    # Create temp directory if it doesn't exist
    temp_dir = os.path.join(os.path.dirname(__file__), 'temp', 'charts')
    os.makedirs(temp_dir, exist_ok=True)
    
    # Full file path
    file_path = os.path.join(temp_dir, filename)
    
    # Save the chart
    plt.savefig(file_path, format='png', bbox_inches='tight', dpi=300)
    plt.close(fig)
    
    # Return relative path
    return f"./temp/charts/{filename}"


def bar_chart(data: str):
    """
    Generate bar chart from data

    Args:
        data (str): data in csv format

    Returns:
        str: file path to the saved bar chart
    """
    try:
        # Convert CSV to DataFrame
        df = pd.read_csv(StringIO(data))
        
        # Use first column as x-axis and second column as y-axis
        x_col = df.columns[0]
        y_col = df.columns[1] if len(df.columns) > 1 else df.columns[0]
        
        # Create bar chart with random colors for each bar
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = plt.cm.Set3(np.linspace(0, 1, len(df)))
        bars = ax.bar(df[x_col].astype(str), df[y_col], color=colors)
        
        # Add labels and title with proper font
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_title(f'{y_col} by {x_col}')
        
        # Rotate x-axis labels if they are strings
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.1f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')
        
        # Adjust layout
        plt.tight_layout()
        
        # Save to project temp folder with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"bar_chart_{timestamp}.png"
        return save_chart(fig, filename)
    except Exception as e:
        return f"Error generating bar chart: {str(e)}"


def line_chart(data: str):
    """
    Generate line chart from data

    Args:
        data (str): data in csv format

    Returns:
        str: file path to the saved line chart
    """
    try:
        # Convert CSV to DataFrame
        df = pd.read_csv(StringIO(data))
        
        # Use first column as x-axis and second column as y-axis
        x_col = df.columns[0]
        y_col = df.columns[1] if len(df.columns) > 1 else df.columns[0]
        
        # Create line chart
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(df[x_col].astype(str), df[y_col], marker='o')
        
        # Add labels and title with proper font
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_title(f'{y_col} by {x_col}')
        
        # Rotate x-axis labels if they are strings
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
        
        # Adjust layout
        plt.tight_layout()
        
        # Save to project temp folder with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"line_chart_{timestamp}.png"
        return save_chart(fig, filename)
    except Exception as e:
        return f"Error generating line chart: {str(e)}"


def pie_chart(data: str):
    """
    Generate pie chart from data

    Args:
        data (str): data in csv format

    Returns:
        str: file path to the saved pie chart
    """
    try:
        # Convert CSV to DataFrame
        df = pd.read_csv(StringIO(data))
        
        # Use first column as labels and second column as values
        labels_col = df.columns[0]
        values_col = df.columns[1] if len(df.columns) > 1 else df.columns[0]
        
        # Create pie chart
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.pie(df[values_col], labels=df[labels_col].astype(str), autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        ax.set_title(f'{values_col} Distribution')
        
        # Adjust layout
        plt.tight_layout()
        
        # Save to project temp folder with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"pie_chart_{timestamp}.png"
        return save_chart(fig, filename)
    except Exception as e:
        return f"Error generating pie chart: {str(e)}"


def histogram(data: str):
    """
    Generate histogram from data

    Args:
        data (str): data in csv format

    Returns:
        str: file path to the saved histogram
    """
    try:
        # Convert CSV to DataFrame
        df = pd.read_csv(StringIO(data))
        
        # Use first column for histogram data
        col = df.columns[0]
        
        # Create histogram
        fig, ax = plt.subplots(figsize=(10, 6))
        n, bins, patches = ax.hist(df[col], bins=20, color='#20B2AA', edgecolor='white', alpha=0.8)
        
        # Add value labels on top of bars
        for i in range(len(n)):
            if n[i] > 0:  # Only show label if there's a value
                ax.text(bins[i] + (bins[i+1] - bins[i])/2, n[i] + max(n)*0.01, 
                       f'{int(n[i])}', ha='center', va='bottom', 
                       fontweight='bold', color='white', fontsize=10)
        
        # Add labels and title with proper font
        ax.set_xlabel(col)
        ax.set_ylabel('Number of students')
        ax.set_title(f'Distribution of {col}')
        
        # Remove grid and set background color
        ax.set_facecolor('white')
        ax.grid(False)
        
        # Adjust layout
        plt.tight_layout()
        
        # Save to project temp folder with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"histogram_{timestamp}.png"
        return save_chart(fig, filename)
    except Exception as e:
        return f"Error generating histogram: {str(e)}"


chart_toolsets = FunctionToolset(tools=[bar_chart, line_chart, pie_chart, histogram])
