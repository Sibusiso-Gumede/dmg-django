from PIL import Image, ImageFont, ImageDraw

class Receipt_Renderer():
    def render():
        resources_path = '/home/workstation33/Documents/Development Environment/Projects/discount_my_groceries/dmg_django/dmg_django_app/resources'
        background = Image.open(f'{resources_path}/wrinkled-paper-texture-7.jpg')
        text_font = ImageFont.truetype(f'{resources_path}/bitMatrix-A2.ttf')
        heading = 'Discount My Groceries'
        subheading = 'Supermarket Name'
        divider = '-'
        list = 'item_1\t\tR0.00\nitem_2\t\tR0.00\nitem_3\t\tR0.00\n...'
        total = 'R2387.00'
        footer = 'created by\nOuter Spectrum Labs'

        #edit = ImageDraw.ImageDraw(background)
        receipt = background.resize((240,480))
        edit = ImageDraw.Draw(receipt)
        edit.text((65, 60), heading, (0,0,0), text_font, spacing=8, align='center', direction='ltr')
        receipt.show()