# Standard library
import sys

# Colorama
from colorama import Fore, Style, Back

# Ngrok - Crea un tunel entre nuestro servidor local e internet.
from pyngrok import ngrok, conf


def init_ngrok(token: str) -> str:
    if not token:
        print(Fore.RED + "ERROR: " + "The API needs the NGROK token")
    else:
        # Toma el valor del puerto de los argumentos de la linea de comandos
        port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else 8000
        # Establece el path del fichero de configuración
        conf.get_default().config_path = "./config_ngrok.yml"
        # Establece la region del servidor
        conf.get_default().region = "sa"
        ngrok.set_auth_token(token)
        ngrok_tunel = ngrok.connect(port, bind_tls=True)
        ngrok_url = ngrok_tunel.public_url

        print(
            Fore.GREEN + "Server running on",
            Style.RESET_ALL + Back.WHITE + Fore.BLACK + ngrok_url + Style.RESET_ALL,
        )

        return ngrok_url
