import pandas as pd
import csv
from django.http import HttpResponse
from .forms import UploadFileForm
from django.shortcuts import render

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            
            # Read the file using pandas
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            elif file.name.endswith('.xlsx'):
                df = pd.read_excel(file)
            
            # Generate the summary (count occurrences of DPD per Cust State and Cust Pin)
            summary = df.groupby(['Cust State', 'Cust Pin']).size().reset_index(name='DPD')

            # Create the HttpResponse object with CSV headers
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="summary.csv"'

            writer = csv.writer(response)
            # Write the headers
            writer.writerow(['Cust State', 'Cust Pin', 'DPD Count'])

            # Write the summary data to the CSV
            for index, row in summary.iterrows():
                writer.writerow([row['Cust State'], row['Cust Pin'], row['DPD']])

            return response
    else:
        form = UploadFileForm()
    
    return render(request, 'upload.html', {'form': form})
