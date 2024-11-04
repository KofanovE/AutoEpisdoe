import PyPDF2
import re

# Открываем PDF файл
word = 'Z57.1'
word_first = word[0] + '00'

with open('MKX10AM.pdf', 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    number_of_pages = len(reader.pages)

    # Извлекаем текст со всех страниц
    for page_num in range(3):
        page = reader.pages[page_num]
        text = page.extract_text()
        #print(f"Page {page_num + 1}:\n{text}")
        if text:
            if word[0] == "U":
                number_1 = 1014
                number_2 = 1018
                break
            else:
                lines = text.split('\n')
                for i, line in enumerate(lines):
                    if word_first.lower() in line.lower():
                        match = re.search(r'(\d+)$', line.strip())
                        if match:
                            number_1 = int(match.group(1))
                            next_match = re.search(r'(\d+)$', lines[i + 1].strip())
                            number_2 = int(next_match.group(1))
                        else:
                            match_2 = re.search(r'(\d+)$', lines[i+1].strip())
                            number_1 = int(match_2.group(1))
                            next_match_2 = re.search(r'(\d+)$', lines[i + 2].strip())
                            number_2 = int(next_match_2.group(1))

    number_1 = number_1 + 41
    number_2 = number_2 + 41


    for page_num in range(number_1-1, number_2+1):
        page = reader.pages[page_num]
        text = page.extract_text()

        if text:
            lines = text.split('\n')
            for line in lines:
                if line.lower().startswith(word.lower()) or line[1:].lower().startswith(word.lower()):
                    remaining_line = line[len(word)+2:].strip()
                    print(f"{remaining_line}")