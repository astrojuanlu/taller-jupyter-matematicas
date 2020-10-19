import smtplib
from email.message import EmailMessage
import os

import pandas as pd

MESSAGE_TPL = """¡Hola {nombre_apellido}!

Está a punto de empezar el taller de Jupyter para Matemáticas.
Este es el servidor de Jupyter que podrás utilizar:

https://jupyterhub.aeropython.org/

Tu nombre de usuario es {email}, y tu contraseña es:

{password}

Este acceso estará habilitado cuando dé comienzo el taller,
¡ten paciencia!

Durante el taller, esperamos de todos los participantes que sean
respetuosos y considerados en sus interacciones, y que se
abstengan absolutamente de hacer comentarios derogatorios de cualquier tipo.
En concreto, el evento se rige por el código de conducta de Python Argentina:

https://ac.python.org.ar/#coc

Si por algún motivo hay problemas durante el transcurso del taller,
recuerda que puedes usar Binder para desplegar un servidor en la nube,
tal y como se explica en la web del taller:

https://astrojuanlu.github.io/taller-jupyter-matematicas/

Y por último, recuerda que el taller se desarrollará en la plataforma
Twitch.tv, y que necesitarás registrarte para poder comentar:

https://www.twitch.tv/astrojuanlu

¡Nos vemos pronto!

Juan Luis Cano
"""


def read_emails():
    df = pd.read_csv(os.environ["USER_DATA_PATH"])
    yield from df["Username"].dropna().unique().tolist()


def read_names():
    df = pd.read_csv(os.environ["USER_DATA_PATH"])
    yield from df["Nombre y apellidos"].dropna().unique().tolist()


def read_passwords():
    df = pd.read_csv(os.environ["PASSWORD_FILE_PATH"])
    yield from df["Password"].unique().tolist()


def send_message(server, sender: str, email: str, nombre_apellido: str, password: str):
    msg = EmailMessage()
    msg.set_content(
        MESSAGE_TPL.format(
            nombre_apellido=nombre_apellido, email=email, password=password,
        )
    )

    msg["Subject"] = "Taller de Jupyter para Matemática - Acceso"
    msg["From"] = sender
    msg["To"] = email

    server.send_message(msg)


def main():
    with smtplib.SMTP(os.environ["SMTP_HOST"], port=587) as server:
        server.starttls()
        server.login(os.environ["SMTP_USER"], os.environ["SMTP_PASSWORD"])
        for email, nombre_apellido, password in zip(
            read_emails(), read_names(), read_passwords()
        ):
            # print(username, password)
            send_message(
                server, os.environ["SMTP_USER"], email, nombre_apellido, password
            )


if __name__ == "__main__":
    main()
