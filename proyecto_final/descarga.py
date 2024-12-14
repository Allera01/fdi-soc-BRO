import asyncio
from pathlib import Path
from pyppeteer import launch

dir_cache = Path("cache")

async def descargar_html_video():
    dir_cache.mkdir(parents=True, exist_ok=True)
    video_url = input("Introduce la URL del video de YouTube: ")
    
    full_info = ""
    # Lanza el navegador
    browser = await launch(args=['--no-sandbox'])
    page = await browser.newPage()
    
    # Ve al video de YouTube
    await page.goto(video_url)
    
    # Espera a que se cargue el contenido principal del video
    await page.waitForSelector('h1.title.style-scope.ytd-video-primary-info-renderer', timeout=10000)

    for _ in range(10):  # Desplázate varias veces para asegurar la carga de comentarios
        await page.evaluate('window.scrollBy(0, 1000)')
        await asyncio.sleep(2)
    # Extraer información del video
    
    '''
    #https://youtu.be/ZtqbjdZ6iok
    
    print("Pulsando botones de 'más respuestas' visibles...")

    while True:
        botones_respuestas = await page.evaluate(''() => {
            // Seleccionar botones dentro de <ytd-button-renderer> con id="more-replies" y que no tengan el atributo `hidden`
            const botones = Array.from(
                document.querySelectorAll('ytd-button-renderer#more-replies:not([hidden]) button.yt-spec-button-shape-next')
            );
            
            // Simular clic en cada botón encontrado
            botones.forEach(btn => btn.click());
            
            // Devolver la cantidad de botones pulsados
            return botones.length;
        }'')
        
        if botones_respuestas == 0:
            break  # Salimos del bucle si no hay más botones visibles
        
        
        print(f"Se han pulsado {botones_respuestas} botones para cargar respuestas.")
        await asyncio.sleep(10)  # Pausa para permitir la carga del contenido
        
        full_info = await page.content()
    '''
    
    
    
        
    info_video = await page.evaluate('''() => {
        const titulo = document.querySelector('h1.title.style-scope.ytd-video-primary-info-renderer') 
                       ? document.querySelector('h1.title.style-scope.ytd-video-primary-info-renderer').innerText : '';
        const canal = document.querySelector('#text-container yt-formatted-string') 
                       ? document.querySelector('#text-container yt-formatted-string').innerText : '';

        return {
            titulo: titulo.trim(),
            canal: canal.trim(),
        };
    }''')
    
    # Crear la ruta donde guardar
    canal_ajustado = info_video['canal'].lower().replace(" ", "_").replace("/", "_")

    guardar = dir_cache / canal_ajustado
    guardar.mkdir(parents=True, exist_ok=True)  # Crear directorios del canal si no existen
    
    # Ruta del archivo HTML
    titulo_ajustado = info_video['titulo'].lower().replace(" ", "_").replace("/", "_")

    archivo_html = guardar / (titulo_ajustado + ".html")
    
    # Guardar el contenido de la página
    contenido = await page.content()
    archivo_html.write_text(contenido, encoding="utf-8", errors="ignore")        
        
    await browser.close()

# Ejecución del programa
if __name__ == "__main__":
    #dir_cache.mkdir(parents=True, exist_ok=True)
    #video_url = input("Introduce la URL del video de YouTube: ")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(descargar_html_video())