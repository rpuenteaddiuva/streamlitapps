import pdfplumber
import re
import os

pdf_path = os.path.join("datos", "Boletín de Calidad_ADS_Octubre 2025 v2.pdf")

def extract_benchmarks():
    print(f"Extracting benchmarks from {pdf_path}...")
    text_content = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text_content += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return

    # Regex for Satisfaction/NPS
    nps_match = re.search(r"NPS.*?(\d+[.,]\d+)", text_content, re.IGNORECASE)
    sla_match = re.search(r"Cumplimiento.*?(\d+[.,]\d+)%", text_content, re.IGNORECASE)
    
    print("\n--- BENCHMARK DATA ---")
    if nps_match:
        print(f"Official NPS: {nps_match.group(1)}")
    else:
        print("Official NPS not found in text.")
        
    if sla_match:
        print(f"Official SLA: {sla_match.group(1)}")
    else:
        print("Official SLA not found in text.")
        
    # Dump text for manual inspection if needed
    with open("results_benchmark_dump.txt", "w", encoding="utf-8") as f:
        f.write(text_content)

if __name__ == "__main__":
    extract_benchmarks()
