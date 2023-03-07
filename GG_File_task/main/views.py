from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse


import pandas as pd
from django.shortcuts import render, get_object_or_404

from .models import UploadedFile

import os


import mimetypes

def index(request):
    return render(request, 'index.html')



def view_uploadedfile(request, file_id):
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)
    file_path = uploaded_file.file.path
    # read the contents of the file using Pandas
    df = pd.read_excel(file_path)
    # render the contents of the file as a table
    return render(request, 'uploadedfile_table.html', {'df': df})
