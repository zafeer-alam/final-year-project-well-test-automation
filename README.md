# CBM Well Test Automation

This project automates the analysis of Coal Bed Methane (CBM) well tests using Python and Excel.

## Features
- Horner Plot (Buildup Test)
- Bourdet Derivative Calculation
- Log-Log Pressure Analysis
- Deliverability (IPR Curve)
- Excel Output Generation

## Tech Stack
- Python (Pandas, NumPy, Matplotlib)
- Microsoft Excel

## Project Structure
```
├── data/                    # Input well test data
├── scripts/                 # Python analysis scripts
├── output/                  # Generated plots and results
├── report/                  # Final PDF reports
└── README.md               # This file
```

## Installation

Install required packages:
```bash
pip install pandas numpy matplotlib openpyxl
```

## Usage

Run the analysis:
```bash
python scripts/analysis.py
```

## Output

The script generates:
- Horner plot graphs
- Derivative analysis plots
- Excel workbook with results
- Analysis summary