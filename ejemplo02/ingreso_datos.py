from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from genera_tablas import Club, Jugador
from configuracion import cadena_base_datos
import os

# generar el enlace al gestor de base de datos
engine = create_engine(cadena_base_datos)

Session = sessionmaker(bind=engine)
session = Session()

ruta_clubs = os.path.join("data", "datos_clubs.txt")
ruta_jugadores = os.path.join("data", "datos_jugadores.txt")

# Insertar Clubes
with open(ruta_clubs, "r", encoding="utf-8") as archivo_clubs:
    for linea in archivo_clubs:
        partes = linea.strip().split(";")
        if len(partes) == 3:
            nombre = partes[0].strip()
            deporte = partes[1].strip()
            fundacion = int(partes[2])
            club = Club(nombre=nombre, deporte=deporte, fundacion=fundacion)
            session.add(club)

# Guardar los clubes para poder usarlos luego
session.commit()

# Insertar Jugadores
with open(ruta_jugadores, "r", encoding="utf-8") as archivo_jugadores:
    for linea in archivo_jugadores:
        partes = linea.strip().split(";")
        if len(partes) == 4:
            nombre_club = partes[0].strip()
            posicion = partes[1].strip()
            dorsal = int(partes[2].strip())
            nombre_jugador = partes[3].strip()

            club = session.query(Club).filter_by(nombre=nombre_club).one()
            jugador = Jugador(nombre=nombre_jugador, dorsal=dorsal, posicion=posicion, club=club)
            session.add(jugador)

# Confirmar todos los cambios
session.commit()
print("Datos insertados correctamente.")