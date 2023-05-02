import os
from PIL import Image
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas

input_folder = '<IMAGES PATH>'  # Replace with your folder path
output_file = 'output.pdf'  # Replace with your desired PDF output name

def get_png_files(input_folder):
    file_list = []
    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.png'):
            file_list.append(os.path.join(input_folder, filename))
    return file_list

def calculate_new_dimensions(width, height, max_width, max_height):
    aspect_ratio = float(width) / float(height)
    new_width = max_width
    new_height = int(new_width / aspect_ratio)
    
    if new_height > max_height:
        new_height = max_height
        new_width = int(new_height * aspect_ratio)

    return new_width, new_height

input_files = get_png_files(input_folder)
c = canvas.Canvas(output_file, pagesize=letter)

for image_file in input_files:
    image = Image.open(image_file)
    width, height = image.size
    page_width, page_height = letter

    if width > height:
        c.setPageSize(landscape(letter))
        page_width, page_height = landscape(letter)

    new_width, new_height = calculate_new_dimensions(width, height, page_width, page_height)
    c.drawImage(image_file, 0, 0, new_width, new_height)
    c.showPage()

c.save()