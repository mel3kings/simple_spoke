import json
import base64
import PyPDF2


def lambda_handler(event, context):
    try:
        # Get the PDF bytes from the request
        print("Event received by Lambda function: " + json.dumps(event, indent=2))
        body = event['body']
        print(body)
        pdf_data = body.read()
        print(pdf_data)
        #pdf_bytes = base64.b64decode(body)

        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(pdf_data)


        # Process the PDF bytes
        # Replace this with your custom processing logic
        #process_pdf(pdf_bytes)

        # Extract text from each page
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        text = sanitize_string(text)
        # Delete the temporary file (optional)
        # Remove this if you don't want to delete the file
        # delete_file(file_path)

        return {
            'statusCode': 200,
            'body': 'PDF processing successful'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': 'Error: {}'.format(str(e))
        }

def process_pdf(pdf_bytes):
    # Replace this with your custom PDF processing logic
    # Example: Save the PDF bytes to a file
    with open('/tmp/uploaded.pdf', 'wb') as file:
        file.write(pdf_bytes)
        print('File saved:', '/tmp/uploaded.pdf')
    # Example: Perform additional operations on the PDF

def delete_file(file_path):
    # Replace this with your custom file deletion logic
    # Example: Delete the file
    import os
    os.remove(file_path)
    print('File deleted:', file_path)

def sanitize_string(s):
    lines = s.split('\n')
    new_lines = []
    for line in lines:
        if len(line.split(' ')) <= 3:
            continue
        if line in new_lines:
            continue
        if line == '':
            continue
        if line.startswith('Title:'):
            continue
        new_lines.append(line)
    return '\n'.join(new_lines)
