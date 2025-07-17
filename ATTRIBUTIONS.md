# Attributions and Third-Party Licenses

## Chilean RUT Validation

This project includes Chilean RUT validation functionality based on code from:

**Repository**: [nocrop/Rut-Chileno-en-Python](https://github.com/nocrop/Rut-Chileno-en-Python)  
**Author**: nocrop  
**License**: MIT License  

### Original License Text

```
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### Modifications Made

The original Python implementation has been adapted for integration with ERPNext/Frappe framework:

1. **Python version** (`nextchile/utils.py`):
   - Wrapped the validation logic in functions suitable for Frappe hooks
   - Added error handling for ERPNext integration
   - Added Spanish error messages for user feedback
   - Maintained the core algorithm unchanged

2. **JavaScript version** (`public/js/rut_validation.js`):
   - Ported the Python algorithm to JavaScript for client-side validation
   - Added integration with Frappe form validation system
   - Added automatic RUT formatting functionality
   - Maintained the same validation logic and range checks

### Acknowledgments

We thank nocrop for creating and maintaining the excellent Chilean RUT validation implementation that serves as the foundation for this ERPNext integration. The original work provides a robust, well-tested solution for Chilean RUT validation.

---

For questions about the original implementation, please visit: https://github.com/nocrop/Rut-Chileno-en-Python