import json


def extract_comments_from_json(json_string):
    """
    Extrae los comentarios que tienen al menos una respuesta del objeto JSON de YouTube.
    """
    # Convertimos el JSON string en un diccionario de Python
    if isinstance(json_string, str):
        json_string = json.loads(json_string)

    comments = []

    # Verificamos si el JSON es una lista y tiene al menos un objeto
    if isinstance(json_string, list):
        for json_obj in json_string:
            if "items" in json_obj:
                for item in json_obj["items"]:
                    if "snippet" in item and "topLevelComment" in item["snippet"]:
                        top_comment = item["snippet"]["topLevelComment"]["snippet"]
                        comment_info = {
                            "author": top_comment["authorDisplayName"],
                            "text": top_comment["textDisplay"],
                            "published_at": top_comment["publishedAt"],
                            "like_count": top_comment["likeCount"],
                            "replies": [],  # Lista para las respuestas
                        }

                        if "replies" in item:
                            replies = item["replies"]["comments"]
                            if replies:
                                for reply in replies:
                                    reply_snippet = reply["snippet"]
                                    reply_info = {
                                        "author": reply_snippet["authorDisplayName"],
                                        "text": reply_snippet["textDisplay"],
                                        "published_at": reply_snippet["publishedAt"],
                                        "like_count": reply_snippet["likeCount"],
                                    }
                                    comment_info["replies"].append(reply_info)

                                comments.append(comment_info)

            else:
                print(
                    "Advertencia: 'items' no está presente en uno de los objetos de la lista."
                )
    else:
        print("Advertencia: El JSON no es una lista como se esperaba.")

    return comments
