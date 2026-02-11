from pathlib import Path
from pypdf import PdfReader
from docx import Document
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import json


search_path = Path(".")  

result = []

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    print("Error: GOOGLE_API_KEY not found.")
    exit()

client = genai.Client(api_key=API_KEY)


def build_prompt(file_path, preview_text):
    return f"""
Analyze the following file for organization.

Filename: {file_path.name}
Extension: {file_path.suffix}
Parent Folder: {file_path.parent}

Text Preview:
{preview_text}

Allowed Categories:
Career, Education, Finance, Projects, Personal
"""


for i in search_path.rglob("*"):

    # Skip directories + junk folders
    if i.is_dir() or any(part in {'.git', 'venv', '__pycache__'} for part in i.parts):
        continue

    preview = None

    try:
        if i.suffix.lower() == ".txt":
            preview = " ".join(i.read_text(errors="ignore").split()[:40])

        elif i.suffix.lower() == ".pdf":
            reader = PdfReader(i)
            full_text = ""
            for page in reader.pages:
                full_text += (page.extract_text() or "") + " "
                if len(full_text.split()) >= 30:
                    break
            preview = " ".join(full_text.split()[:30])

        elif i.suffix.lower() == ".docx":
            doc = Document(i)
            full_text = " ".join(p.text for p in doc.paragraphs)
            preview = " ".join(full_text.split()[:40])

        elif i.suffix.lower() == ".md":
            preview = " ".join(
                i.read_text(encoding="utf-8", errors="ignore").split()[:40]
            )

        else:
            continue

    except Exception:
        continue

    if not preview:
        preview = "No text content found."

    prompt = build_prompt(i, preview)

    try:
        print(f"Analyzing: {i.name}...")

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            config=types.GenerateContentConfig(
                system_instruction="""
You are an AI file analysis assistant.

Your task is to analyze short text previews of files and classify them
for a file organization system.

You DO NOT have access to the filesystem.
You DO NOT move or create files.
You ONLY analyze meaning and return structured decisions.

You must strictly follow these rules:

1. You will be given:
   - Filename
   - File extension
   - Parent folder path
   - A short text preview (may be incomplete)
   - A fixed list of allowed categories

2. Your job is to:
   - Understand the semantic meaning of the file
   - Choose the MOST appropriate category from the allowed list
   - Suggest a clear, human-readable subfolder name
   - Write a ONE-LINE summary of what the file contains
   - Assign a confidence score between 0.0 and 1.0

3. Allowed categories are FIXED.
   You MUST choose ONLY from the provided category list.
   If the content is unclear, choose the closest match and lower confidence.

4. Folder naming rules:
   - Use simple English words
   - No special characters
   - No file extensions
   - Max 3 words
   - Title Case (e.g. "College Notes", "Bank Statements")

5. You must NOT:
   - Invent new categories
   - Output explanations
   - Ask questions
   - Include markdown
   - Include extra text

6. If the text preview is empty or meaningless:
   - Still return a best-guess classification
   - Set confidence below 0.5

7. Your response MUST be valid JSON ONLY, in this exact format:

{
  "category": "<one of allowed categories>",
  "subfolder": "<suggested subfolder name>",
  "summary": "<one line summary>",
  "confidence": <number between 0.0 and 1.0>
}

Failure to follow these rules is considered an error.
"""
            ),
            contents=prompt
        )
        raw = response.text.strip()
        
        if "```" in raw:
            raw = raw.replace("```json", "").replace("```", "").strip()

        try:
            data = json.loads(raw)
            
            entry = {
                "file_name": i.name,
                "full_path": str(i.resolve()),
                "category": data.get("category", "Uncategorized"),
                "subfolder": data.get("subfolder", "Misc"),
                "summary": data.get("summary", "No summary"),
                "confidence": data.get("confidence", 0.0)
            }
            result.append(entry)
            
            print(f"  -> Category: {entry['category']}")
            print(f"  -> Subfolder: {entry['subfolder']}")
            print("-" * 40)

        except json.JSONDecodeError:
            print(f"  [ERROR] Failed to parse JSON for {i.name}")
            print(f"  Raw output: {raw}")

    except Exception as e:
        print(f"  [ERROR] API/Network error for {i.name}: {e}")



print("\n" + "="*30)
print(f"Processing Complete. Analyzed {len(result)} files.")
print("="*30)


with open("analysis_results.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2)
print("Results saved to 'analysis_results.json'")


print("\n" + "="*50)
print("DRY RUN PREVIEW")
print("="*50)


if not result:
    print("No files were analyzed. Exiting.")
    exit()

for item in result:
    status_icon = "✅" if item["confidence"] >= 0.7 else "⚠️ [SKIP]"
    
    print(f"{status_icon} {item['file_name']} → {item['category']}/{item['subfolder']} (Conf: {item['confidence']})")

print("-" * 50)


user_input = input(f"\nProceed with moving {len([r for r in result if r['confidence'] >= 0.7])} files? (y/n): ").strip().lower()

if user_input != 'y':
    print("Operation cancelled. No files were moved.")
    exit()

print("\nMoving files...")

success_count = 0
skip_count = 0
error_count = 0

for item in result:
    try:
        source = Path(item["full_path"])

        if item["confidence"] < 0.7:
            print(f"Skipping low confidence: {source.name}")
            skip_count += 1
            continue

        if not source.exists():
            print(f"Error: File not found (maybe moved?): {source.name}")
            error_count += 1
            continue

        target_folder = Path(".") / item["category"] / item["subfolder"]
        target_folder.mkdir(parents=True, exist_ok=True)

        destination = target_folder / source.name

        if destination.exists():
            print(f"Skipping duplicate: {source.name} already exists in {target_folder}")
            skip_count += 1
            continue

        source.rename(destination)
        print(f"Moved: {source.name} → {target_folder}")
        success_count += 1

    except Exception as e:
        print(f"Failed to move {item['file_name']}: {e}")
        error_count += 1

print("\n" + "="*50)
print(f"COMPLETE ")
print(f"Successfully Moved: {success_count}")
print(f"Skipped (Low Conf/Dupes): {skip_count}")
print(f"Errors: {error_count}")
print("="*50)

