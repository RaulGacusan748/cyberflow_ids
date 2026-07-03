import zipfile
import xml.etree.ElementTree as ET
import os
import sys

# Ensure stdout handles UTF-8 correctly
sys.stdout.reconfigure(encoding='utf-8')

def get_docx_text(path):
    WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    PARA = WORD_NAMESPACE + 'p'
    TEXT = WORD_NAMESPACE + 't'
    
    if not os.path.exists(path):
        return f"File not found: {path}"
        
    try:
        with zipfile.ZipFile(path) as docx:
            xml_content = docx.read('word/document.xml')
            root = ET.fromstring(xml_content)
            paragraphs = []
            for paragraph in root.iter(PARA):
                texts = [node.text for node in paragraph.iter(TEXT) if node.text]
                if texts:
                    paragraphs.append(''.join(texts))
            return '\n'.join(paragraphs)
    except Exception as e:
        return f"Error reading {path}: {str(e)}"

downloads_dir = r"C:\Users\user\Downloads"
files_to_check = [
    "CyberFlow IDS June 24 full literature.docx",
    "FINAL MANUSCRIPT.docx",
    "FINAL MANUSCRIPT edited.docx",
    "GROUP-2-MANUSCRIPT-REPORT (REVISED).docx"
]

for filename in files_to_check:
    full_path = os.path.join(downloads_dir, filename)
    if os.path.exists(full_path):
        print(f"\n--- Reading {filename} (Size: {os.path.getsize(full_path)} bytes) ---")
        text = get_docx_text(full_path)
        print(f"Length of text: {len(text)} characters")
        out_name = filename.replace(".docx", "_extracted.txt")
        out_path = os.path.join("scratch", out_name)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Successfully wrote extracted text to {out_path}")
        print("Sample of first 500 characters:")
        print(text[:500])
