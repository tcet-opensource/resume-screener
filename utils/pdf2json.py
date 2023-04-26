import PyPDF2
import json

# Open the PDF file
pdf_file = open("utils\example.pdf", "rb")

# Read the PDF content
pdf_reader = PyPDF2.PdfReader(pdf_file)
pdf_content = ""
for i in range(len(pdf_reader.pages)):
    pdf_content += pdf_reader.pages[i].extract_text()

# Close the PDF file
pdf_file.close()

# Convert the PDF content to JSON
json_content = json.dumps(pdf_content)

# Print the JSON content
print(pdf_content)
with open("models\json_data\converted_resume.json", "w") as f:
    json.dump(json_content, f, indent=4)
