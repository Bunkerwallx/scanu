import requests
import time
import subprocess
from colorama import Fore, Style

# API Key de URLScan.io
API_KEY = "88769b45-7a5b-4d55-8e53-221bf3de9725"

# URL de la API
URLSCAN_API = "https://urlscan.io/api/v1/scan/"
URLSCAN_RESULT = "https://urlscan.io/api/v1/result/"

def enviar_url(url):
    """
    Envía una URL para escanear con URLScan.io
    """
    headers = {
        "Content-Type": "application/json",
        "API-Key": API_KEY,
    }
    data = {
        "url": url,
        "visibility": "public",  # Cambia a "private" si deseas ocultar el escaneo
    }
    try:
        response = requests.post(URLSCAN_API, json=data, headers=headers)
        response.raise_for_status()  # Lanza excepción si la respuesta tiene un código de error
        return response.json().get("uuid")
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Error enviando URL: {e}{Style.RESET_ALL}")
        return None

def obtener_resultados(uuid):
    """
    Obtiene los resultados del escaneo usando el UUID
    """
    result_url = f"{URLSCAN_RESULT}{uuid}/"
    try:
        response = requests.get(result_url)
        response.raise_for_status()  # Lanza excepción si la respuesta tiene un código de error
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Error obteniendo resultados: {e}{Style.RESET_ALL}")
        return None

def analizar_con_xsstrike(url):
    """
    Realiza un análisis de XSS con XSStrike.
    """
    print(f"{Fore.YELLOW}Iniciando análisis de XSS con XSStrike para: {url}{Style.RESET_ALL}")
    try:
        result = subprocess.run(
            ["/usr/bin/xsstrike","-l 20", "-u", url, "--crawl", "--fuzzer"],
            text=True,
            capture_output=True
        )
        print(f"{Fore.GREEN}Análisis de XSStrike completo:{Style.RESET_ALL}\n")
        print(result.stdout)
    except Exception as e:
        print(f"{Fore.RED}Error ejecutando XSStrike: {e}{Style.RESET_ALL}")

def main():
    url = input(f"{Fore.CYAN}Ingresa la URL a escanear: {Style.RESET_ALL}").strip()
    uuid = enviar_url(url)
    if uuid:
        print(f"{Fore.GREEN}URL enviada correctamente. UUID: {uuid}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Esperando resultados...{Style.RESET_ALL}")
        time.sleep(15)  # Espera 10 segundos antes de intentar obtener los resultados del escaneo
        resultados = obtener_resultados(uuid)
        if resultados:
            print(f"{Fore.BLUE}Resultados obtenidos:{Style.RESET_ALL}")
            print(f"1. {Fore.MAGENTA}Page URL:{Style.RESET_ALL} {resultados['page']['url']}")
            print(f"2. {Fore.MAGENTA}Task ID:{Style.RESET_ALL} {resultados['task']['uuid']}")
            print(f"3. {Fore.MAGENTA}Stats:{Style.RESET_ALL}")
            for key, value in resultados['stats'].items():
                print(f"   - {Fore.YELLOW}{key}:{Style.RESET_ALL} {value}")
            
            # Llamar a XSStrike para un análisis adicional
            analizar_con_xsstrike(resultados['page']['url'])
        else:
            print(f"{Fore.RED}No se pudieron obtener los resultados.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Error al procesar la URL.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
