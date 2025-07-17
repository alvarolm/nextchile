import re
import frappe


def validate_chilean_rut(rut):
    """
    Validates Chilean RUT (Rol Único Tributario) format and check digit.
    
    Args:
        rut (str): RUT string in format XX.XXX.XXX-X or XXXXXXXX-X
        
    Returns:
        bool: True if RUT is valid, False otherwise
    """
    if not rut:
        return False
    
    # Clean RUT: remove dots and convert to uppercase
    clean_rut = rut.replace(".", "").replace(" ", "").upper()
    
    # Check format: 8-9 digits + hyphen + check digit
    if not re.match(r'^\d{7,8}-[0-9K]$', clean_rut):
        return False
    
    # Split RUT and check digit
    parts = clean_rut.split("-")
    if len(parts) != 2:
        return False
    
    rut_number = parts[0]
    check_digit = parts[1]
    
    # Calculate check digit
    calculated_check_digit = calculate_rut_check_digit(rut_number)
    
    return check_digit == calculated_check_digit


def calculate_rut_check_digit(rut_number):
    """
    Calculates the check digit for a Chilean RUT number.
    
    Args:
        rut_number (str): RUT number without check digit
        
    Returns:
        str: Check digit (0-9 or K)
    """
    multipliers = [2, 3, 4, 5, 6, 7]
    total = 0
    
    # Process digits from right to left
    for i, digit in enumerate(reversed(rut_number)):
        multiplier = multipliers[i % 6]
        total += int(digit) * multiplier
    
    # Calculate check digit
    remainder = total % 11
    check_digit = 11 - remainder
    
    if check_digit == 11:
        return "0"
    elif check_digit == 10:
        return "K"
    else:
        return str(check_digit)


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