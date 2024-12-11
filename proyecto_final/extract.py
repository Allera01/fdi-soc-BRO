from bs4 import BeautifulSoup

def extract_comments_from_html(html_file, num_comments):
    """
    Extrae los comentarios del archivo HTML de YouTube que contienen la estructura mencionada.
    """
    # Usamos BeautifulSoup para analizar el HTML
    soup = BeautifulSoup(html_file, 'html.parser')
    
    # Lista para almacenar los comentarios extraídos
    comments = []

    # Buscamos todos los divs con id="body" y class="style-scope ytd-comment-view-model"
    body_divs = soup.find_all('div', {'id': 'body', 'class': 'style-scope ytd-comment-view-model'})

    # Ahora buscamos los comentarios dentro de esos divs
    for body_div in body_divs:
        # Buscamos los comentarios dentro de 'yt-attributed-string' con role="text" dentro de cada div de cuerpo
        for comment in body_div.find_all('yt-attributed-string'):
            # Extraemos el texto del comentario
            comment_text = comment.get_text(strip=True)
            if comment_text:
                comments.append(comment_text)

    # Limitamos la cantidad de comentarios si es necesario
    return comments[:num_comments]

def extract_comments(html_file, num_comments):
    """
    Función principal que invoca extract.py con la ruta del HTML y el número de comentarios.
    """
    # Llamamos directamente a la función de extract.py para extraer los comentarios
    comments = extract_comments_from_html(html_file, num_comments)
    
    # Mostramos los comentarios extraídos
    return comments

