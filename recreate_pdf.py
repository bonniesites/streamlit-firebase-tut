import base64

def decode_base64_and_save_pdf(base64_data, output_filename='reconstructed.pdf'):
    try:
        # Decode base64 data
        decoded_data = base64.b64decode(base64_data)

        # Save the decoded data to a PDF file
        with open(output_filename, 'wb') as pdf_file:
            pdf_file.write(decoded_data)

        print(f"PDF file '{output_filename}' has been reconstructed successfully.")
    except Exception as e:
        print(f"Error: {e}")

# Example base64-encoded PDF data
example_base64_data = ""  # Replace this with your actual base64 data

# Reconstruct the PDF file and save it
decode_base64_and_save_pdf(example_base64_data)
