from django.urls import path
from django.urls import reverse_lazy
from django.utils.html import format_html
from django.contrib import admin
from main.models import UploadedFile
import pandas as pd
from django.http import HttpResponse

@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ['id', 'file', 'uploaded_at', 'download_link', 'open_link']
    
    def download_link(self, obj):
        return format_html('<a href="{}" download>Download</a>', obj.file.url)
    
    download_link.allow_tags = True
    download_link.short_description = 'Download'
    
    def open_link(self, obj):
        return format_html('<a href="{}" target="_blank">Open</a>', reverse_lazy    ('admin:view_uploadedfile', args=[obj.pk]))
        #return format_html('<a href="/admin/main/uploadedfile/%s/view/" target="_blank">Open</a>' % (obj.pk,))
    open_link.allow_tags = True
    open_link.short_description = 'Open'

    def view(self, request, object_id):
        # Get the UploadedFile object for the given ID
        uploaded_file = self.model.objects.get(pk=object_id)

        # Check if the uploaded file is a CSV or Excel file
        if uploaded_file.file.name.endswith('.csv'):
            # Read the CSV file using pandas
            data = pd.read_csv(uploaded_file.file.path)
        elif uploaded_file.file.name.endswith('.xlsx'):
            # Read the Excel file using pandas
            data = pd.read_excel(uploaded_file.file.path)
        else:
            # If the file format is not supported, return an error message
            return HttpResponse('File format not supported.')

        # Render the data as an HTML table
        table = '<table>'
        table += '<tr><th>' + '</th><th>'.join(data.columns) + '</th></tr>'
        for _, row in data.iterrows():
            table += '<tr><td>' + '</td><td>'.join(str(x) for x in row.values) + '</td></tr>'
        table += '</table>'
        return HttpResponse(table)
    view.short_description = 'View'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('<int:object_id>/view/', self.admin_site.admin_view(self.view), name='view_uploadedfile'),
        ]
        return my_urls + urls


