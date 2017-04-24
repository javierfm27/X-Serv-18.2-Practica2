from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseNotFound, HttpResponsePermanentRedirect
from django.views.decorators.csrf import csrf_exempt
from acorta.models import URLS
from django.core.exceptions import ObjectDoesNotExist
import socket

# Create your views here.
@csrf_exempt
def main(request):
    response = HttpResponse()
    if request.method == "GET":
        response.write("<form method='post' width='300'>\n" \
                + "\t<label>Introduce la URL que desea acortar</br></label>\n" \
                + "\t\t<input name='url' type='text' size='100'>\n" \
                + "\t\t<input type='submit' value='Enviar'>\n" \
                + "</form>\n" \
                + "<ul>\n")
        host = request.META['HTTP_HOST']
        for url in URLS.objects.all():
            response.write("<li> " + url.longURL + " - "  \
                + host + "/" + str(url.id) + "</li>\n")
    elif request.method == "POST":
        url = request.POST.get('url')
        if (not url.startswith("http://") or not url.startswith("https://")):
            url = 'http://www.' + url
        try:
            savedUrl = URLS.objects.get(longURL=url)
            host = request.META['HTTP_HOST']
            htmlAnswer = host + "/" + str(savedUrl.id)
            response.write(htmlAnswer)
        except ObjectDoesNotExist:
            newUrl = URLS(longURL=url)
            newUrl.save()
            host = request.META['HTTP_HOST']
            urlAnswer = host + "/" + str(newUrl.id)
            htmlAnswer ="<p> Esta es su nueva URL acortada " + urlAnswer
            response.write(htmlAnswer)
    else:
        response = HttpResponseNotFound()
        response.write("Este recurso no soporta esta operacion")
    return (response)

def acortada(request, identificador):
    try:
        objectUrl = URLS.objects.get(id=identificador)
        return HttpResponsePermanentRedirect(objectUrl.longURL)
    except ObjectDoesNotExist:
        return HttpResponseNotFound("No existe URL asociada al id: " + identificador)
