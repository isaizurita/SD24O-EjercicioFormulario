from fastapi import FastAPI, UploadFile, File, Form
from typing import Optional
from pydantic import BaseModel
import shutil
import os #Para acceder a la ruta de home
import uuid #Para generar nombres aleatorios tipo hash

# creación del servidor
app = FastAPI()

#definición de la base del usuario
class UsuarioBase(BaseModel):
    nombre:Optional[str]=None
    edad:int
    domicilio:str    
    
usuarios = [{
    "id": 0,
    "nombre": "Homero Simpson",
    "edad": 40,
    "domicilio": "Av. Simpre Viva"
}, {
    "id": 1,
    "nombre": "Marge Simpson",
    "edad": 38,
    "domicilio": "Av. Simpre Viva"
}, {
    "id": 2,
    "nombre": "Lisa Simpson",
    "edad": 8,
    "domicilio": "Av. Simpre Viva"
}, {
    "id": 3,
    "nombre": "Bart Simpson",
    "edad": 10,
    "domicilio": "Av. Simpre Viva"
}]

#Form(...) -> Operador Ellipsis
@app.post("/fotos")
async def guarda_foto(titulo:str=Form(None), descripcion:str=Form(...), foto:UploadFile=File(...)):
    print("Título: ", titulo)
    print("Descripción: ", descripcion)
    home_usuario = os.path.expanduser("~") #Para obetener la ruta del home del usuario
    nombre_archivo = uuid.uuid4() #Nuevo nombre en formato hexadecimal
    extension_foto = os.path.splitext(foto.filename)[1]
    ruta_imagen = f'{home_usuario}/fotosEjemplo/{nombre_archivo}{extension_foto}'
    print("Guardando foto en ", ruta_imagen);
    with open(ruta_imagen, "wb") as imagen:
        contenido = await foto.read()
        imagen.write(contenido)

    respuesta = {
        "Titulo":titulo,
        "Descripcion":descripcion,
        "Ruta": ruta_imagen
    }
    return respuesta


# decorator
@app.get("/")
def hola_mundo():
    print("invocando a ruta /")
    respuesta = {
        "mensaje": "hola mundo!"
    }

    return respuesta


@app.get("/usuarios/{id}")
def usuario_por_id(id: int):
    print("buscando usuario por id:", id)
    # simulamos consulta a la base:
    return usuarios[id]


@app.get("/usuarios/{id}/compras/{id_compra}")
def compras_usuario_por_id(id: int, id_compra: int):
    print("buscando compra con id:", id_compra, " del usuario con id:", id)
    # simulamos la consulta
    compra = {
        "id_compra": 787,
        "producto": "TV",
        "precio": 14000
    }

    return compra

@app.get("/usuarios")
def lista_usuarios(*,lote:int=10,pag:int,orden:Optional[str]=None): #parametros de consulta ?lote=10&pag=1
    print("lote:",lote, " pag:", pag, " orden:", orden)
    #simulamos la consulta
    return usuarios

@app.post("/usuarios")
def guardar_usuario(usuario:UsuarioBase, parametro1:str):
    print("usuario a guardar:", usuario, ", parametro1:", parametro1)
    #simulamos guardado en la base.
    
    usr_nuevo = {}
    usr_nuevo["id"] = len(usuarios)
    usr_nuevo["nombre"] = usuario.nombre
    usr_nuevo["edad"] = usuario.edad
    usr_nuevo["domicilio"] = usuario.domicilio

    usuarios.append(usuario)

    return usr_nuevo

@app.put("/usuario/{id}")
def actualizar_usuario(id:int, usuario:UsuarioBase):
    #simulamos consulta
    usr_act = usuarios[id]
    #simulamos la actualización
    usr_act["nombre"] = usuario.nombre
    usr_act["edad"] = usuario.edad
    usr_act["domicilio"] = usuario.domicilio    

    return usr_act
    
@app.delete("/usuario/{id}")
def borrar_usuario(id:int):
    #simulamos una consulta
    if id>=0 and id< len(usuarios):
        usuario = usuarios[id]
    else:
        usuario = None
    
    if usuario is not None:
        usuarios.remove(usuario)
    
    return {"status_borrado", "ok"}

@app.post("/registro")
async def registrar_usuario(nombre: str = Form(...), direccion: str = Form(...), fotografia: UploadFile = File(...), vip: bool = Form(False)
):
    print("Nombre:", nombre)
    print("Dirección:", direccion)
    print("VIP:", vip)
   
    home_usuario = os.path.expanduser("~")
    nombre_archivo = uuid.uuid4()
    extension_foto = os.path.splitext(fotografia.filename)[1]
    if vip == True:
        ruta_imagen = f'{home_usuario}/fotosUsuariosVIP/{nombre_archivo}{extension_foto}'
    else:
        ruta_imagen = f'{home_usuario}/fotosUsuarios/{nombre_archivo}{extension_foto}'

    print("Guardando fotografía en:", ruta_imagen)
    with open(ruta_imagen, "wb") as imagen:
        contenido = await fotografia.read()
        imagen.write(contenido)
    
    respuesta = {
        "Nombre": nombre,
        "Dirección": direccion,
        "VIP": vip,
        "Ruta": ruta_imagen
    }
    return respuesta
