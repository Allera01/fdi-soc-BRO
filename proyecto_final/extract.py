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
        # Extraemos el autor
        author_tag = body_div.find('a', {'id': 'author-text'})
        author_name = author_tag.get_text(strip=True) if author_tag else "Desconocido"
        
        # Extraemos la fecha del comentario
        date_tag = body_div.find('span', {'id': 'published-time-text'})
        comment_date = date_tag.get_text(strip=True) if date_tag else "Fecha desconocida"

        # Extraemos el texto del comentario
        comment_text_tag = body_div.find('yt-attributed-string')
        comment_text = comment_text_tag.get_text(strip=True) if comment_text_tag else "Comentario vacío"
        
        # Extraemos si el comentario es pagado y cuánto
        paid_amount = None
        paid_tag = body_div.find('yt-pdg-comment-chip-renderer')
        if paid_tag:
            paid_amount_tag = paid_tag.find('span', {'id': 'comment-chip-price'})
            paid_amount = paid_amount_tag.get_text(strip=True) if paid_amount_tag else None
        
        # Almacenamos la información extraída
        comment_data = {
            'author_name': author_name,
            'comment_date': comment_date,
            'comment_text': comment_text,
            'paid_amount': paid_amount
        }
        comments.append(comment_data)

    # Limitamos la cantidad de comentarios si es necesario
    return comments[:num_comments]

def print_comments(comments):
    """
    Imprime los comentarios de forma ordenada y legible.
    """
    for idx, comment in enumerate(comments, 1):
        print(f"Comentario {idx}:")
        print(f"  Autor: {comment['author_name']}")
        print(f"  Fecha: {comment['comment_date']}")
        print(f"  Comentario: {comment['comment_text']}")
        print(f"  Pagado: {'Sí' if comment['paid_amount'] else 'No'}")
        if comment['paid_amount']:
            print(f"  Monto: {comment['paid_amount']}")
        print("-" * 40)

def extract_comments(html_file, num_comments):
    """
    Función principal que invoca extract.py con la ruta del HTML y el número de comentarios.
    """
    # Llamamos directamente a la función para extraer los comentarios
    comments = extract_comments_from_html(html_file, num_comments)
    
    # Imprimimos los comentarios de forma ordenada
    print_comments(comments)
    
    # Retornamos los comentarios extraídos
    return comments


