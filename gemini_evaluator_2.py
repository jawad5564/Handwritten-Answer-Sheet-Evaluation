"""
Handwritten Answer Sheet Evaluator (Gemini)

Flow: model answer PDF + student sheet PDF -> Gemini -> "Question 1: 5/10" lines
      -> extract numbers -> save to CSV and JSON

Install:  pip install google-genai
Run:      python gemini_evaluator.py
"""

import csv
import json
import re
import os
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

from google import genai
from google.genai import types

# ---- Configuration ----

MODEL_NAME = "gemini-4-hydrogen"     #gemini-3.1-flash-lite       gemini-4-hydrogen
STUDENT_PDF = "/home/jawad/Documents/project/Handwritten_Answer_Sheet_Evaluation/output.pdf"
MODEL_ANSWER_PDF = "/home/jawad/Documents/project/Handwritten_Answer_Sheet_Evaluation/1_2_3_4.pdf"
OUTPUT_CSV = "result.csv"
OUTPUT_JSON = "result.json"

PROMPT = """You are an examiner. The first PDF is the model answer with marks per question.
The second PDF is a scanned handwritten student answer sheet.
Read the handwriting, compare each answer with the model answer (meaning, not exact words),
and give marks (partial credit allowed, steps of 0.5, never above the maximum). per question max_mark=5 .
Reply ONLY with one line per question in exactly this format, nothing else:
Question 1: 5/10
Question 2: 7/10"""


def read_pdf(path: str) -> types.Part:
    with open(path, "rb") as f:
        return types.Part.from_bytes(data=f.read(), mime_type="application/pdf")


def ask_gemini() -> str:
    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[PROMPT, read_pdf(MODEL_ANSWER_PDF), read_pdf(STUDENT_PDF)],
        config=types.GenerateContentConfig(temperature=0),
    )
    return response.text


def extract_marks(text: str) -> list:
    """Pull (question, marks, max) out of lines like 'Question 1: 5/10'."""
    rows = []
    for q, got, mx in re.findall(r"Question\s*(\d+)\s*:\s*([\d.]+)\s*/\s*([\d.]+)", text, re.I):
        rows.append({"question": int(q), "marks": float(got), "max_marks": float(mx)})
    return rows


def save_csv(rows: list, path: str):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["question", "marks", "max_marks"])
        writer.writeheader()
        writer.writerows(rows)


def save_json(rows: list, path: str):
    total = sum(r["marks"] for r in rows)
    max_total = sum(r["max_marks"] for r in rows)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"questions": rows, "total": total, "out_of": max_total}, f, indent=2)


def main():
    text = ask_gemini()
    print(text)

    rows = extract_marks(text)
    if not rows:
        print("Could not find any 'Question N: x/y' lines in the reply.")
        return

    save_csv(rows, OUTPUT_CSV)
    save_json(rows, OUTPUT_JSON)
    print(f"\nSaved {len(rows)} questions to {OUTPUT_CSV} and {OUTPUT_JSON}")


if __name__ == "__main__":
    main()
