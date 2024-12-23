# Análisis de Tuits

## Archivo Analizado

**Ruta del archivo**: cyberpunk.csv

## Procedimiento

1. Cargamos los datos desde el archivo CSV.
2. Filtramos los tuits con al menos 10 retweets para enfocarnos en los de mayor relevancia.
3. Seleccionamos una muestra representativa de hasta 1000 registros.
4. Procesamos el contenido textual eliminando puntuación, convirtiendo a minúsculas y eliminando stopwords.
5. Analizamos los términos más frecuentes para identificar patrones en el contenido.
6. Exploramos las relaciones clave mediante gráficos, como la longitud del texto y los retweets, tendencias temporales, palabras clave y la distribución de retweets.

## Términos Más Frecuentes

| Término | Frecuencia |
|---------|------------|
| rt | 988 |
| cyberpunk | 768 |
| cyberpunkcortes | 161 |
| 2077 | 160 |
| boys | 156 |
| amp | 87 |
| game | 78 |
| farevalee9s | 78 |
| genshinimpact | 78 |
| \textbackslash{}u539F\textbackslash{}u795E | 78 |

## Análisis Adicionales

### Relación entre longitud del texto y retweets

Este gráfico muestra cómo la longitud de un tuit afecta a su popularidad, medida en retweets.

![Relación entre longitud del texto y retweets](retweets_vs_length.png)

### Cantidad de tuits a lo largo del tiempo

Este gráfico refleja la distribución temporal de los tuits, destacando picos de actividad.

![Cantidad de tuits a lo largo del tiempo](tweets_over_time.png)

### Promedio de retweets según palabras clave

Aquí se comparan las palabras clave más relevantes según su influencia en los retweets.

![Promedio de retweets según palabras clave](keywords_vs_retweets.png)

### Distribución de retweets

Este gráfico ilustra cómo están distribuidos los retweets en el conjunto de datos.

![Distribución de retweets](retweet_distribution.png)

