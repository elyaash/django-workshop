from django.shortcuts import render


# custom 404 view
def custom_404(request, exception):
    raise Exception("Sorry, no numbers below zero")
    return render(request, 'core/404.html', status=404)

def handler404(request, *args, **argv):
    return render(request,"core/404.html",status=404)

def handler500(request, *args, **argv):
    return render(request,"core/500.html",status=500)