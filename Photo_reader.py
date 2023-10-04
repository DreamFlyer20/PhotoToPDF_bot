import easyocr

def text_recognition(file_path, text_file_name):
    reader = easyocr.Reader(['ru', 'en', 'uk'])
    result = reader.readtext(file_path, detail=0, paragraph=True)
    with open(text_file_name, "w", encoding='utf-16') as file:
        for line in result:
            file.write(f"{line}" )