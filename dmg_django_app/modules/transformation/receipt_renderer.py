from PIL import Image, ImageFont, ImageDraw

class ReceiptRenderer():
    
    def __init__(self):
        self.resources_path = '/home/workstation33/Documents/Development Environment/Projects/discount_my_groceries/dmg_django/dmg_django_app/resources'
        # Properties and settings.
        self.items: dict[str] = {}
        self.black_ink = (0,0,0)
        self.y_spacing = 30                             # vertical space between the entries.
        self.grouped_entries_space = 12
        self.vertical_cursor: float = 20.00             # vertical cursor.
        self.horizontal_cursor: float = 0.00
        self.body_lm_rm = (10, 200)                     # the body's left and right margin coordinates.
        self.header_lm = 45                             # header left margin coordinate.
        self.footer_lm = 70                             # footer left margin coordinate.
        self.footer_tb: float = 0.00
        self.footer_bb: float = 460
        self.items_segment_limit = 380                  # segment limit.
        self.supermarket_logo: str = ""
        self.receipts:list[Image.Image] = []

        # Receipt properties.
        self.receipt_w, self.receipt_h = 240, 480
        self.text_font = ImageFont.truetype(f'{self.resources_path}/bitMatrix-A2.ttf')
        self.edit: ImageDraw.ImageDraw
        self.__create_new_canvas()

    def render(self, _items: dict[str]):
        self.__set_items(_items)
        # Header.
        cashier = 'CASHIER: DISCOUNT MY GROCERIES\n'
        self.edit.multiline_text((self.header_lm, self.vertical_cursor), self.supermarket_logo+'\n'+cashier, self.black_ink, self.text_font, spacing=4, align='center', direction='ltr')

        # Header divider.
        self._move_cursor(self.y_spacing)
        divider = '--------------------------------------------'
        self.edit.text((self.body_lm_rm[0], self.vertical_cursor), divider, self.black_ink, self.text_font, align='center', direction='ltr')

        # Populate items to the receipt.
        self._items_segment()

        # Footer divider.
        self._move_cursor(self.y_spacing)
        self.edit.line([(self.body_lm_rm[0], self.vertical_cursor), (230, self.vertical_cursor)], fill=self.black_ink, width=0)

        self._footer_segment()

        # Credits.
        self._move_cursor(self.y_spacing)
        credits_top_border = self.vertical_cursor
        footer_text = 'CREATED BY\nOUTER SPECTRUM LABS'        
        self.edit.multiline_text((self.footer_lm, credits_top_border), footer_text, self.black_ink, self.text_font, spacing=4, align='center', direction='ltr')
    
        for receipt in self.receipts:
            receipt.show()

    def _items_segment(self):
        # Item names and prices.
        self._move_cursor(self.y_spacing-10)
        total_amount:float = 0.00
        count: int = 0
        for (name, data) in self.items.items():
            count += 1
            if count > 1:
                self._move_cursor(self.grouped_entries_space)
            
            # extend the receipt if a specific margin is exceeded.
            if self.vertical_cursor > self.items_segment_limit:
                self.__reset_cursor()
                self.__create_new_canvas()
            
            # item quantity and name
            if data.get('quantity') is not '1':
                self.edit.text((self.body_lm_rm[0] + 25.00, self.vertical_cursor), name, self.black_ink, self.text_font, align='left', direction='ltr')
                self._move_cursor(self.grouped_entries_space)
                self.edit.text((100.00, self.vertical_cursor), f"{data.get('quantity')} @ {data.get('cost_of_item')}", self.black_ink, self.text_font, align='center', direction='ltr')
            else:
                self.edit.text((self.body_lm_rm[0], self.vertical_cursor), name, self.black_ink, self.text_font, align='left', direction='ltr')

            # item price
            self.edit.text((self.__get_price_margin(data.get('total_price')), self.vertical_cursor), data.get('total_price'), self.black_ink, self.text_font, align='right', direction='ltr')
            total_amount += float(data.get('total_price')[1:]) # remove R

        # Total cost.
        self._move_cursor(self.grouped_entries_space)
        label = 'DUE VAT INCL'
        str_total_amount = 'R'+str(round(total_amount, 2))

        # let the label of the total cost begin at the footer_lm for center alignment. 
        self.edit.text((self.footer_lm, self.vertical_cursor), label, self.black_ink, self.text_font, align='center', direction='ltr')
        self.edit.text((self.__get_price_margin(str_total_amount), self.vertical_cursor), str_total_amount, self.black_ink, self.text_font, align='right', direction='ltr')

        # Tax invoice segment.
        self._move_cursor(self.y_spacing)
        tax_inv_divider = '-----------------TAX INVOICE----------------'
        self.edit.text((self.body_lm_rm[0], self.vertical_cursor), tax_inv_divider, self.black_ink, self.text_font, align='center', direction='ltr')
        
        # Calculate tax.
        self._move_cursor(self.grouped_entries_space)
        vat_value = round(total_amount * 0.15, 2)
        self.edit.text((self.body_lm_rm[0], self.vertical_cursor), 'VAT VAL', self.black_ink, self.text_font, align='left', direction='ltr')
        self.edit.text((self.__get_price_margin('R'+str(vat_value)), self.vertical_cursor), 'R'+str(vat_value), self.black_ink, self.text_font, align='right', direction='ltr')
        self._move_cursor(self.grouped_entries_space)
        taxable_value = round(total_amount - vat_value, 2)
        self.edit.text((self.body_lm_rm[0], self.vertical_cursor), 'TAXABLE VAL', self.black_ink, self.text_font, align='left', direction='ltr')
        self.edit.text((self.__get_price_margin('R'+str(taxable_value)), self.vertical_cursor), 'R'+str(taxable_value), self.black_ink, self.text_font, align='right', direction='ltr')

    def _footer_segment(self):
        # Footer.
        self._move_cursor(self.grouped_entries_space)    
        # Barcode.
        barcode_h: float = 20
        barcode_lm: float = 20
        barcode_rm: float = 220
        horizontal_cursor = barcode_lm
        barcode_sizes = [1, 1.2, 1.5, 1.6, 2, 1.8, 1.4, 2, 1.5, 1.2, 1.7]
        barcode_top = self.vertical_cursor
        barcode_bottom = barcode_top+barcode_h
        x, k, index_limit = 2, 0, len(barcode_sizes)-1
        while not (horizontal_cursor > barcode_rm):
            if x % 2 == 0:
                self.edit.rectangle([(horizontal_cursor, barcode_top), (horizontal_cursor+barcode_sizes[k], barcode_bottom)], self.black_ink, width=0)
            horizontal_cursor += barcode_sizes[k]
            x += 1
            k += 1
            if k > index_limit:
                k = 0

    def _move_cursor(self, amount: float):
        self.vertical_cursor += amount

    def __set_items(self, _items: dict[str]):
        for (name, products) in _items.items():
            self.supermarket_logo = name
            self.items = products

    def __create_new_canvas(self):
        self.receipts.append(Image.open(f'{self.resources_path}/wrinkled-paper-texture-7.jpg').resize((self.receipt_w, self.receipt_h)))
        count = len(self.receipts)
        self.edit = ImageDraw.Draw(self.receipts[count-1])

    def __reset_cursor(self):
        self.vertical_cursor = 20.00

    def __get_price_margin(self, _price:str) -> float:
        price_margin = self.body_lm_rm[1]
        units = len(_price[:_price.find('.')])
        # draw price from right to left.
        if units == 4:
            price_margin -= 5
        elif units == 5:
            price_margin -= 10
        return price_margin