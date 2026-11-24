# Handwritten-Answer-Sheet-Evaluation
Built a Python tool that automatically grades scanned handwritten answer sheets. It takes the student's sheet and a model answer as PDFs, uses the  multimodal VLM API to read the handwriting and compare each answer with the model answer, and awards question-wise marks. Regex-based extraction turns the model's output into structured marks.
