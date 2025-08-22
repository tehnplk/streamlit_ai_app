import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import pandas as pd
from io import StringIO
from pydantic_ai.toolsets import FunctionToolset

# Configure matplotlib to handle Thai characters
plt.rcParams['font.family'] = ['Tahoma', 'DejaVu Sans', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# Try to find and use a system font that supports Thai characters
import matplotlib.font_manager as fm
import os

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
        
        # Create bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(df[x_col].astype(str), df[y_col])
        
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
        import os
        from datetime import datetime
        
        # Create temp directory if it doesn't exist
        temp_dir = os.path.join(os.path.dirname(__file__), 'temp', 'charts')
        os.makedirs(temp_dir, exist_ok=True)
        
        # Generate timestamped filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"bar_chart_{timestamp}.png"
        file_path = os.path.join(temp_dir, filename)
        
        # Save the chart
        plt.savefig(file_path, format='png', bbox_inches='tight', dpi=300)
        plt.close(fig)
        
        return file_path
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
        import os
        from datetime import datetime
        
        # Create temp directory if it doesn't exist
        temp_dir = os.path.join(os.path.dirname(__file__), 'temp', 'charts')
        os.makedirs(temp_dir, exist_ok=True)
        
        # Generate timestamped filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"line_chart_{timestamp}.png"
        file_path = os.path.join(temp_dir, filename)
        
        # Save the chart
        plt.savefig(file_path, format='png', bbox_inches='tight', dpi=300)
        plt.close(fig)
        
        return file_path
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
        import os
        from datetime import datetime
        
        # Create temp directory if it doesn't exist
        temp_dir = os.path.join(os.path.dirname(__file__), 'temp', 'charts')
        os.makedirs(temp_dir, exist_ok=True)
        
        # Generate timestamped filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"pie_chart_{timestamp}.png"
        file_path = os.path.join(temp_dir, filename)
        
        # Save the chart
        plt.savefig(file_path, format='png', bbox_inches='tight', dpi=300)
        plt.close(fig)
        
        return file_path
    except Exception as e:
        return f"Error generating pie chart: {str(e)}"


chart_toolsets = FunctionToolset(tools=[bar_chart, line_chart, pie_chart])
