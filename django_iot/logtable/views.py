from django.shortcuts import render

# Create your views here.
def log_list(request):
    return render(request, 'logtable/log_list.html', {})