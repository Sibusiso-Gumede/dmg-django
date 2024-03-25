from PIL import Image, ImageFont, ImageDraw, ImageColor

class Receipt_Renderer():
    def render():
        resources_path = '/home/workstation33/Documents/Development Environment/Projects/discount_my_groceries/dmg_django/dmg_django_app/resources'
        # Properties and settings.
        black_ink = (0,0,0)
        white_ink = (255,255,255)
        black_shades = (0,127)
        white_shades = (128,255)
        y_spacing = 30                  # vertical space between the entries.
        grouped_entries_space = 12
        vertical_cursor = 20            # vertical cursor.
        horizontal_cursor = 0.00
        body_lm_rm = (10, 200)          # the body's left and right margin coordinates.
        header_lm = 45                  # header left margin coordinate.
        footer_lm = 70                  # footer left margin coordinate.

        # Receipt.
        background = Image.open(f'{resources_path}/wrinkled-paper-texture-7.jpg')
        text_font = ImageFont.truetype(f'{resources_path}/bitMatrix-A2.ttf')
        receipt_w, receipt_h = 240, 480
        receipt = background.resize((receipt_w, receipt_h))
        edit = ImageDraw.Draw(receipt)

        # Header.
        supermarket_name = 'SUPERMARKET NAME\n'
        cashier = 'CASHIER: DISCOUNT MY GROCERIES\n'
        edit.multiline_text((header_lm, vertical_cursor), supermarket_name+cashier, black_ink, text_font, spacing=4, align='center', direction='ltr')

        # Header divider.
        vertical_cursor += y_spacing
        divider = '--------------------------------------------'
        edit.text((body_lm_rm[0], vertical_cursor), divider, black_ink, text_font, align='center', direction='ltr')

        # Item names and prices.
        vertical_cursor += (y_spacing-10)
        price = '0.00'
        edit.text((body_lm_rm[0], vertical_cursor), f'ITEM 1', black_ink, text_font, align='left', direction='ltr')
        edit.text((body_lm_rm[1], vertical_cursor), price, black_ink, text_font, align='right', direction='ltr')
        for j in range(2, 6):
            vertical_cursor += grouped_entries_space
            edit.text((body_lm_rm[0], vertical_cursor), f'ITEM {j}', black_ink, text_font, align='left', direction='ltr')
            edit.text((body_lm_rm[1], vertical_cursor), price, black_ink, text_font, align='right', direction='rtl')

        # Total cost.
        vertical_cursor += grouped_entries_space
        label = 'DUE VAT INCL'
        total_amount = '2387.00'
        # Made the label of the total cost begin at the footer_lm for center alignment. 
        edit.text((footer_lm, vertical_cursor), label, black_ink, text_font, align='center', direction='ltr')
        edit.text((body_lm_rm[1], vertical_cursor), total_amount, black_ink, text_font, align='right', direction='rtl')

        # Tax invoice segment.
        vertical_cursor += y_spacing
        tax_inv_divider = '-----------------TAX INVOICE----------------'
        edit.text((body_lm_rm[0], vertical_cursor), tax_inv_divider, black_ink, text_font, align='center', direction='ltr')
        # Calculate tax.
        vertical_cursor += grouped_entries_space
        vat_value = float(total_amount) * 0.15
        taxable_value = float(total_amount) - vat_value
        edit.text((body_lm_rm[0], vertical_cursor), 'VAT VAL', black_ink, text_font, align='left', direction='ltr')
        edit.text((body_lm_rm[1], vertical_cursor), str(vat_value), black_ink, text_font, align='right', direction='rtl')
        vertical_cursor += grouped_entries_space
        edit.text((body_lm_rm[0], vertical_cursor), 'TAXABLE VAL', black_ink, text_font, align='left', direction='ltr')
        edit.text((body_lm_rm[1], vertical_cursor), str(taxable_value), black_ink, text_font, align='right', direction='rtl')

        # Footer divider.
        vertical_cursor += y_spacing
        edit.line([(body_lm_rm[0], vertical_cursor),(230, vertical_cursor)], fill=black_ink, width=0)

        # Footer.
        vertical_cursor += y_spacing    
        # FIXME: Barcode.
        barcode_w, barcode_h = 200, 20
        barcode_lm, barcode_rm = 20, 220.00
        horizontal_cursor = barcode_lm
        barcode_sizes = [1.2, 1, 1.5, 1, 2, 1, 2.3, 1, 1.5, 1, 1.7]
        barcode_bottom = vertical_cursor+barcode_h
        barcode_top = vertical_cursor
        barcode_right = horizontal_cursor
        x, k, index_limit = 2, 0, len(barcode_sizes)-1
        while not (horizontal_cursor > barcode_rm):
            if x % 2 == 0:
                edit.rectangle([(horizontal_cursor, barcode_top), (horizontal_cursor+barcode_sizes[k], barcode_bottom)], black_ink, width=0)
            horizontal_cursor += barcode_sizes[k]
            x += 1
            k += 1
            if k > index_limit:
                k = 0

        # Credits.
        vertical_cursor += (grouped_entries_space + barcode_h)
        footer_text = 'CREATED BY\nOUTER SPECTRUM LABS'        
        edit.multiline_text((footer_lm, vertical_cursor), footer_text, black_ink, text_font, spacing=4, align='center', direction='ltr')
        receipt.show()