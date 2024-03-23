from PIL import Image, ImageFont, ImageDraw

class Receipt_Renderer():
    def render():
        resources_path = '/home/workstation33/Documents/Development Environment/Projects/discount_my_groceries/dmg_django/dmg_django_app/resources'
        background = Image.open(f'{resources_path}/wrinkled-paper-texture-7.jpg')
        text_font = ImageFont.truetype(f'{resources_path}/bitMatrix-A2.ttf')
        
        ink = (0,0,0)
        y_spacing = 30                  # vertical space between the entries.
        grouped_entries_space = 12
        vertical_cursor = 20            # vertical cursor.
        body_lm_rm = (10, 200)          # the body's left and right margin coordinates.
        header_lm = 45                  # header left margin coordinate.
        footer_lm = 70                  # footer left margin coordinate.

        receipt_w, receipt_h = 240, 480
        receipt = background.resize((receipt_w, receipt_h))
        edit = ImageDraw.Draw(receipt)

        # Header.
        supermarket_name = 'SUPERMARKET NAME\n'
        cashier = 'CASHIER: DISCOUNT MY GROCERIES\n'
        edit.multiline_text((header_lm, vertical_cursor), supermarket_name+cashier, ink, text_font, spacing=4, align='center', direction='ltr')

        # Header divider.
        vertical_cursor += y_spacing
        divider = '--------------------------------------------'
        edit.text((body_lm_rm[0], vertical_cursor), divider, ink, text_font, align='center', direction='ltr')

        # Item names and prices.
        vertical_cursor += (y_spacing-10)
        price = '0.00'
        edit.text((body_lm_rm[0], vertical_cursor), f'ITEM 1', ink, text_font, align='left', direction='ltr')
        edit.text((body_lm_rm[1], vertical_cursor), price, ink, text_font, align='right', direction='ltr')
        for j in range(2, 6):
            vertical_cursor += grouped_entries_space
            edit.text((body_lm_rm[0], vertical_cursor), f'ITEM {j}', ink, text_font, align='left', direction='ltr')
            edit.text((body_lm_rm[1], vertical_cursor), price, ink, text_font, align='right', direction='rtl')

        # Total cost.
        vertical_cursor += grouped_entries_space
        label = 'DUE VAT INCL'
        total_amount = '2387.00'
        # Made the label of the total cost begin at the footer_lm for center alignment. 
        edit.text((footer_lm, vertical_cursor), label, ink, text_font, align='center', direction='ltr')
        edit.text((body_lm_rm[1], vertical_cursor), total_amount, ink, text_font, align='right', direction='rtl')

        # Tax invoice segment.
        vertical_cursor += y_spacing
        tax_inv_divider = '-----------------TAX INVOICE----------------'
        edit.text((body_lm_rm[0], vertical_cursor), tax_inv_divider, ink, text_font, align='center', direction='ltr')
        # Calculate tax.
        vertical_cursor += grouped_entries_space
        vat_value = float(total_amount) * 0.15
        taxable_value = float(total_amount) - vat_value
        edit.text((body_lm_rm[0], vertical_cursor), 'VAT VAL', ink, text_font, align='left', direction='ltr')
        edit.text((body_lm_rm[1], vertical_cursor), str(vat_value), ink, text_font, align='right', direction='rtl')
        vertical_cursor += grouped_entries_space
        edit.text((body_lm_rm[0], vertical_cursor), 'TAXABLE VAL', ink, text_font, align='left', direction='ltr')
        edit.text((body_lm_rm[1], vertical_cursor), str(taxable_value), ink, text_font, align='right', direction='rtl')

        # Footer divider.
        vertical_cursor += y_spacing
        edit.line([(body_lm_rm[0], vertical_cursor),(230, vertical_cursor)], fill=ink, width=0)

        # Footer.
        vertical_cursor += y_spacing    
        # FIXME: Barcode.
        barcode_w, barcode_h = 180, 30
        barcode = Image.open(f'{resources_path}/barcode.png').resize((barcode_w, barcode_h))
        receipt.paste(barcode, (footer_lm-50, vertical_cursor))
        # Credits.
        vertical_cursor += (grouped_entries_space + barcode_h)
        footer_text = 'CREATED BY\nOUTER SPECTRUM LABS'        
        edit.multiline_text((footer_lm, vertical_cursor), footer_text, ink, text_font, spacing=4, align='center', direction='ltr')
        receipt.show()