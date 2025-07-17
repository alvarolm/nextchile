/**
 * Chilean RUT validation for client-side
 * Based on nocrop's Rut-Chileno-en-Python implementation
 * https://github.com/nocrop/Rut-Chileno-en-Python
 * 
 * Original code by nocrop, licensed under MIT License
 * Adapted for JavaScript/ERPNext by nextchile app
 */

function validateChileanRUT(rut) {
    if (!rut) return false;
    
    try {
        // Clean RUT using nocrop's method - remove dots, hyphens, and convert to uppercase
        rut = rut.toUpperCase().replace(/-/g, '').replace(/\./g, '');
        const rutAux = rut.slice(0, -1);
        const dv = rut.slice(-1);
        
        // Check if rutAux is numeric and within realistic range (1,000,000 to 25,000,000)
        if (!/^\d+$/.test(rutAux) || !(1000000 <= parseInt(rutAux) && parseInt(rutAux) <= 25000000)) {
            return false;
        }
        
        // Reverse the digits and apply nocrop's algorithm
        const revertido = rutAux.split('').reverse().map(d => parseInt(d));
        const factors = [2, 3, 4, 5, 6, 7];
        let suma = 0;
        
        for (let i = 0; i < revertido.length; i++) {
            suma += revertido[i] * factors[i % 6];
        }
        
        const residuo = suma % 11;
        
        if (dv === 'K') {
            return residuo === 1;
        }
        if (dv === '0') {
            return residuo === 11;
        }
        return residuo === 11 - parseInt(dv);
        
    } catch (error) {
        return false;
    }
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