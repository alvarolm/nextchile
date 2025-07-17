"""
Chilean RUT Validation for ERPNext
Based on nocrop's Rut-Chileno-en-Python implementation
https://github.com/nocrop/Rut-Chileno-en-Python

Original code by nocrop, licensed under MIT License
Adapted for ERPNext integration by nextchile app
"""

import re
import frappe
from itertools import cycle


def validate_chilean_rut(rut):
    """
    Validates Chilean RUT (Rol Único Tributario) using nocrop's algorithm.
    
    This implementation is based on nocrop's Rut-Chileno-en-Python:
    https://github.com/nocrop/Rut-Chileno-en-Python
    
    Args:
        rut (str): RUT string in any format (with/without dots and hyphens)
        
    Returns:
        bool: True if RUT is valid, False otherwise
    """
    if not rut:
        return False
    
    try:
        # Clean RUT using nocrop's method
        rut = rut.upper().replace("-", "").replace(".", "")
        rut_aux = rut[:-1]
        dv = rut[-1:]

        if not rut_aux.isdigit() or not (1_000_000 <= int(rut_aux) <= 25_000_000):
            return False

        revertido = map(int, reversed(rut_aux))
        factors = cycle(range(2, 8))
        suma = sum(d * f for d, f in zip(revertido, factors))
        residuo = suma % 11

        if dv == 'K':
            return residuo == 1
        if dv == '0':
            return residuo == 11
        return residuo == 11 - int(dv)
    
    except (ValueError, IndexError):
        return False


def format_chilean_rut(rut):
    """
    Formats a Chilean RUT with proper punctuation.
    
    Args:
        rut (str): Raw RUT string
        
    Returns:
        str: Formatted RUT (XX.XXX.XXX-X)
    """
    if not rut:
        return ""
    
    # Clean RUT
    clean_rut = rut.replace(".", "").replace("-", "").replace(" ", "").upper()
    
    # Validate format
    if not re.match(r'^\d{7,8}[0-9K]$', clean_rut):
        return rut  # Return original if invalid
    
    # Split number and check digit
    rut_number = clean_rut[:-1]
    check_digit = clean_rut[-1]
    
    # Add dots every 3 digits from right
    formatted_number = ""
    for i, digit in enumerate(reversed(rut_number)):
        if i > 0 and i % 3 == 0:
            formatted_number = "." + formatted_number
        formatted_number = digit + formatted_number
    
    return f"{formatted_number}-{check_digit}"


@frappe.whitelist()
def validate_tax_id(doc, method=None):
    """
    Hook function to validate tax_id field for Chilean RUT.
    This function is called during document validation.
    
    Args:
        doc: Document instance
        method: Method name (not used)
    """
    if hasattr(doc, 'tax_id') and doc.tax_id:
        if not validate_chilean_rut(doc.tax_id):
            frappe.throw(
                f"RUT inválido: {doc.tax_id}. Por favor ingrese un RUT chileno válido (formato: XX.XXX.XXX-X)",
                title="Error de validación de RUT"
            )
        
        # Format the RUT properly
        doc.tax_id = format_chilean_rut(doc.tax_id)