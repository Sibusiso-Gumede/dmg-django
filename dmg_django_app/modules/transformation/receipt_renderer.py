from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
from dmg_django.settings import BASE_DIR
import base64

class ReceiptRenderer():

    def __init__(self, _items: dict[str]):
        # Properties and settings.
        self.resources_dir = f'{BASE_DIR}/dmg_django_app/resources'
        self.items: dict[str] = {}
        self.black_ink = (0,0,0)
        self.y_spacing = 30                             # vertical space between the entries.
        self.grouped_entries_space = 12
        self.vertical_cursor: float = 20.00             # vertical cursor.
        self.horizontal_cursor: float = 0.00
        self.body_lm_rm = (10, 200)                     # the body's left and right margin coordinates.
        self.header_lm = 45                             # header left margin coordinate.
        self.footer_lm = 70                             # footer left margin coordinate.
        self.bottom_margin = 460
        self.items_limit = 400                          # segment limit.
        self.supermarket_logo: str = ""
        self.receipts:list[Image.Image] = []
        self.bin_imgs:list[bytes] = []

        # Receipt properties.
        self.TITLE_LENGTH:int = 30
        self.receipt_w, self.receipt_h = 240, 480
        self.barcode_height:int = 25
        self.divider = '--------------------------------------------'
        self.text_font = ImageFont.truetype(f'{self.resources_dir}/bitMatrix-A2.ttf')
        self.edit: ImageDraw.ImageDraw
        self.__create_new_canvas()
        self.__set_items(_items)

    def render(self) -> dict[str]:
        # Header.
        cashier = 'CASHIER: DISCOUNT MY GROCERIES\n'
        self.edit.multiline_text((self.header_lm, self.vertical_cursor), self.supermarket_logo+"\n"+cashier, self.black_ink, self.text_font, spacing=4, align='center', direction='ltr', font_size=10)

        # Header divider.
        self.__move_cursor(self.y_spacing)
        self.edit.text((self.body_lm_rm[0], self.vertical_cursor), self.divider, self.black_ink, self.text_font, align='center', direction='ltr')

        # Populate items to the receipt.
        self.__items_segment()

        # Footer segment.
        self.__footer_segment()

        for receipt in self.receipts:
            img_byte_arr = BytesIO()
            receipt.save(img_byte_arr, "PNG")
            self.bin_imgs.append(img_byte_arr.getvalue())

        return self.__encode_images()

    def __items_segment(self):
        # Item names and prices.
        self.__move_cursor(self.y_spacing-10, "is")
        total_amount: float = 0.00
        count: int = 0
        for (name, data) in self.items.items():
            if count > 0:
                self.__move_cursor(self.grouped_entries_space, "is")

            # item quantity and name.
            self.edit.text((self.body_lm_rm[0], self.vertical_cursor), name, self.black_ink, self.text_font, align='left', direction='ltr')
            if data.get('quantity') != '1':
                self.__move_cursor(self.grouped_entries_space, "is")
                self.edit.text((80.00, self.vertical_cursor), f"{data.get('quantity')} @ {data.get('cost_of_item')}", self.black_ink, self.text_font, align='center', direction='ltr')

            # item price.
            total_price:str = data.get('total_price')
            # if there are two prices then use the less one.
            if total_price.count('R') > 1:
                total_price = total_price[total_price.rfind('R'):]
            self.edit.text((self.__get_price_margin(total_price), self.vertical_cursor), total_price, self.black_ink, self.text_font, align='right', direction='ltr')
            
            total_amount += float(total_price[1:]) # remove R
            count += 1

        # Total cost.
        self.__move_cursor(self.grouped_entries_space, "is")
        label = 'DUE VAT INCL'
        str_total_amount = 'R'+str(round(total_amount, 2))

        # let the label of the total cost begin at the footer_lm for center alignment. 
        self.edit.text((self.footer_lm, self.vertical_cursor), label, self.black_ink, self.text_font, align='center', direction='ltr')
        self.edit.text((self.__get_price_margin(str_total_amount), self.vertical_cursor), str_total_amount, self.black_ink, self.text_font, align='right', direction='ltr')

        # Tax invoice segment.
        self.__test_area()
        self.__move_cursor(self.y_spacing, "is")
        tax_inv_divider = '-----------------TAX INVOICE----------------'
        self.edit.text((self.body_lm_rm[0], self.vertical_cursor), tax_inv_divider, self.black_ink, self.text_font, align='center', direction='ltr')

        # Calculate tax.
        self.__move_cursor(self.grouped_entries_space, "is")
        vat_value = round(total_amount * 0.15, 2)
        self.edit.text((self.body_lm_rm[0], self.vertical_cursor), 'VAT VAL', self.black_ink, self.text_font, align='left', direction='ltr')
        self.edit.text((self.__get_price_margin('R'+str(vat_value)), self.vertical_cursor), 'R'+str(vat_value), self.black_ink, self.text_font, align='right', direction='ltr')
        self.__move_cursor(self.grouped_entries_space, "is")
        taxable_value = round(total_amount - vat_value, 2)
        self.edit.text((self.body_lm_rm[0], self.vertical_cursor), 'TAXABLE VAL', self.black_ink, self.text_font, align='left', direction='ltr')
        self.edit.text((self.__get_price_margin('R'+str(taxable_value)), self.vertical_cursor), 'R'+str(taxable_value), self.black_ink, self.text_font, align='right', direction='ltr')

    def __footer_segment(self):
        if self.vertical_cursor > self.items_limit:
            self.__reset_cursor()
            self.__create_new_canvas()

        # Footer divider.
        self.__move_cursor(self.y_spacing, "fs")
        self.edit.text((self.body_lm_rm[0], self.vertical_cursor), self.divider, self.black_ink, self.text_font, align='center', direction='ltr')

        # Footer.
        self.__move_cursor(self.grouped_entries_space, "fs")

        # Barcode.
        barcode_lm: int = 10
        barcode = Image.open(f"{self.resources_dir}/barcode.png").resize((int(220), self.barcode_height))
        self.receipts[-1].alpha_composite(barcode, (barcode_lm, int(self.vertical_cursor)))

        # Credits.
        self.__move_cursor(self.barcode_height+5)
        credits_top_border = self.vertical_cursor
        footer_text = 'CREATED BY\nSIBUSISO J. GUMEDE'
        self.edit.multiline_text((self.footer_lm, credits_top_border), footer_text, self.black_ink, self.text_font, spacing=4, align='center', direction='ltr')

    def __move_cursor(self, amount: float, area: str = None):
        self.vertical_cursor += amount
        if (self.vertical_cursor > self.bottom_margin):
            self.__reset_cursor()
            self.__create_new_canvas()

    def __set_items(self, _items: dict[str]):
        for (name, products) in _items.items():
            self.supermarket_logo = name.upper()
            for (title, data) in products.items():
                if(not(len(title) <= self.TITLE_LENGTH)):
                    self.items.update({self.__shorten_string(title): data})
                else:
                    self.items.update({title: data})

    def __create_new_canvas(self):
        self.receipts.append(Image.open(f'{self.resources_dir}/wrinkled-paper-texture.png').convert('RGBA').resize((self.receipt_w, self.receipt_h)))
        count = len(self.receipts)
        self.edit = ImageDraw.Draw(self.receipts[count-1], 'RGBA')

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

    def __shorten_string(self, s:str) -> str:
        '''Returns a shorter version of a string provided the maximum
            length.'''
        formatted: str = ""
        count: int = 0

        # find the position of the first digit in the string.
        while count < len(s):
            if s[count].isdigit():
                break
            count += 1

        # remove the rest of the string starting from the first
        # digit found.
        formatted = s[:count]

        # slice formatted string if it's longer than 30 characters.
        if len(formatted) > self.TITLE_LENGTH:
            formatted = formatted[:self.TITLE_LENGTH-1]

        restricted:set[str] = ["with", "in", "on", "No", "&"]
        formatted_terms:list[str] = []
        formatted_terms = formatted.split(' ')

        # find the last term of the formatted string.
        # ascertain that it meets the required format constraints.
        # the constraints are: a string should not end with a
        # prepostion or it's last term should not be partial.
        while True:
            if (formatted_terms[-1] in restricted) or (not (formatted_terms[-1] == s.split(' ')[len(formatted_terms)-1])):
                formatted_terms.pop()
                formatted = ' '.join(formatted_terms)
            else:
                break
        return formatted

    def __encode_images(self) -> dict[str]:
        encoded_images:dict[str] = {}
        count:int = 1
        for image in self.bin_imgs:
            encoded_images.update({count: base64.b64encode(image).decode('ascii')})
            count += 1
        return encoded_images

    def __test_area(self):
        if self.vertical_cursor > self.items_limit:
            self.__reset_cursor()
            self.__create_new_canvas()
