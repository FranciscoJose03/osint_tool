# Herramientas OSINT

Bienvenido a la aplicación de herramientas OSINT (Open Source Intelligence). Esta es una página web que te permite introducir una URL y obtener información a través de diversas herramientas de análisis.

## Características

La aplicación utiliza las siguientes herramientas para extraer información:

- **Nmap**: Escaneo de puertos y descubrimiento de hosts.
- **Ip_location**: Obtención de información geográfica sobre una dirección IP.
- **VirusTotal**: Análisis de URLs y archivos en busca de malware y amenazas.
- **Robots.txt**: Acceso y análisis del archivo robots.txt de un sitio web para entender las restricciones de acceso.
- **Wayback Machine**: Acceso a versiones archivadas de páginas web a lo largo del tiempo.
- **Nuclei**: Escaneo de vulnerabilidades utilizando plantillas personalizadas.

## Cómo usar la aplicación

1. Descarga el codigo y ejecutalo
2. Ve a la pagina web ofrecida
3. Introduce la URL que deseas analizar en el campo correspondiente.
4. Selecciona la informacion que deseas obtener.
5. Haz clic en el botón de análisis.
6. Revisa los resultados obtenidos de las diferentes herramientas.
**Opcional**
7. Si quieres guardar la información, puedes registrarte para poder ver la diferencia entre una busqueda de hace meses y la de hoy, para ver si hay nuevos cambios.

## Requisitos

- Navegador web moderno (Recomiendo FireFox)
- Conexión a Internet
- Además deberas intalar estos requisitos:
  ```bash
  pip install -r requirements.txt --break-system-packages
  ```
  ```bash
  apt install nmap
  ```

## Instalación

Si deseas ejecutar la aplicación localmente, sigue estos pasos:

1. Clona este repositorio:
   ```bash
   git clone https://github.com/FranciscoJose03/osint_tool.git
   ```
2. Entra a la carpeta:
   ```bash
   cd osint_tool
   ```
4. Ejecuta el programa:
   ```bash
   python3 app.py
   ```
5. Disfruta de las busquedas
