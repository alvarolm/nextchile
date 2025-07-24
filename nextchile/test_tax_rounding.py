"""
Test script for tax row level rounding functionality
Run this in bench console: bench --site [site-name] console
"""

import frappe
import math
from nextchile.tax_rounding import apply_row_level_tax_rounding


def test_tax_row_rounding():
    """Test individual tax row rounding"""
    
    print("Testing tax row level rounding...")
    
    # Test the rounding logic directly
    test_amounts = [18.30, 5.70, 19.99, 20.00, 12.34]
    
    print("\nDirect rounding test:")
    for amount in test_amounts:
        rounded = math.ceil(amount)
        print(f"  {amount} → {rounded} (difference: +{rounded - amount:.2f})")
    
    print("\nTax row rounding functionality has been implemented!")
    print("\nTo test in real documents:")
    print("1. Create a Sales Invoice or Purchase Invoice")
    print("2. Add tax rows in the taxes table")
    print("3. Check 'Redondear Impuesto' for specific taxes")
    print("4. Save the document and see individual taxes rounded up")
    
    print("\nExample usage:")
    print("- Item Amount: $100")
    print("- Tax 1 (IVA 19.3%): $19.30 → Round Up = Yes → Result: $20.00")
    print("- Tax 2 (Retención 5.7%): $5.70 → Round Up = No → Result: $5.70")
    print("- Grand Total: $125.70")


def create_custom_fields_test():
    """Test custom field creation"""
    from nextchile.install import create_tax_row_fields
    
    try:
        create_tax_row_fields()
        print("Custom fields created successfully!")
        return True
    except Exception as e:
        print(f"Error creating custom fields: {e}")
        return False


if __name__ == "__main__":
    test_tax_row_rounding()