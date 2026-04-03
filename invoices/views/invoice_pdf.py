from django.http import FileResponse, HttpResponse
from invoices.models import Invoice
from invoices.utils.pdf import generate_invoice_pdf
import zipfile
import os


def invoice_pdf_view(request, invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)

    # Generate all 4 copies
    copies = ['ORIGINAL', 'DUPLICATE', 'TRIPLICATE', 'EXTRA']
    pdf_paths = []

    for copy_type in copies:
        pdf_path = generate_invoice_pdf(invoice, copy_type)
        pdf_paths.append(pdf_path)

    # Create a zip file with all PDFs
    zip_path = f"media/invoices/{invoice.invoice_no}_all_copies.zip"
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for pdf_path in pdf_paths:
            zipf.write(pdf_path, os.path.basename(pdf_path))

    return FileResponse(open(zip_path, 'rb'), content_type='application/zip', as_attachment=True, filename=f"{invoice.invoice_no}_invoices.zip")