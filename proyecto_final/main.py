import asyncio
import click
from cargar import cargar
from analisis import generar_graficos
from extract import extract_comments_from_json
import descarga
from pathlib import Path
from grafo import generar_grafo_desde_json

'''async def obtener_informacion_video(video_url):
    """Obtiene información general del video."""
    # Lanza el navegador
    browser = await launch(args=['--no-sandbox'])
    page = await browser.newPage()
    
    # Ve al video de YouTube
    await page.goto(video_url)
    
    # Espera a que se cargue el contenido principal del video
    await page.waitForSelector('h1.title.style-scope.ytd-video-primary-info-renderer', timeout=10000)

    # Simula interacción con la página
    await page.evaluate('window.scrollBy(0, 500)')
    await asyncio.sleep(2)  # Tiempo para cargar elementos dinámicos
    await page.evaluate('window.scrollBy(0, -500)')
    await asyncio.sleep(2)

    # Extraer información del video
    info_video = await page.evaluate(''#'() => {
        const titulo = document.querySelector('h1.title.style-scope.ytd-video-primary-info-renderer') 
                       ? document.querySelector('h1.title.style-scope.ytd-video-primary-info-renderer').innerText : '';
        const canal = document.querySelector('#text-container yt-formatted-string') 
                       ? document.querySelector('#text-container yt-formatted-string').innerText : '';
        const visitas = document.querySelector('.view-count.style-scope.ytd-video-view-count-renderer') 
                        ? document.querySelector('.view-count.style-scope.ytd-video-view-count-renderer').innerText : '';
        const likes = document.querySelector('ytd-toggle-button-renderer:nth-child(1) yt-formatted-string#text') 
                      ? document.querySelector('ytd-toggle-button-renderer:nth-child(1) yt-formatted-string#text').getAttribute('aria-label') 
                      || document.querySelector('ytd-toggle-button-renderer:nth-child(1) yt-formatted-string#text').innerText : 'No disponible';

        return {
            titulo: titulo.trim(),
            canal: canal.trim(),
            visitas: visitas.trim(),
            likes: likes.trim()
        };
    }''#')
    
    print("Información general del video:")
    print(f"Título: {info_video['titulo']}")
    print(f"Canal: {info_video['canal']}")
    print(f"Visitas: {info_video['visitas']}")
    print(f"Likes: {info_video['likes']}")
    print('-' * 40)
    
    # Devuelve el navegador y la página para seguir reutilizándolos
    return browser, page

async def obtener_comentarios(page):
    """Obtiene los comentarios de un video abierto en la pestaña dada."""
    # Espera a que los comentarios se carguen
    await page.waitForSelector('ytd-comments')

    # Desplazarse hacia abajo para cargar más comentarios (opcional)
    for _ in range(10):  # Se desplaza hacia abajo
        await page.evaluate('window.scrollBy(0, 1000)')
        await asyncio.sleep(2)

    # Extrae los comentarios
    comentarios = await page.evaluate(''#'() => {
        let comentarios_data = [];
        let commentElements = document.querySelectorAll('ytd-comment-thread-renderer');

        commentElements.forEach(commentElement => {
            const comentario = commentElement.querySelector('#content-text') ? commentElement.querySelector('#content-text').innerText : '';
            const usuario = commentElement.querySelector('#author-text') ? commentElement.querySelector('#author-text').innerText : '';
            const likes = commentElement.querySelector('#vote-count-middle') ? commentElement.querySelector('#vote-count-middle').innerText : '0';

            comentarios_data.push({
                comentario: comentario.trim(),
                usuario: usuario.trim(),
                likes: likes.trim(),
            });
        });

        return comentarios_data;
    }''#')

    print("Comentarios del video:")
    for i, data in enumerate(comentarios[:10]):
        print(f"{i+1}:")
        print(f"Usuario: {data['usuario']}")
        print(f"Comentario: {data['comentario']}")
        print(f"Likes: {data['likes']}")
        print('-' * 40)'''
        
@click.command()
@click.option(
    "-d", "--descargar", is_flag=True, help= "Permite descargar el HTML de un video de YouTube a traves de su URL.\n"
)
@click.option(
    "-a", "--all", is_flag=True, help= "Se ejecutan todas las funciones opcionales.\n"
)
@click.option(
    "-g", "--graficos", is_flag=True, help= "Genera graficos de un JSON en concreto.\n"
)
@click.option(
    "-gs", "--grafosent", is_flag=True, help= "Genera un grafo que relaciona los sentimientos del autor\n"
)
@click.option(
    "-ga", "--grafoact", is_flag=True, help= "Genera un grafo que relaciona la actividad de los autores\n"
)

def my_main(graficos, grafosent, grafoact, descargar, all):
    '''if (descargar):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(descarga.descargar_html_video())'''
    if graficos:
        nombre_yt = input("Introduce el nombre del youtuber del que quieras saber: ").strip()

        nombre_json = input("Introduce el nombre del archivo JSON (sin .json): ").strip()

        archivo_json = Path(f"cache/{nombre_yt}/{nombre_json}.json")
        
        if archivo_json.exists():
            generar_graficos(archivo_json)
        else:
            print(f"El archivo {archivo_json} no existe. Por favor verifica el nombre.")

    if(grafosent):

        #nombre_yt = input("Introduce el nombre del youtuber del que quieras saber: ").strip()

        #nombre_json = input("Introduce el nombre del archivo JSON (sin .json): ").strip()

        archivo_json = Path(f"cache/baitybait/el_odio_en_internet.json")
        
        generar_grafo_desde_json(archivo_json, 'sentimiento_autor')

    if(grafoact):
        #nombre_yt = input("Introduce el nombre del youtuber del que quieras saber: ").strip()

        #nombre_json = input("Introduce el nombre del archivo JSON (sin .json): ").strip()

        archivo_json = Path(f"cache/baitybait/el_odio_en_internet.json")
        
        generar_grafo_desde_json(archivo_json, 'actividad_autor')

    else:
        # Flujo normal del programa
        html = cargar()
        comentarios = extract_comments_from_json(html)
        print(comentarios)
    #hay que pasar estos comentarios a un analisis.py que lo analiza, es posible que haya que aumentar el extract.py para sacar más datos que analizar

# Ejecución del programa
if __name__ == "__main__":
    my_main()
