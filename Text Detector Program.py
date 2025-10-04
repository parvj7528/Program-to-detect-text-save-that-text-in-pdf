import os
from tkinter import filedialog, Tk, messagebox
from PIL import Image
import pytesseract
from fpdf import FPDF

# Update this path according to your Tesseract installation
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Function to extract text from image
def extract_text_from_image(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img, lang="eng")  # change lang if needed
    return text.strip()

# Function to save text as PDF with Unicode support
def save_text_as_pdf(text, pdf_path):
    pdf = FPDF()
    pdf.add_page()

    # ✅ Add Arial TTF font (no uni=True needed in fpdf2)
    font_path = r"C:\Windows\Fonts\arial.ttf"
    if not os.path.exists(font_path):
        messagebox.showerror("Font Error", f"Font not found: {font_path}\nPlease install Arial or change the font path.")
        return

    pdf.add_font("ArialUnicode", "", font_path)
    pdf.set_font("ArialUnicode", "", 14)

    # ✅ Write extracted text
    pdf.multi_cell(0, 10, text)

    # Save PDF
    pdf.output(pdf_path)

# Main function
def main():
    root = Tk()
    root.withdraw()

    # Ask user to select an image
    image_path = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.tif *.tiff")]
    )

    if not image_path:
        messagebox.showinfo("No Image Selected", "You didn't select any image. Exiting.")
        return

    # Extract text
    text = extract_text_from_image(image_path)

    if not text:
        messagebox.showinfo("No Text Found", "No text could be extracted from the image.")
        return

    # Save PDF in Downloads folder
    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    os.makedirs(downloads_folder, exist_ok=True)
    pdf_path = os.path.join(downloads_folder, "Extracted_Text.pdf")

    save_text_as_pdf(text, pdf_path)

    messagebox.showinfo("Success", f"PDF saved successfully at:\n{pdf_path}")

if __name__ == "__main__":
    main()
