# PRA2_visualizacion
    Autor: **Rubén Moya Vázquez**(*rmoyav@uoc.edu*)
    Asignatura: **Visualización de datos**
    Institución: **Universitat Oberta de Catalunya**
    Fecha: **13/06/2022**
## A9: Creación de la visualización y entrega del proyecto (Práctica II)
Este repositorio contiene el código de un dashboard de visualización creado a partir del framerwor [Dash](https://dash.plotly.com/)
de **Plotly** y los datos obtenidos de [Eurostat](https://link-url-here.org).

### Estructura del repositorio.
El repositorio contiene la siguiente arborescencia:

1. **assets**. Carpeta que contiene el css de estilos para nuestro dashboard.
2. **venv**. Entorno virtual de python, utilizado para el despliegue en ``Heroku``.
3. **app.py**. El código python que conforma nuestro dashboard.
4. **europe.geo.json**. Archivo geojson utilizado para generar los poligonos de los paises en el mapa. Fuente: [Geojson Maps](https://geojson-maps.ash.ms/)
5. **hlth_ehis_bm1e_linear.csv**. Origen de datos para nuestro dashboard. Fuente: [Body mass index (BMI) by sex, age and educational attainment level](https://ec.europa.eu/eurostat/databrowser/view/HLTH_EHIS_BM1E/default/table?lang=en)
6. **Procfile**. Archivo de configuración del deploy en ``Heroku``.
7. **README.md**. Este archivo :)
8. **requirements.txt**. Archivo de requisitos de python para la generación del entorno virtual.

Además de los archivos mencionados contamos con la hoja de estilos ``style.css`` obtenida de las plantillas de Dash. Se ha retocado levemente para ajustarse a nuestro dashboard.

### Dashboard
El dashboard está accesible en la plataforma ``Heroku`` a través del siguiente link: [Fit or Fat (Europe's Edition)](https://google.es)

### Disclaimer
This repository has been made just for educational purpouses. Any use outside of the mentioned is not recommended by the author.