import asyncio
from pyppeteer import launch

async def obtener_comentarios(video_url):
    # Lanza el navegador
    browser = await launch(args=['--no-sandbox'])  # headless=True para no abrir la ventana del navegador
    page = await browser.newPage()
    
    # Ve al video de YouTube
    await page.goto(video_url)
    
    # Espera a que los comentarios se carguen (puede que tengas que ajustar el selector)
    await page.waitForSelector('ytd-comments')

    # Desplazarse hacia abajo para cargar más comentarios (opcional)
    for _ in range(10):  # Se desplaza 3 veces hacia abajo
        await page.evaluate('window.scrollBy(0, 1000)')
        await asyncio.sleep(2)

    # Extrae los comentarios
    comentarios = await page.evaluate('''() => {
        let comentarios = [];
        let commentElements = document.querySelectorAll('ytd-comment-thread-renderer #content-text');
        commentElements.forEach(comment => {
            comentarios.push(comment.innerText);
        });
        return comentarios;
    }''')

    # Cierra el navegador
    await browser.close()

    for i, comentario in enumerate(comentarios[:50]):
        print(f"{i+1}: {comentario}")

# Ejecuta la función
video_url = 'https://www.youtube.com/watch?v=QqLGF_ghc8A'
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
comentarios = loop.run_until_complete(obtener_comentarios(video_url))

