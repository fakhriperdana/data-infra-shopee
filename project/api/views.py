import requests
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .tasks import send_to_rabbitmq

@csrf_exempt
def generate(request):
    if request.method == 'POST':
        csv_url = "https://sample-videos.com/csv/Sample-Spreadsheet-100-rows.csv"

        response = requests.get(csv_url)
        csv_content = response.content
        response = HttpResponse(csv_content, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Sample-Spreadsheet-100-rows.csv"'
        local_file_path = "/Users/fakhriperdana/personal/shopee-test/project/Sample-Spreadsheet-100-rows.csv"

        with open(local_file_path, 'wb') as local_file:
            local_file.write(csv_content)

        return response
    
def download(request):
    csv_url = "https://sample-videos.com/csv/Sample-Spreadsheet-100-rows.csv"
    
    response = HttpResponse(content_type='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename="Sample-Spreadsheet-100-rows.csv"'

    csv_response = requests.get(csv_url, stream=True)
    for chunk in csv_response.iter_content(chunk_size=4096):
        if chunk:
            response.write(chunk)

    return response

def send_mq(request):
    if request.method == 'GET':
        message = request.get('message')
        send_to_rabbitmq.apply_async(args=[message], countdown=2)
        return JsonResponse({'status': 'Message sent to RabbitMQ'})
    
    return JsonResponse({'error': 'Invalid request method'})