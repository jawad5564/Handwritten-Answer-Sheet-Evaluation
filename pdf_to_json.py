
import pdfplumber
import json
import os

# Input PDF
INPUT_PDF = "/home/jawad/Documents/project/Handwritten_Answer_Sheet_Evaluation/1_2_3_4.pdf"

# Output directory
OUTPUT_DIR = "/home/jawad/Documents/project/Handwritten_Answer_Sheet_Evaluation"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def pdf_to_json(pdf_path):

    filename = os.path.splitext(
        os.path.basename(pdf_path)
    )[0]

    extracted_data = []

    with pdfplumber.open(pdf_path) as pdf:

        for page_number, page in enumerate(pdf.pages, start=1):

            # Extract complete page text
            text = page.extract_text(layout=True)

            # Extract tables separately
            tables = page.extract_tables()

            page_data = {
                "page": page_number,
                "content": text if text else "",
                "tables": tables if tables else []
            }

            extracted_data.append(page_data)

    # Output JSON path
    output_path = os.path.join(
        OUTPUT_DIR,
        filename + ".json"
    )

    # Save JSON
    with open(output_path, "w", encoding="utf-8") as file:

        json.dump(
            extracted_data,
            file,
            ensure_ascii=False,
            indent=4
        )

    print("JSON saved:", output_path)


if os.path.isfile(INPUT_PDF):

    pdf_to_json(INPUT_PDF)

else:
    print("PDF file not found:", INPUT_PDF)


print("Conversion completed!")
