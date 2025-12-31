"""
================================================================================
A-INCOME TAX CALCULATOR
================================================================================

A comprehensive tax calculation system based on ATO (A-Taxation Office)
guidelines for the 2024-25 financial year.

Features:
- Progressive income tax calculation
- Weekly withholding tax computation
- Superannuation contribution handling
- Tax refund estimation
- Batch processing for multiple employees

Author: Victor Prefa
Institution: Deakin University
Course: MSc Data Science & Business Analytics

================================================================================
"""

import math
import numpy as np
from typing import List, Dict, Tuple, Optional

# =============================================================================
# CONSTANTS - ATO Tax Rates 2024-25
# =============================================================================

# Annual income tax brackets
TAX_BRACKETS = [
    (0, 18200, 0, 0),           # Tax-free threshold
    (18201, 45000, 0.19, 0),    # 19 cents per dollar over $18,200
    (45001, 120000, 0.325, 5092),   # 32.5 cents per dollar over $45,000
    (120001, 180000, 0.37, 29467),  # 37 cents per dollar over $120,000
    (180001, float('inf'), 0.45, 51667)  # 45 cents per dollar over $180,000
]

# Weekly withholding tax coefficients (Scale 2 - with tax-free threshold)
WITHHOLDING_COEFFICIENTS = [
    (0, 359, 0, 0),
    (359, 438, 0.1900, 68.3462),
    (438, 548, 0.2900, 112.1942),
    (548, 721, 0.2100, 68.3465),
    (721, 865, 0.2190, 74.8369),
    (865, 1282, 0.3477, 186.2119),
    (1282, 2307, 0.3450, 182.7504),
    (2307, 3461, 0.3900, 286.5965),
    (3461, float('inf'), 0.4700, 563.5196)
]

# Superannuation guarantee rate
SUPER_RATE = 0.11  # 11% for 2024-25


# =============================================================================
# TAX CALCULATOR CLASS
# =============================================================================

class AustralianTaxCalculator:
    """
    A comprehensive Australian tax calculator implementing ATO guidelines.
    
    Attributes:
        super_rate (float): Superannuation guarantee rate (default 11%)
        
    Example:
        >>> calc = AustralianTaxCalculator()
        >>> result = calc.calculate_full_breakdown(1693)
        >>> print(f"Tax Refund: ${result['tax_refund']:.2f}")
    """
    
    def __init__(self, super_rate: float = SUPER_RATE):
        """
        Initialize the tax calculator.
        
        Args:
            super_rate: Superannuation rate (default 0.11 for 11%)
        """
        self.super_rate = super_rate
    
    # -------------------------------------------------------------------------
    # Core Calculation Methods
    # -------------------------------------------------------------------------
    
    def calculate_annual_tax(self, annual_income: float) -> float:
        """
        Calculate annual income tax based on progressive tax brackets.
        
        Args:
            annual_income: Gross annual income in dollars
            
        Returns:
            Annual tax liability in dollars
            
        Example:
            >>> calc = AustralianTaxCalculator()
            >>> calc.calculate_annual_tax(88036)
            19078.70
        """
        if annual_income <= 18200:
            return 0.0
        elif annual_income <= 45000:
            return 0.19 * (annual_income - 18200)
        elif annual_income <= 120000:
            return 5092 + 0.325 * (annual_income - 45000)
        elif annual_income <= 180000:
            return 29467 + 0.37 * (annual_income - 120000)
        else:
            return 51667 + 0.45 * (annual_income - 180000)
    
    def calculate_weekly_withholding(self, weekly_salary: float) -> float:
        """
        Calculate weekly withholding tax using ATO coefficients.
        
        Formula: y = a × (x + 0.99) - b
        
        Args:
            weekly_salary: Gross weekly salary in dollars
            
        Returns:
            Weekly withholding tax amount in dollars
            
        Example:
            >>> calc = AustralianTaxCalculator()
            >>> calc.calculate_weekly_withholding(1693)
            401.68
        """
        if weekly_salary < 359:
            return 0.0
        
        for lower, upper, a, b in WITHHOLDING_COEFFICIENTS:
            if lower <= weekly_salary < upper:
                return round(a * (weekly_salary + 0.99) - b, 2)
        
        return 0.0
    
    def calculate_superannuation(self, base_salary: float) -> float:
        """
        Calculate superannuation contribution.
        
        Args:
            base_salary: Base salary before super
            
        Returns:
            Superannuation contribution amount
        """
        return round(base_salary * self.super_rate, 2)
    
    def separate_super_from_package(self, total_package: float) -> Tuple[float, float]:
        """
        Separate base salary and super from a total package.
        
        Args:
            total_package: Total salary package including super
            
        Returns:
            Tuple of (base_salary, super_amount)
            
        Example:
            >>> calc = AustralianTaxCalculator()
            >>> base, super = calc.separate_super_from_package(1693)
            >>> print(f"Base: ${base:.2f}, Super: ${super:.2f}")
        """
        base_salary = total_package / (1 + self.super_rate)
        super_amount = base_salary * self.super_rate
        return round(base_salary, 2), round(super_amount, 2)
    
    # -------------------------------------------------------------------------
    # Comprehensive Calculation Methods
    # -------------------------------------------------------------------------
    
    def calculate_full_breakdown(self, weekly_salary: float, 
                                  include_super_in_salary: bool = True) -> Dict:
        """
        Calculate complete tax breakdown for an individual.
        
        Args:
            weekly_salary: Weekly salary amount
            include_super_in_salary: If True, super is included in salary
            
        Returns:
            Dictionary with all tax calculations
        """
        if include_super_in_salary:
            base_weekly, weekly_super = self.separate_super_from_package(weekly_salary)
        else:
            base_weekly = weekly_salary
            weekly_super = self.calculate_superannuation(weekly_salary)
        
        # Weekly calculations
        weekly_withholding = self.calculate_weekly_withholding(base_weekly)
        weekly_net = base_weekly - weekly_withholding
        
        # Annual calculations
        annual_base = base_weekly * 52
        annual_super = weekly_super * 52
        annual_withholding = weekly_withholding * 52
        annual_tax = self.calculate_annual_tax(annual_base)
        tax_refund = annual_withholding - annual_tax
        
        # Effective tax rate
        effective_rate = (annual_tax / annual_base * 100) if annual_base > 0 else 0
        
        return {
            'weekly_salary': weekly_salary,
            'base_weekly': base_weekly,
            'weekly_super': weekly_super,
            'weekly_withholding': weekly_withholding,
            'weekly_net': weekly_net,
            'annual_base': annual_base,
            'annual_super': annual_super,
            'annual_withholding': annual_withholding,
            'annual_tax': annual_tax,
            'tax_refund': tax_refund,
            'effective_rate': effective_rate
        }
    
    def process_batch(self, salaries: List[float]) -> List[Dict]:
        """
        Process tax calculations for multiple employees.
        
        Args:
            salaries: List of weekly salaries
            
        Returns:
            List of calculation results for each employee
        """
        return [self.calculate_full_breakdown(salary) for salary in salaries]
    
    # -------------------------------------------------------------------------
    # Reporting Methods
    # -------------------------------------------------------------------------
    
    def print_individual_report(self, result: Dict, person_num: int = 1) -> None:
        """Print formatted report for an individual."""
        print(f"\n## Person {person_num}")
        print(f"   Weekly Salary:              ${result['weekly_salary']:,.2f}")
        print(f"   Superannuation (11%):       ${result['weekly_super']:,.2f}")
        print(f"   Weekly Withholding Tax:     ${result['weekly_withholding']:,.2f}")
        print(f"   Weekly Take-Home Pay:       ${result['weekly_net']:,.2f}")
        print(f"   Annual Income Tax:          ${result['annual_tax']:,.2f}")
        print(f"   Estimated Tax Refund:       ${result['tax_refund']:,.2f}")
        print(f"   Effective Tax Rate:         {result['effective_rate']:.1f}%")
    
    def print_report(self, results: List[Dict]) -> None:
        """Print comprehensive report for all employees."""
        print("\n" + "=" * 80)
        print("                    AUSTRALIAN TAX CALCULATION REPORT")
        print("=" * 80)
        
        for i, result in enumerate(results, 1):
            self.print_individual_report(result, i)
        
        # Summary statistics
        print("\n" + "-" * 80)
        print("SUMMARY STATISTICS")
        print("-" * 80)
        
        total_salaries = sum(r['weekly_salary'] for r in results)
        avg_salary = total_salaries / len(results)
        total_tax = sum(r['annual_tax'] for r in results)
        total_refunds = sum(r['tax_refund'] for r in results)
        avg_rate = sum(r['effective_rate'] for r in results) / len(results)
        
        print(f"   Total Employees:              {len(results)}")
        print(f"   Average Weekly Salary:        ${avg_salary:,.2f}")
        print(f"   Total Annual Tax Collected:   ${total_tax:,.2f}")
        print(f"   Total Tax Refunds:            ${total_refunds:,.2f}")
        print(f"   Average Effective Tax Rate:   {avg_rate:.1f}%")
        print("=" * 80)
    
    def generate_summary_string(self, result: Dict, person_num: int) -> str:
        """Generate a formatted summary string for an individual."""
        return (
            f"## Person {person_num} "
            f"weekly salary ${result['weekly_salary']:.2f} "
            f"weekly superannuation contribution ${result['weekly_super']:.2f} "
            f"weekly withholding tax ${result['weekly_withholding']:.2f} "
            f"weekly income ${result['weekly_net']:.2f} "
            f"income tax ${result['annual_tax']:.2f} "
            f"tax return ${result['tax_refund']:.2f}."
        )


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def generate_sample_salaries(n: int = 10, mean: float = 1431, 
                              std: float = 527, seed: int = 42) -> List[int]:
    """
    Generate sample weekly salaries using normal distribution.
    
    Args:
        n: Number of salaries to generate
        mean: Mean salary
        std: Standard deviation
        seed: Random seed for reproducibility
        
    Returns:
        List of rounded weekly salaries
    """
    np.random.seed(seed)
    salaries = np.random.normal(mean, std, n)
    return [int(round(s)) for s in salaries]


def calculate_tax_bracket_info(annual_income: float) -> Dict:
    """
    Get information about which tax bracket an income falls into.
    
    Args:
        annual_income: Annual income amount
        
    Returns:
        Dictionary with bracket information
    """
    brackets = [
        {'range': '$0 - $18,200', 'rate': '0%', 'threshold': 18200},
        {'range': '$18,201 - $45,000', 'rate': '19%', 'threshold': 45000},
        {'range': '$45,001 - $120,000', 'rate': '32.5%', 'threshold': 120000},
        {'range': '$120,001 - $180,000', 'rate': '37%', 'threshold': 180000},
        {'range': '$180,001+', 'rate': '45%', 'threshold': float('inf')}
    ]
    
    for i, bracket in enumerate(brackets):
        if annual_income <= bracket['threshold']:
            return {
                'bracket_number': i + 1,
                'range': bracket['range'],
                'marginal_rate': bracket['rate'],
                'annual_income': annual_income
            }
    
    return brackets[-1]


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main function demonstrating the tax calculator."""
    
    print("=" * 80)
    print("       AUSTRALIAN INCOME TAX CALCULATOR - DEMONSTRATION")
    print("=" * 80)
    
    # Initialize calculator
    calc = AustralianTaxCalculator()
    
    # Generate sample salaries (matching the assignment)
    salaries = [1693, 1358, 1772, 2234, 1308, 1308, 2263, 1835, 1184, 1717]
    
    print(f"\nProcessing {len(salaries)} employees...")
    print(f"Weekly Salaries: {salaries}")
    
    # Process all employees
    results = calc.process_batch(salaries)
    
    # Print comprehensive report
    calc.print_report(results)
    
    # Print compact format (as per assignment requirement)
    print("\n" + "=" * 80)
    print("COMPACT OUTPUT FORMAT")
    print("=" * 80)
    
    for i, result in enumerate(results, 1):
        print(calc.generate_summary_string(result, i))
    
    print("\n✓ Tax calculations completed successfully!")
    

if __name__ == "__main__":
    main()
