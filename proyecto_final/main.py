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
    for _ in range(10):  # Se desplaza hacia abajo
        await page.evaluate('window.scrollBy(0, 1000)')
        await asyncio.sleep(2)

    # Extrae los comentarios
    comentarios = await page.evaluate('''() => {
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
    }''')

    # Cierra el navegador
    await browser.close()

    for i, data in enumerate(comentarios[:10]):
        print(f"{i+1}:")
        print(f"Usuario: {data['usuario']}")
        print(f"Comentario: {data['comentario']}")
        print(f"Likes: {data['likes']}")
        print('-' * 40)

# Ejecuta la función
video_url = 'https://www.youtube.com/watch?v=QqLGF_ghc8A'
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
comentarios = loop.run_until_complete(obtener_comentarios(video_url))

