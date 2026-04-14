from django.shortcuts import render
from .models import Alumnos #Accedemos al modelo Alumnos que contiene la estructura de la tabla.
from .forms import ComentarioContactoForm
from .models import ComentarioContacto
from django.shortcuts import get_object_or_404
import datetime


def registros(request):
    alumnos=Alumnos.objects.all()
#all recupera todos los objetos del modelo (registros de la tabla alumnos)
    return render(request,"registros/principal.html",{'alumnos':alumnos})
#Indicamos el lugar donde se renderizará el resultado de esta vista
# y enviamos la lista de alumnos recuparados

def registrar(request):
    if request.method == 'POST':
        form = ComentarioContactoForm(request.POST)
        if form.is_valid():#Si los datos recibidos son correctos
            form.save()#Inserta
            comentarios=ComentarioContacto.objects.all()
            return render(request,"registros/consultarContacto.html", {'comentarios':comentarios})
    form = ComentarioContactoForm()
    #si algo sale mal se reenvian al formulario los datos ingresados
    return render(request,'inicio/contacto.html',{'form': form})

def consultarComentarioContacto(request):
    comentarios=ComentarioContacto.objects.all()
    #All recupera todos los objetos del modelo (registros de la tabla comentariosContacto)
    return render(request,"registros/consultarContacto.html",{'comentarios':comentarios})
#indicamos el lugar donde se renderizara el resultado de esta vista y enviamos la lista de comentarios recuperados

def eliminarComentarioContacto(request, id,
        confirmacion ='registros/confirmarEliminacion.html'):
        comentario = get_object_or_404(ComentarioContacto, id=id)
        if request.method=='POST':
            comentario.delete()
            comentarios=ComentarioContacto.objects.all()
            return render(request,"registros/consultarContacto.html",{'comentarios':comentarios})
        return render(request, confirmacion, {'object':comentario}) 

def consultarComentarioIndividual(request, id):
    comentario=ComentarioContacto.objects.get(id=id)    
    return render(request,"registros/formEditarComentario.html",{'comentario':comentario})

def editarComentarioContacto(request, id):
     comentario=get_object_or_404(ComentarioContacto, id=id)
     form=ComentarioContactoForm(request.POST, instance=comentario)
     if form.is_valid():
        form.save()
        comentarios=ComentarioContacto.objects.all()
        return render(request, "registros/consultarContacto.html", {'comentarios':comentarios})
     return render(request, "registros/formEditarComentario.html", {'comentario':comentario})

def consultar1(request):
#con una sola condición
    alumnos=Alumnos.objects.filter(carrera="TI")
    return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultar2(request):
#multiples condiciones adicionando .filter() se analiza #como AND
    alumnos=Alumnos.objects.filter(carrera="TI").filter(turno="Matutino")
    return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultar3(request):
#Si solo deseamos recuperar ciertos datos agregamos la #función only,
#listando los campos que queremos obtener de #la consulta emplear filter() o #en el ejemplo all()
    alumnos=Alumnos.objects.all().only("matricula", "nombre", "carrera",
    "turno", "imagen")
    return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultar4(request):
    alumnos=Alumnos.objects.filter(turno__contains="Vesp")
    return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultar5(request):
    alumnos=Alumnos.objects.filter(nombre__in=["Juan", "Ana"])
    return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultar6(request):
    fechaInicio = datetime.date(2026, 2, 10)
    fechaFin = datetime.date(2026, 2, 26)
    alumnos=Alumnos.objects.filter(created__range=(fechaInicio,fechaFin))
    return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultar7(request):
#Consultando entre modelos
    alumnos=Alumnos.objects.filter(comentario__coment__contains='No inscrito')
    return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultasSQL(request):
    alumnos = Alumnos.objects.raw('''
        SELECT id, matricula, nombre, carrera, turno, imagen 
        FROM registros_alumnos 
        WHERE carrera = 'TI' 
        ORDER BY turno DESC
    ''')
    
    return render(request, "registros/consultas.html", {'alumnos': alumnos})

def seguridad(request, nombre=None):
    nombre = request.GET.get('nombre')
    return render(request,"registros/seguridad.html",{'nombre':nombre})