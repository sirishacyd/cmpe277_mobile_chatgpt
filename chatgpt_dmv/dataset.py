import pdfplumber
pdf_path = '/Users/siri/Desktop/dmv_2023.pdf'
def pdf_to_text(file_path):
    with pdfplumber.open(file_path) as pdf:
        num_pages = len(pdf.pages)
        extracted_text = ''

        for page_num in range(num_pages):
            page = pdf.pages[page_num]
            extracted_text += page.extract_text()

    return extracted_text

text = pdf_to_text(pdf_path)

with open('output.txt', 'w', encoding='utf-8') as output_file:
    output_file.write(text)
