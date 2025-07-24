"""
Tax Row Level Rounding for Chilean ERPNext
Implements individual tax row rounding functionality
"""

import frappe
import math


def apply_row_level_tax_rounding(doc, method):
    """
    Apply rounding to individual tax rows based on their custom field
    """
    if not hasattr(doc, 'taxes') or not doc.taxes:
        return
    
    changes_made = False
    rounding_details = []
    
    # Process each tax row individually
    for tax_row in doc.taxes:
        # Check if this specific tax row should be rounded up
        should_round = getattr(tax_row, 'custom_round_up_tax', 0)
        
        if should_round and tax_row.tax_amount and tax_row.tax_amount > 0:
            original_amount = tax_row.tax_amount
            rounded_amount = math.ceil(original_amount)
            
            # Only update if rounding actually changes the value
            if rounded_amount != original_amount:
                tax_row.tax_amount = rounded_amount
                changes_made = True
                
                # Track the change for user feedback
                rounding_details.append({
                    'tax_name': tax_row.description or tax_row.account_head,
                    'original': original_amount,
                    'rounded': rounded_amount,
                    'difference': rounded_amount - original_amount
                })
    
    # If any changes were made, recalculate and notify user
    if changes_made:
        # Let ERPNext handle all the recalculations
        doc.calculate_taxes_and_totals()
        
        # Show summary of rounded taxes
        show_rounding_summary(rounding_details)


def show_rounding_summary(rounding_details):
    """Show user-friendly summary of tax rounding"""
    if not rounding_details:
        return
    
    # Create summary message
    total_adjustment = sum(detail['difference'] for detail in rounding_details)
    
    message_lines = ["<b>Redondeo de Impuestos Aplicado:</b><br>"]
    for detail in rounding_details:
        message_lines.append(
            f"• {detail['tax_name']}: "
            f"{detail['original']:.2f} → {detail['rounded']:.2f} "
            f"(+{detail['difference']:.2f})"
        )
    
    message_lines.append(f"<br><b>Ajuste Total: +{total_adjustment:.2f}</b>")
    
    frappe.msgprint(
        "<br>".join(message_lines),
        title="Impuestos Redondeados",
        indicator="blue"
    )