import click
from cargar import cargar
import analisis
from extract import extract_comments_from_html
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
        

@click.option(
    "-a", "--all", is_flag=True, help="Se ejecutan todas las funciones opcionales.\n"
)
@click.option('--num-comments', default=50, type=int, help="Número de comentarios a extraer (por defecto 50).")
def extract_comments(video_html, num_comments):
    """
    Función principal que invoca extract.py con la ruta del HTML y el número de comentarios.
    """
    # Llamamos directamente a la función de extract.py para extraer los comentarios
    comments = extract_comments_from_html(video_html, num_comments)
    
    # Mostramos los comentarios extraídos
    for idx, comment in enumerate(comments, start=1):
        print(f"Comentario {idx}: {comment}")
def my_main():
    html = cargar()
    extract_comments()
    print(html)
    #el contenido de los comentarios se encuentra en la id paid-comment-chip 
    #lo podeis buscar en los datasets si se necesita otra forma de encontrarlo
    #si los sacais hacerlo utilizando Beautiful Soup y en el archivo analisis

# Ejecución del programa
if __name__ == "__main__":
    my_main()
