from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseNotFound, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from acorta.models import URLS
from django.core.exceptions import ObjectDoesNotExist
import socket

# Create your views here.
#FALTTA LISTAS DE URLS AL HACER EL GET, Y TAMBIEN FALTA REVISAR EL ENUNCIADO
#PARA COMPROBAR QUR TODAS LAS FUNCIONALIDADES DE LA PRACTICA ESTEN CUBIERTAS
@csrf_exempt
def main(request):
    response = HttpResponse()
    if request.method == "GET":
        response.write("<form method='post' width='300'>\n" \
                + "\t<label>Introduce la URL que desea acortar</br></label>\n" \
                + "\t\t<input name='url' type='text' size='100'>\n" \
                + "\t\t<input type='submit' value='Enviar'>\n" \
                + "</form>\n" )
    elif request.method == "POST":
        url = request.POST.get('url')
        try:
            savedUrl = URLS.objects.get(longURL=url)
            host = request.META['HTTP_HOST']
            urlAnswer = host + "/" + str(savedUrl.id)
            htmlAnswer = "<a href='" + urlAnswer + "'>" + urlAnswer + "</a>"
            response.write(htmlAnswer)
        except ObjectDoesNotExist:
            newUrl = URLS(longURL=url)
            newUrl.save()
            host = request.META['HTTP_HOST']
            urlAnswer = host + "/" + str(newUrl.id)
            htmlAnswer ="<p> Esta es su nueva URL acortada "  \
            + "<a href='" + urlAnswer + "'>" + urlAnswer + "</a>"
            response.write(htmlAnswer)
    return (response)

def acortada(request, identificador):
    try:
        objectUrl = URLS.objects.get(id=identificador)
        return HttpResponseRedirect(objectUrl.longURL)
    except ObjectDoesNotExist:
        return HttpResponseNotFound("No existe URL asociada al id: " + identificador)
