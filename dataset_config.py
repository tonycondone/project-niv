#!/usr/bin/env python3
"""
PROJECT NIV - Dataset Configuration System
Manages configurations for different types of datasets
"""

import json
import os
from typing import Dict, List, Any, Optional
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table

console = Console()

class DatasetConfig:
    def __init__(self, config_file: str = 'dataset_configs.json'):
        self.config_file = config_file
        self.configs = self.load_configs()
        
    def load_configs(self) -> Dict[str, Any]:
        """Load existing configurations"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                console.print(f"⚠️ [yellow]Error loading config file: {e}[/yellow]")
                return self.get_default_configs()
        else:
            return self.get_default_configs()
    
    def save_configs(self):
        """Save configurations to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.configs, f, indent=2)
            console.print(f"✅ [green]Configurations saved to {self.config_file}[/green]")
        except Exception as e:
            console.print(f"❌ [red]Error saving config file: {e}[/red]")
    
    def get_default_configs(self) -> Dict[str, Any]:
        """Get default configurations for common dataset types"""
        return {
            "sales_data": {
                "name": "Sales Data",
                "description": "Sales transactions and revenue data",
                "expected_columns": {
                    "date_columns": ["date", "timestamp", "month", "year", "period"],
                    "numeric_columns": ["sales", "revenue", "amount", "quantity", "price"],
                    "categorical_columns": ["product", "category", "region", "customer_type"]
                },
                "primary_metrics": ["sales", "revenue", "amount"],
                "kpi_focus": ["total_sales", "average_sales", "growth_rate", "top_products"],
                "visualization_preferences": ["time_series", "bar_chart", "pie_chart"],
                "date_format": "%Y-%m-%d",
                "currency_symbol": "$"
            },
            "financial_data": {
                "name": "Financial Data",
                "description": "Financial statements and metrics",
                "expected_columns": {
                    "date_columns": ["date", "period", "quarter", "fiscal_year"],
                    "numeric_columns": ["revenue", "expenses", "profit", "assets", "liabilities"],
                    "categorical_columns": ["account_type", "department", "category"]
                },
                "primary_metrics": ["revenue", "profit", "expenses"],
                "kpi_focus": ["total_revenue", "profit_margin", "expense_ratio", "growth_rate"],
                "visualization_preferences": ["time_series", "waterfall", "bar_chart"],
                "date_format": "%Y-%m-%d",
                "currency_symbol": "$"
            },
            "customer_data": {
                "name": "Customer Data",
                "description": "Customer demographics and behavior",
                "expected_columns": {
                    "date_columns": ["registration_date", "last_purchase", "birth_date"],
                    "numeric_columns": ["age", "income", "purchase_amount", "frequency"],
                    "categorical_columns": ["gender", "location", "segment", "status"]
                },
                "primary_metrics": ["purchase_amount", "frequency", "age"],
                "kpi_focus": ["customer_count", "average_age", "total_purchases", "segments"],
                "visualization_preferences": ["histogram", "bar_chart", "scatter_plot"],
                "date_format": "%Y-%m-%d",
                "currency_symbol": "$"
            },
            "inventory_data": {
                "name": "Inventory Data",
                "description": "Stock levels and inventory management",
                "expected_columns": {
                    "date_columns": ["date", "last_updated", "reorder_date"],
                    "numeric_columns": ["quantity", "cost", "price", "reorder_level"],
                    "categorical_columns": ["product_id", "category", "supplier", "status"]
                },
                "primary_metrics": ["quantity", "cost", "price"],
                "kpi_focus": ["total_inventory", "low_stock_items", "inventory_value", "turnover"],
                "visualization_preferences": ["bar_chart", "heatmap", "scatter_plot"],
                "date_format": "%Y-%m-%d",
                "currency_symbol": "$"
            },
            "web_analytics": {
                "name": "Web Analytics",
                "description": "Website traffic and user behavior",
                "expected_columns": {
                    "date_columns": ["date", "timestamp", "session_start"],
                    "numeric_columns": ["page_views", "sessions", "bounce_rate", "duration"],
                    "categorical_columns": ["source", "medium", "device", "country"]
                },
                "primary_metrics": ["page_views", "sessions", "bounce_rate"],
                "kpi_focus": ["total_sessions", "average_duration", "bounce_rate", "top_sources"],
                "visualization_preferences": ["time_series", "pie_chart", "bar_chart"],
                "date_format": "%Y-%m-%d",
                "currency_symbol": ""
            },
            "hr_data": {
                "name": "HR Data",
                "description": "Employee and human resources data",
                "expected_columns": {
                    "date_columns": ["hire_date", "birth_date", "review_date"],
                    "numeric_columns": ["salary", "age", "years_experience", "rating"],
                    "categorical_columns": ["department", "position", "gender", "status"]
                },
                "primary_metrics": ["salary", "rating", "years_experience"],
                "kpi_focus": ["employee_count", "average_salary", "turnover_rate", "satisfaction"],
                "visualization_preferences": ["histogram", "bar_chart", "box_plot"],
                "date_format": "%Y-%m-%d",
                "currency_symbol": "$"
            },
            "generic": {
                "name": "Generic Dataset",
                "description": "General purpose data analysis",
                "expected_columns": {
                    "date_columns": [],
                    "numeric_columns": [],
                    "categorical_columns": []
                },
                "primary_metrics": [],
                "kpi_focus": ["data_overview", "quality_metrics", "distribution_analysis"],
                "visualization_preferences": ["histogram", "bar_chart", "correlation_heatmap"],
                "date_format": "%Y-%m-%d",
                "currency_symbol": ""
            }
        }
    
    def detect_dataset_type(self, column_names: List[str]) -> str:
        """Detect the most likely dataset type based on column names"""
        column_names_lower = [col.lower() for col in column_names]
        
        best_match = "generic"
        best_score = 0
        
        for config_type, config in self.configs.items():
            if config_type == "generic":
                continue
                
            score = 0
            expected_cols = config["expected_columns"]
            
            # Check for matching column patterns
            for col_type, expected_names in expected_cols.items():
                for expected_name in expected_names:
                    if any(expected_name in col_name for col_name in column_names_lower):
                        score += 1
            
            # Bonus for primary metrics
            for metric in config["primary_metrics"]:
                if any(metric in col_name for col_name in column_names_lower):
                    score += 2
            
            if score > best_score:
                best_score = score
                best_match = config_type
        
        return best_match
    
    def get_config_for_dataset(self, dataset_type: str) -> Dict[str, Any]:
        """Get configuration for a specific dataset type"""
        return self.configs.get(dataset_type, self.configs["generic"])
    
    def create_custom_config(self, dataset_path: str, column_names: List[str]) -> Dict[str, Any]:
        """Create a custom configuration interactively"""
        console.print("🛠️ [bold blue]Creating Custom Dataset Configuration[/bold blue]")
        
        # Detect suggested type
        suggested_type = self.detect_dataset_type(column_names)
        console.print(f"💡 [yellow]Suggested dataset type: {suggested_type}[/yellow]")
        
        # Get basic info
        config_name = Prompt.ask("Enter configuration name", default=os.path.basename(dataset_path).replace('.csv', ''))
        description = Prompt.ask("Enter dataset description", default="Custom dataset configuration")
        
        # Show columns and let user categorize
        console.print("\n📋 [bold]Column Categorization[/bold]")
        console.print("Available columns:")
        
        col_table = Table()
        col_table.add_column("Index", style="dim")
        col_table.add_column("Column Name", style="bold")
        
        for i, col in enumerate(column_names):
            col_table.add_row(str(i), col)
        
        console.print(col_table)
        
        # Categorize columns
        date_columns = self._select_columns("date/time columns", column_names)
        numeric_columns = self._select_columns("numeric columns", column_names)
        categorical_columns = self._select_columns("categorical columns", column_names)
        
        # Select primary metrics
        if numeric_columns:
            console.print(f"\n📊 Available numeric columns: {', '.join(numeric_columns)}")
            primary_metrics = self._select_columns("primary metric columns", numeric_columns)
        else:
            primary_metrics = []
        
        # Create configuration
        custom_config = {
            "name": config_name,
            "description": description,
            "expected_columns": {
                "date_columns": date_columns,
                "numeric_columns": numeric_columns,
                "categorical_columns": categorical_columns
            },
            "primary_metrics": primary_metrics,
            "kpi_focus": self._generate_kpi_focus(date_columns, numeric_columns, categorical_columns),
            "visualization_preferences": self._suggest_visualizations(date_columns, numeric_columns, categorical_columns),
            "date_format": "%Y-%m-%d",
            "currency_symbol": Prompt.ask("Currency symbol (if applicable)", default="$")
        }
        
        # Save configuration
        if Confirm.ask("Save this configuration for future use?"):
            config_key = config_name.lower().replace(' ', '_')
            self.configs[config_key] = custom_config
            self.save_configs()
        
        return custom_config
    
    def _select_columns(self, column_type: str, available_columns: List[str]) -> List[str]:
        """Helper to select columns of a specific type"""
        if not available_columns:
            return []
        
        console.print(f"\n🎯 Select {column_type}:")
        console.print("Enter column indices separated by commas (e.g., 0,2,5) or 'none' for no columns")
        
        while True:
            selection = Prompt.ask(f"Select {column_type}", default="none")
            
            if selection.lower() == 'none':
                return []
            
            try:
                indices = [int(i.strip()) for i in selection.split(',')]
                selected_columns = [available_columns[i] for i in indices if 0 <= i < len(available_columns)]
                
                if selected_columns:
                    console.print(f"✅ Selected: {', '.join(selected_columns)}")
                    return selected_columns
                else:
                    console.print("❌ No valid columns selected")
                    
            except (ValueError, IndexError):
                console.print("❌ Invalid input. Please enter valid column indices.")
    
    def _generate_kpi_focus(self, date_cols: List[str], numeric_cols: List[str], cat_cols: List[str]) -> List[str]:
        """Generate appropriate KPI focus based on column types"""
        kpis = ["data_overview", "quality_metrics"]
        
        if numeric_cols:
            kpis.extend(["summary_statistics", "distribution_analysis"])
            
        if date_cols and numeric_cols:
            kpis.append("trend_analysis")
            
        if cat_cols and numeric_cols:
            kpis.append("category_analysis")
            
        if len(numeric_cols) > 1:
            kpis.append("correlation_analysis")
            
        return kpis
    
    def _suggest_visualizations(self, date_cols: List[str], numeric_cols: List[str], cat_cols: List[str]) -> List[str]:
        """Suggest appropriate visualizations based on column types"""
        viz = []
        
        if date_cols and numeric_cols:
            viz.append("time_series")
            
        if cat_cols and numeric_cols:
            viz.append("bar_chart")
            
        if numeric_cols:
            viz.append("histogram")
            
        if len(numeric_cols) > 1:
            viz.append("correlation_heatmap")
            
        if cat_cols:
            viz.append("pie_chart")
            
        if not viz:
            viz = ["bar_chart", "histogram"]
            
        return viz
    
    def list_available_configs(self):
        """Display all available configurations"""
        console.print("📋 [bold blue]Available Dataset Configurations[/bold blue]")
        
        config_table = Table()
        config_table.add_column("Type", style="bold yellow")
        config_table.add_column("Name", style="green")
        config_table.add_column("Description", style="blue")
        config_table.add_column("Primary Metrics", style="magenta")
        
        for config_type, config in self.configs.items():
            primary_metrics = ", ".join(config.get("primary_metrics", [])[:3])
            if len(config.get("primary_metrics", [])) > 3:
                primary_metrics += "..."
                
            config_table.add_row(
                config_type,
                config["name"],
                config["description"][:50] + "..." if len(config["description"]) > 50 else config["description"],
                primary_metrics
            )
        
        console.print(config_table)
    
    def get_config_recommendations(self, column_names: List[str]) -> Dict[str, Any]:
        """Get configuration recommendations for a dataset"""
        detected_type = self.detect_dataset_type(column_names)
        config = self.get_config_for_dataset(detected_type)
        
        recommendations = {
            "detected_type": detected_type,
            "confidence": self._calculate_confidence(column_names, config),
            "config": config,
            "suggestions": self._generate_suggestions(column_names, config)
        }
        
        return recommendations
    
    def _calculate_confidence(self, column_names: List[str], config: Dict[str, Any]) -> float:
        """Calculate confidence score for dataset type detection"""
        column_names_lower = [col.lower() for col in column_names]
        
        total_expected = 0
        matches = 0
        
        for col_type, expected_names in config["expected_columns"].items():
            total_expected += len(expected_names)
            for expected_name in expected_names:
                if any(expected_name in col_name for col_name in column_names_lower):
                    matches += 1
        
        if total_expected == 0:
            return 0.0
        
        return min(1.0, matches / total_expected)
    
    def _generate_suggestions(self, column_names: List[str], config: Dict[str, Any]) -> List[str]:
        """Generate suggestions for improving dataset structure"""
        suggestions = []
        column_names_lower = [col.lower() for col in column_names]
        
        # Check for missing important columns
        for metric in config["primary_metrics"]:
            if not any(metric in col_name for col_name in column_names_lower):
                suggestions.append(f"Consider adding a '{metric}' column for better analysis")
        
        # Check for date columns
        if config["expected_columns"]["date_columns"] and not any(
            any(date_col in col_name for col_name in column_names_lower)
            for date_col in config["expected_columns"]["date_columns"]
        ):
            suggestions.append("Consider adding date/time columns for temporal analysis")
        
        return suggestions[:3]  # Return top 3 suggestions

def main():
    """Test the configuration system"""
    config_manager = DatasetConfig()
    config_manager.list_available_configs()
    
    # Test detection
    sample_columns = ["date", "sales", "product", "region"]
    recommendations = config_manager.get_config_recommendations(sample_columns)
    
    console.print(f"\n🎯 [bold]Detection Results:[/bold]")
    console.print(f"Detected Type: {recommendations['detected_type']}")
    console.print(f"Confidence: {recommendations['confidence']:.2f}")

if __name__ == "__main__":
    main()