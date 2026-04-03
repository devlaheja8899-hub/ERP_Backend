from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
import os


def generate_invoice_pdf(invoice, copy_type='ORIGINAL'):
    # Create media/invoices directory if it doesn't exist
    os.makedirs('media/invoices', exist_ok=True)

    file_path = f"media/invoices/{invoice.invoice_no}_{copy_type.lower()}.pdf"
    doc = SimpleDocTemplate(file_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # Company Header
    company = invoice.company
    story.append(Paragraph(f"<b>{company.name}</b>", styles['Heading1']))
    story.append(Paragraph(company.address, styles['Normal']))
    story.append(Paragraph(f"GST No: {company.gst_no} | State: {company.state_name} ({company.state_code})", styles['Normal']))
    story.append(Paragraph(f"CIN: {company.cin_no} | PAN: {company.pan_no}", styles['Normal']))
    story.append(Paragraph(f"Email: {company.email} | Contact: {company.contact_no}", styles['Normal']))
    story.append(Spacer(1, 12))

    # Invoice Title
    story.append(Paragraph(f"<b>INVOICE - {copy_type}</b>", styles['Heading2']))
    story.append(Spacer(1, 12))

    # Invoice Details
    invoice_data = [
        # ['Invoice No:', invoice.invoice_no, 'Date:', invoice.invoice_date.strftime('%d/%m/%Y')],
        ['Invoice No:', invoice.invoice_no, 'Date:', invoice.invoice_date.strftime('%Y/%m/%d')],
        ['E-Way Bill No:', invoice.e_way_bill_no or '', 'E-Invoice No:', invoice.e_invoice_no or ''],
        ['Insurance No:', invoice.insurance_no or '', 'Due Date:', invoice.due_date.strftime('%d/%m/%Y')],
        ['Mode of Payment:', invoice.mode_of_payment or '', 'Delivery Date:', invoice.delivery_date.strftime('%d/%m/%Y') if invoice.delivery_date else ''],
        ['Customer PO No:', invoice.customer_po_no or '', 'PO Date:', invoice.customer_po_date.strftime('%d/%m/%Y') if invoice.customer_po_date else ''],
        ['Dispatch Docket No:', invoice.dispatch_docket_no or '', 'Courier:', invoice.dispatch_courier_name or ''],
        ['Dispatch Mode:', invoice.dispatch_mode or '', '', ''],
    ]

    invoice_table = Table(invoice_data, colWidths=[100, 150, 100, 150])
    invoice_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
    ]))
    story.append(invoice_table)
    story.append(Spacer(1, 12))

    # Buyer Details
    customer = invoice.customer
    story.append(Paragraph("<b>Buyer Details:</b>", styles['Heading3']))
    buyer_data = [
        ['Name:', customer.company_name],
        ['Address:', customer.dispatch_address or ''],
        ['GST No:', customer.gst_number or ''],
        ['PAN No:', customer.pan_no or ''],
        ['State:', f"{customer.state} ({customer.state_code})" if customer.state and customer.state_code else ''],
        ['Contact Person:', customer.contact_person_name],
        ['Contact No:', customer.contact_number],
        ['Project/Product:', customer.buyer_project_name or ''],
    ]

    buyer_table = Table(buyer_data, colWidths=[100, 300])
    buyer_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))
    story.append(buyer_table)
    story.append(Spacer(1, 12))

    # Items Table
    story.append(Paragraph("<b>Items:</b>", styles['Heading3']))
    items_data = [['S.No', 'Description', 'HSN', 'Qty', 'Rate', 'Amount', 'Mfg Name', 'Date Code', 'Cust Item Code']]
    for i, item in enumerate(invoice.items.all(), 1):
        items_data.append([
            i,
            item.description,
            item.hsn_code,
            item.quantity,
            item.rate,
            item.amount,
            item.manufacture_name or '',
            item.date_code or '',
            item.customer_item_code or '',
        ])

    items_table = Table(items_data, colWidths=[30, 100, 50, 40, 50, 60, 60, 50, 60])
    items_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(items_table)
    story.append(Spacer(1, 12))

    # Totals
    totals_data = [
        ['Total Quantity:', invoice.total_quantity],
        ['Taxable Value:', f"₹{invoice.taxable_value}"],
        ['GST Amount:', f"₹{invoice.gst_amount}"],
        ['Discount:', f"₹{invoice.discount}"],
        ['Shipping Charges:', f"₹{invoice.shipping_charges}"],
        ['Round Off:', f"₹{invoice.round_off}"],
        ['Grand Total:', f"₹{invoice.grand_total}"],
    ]

    totals_table = Table(totals_data, colWidths=[150, 100])
    totals_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,-1), (-1,-1), colors.lightgrey),
    ]))
    story.append(totals_table)
    story.append(Spacer(1, 12))

    # Amount in Words
    story.append(Paragraph(f"<b>Amount Chargable (in words): {invoice.amount_in_words}</b>", styles['Normal']))
    story.append(Spacer(1, 12))

    # Bank Details
    story.append(Paragraph("<b>Company Bank Details:</b>", styles['Heading3']))
    bank_data = [
        ['Bank Name:', company.bank_name],
        ['Account No:', company.bank_account_no],
        ['IFSC:', company.bank_ifsc],
        ['Branch:', company.bank_branch or ''],
    ]

    bank_table = Table(bank_data, colWidths=[100, 200])
    bank_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))
    story.append(bank_table)
    story.append(Spacer(1, 12))

    # Signatories
    signatories_data = [
        ['Prepared By:', invoice.prepared_by or '', 'Verified By:', invoice.verified_by or '', 'Authorized By:', invoice.authorized_by or ''],
    ]

    signatories_table = Table(signatories_data, colWidths=[80, 100, 80, 100, 80, 100])
    signatories_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))
    story.append(signatories_table)
    story.append(Spacer(1, 24))

    # Terms and Conditions on second page
    doc.build(story)

    # Add T&C on second page
    c = canvas.Canvas(file_path, pagesize=A4)
    c.showPage()  # New page

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 800, "Terms and Conditions")

    c.setFont("Helvetica", 10)
    y = 780
    tc_text = ""
    if copy_type == 'ORIGINAL':
        tc_text = invoice.terms_conditions_original
    elif copy_type == 'DUPLICATE':
        tc_text = invoice.terms_conditions_duplicate
    else:
        tc_text = invoice.terms_conditions_extra

    for line in tc_text.split('\n'):
        c.drawString(50, y, line)
        y -= 15
        if y < 50:
            c.showPage()
            y = 800

    c.save()

    return file_path