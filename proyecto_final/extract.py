import sys
from bs4 import BeautifulSoup

def extract_comments_from_html(html_file, num_comments):
    """
    Extrae los comentarios del archivo HTML de YouTube.
    """
    # Abre y lee el archivo HTML
    with open(html_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
    
    # Aquí asumimos que los comentarios están dentro de un contenedor específico en el HTML
    comments = []
    
    # Buscamos los comentarios. Este es un ejemplo, puede variar dependiendo de cómo esté estructurado el HTML
    for comment in soup.find_all('ytd-comment-thread-renderer'):
        comment_text = comment.find('yt-formatted-string', {'id': 'content-text'})
        if comment_text:
            comments.append(comment_text.get_text())

    # Limitamos la cantidad de comentarios si es necesario
    return comments[:num_comments]

def main():
    if len(sys.argv) != 3:
        print("Uso: python extract.py <video-html> <num-comments>")
        sys.exit(1)
    
    html_file = sys.argv[1]
    num_comments = int(sys.argv[2])
    
    # Extraemos los comentarios
    comments = extract_comments_from_html(html_file, num_comments)
    
    # Mostramos los comentarios extraídos
    for idx, comment in enumerate(comments, start=1):
        print(f"Comentario {idx}: {comment}")

if __name__ == '__main__':
    main()
