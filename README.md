# CBM Well Test Automation

This project automates the analysis of Coal Bed Methane (CBM) well test data using Python and Excel.

## Features
- Horner Plot (Buildup Test)
- Bourdet Derivative (Log-log analysis)
- Flow Regime Identification
- Deliverability (IPR Curve)
- Excel Report Generation
- Permeability Estimation

## Technologies
- Python (Pandas, NumPy, Matplotlib)
- OpenPyXL (Excel Automation)

## How to Run
```bash
python scripts/analysis.py
```

## Output
- Horner Plot
- Bourdet Derivative Plot
- Log-Log Plot
- Excel Report

## Author
Mohammad Zafeer Alam  
B.Tech Petroleum Engineering  
IIT (ISM) Dhanbad

## Project Structure
```
├── data/                    # Input well test data
├── scripts/                 # Python analysis scripts
│   └── analysis.py         # Main analysis module
├── output/                  # Generated plots and results
│   └── plots/              # Output plot directory
└── report/                  # Analysis reports
```

## Installation

Install required packages:
```bash
pip install pandas numpy matplotlib openpyxl
```

## How It Works

1. **Load Data** - Reads CSV with time and pressure columns
2. **Horner Plot** - Buildup test interpretation for permeability
3. **Bourdet Derivative** - Central difference method for type curve matching
4. **Flow Regime ID** - Automatic detection of Early Fracture/Radial/Boundary flows
5. **Log-Log Analysis** - Identifies pressure drop behavior
6. **Excel Export** - Multi-sheet workbook with all results

## Key Features

✓ Automated well test interpretation  
✓ Permeability calculation from Horner slope  
✓ Flow regime classification  
✓ Professional Excel reports  
✓ Multiple analysis plots  

## Example Usage

```python
from scripts.analysis import WellTestAnalysis

analysis = WellTestAnalysis('data/well_test_data.csv')
analysis.run_complete_analysis()
```

## Technical Details

- **Horner Plot Formula**: k = (162.6 × q × μ × B) / (m × h)
- **Bourdet Derivative**: Central difference, d(Δp)/d(ln(t))
- **Flow Regime**: Early-time vs late-time derivative comparison
- **Excel Sheets**: Horner, Derivative, LogLog