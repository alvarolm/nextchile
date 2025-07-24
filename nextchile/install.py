"""
Installation scripts for nextchile app
"""

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def create_tax_row_fields():
    """Create custom fields on tax row child tables"""
    
    # Define custom field for tax rows (child tables)
    tax_row_fields = {
        # Sales-related tax tables
        "Sales Taxes and Charges": [
            {
                "fieldname": "custom_round_up_tax",
                "label": "Redondear Impuesto",
                "fieldtype": "Check",
                "insert_after": "rate",
                "description": "Marcar para redondear hacia arriba este impuesto al número entero más cercano",
                "default": 0,
                "in_list_view": 1,  # Show in tax table
                "columns": 1
            }
        ],
        
        # Purchase-related tax tables  
        "Purchase Taxes and Charges": [
            {
                "fieldname": "custom_round_up_tax",
                "label": "Redondear Impuesto", 
                "fieldtype": "Check",
                "insert_after": "rate",
                "description": "Marcar para redondear hacia arriba este impuesto al número entero más cercano",
                "default": 0,
                "in_list_view": 1,  # Show in tax table
                "columns": 1
            }
        ]
    }
    
    # Create custom fields
    create_custom_fields(tax_row_fields, update=True)
    frappe.db.commit()
    
    frappe.msgprint(
        "Campos personalizados para redondeo de impuestos creados exitosamente!",
        title="Instalación Completada"
    )


def after_install():
    """Run after app installation"""
    create_tax_row_fields()