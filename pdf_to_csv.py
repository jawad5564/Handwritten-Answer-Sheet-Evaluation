
import pdfplumber
import pandas as pd
import os

# Input PDF
INPUT_PDF = "/home/jawad/Documents/project/Handwritten_Answer_Sheet_Evaluation/1_2_3_4.pdf"

# Output folder
OUTPUT_DIR = "/home/jawad/Documents/project/Handwritten_Answer_Sheet_Evaluation"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def pdf_to_csv(pdf_path):

    filename = os.path.splitext(os.path.basename(pdf_path))[0]

    extracted_data = []

    with pdfplumber.open(pdf_path) as pdf:

        for page_number, page in enumerate(pdf.pages, start=1):

            # Extract all text from the page
            text = page.extract_text(
                layout=True
            )

            if text and text.strip():

                extracted_data.append({
                    "Page": page_number,
                    "Content": text
                })

            else:
                extracted_data.append({
                    "Page": page_number,
                    "Content": "No extractable text found"
                })

    # Create DataFrame
    df = pd.DataFrame(extracted_data)

    # Save CSV
    output_path = os.path.join(
        OUTPUT_DIR,
        filename + ".csv"
    )

    df.to_csv(
        output_path,
        index=False,
        encoding="utf-8-sig"
    )

    print("CSV successfully saved:", output_path)


if os.path.isfile(INPUT_PDF):

    pdf_to_csv(INPUT_PDF)

else:
    print("PDF file not found:", INPUT_PDF)


print("Conversion completed!")
