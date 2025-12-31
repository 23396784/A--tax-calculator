# 🇦🇺 Australian Income Tax Calculator

A comprehensive Python application for calculating Australian income tax, withholding tax, superannuation contributions, and tax refunds based on ATO (Australian Taxation Office) guidelines.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![ATO](https://img.shields.io/badge/ATO-2024--25-orange.svg)

## 📋 Overview

This project demonstrates a real-world application of the Australian taxation system, calculating:

- **Weekly Withholding Tax** - Tax deducted by employers each pay period
- **Annual Income Tax** - Total tax liability for the financial year
- **Superannuation Contributions** - Mandatory 11% retirement savings
- **Tax Refunds** - Difference between withheld and actual tax owed

## 🎯 Features

- ✅ Progressive tax bracket calculations (2024-25 rates)
- ✅ Weekly withholding tax using ATO coefficients
- ✅ 11% superannuation contribution calculations
- ✅ Tax refund estimations
- ✅ Batch processing for multiple employees
- ✅ Detailed breakdown reports
- ✅ Visualization of tax distributions

## 📊 Tax Brackets (2024-25)

| Taxable Income | Tax Rate |
|----------------|----------|
| $0 - $18,200 | 0% (Tax-free threshold) |
| $18,201 - $45,000 | 19c for each $1 over $18,200 |
| $45,001 - $120,000 | $5,092 + 32.5c for each $1 over $45,000 |
| $120,001 - $180,000 | $29,467 + 37c for each $1 over $120,000 |
| $180,001+ | $51,667 + 45c for each $1 over $180,000 |

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/YOUR_USERNAME/australian-tax-calculator.git
cd australian-tax-calculator
pip install -r requirements.txt
```

### Basic Usage

```python
from tax_calculator import AustralianTaxCalculator

# Create calculator instance
calc = AustralianTaxCalculator()

# Calculate tax for a single employee
weekly_salary = 1693
result = calc.calculate_full_breakdown(weekly_salary)

print(f"Weekly Salary: ${result['weekly_salary']:.2f}")
print(f"Superannuation: ${result['weekly_super']:.2f}")
print(f"Withholding Tax: ${result['weekly_withholding']:.2f}")
print(f"Take-Home Pay: ${result['weekly_net']:.2f}")
print(f"Annual Tax: ${result['annual_tax']:.2f}")
print(f"Tax Refund: ${result['tax_refund']:.2f}")
```

### Batch Processing

```python
# Process multiple employees
salaries = [1693, 1358, 1772, 2234, 1308, 1308, 2263, 1835, 1184, 1717]
results = calc.process_batch(salaries)

# Generate report
calc.print_report(results)
```

## 📁 Project Structure

```
australian-tax-calculator/
├── README.md
├── requirements.txt
├── tax_calculator.py          # Main calculator module
├── australian_tax_analysis.ipynb  # Jupyter notebook with full analysis
├── visualizations.py          # Charts and graphs
└── tests/
    └── test_calculator.py     # Unit tests
```

## 📈 Sample Output

```
================================================================================
                    AUSTRALIAN TAX CALCULATION REPORT
================================================================================

Person 1:
  Weekly Salary:              $1,693.00
  Superannuation (11%):       $167.77
  Weekly Withholding Tax:     $343.80
  Weekly Take-Home Pay:       $1,181.43
  Annual Income Tax:          $16,243.39
  Estimated Tax Refund:       $1,634.21

--------------------------------------------------------------------------------
SUMMARY STATISTICS
--------------------------------------------------------------------------------
Total Employees:              10
Average Weekly Salary:        $1,667.20
Total Annual Tax Collected:   $186,432.50
Total Tax Refunds:            $16,802.46
Average Effective Tax Rate:   22.3%
================================================================================
```

## 🔬 Key Calculations

### 1. Weekly Withholding Tax Formula
```
y = a × (x + 0.99) - b
```
Where:
- `x` = weekly earnings
- `a` = rate coefficient
- `b` = threshold adjustment

### 2. Superannuation
```
Super = Base Salary × 11%
Taxable Income = Total Package / 1.11
```

### 3. Tax Refund
```
Tax Refund = (Weekly Withholding × 52) - Annual Tax Liability
```

## 📊 Visualizations

The project includes visualizations for:
- Tax bracket distribution
- Effective tax rates by income level
- Withholding vs actual tax comparison
- Superannuation growth projections

## 🎓 Educational Value

This project demonstrates:
- **Financial Literacy**: Understanding Australian taxation
- **Python Programming**: Functions, loops, conditionals
- **Data Analysis**: Processing and summarizing financial data
- **Real-World Application**: Practical use of programming skills

## 👨‍💼 Author

**Victor Prefa**
- Medical Doctor & Data Scientist
- MSc Data Science & Business Analytics, Deakin University
- Student ID: 225187913

## 📚 References

- [Australian Taxation Office (ATO)](https://www.ato.gov.au)
- [Tax Withheld Calculator](https://www.ato.gov.au/calculators-and-tools/tax-withheld-calculator)
- [Superannuation Guarantee](https://www.ato.gov.au/business/super-for-employers/paying-super-contributions/how-much-super-to-pay/)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

*This project was developed as part of the Data Science coursework at Deakin University.*
