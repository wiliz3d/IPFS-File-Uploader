from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
import ipfshttpclient
import os

def upload_file(request):
    file_hash = None
    status_message = None
    error_message = None

    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']

        # File validation: size limit (e.g., 10MB)
        if file.size > 10 * 1024 * 1024:
            error_message = "File size exceeds the 10MB limit."
        else:
            try:
                file_hash = handle_uploaded_file(file)
                status_message = "File uploaded successfully!"
            except Exception as e:
                error_message = f"An error occurred: {str(e)}"
    else:
        if request.method == 'POST':
            error_message = "No file uploaded."

    return render(request, 'app.html', {
        'file_hash': file_hash,
        'status_message': status_message,
        'error_message': error_message
    })

def handle_uploaded_file(file):
    client = ipfshttpclient.connect()
    res = client.add(file)
    return res['Hash']
