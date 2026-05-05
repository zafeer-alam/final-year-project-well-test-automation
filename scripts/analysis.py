"""
CBM Well Test Automation - Analysis Module
This module analyzes Coal Bed Methane (CBM) well test data including Horner plots,
Bourdet derivatives, and deliverability calculations.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill


class WellTestAnalysis:
    """Performs well test analysis on CBM data"""
    
    def __init__(self, data_path='data/well_test_data.csv'):
        """Initialize with data file"""
        self.data_path = data_path
        self.df = None
        self.output_dir = Path('output')
        self.output_dir.mkdir(exist_ok=True)
        
    def load_data(self):
        """Load well test data from CSV"""
        try:
            self.df = pd.read_csv(self.data_path)
            print(f"✓ Data loaded: {len(self.df)} records")
            return self.df
        except FileNotFoundError:
            print(f"✗ File not found: {self.data_path}")
            return None
    
    def horner_plot(self, time_col='time', pressure_col='pressure', 
                    shut_in_time=None):
        """
        Calculate Horner plot data (buildup test analysis)
        Formula: (p* - p) / qB vs (t + Δt) / Δt on semi-log scale
        """
        if self.df is None:
            self.load_data()
        
        if shut_in_time is None:
            shut_in_time = self.df[time_col].max()
        
        # Calculate Horner time function
        dt = self.df[time_col].values
        pressure = self.df[pressure_col].values
        
        horner_time = (shut_in_time + dt) / dt
        
        results = pd.DataFrame({
            'Shutdown Time (hours)': dt,
            'Pressure (psi)': pressure,
            'Horner Time Function': horner_time
        })
        
        # Create Horner plot
        plt.figure(figsize=(10, 6))
        plt.semilogx(horner_time, pressure, 'b-o', linewidth=2, markersize=4)
        plt.xlabel('(t + Δt) / Δt (Horner Time Function)', fontsize=11)
        plt.ylabel('Pressure (psi)', fontsize=11)
        plt.title('Horner Plot - Buildup Test Analysis', fontsize=13, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(self.output_dir / 'horner_plot.png', dpi=300)
        print("✓ Horner plot saved: output/horner_plot.png")
        plt.close()
        
        return results
    
    def bourdet_derivative(self, time_col='time', pressure_col='pressure'):
        """
        Calculate Bourdet derivative: d(Δp)/d(ln(t))
        Used for type curve matching in well testing
        """
        if self.df is None:
            self.load_data()
        
        time = self.df[time_col].values
        pressure = self.df[pressure_col].values
        
        # Calculate pressure changes
        dp = np.diff(pressure)
        dt = np.diff(time)
        
        # Calculate derivative
        derivative = dp / np.log(time[1:] / time[:-1])
        
        results = pd.DataFrame({
            'Time (hours)': time[:-1],
            'Pressure (psi)': pressure[:-1],
            'Bourdet Derivative': derivative
        })
        
        # Create derivative plot
        plt.figure(figsize=(10, 6))
        plt.loglog(time[:-1], np.abs(derivative), 'r-o', linewidth=2, markersize=4)
        plt.xlabel('Time (hours)', fontsize=11)
        plt.ylabel('|Bourdet Derivative| (psi)', fontsize=11)
        plt.title('Bourdet Derivative - Type Curve Analysis', fontsize=13, fontweight='bold')
        plt.grid(True, alpha=0.3, which='both')
        plt.tight_layout()
        plt.savefig(self.output_dir / 'bourdet_derivative.png', dpi=300)
        print("✓ Bourdet derivative plot saved: output/bourdet_derivative.png")
        plt.close()
        
        return results
    
    def log_log_analysis(self, time_col='time', pressure_col='pressure'):
        """
        Log-Log pressure analysis - helps identify flow regimes
        """
        if self.df is None:
            self.load_data()
        
        time = self.df[time_col].values
        pressure = self.df[pressure_col].values
        dp = pressure - pressure[0]  # Pressure drop from initial
        
        plt.figure(figsize=(10, 6))
        plt.loglog(time, np.abs(dp) + 1e-6, 'g-s', linewidth=2, markersize=4)
        plt.xlabel('Time (hours)', fontsize=11)
        plt.ylabel('Pressure Drop (psi)', fontsize=11)
        plt.title('Log-Log Pressure Analysis - Flow Regime Identification', 
                  fontsize=13, fontweight='bold')
        plt.grid(True, alpha=0.3, which='both')
        plt.tight_layout()
        plt.savefig(self.output_dir / 'loglog_analysis.png', dpi=300)
        print("✓ Log-Log analysis plot saved: output/loglog_analysis.png")
        plt.close()
        
        return pd.DataFrame({
            'Time (hours)': time,
            'Pressure Drop (psi)': dp
        })
    
    def deliverability_curve(self, rates, pressures, prod_pressure=None):
        """
        Generate IPR (Inflow Performance Relationship) curve
        Used for deliverability assessment
        """
        if prod_pressure is None:
            prod_pressure = pressures[0]
        
        # Fit quadratic equation: q = C0(Pr² - Pwf²) + C1(Pr - Pwf)
        pwf_range = np.linspace(0, prod_pressure, 100)
        
        plt.figure(figsize=(10, 6))
        plt.plot(rates, pressures, 'ko-', linewidth=2, markersize=6, label='Test Data')
        plt.xlabel('Production Rate (BOPD)', fontsize=11)
        plt.ylabel('Wellhead Pressure (psi)', fontsize=11)
        plt.title('Deliverability (IPR) Curve', fontsize=13, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.savefig(self.output_dir / 'ipr_curve.png', dpi=300)
        print("✓ IPR curve saved: output/ipr_curve.png")
        plt.close()
    
    def export_to_excel(self, horner_results=None, derivative_results=None):
        """Export analysis results to Excel workbook"""
        wb = Workbook()
        ws = wb.active
        ws.title = "Analysis Results"
        
        # Header style
        header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
        header_font = Font(bold=True, color="FFFFFF")
        
        # Add title
        ws['A1'] = "CBM Well Test Analysis Report"
        ws['A1'].font = Font(size=14, bold=True)
        ws.merge_cells('A1:D1')
        
        # Add Horner results if available
        if horner_results is not None:
            ws['A3'] = "Horner Plot Data"
            ws['A3'].font = Font(size=11, bold=True)
            
            for col_num, header in enumerate(horner_results.columns, 1):
                cell = ws.cell(row=4, column=col_num)
                cell.value = header
                cell.fill = header_fill
                cell.font = header_font
            
            for row_num, row_data in enumerate(horner_results.values, 5):
                for col_num, value in enumerate(row_data, 1):
                    ws.cell(row=row_num, column=col_num).value = value
        
        # Save workbook
        excel_path = self.output_dir / 'analysis_results.xlsx'
        wb.save(excel_path)
        print(f"✓ Excel report saved: {excel_path}")
    
    def run_complete_analysis(self):
        """Run all analysis steps"""
        print("\n" + "="*50)
        print("CBM Well Test Analysis")
        print("="*50 + "\n")
        
        # Load data
        self.load_data()
        if self.df is None:
            print("\n⚠ Cannot proceed without data file")
            return
        
        print("\n📊 Running analyses...\n")
        
        # Run analyses
        horner_results = self.horner_plot()
        print(f"   Horner plot data: {len(horner_results)} points")
        
        deriv_results = self.bourdet_derivative()
        print(f"   Bourdet derivative: {len(deriv_results)} points")
        
        loglog_results = self.log_log_analysis()
        print(f"   Log-Log analysis: {len(loglog_results)} points")
        
        # Export to Excel
        self.export_to_excel(horner_results, deriv_results)
        
        print("\n" + "="*50)
        print("✓ Analysis complete!")
        print(f"📁 Output saved to: {self.output_dir.absolute()}")
        print("="*50 + "\n")


if __name__ == "__main__":
    # Create sample data if it doesn't exist
    data_file = Path('data/well_test_data.csv')
    if not data_file.exists():
        print("📝 Creating sample dataset...")
        np.random.seed(42)
        time = np.logspace(0, 3, 50)  # 1 to 1000 hours
        pressure = 3000 - 100 * np.log(time) + np.random.normal(0, 5, len(time))
        sample_data = pd.DataFrame({
            'time': time,
            'pressure': pressure
        })
        data_file.parent.mkdir(exist_ok=True)
        sample_data.to_csv(data_file, index=False)
        print(f"✓ Sample data created: {data_file}\n")
    
    # Run analysis
    analysis = WellTestAnalysis()
    analysis.run_complete_analysis()
