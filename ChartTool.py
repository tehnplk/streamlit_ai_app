import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import pandas as pd
from io import StringIO
from pydantic_ai.toolsets import FunctionToolset


def bar_chart(data: str):
    """
    Generate bar chart from data

    Args:
        data (str): data in csv format

    Returns:
        str: bar chart in svg format
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
        
        # Add labels and title
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
        
        # Convert to SVG
        import io
        svg_buffer = io.StringIO()
        plt.savefig(svg_buffer, format='svg', bbox_inches='tight')
        svg_content = svg_buffer.getvalue()
        plt.close(fig)
        
        return svg_content
    except Exception as e:
        return f"Error generating bar chart: {str(e)}"


def line_chart(data: str):
    """
    Generate line chart from data

    Args:
        data (str): data in csv format

    Returns:
        str: line chart in svg format
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
        
        # Add labels and title
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_title(f'{y_col} by {x_col}')
        
        # Rotate x-axis labels if they are strings
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
        
        # Adjust layout
        plt.tight_layout()
        
        # Convert to SVG
        import io
        svg_buffer = io.StringIO()
        plt.savefig(svg_buffer, format='svg', bbox_inches='tight')
        svg_content = svg_buffer.getvalue()
        plt.close(fig)
        
        return svg_content
    except Exception as e:
        return f"Error generating line chart: {str(e)}"


def pie_chart(data: str):
    """
    Generate pie chart from data

    Args:
        data (str): data in csv format

    Returns:
        str: pie chart in svg format
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
        
        # Convert to SVG
        import io
        svg_buffer = io.StringIO()
        plt.savefig(svg_buffer, format='svg', bbox_inches='tight')
        svg_content = svg_buffer.getvalue()
        plt.close(fig)
        
        return svg_content
    except Exception as e:
        return f"Error generating pie chart: {str(e)}"


chart_toolsets = FunctionToolset(tools=[bar_chart, line_chart, pie_chart])
