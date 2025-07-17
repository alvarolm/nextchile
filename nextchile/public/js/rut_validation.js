// Chilean RUT validation for client-side
function validateChileanRUT(rut) {
    if (!rut) return false;
    
    // Clean RUT: remove dots and convert to uppercase
    const cleanRUT = rut.replace(/\./g, '').replace(/\s/g, '').toUpperCase();
    
    // Check format: 7-8 digits + hyphen + check digit
    if (!/^\d{7,8}-[0-9K]$/.test(cleanRUT)) {
        return false;
    }
    
    // Split RUT and check digit
    const parts = cleanRUT.split('-');
    if (parts.length !== 2) return false;
    
    const rutNumber = parts[0];
    const checkDigit = parts[1];
    
    // Calculate check digit
    const calculatedCheckDigit = calculateRUTCheckDigit(rutNumber);
    
    return checkDigit === calculatedCheckDigit;
}

function calculateRUTCheckDigit(rutNumber) {
    const multipliers = [2, 3, 4, 5, 6, 7];
    let total = 0;
    
    // Process digits from right to left
    for (let i = 0; i < rutNumber.length; i++) {
        const digit = parseInt(rutNumber[rutNumber.length - 1 - i]);
        const multiplier = multipliers[i % 6];
        total += digit * multiplier;
    }
    
    // Calculate check digit
    const remainder = total % 11;
    const checkDigit = 11 - remainder;
    
    if (checkDigit === 11) return '0';
    if (checkDigit === 10) return 'K';
    return checkDigit.toString();
}

function formatChileanRUT(rut) {
    if (!rut) return '';
    
    // Clean RUT
    let cleanRUT = rut.replace(/\./g, '').replace(/-/g, '').replace(/\s/g, '').toUpperCase();
    
    // Validate basic format
    if (!/^\d{7,8}[0-9K]$/.test(cleanRUT)) {
        return rut; // Return original if invalid
    }
    
    // Split number and check digit
    const rutNumber = cleanRUT.slice(0, -1);
    const checkDigit = cleanRUT.slice(-1);
    
    // Add dots every 3 digits from right
    let formattedNumber = '';
    for (let i = 0; i < rutNumber.length; i++) {
        if (i > 0 && i % 3 === 0) {
            formattedNumber = '.' + formattedNumber;
        }
        formattedNumber = rutNumber[rutNumber.length - 1 - i] + formattedNumber;
    }
    
    return `${formattedNumber}-${checkDigit}`;
}

// Apply validation to Customer doctype
frappe.ui.form.on('Customer', {
    tax_id: function(frm) {
        if (frm.doc.tax_id) {
            if (!validateChileanRUT(frm.doc.tax_id)) {
                frappe.msgprint({
                    title: 'RUT Inválido',
                    message: `El RUT "${frm.doc.tax_id}" no es válido. Por favor ingrese un RUT chileno válido (formato: XX.XXX.XXX-X)`,
                    indicator: 'red'
                });
                frm.set_value('tax_id', '');
            } else {
                // Format the RUT properly
                frm.set_value('tax_id', formatChileanRUT(frm.doc.tax_id));
            }
        }
    }
});

// Apply validation to Supplier doctype
frappe.ui.form.on('Supplier', {
    tax_id: function(frm) {
        if (frm.doc.tax_id) {
            if (!validateChileanRUT(frm.doc.tax_id)) {
                frappe.msgprint({
                    title: 'RUT Inválido',
                    message: `El RUT "${frm.doc.tax_id}" no es válido. Por favor ingrese un RUT chileno válido (formato: XX.XXX.XXX-X)`,
                    indicator: 'red'
                });
                frm.set_value('tax_id', '');
            } else {
                // Format the RUT properly
                frm.set_value('tax_id', formatChileanRUT(frm.doc.tax_id));
            }
        }
    }
});

// Apply validation to Company doctype
frappe.ui.form.on('Company', {
    tax_id: function(frm) {
        if (frm.doc.tax_id) {
            if (!validateChileanRUT(frm.doc.tax_id)) {
                frappe.msgprint({
                    title: 'RUT Inválido',
                    message: `El RUT "${frm.doc.tax_id}" no es válido. Por favor ingrese un RUT chileno válido (formato: XX.XXX.XXX-X)`,
                    indicator: 'red'
                });
                frm.set_value('tax_id', '');
            } else {
                // Format the RUT properly
                frm.set_value('tax_id', formatChileanRUT(frm.doc.tax_id));
            }
        }
    }
});