import json

from response import Response

filepath = 'tickets.json'


def read_json_file():
    """
    Reads a JSON file and returns its content as a dictionary.
    Returns:
        response (Response): An object containing status, message, and data if successful.
        data (dict): The content of the JSON file as a dictionary.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return Response(200, "Success", data)
    
    except FileNotFoundError:
        return Response(404, f"Fichier {filepath} introuvable.", None)
    
    except json.JSONDecodeError:
        return Response(400, "Format invalide.", None)
    
    except Exception as e:
        return Response(500, f"Erreur lors de la lecture du fichier: {str(e)}", None)


# TODO: Auto-incrémenter l'ID lors de l'ajout d'un nouveau ticket
# TODO: Vérifier que le ticket n'existe pas déjà avant de l'ajouter
# TODO: Valider le format du ticket avant de l'ajouter
def write_json_file(json_object):
    """
    Writes a dictionary to a JSON file.
    Args:
        json_object (dict): The dictionary to write to the JSON file.
    Returns:
        response (Response): An object containing status, message, and data if successful.
        data (dict): The added object.
    """
    read_response = read_json_file()
    if read_response.status != 200:
        return read_response
    
    try:
        data = read_response.data
        data.append(json_object)
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        return Response(201, "Objet ajouté avec succès.", json_object)
    
    except FileNotFoundError:
        return Response(404, f"Fichier {filepath} introuvable.", None)
    
    except json.JSONDecodeError:
        return Response(400, "Format invalide.", None)
    
    except Exception as e:
        return Response(500, f"Erreur lors de l'écriture du fichier: {str(e)}", None)


def count_status():
    """
    Counts the occurrences of each status in the JSON file.
    Returns:
        response (Response): An object containing status, message, and data if successful.
        data (dict): A dictionary with statuses as keys and their counts as values.
    """
    read_response = read_json_file()
    if read_response.status != 200:
        return read_response
    
    if len(read_response.data) == 0:
        return Response(404, "Aucun ticket à analyser.", None)
    
    status_count = {}
    data = read_response.data
    if data:
        for item in data:
            status = item.get("status")
            if status:
                if status in status_count:
                    status_count[status] += 1
                else:
                    status_count[status] = 1
    return Response(200, "Statut compté avec succès.", status_count)


def delete_ticket_by_id(ticket_id):
    """
    Deletes a ticket from the JSON file by its ID.
    Args:
        ticket_id (int): The ID of the ticket to delete.
    Returns:
        response (Response): An object containing status and message.
    """
    read_response = read_json_file()
    if read_response.status != 200:
        return read_response
    
    if len(read_response.data) == 0:
        return Response(404, "Aucun ticket à supprimer.", None)
    
    data = read_response.data
    new_data = [item for item in data if item.get("id") != ticket_id]

    if len(new_data) == len(data):
        return Response(404, f"Ticket d'id : {ticket_id} introuvable.", None)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(new_data, file, indent=4, ensure_ascii=False)
        return Response(200, f"Le ticket d'id : {ticket_id} a été supprimé.", None)
    
    except FileNotFoundError:
        return Response(404, f"Fichier {filepath} introuvable.", None)
    
    except json.JSONDecodeError:
        return Response(400, "Format invalide.", None)
    
    except Exception as e:
        return Response(500, f"Erreur lors de l'écriture du fichier: {str(e)}", None)


def update_json_ticket_status(ticket_id, new_status):
    """
    Updates the status of a ticket in the JSON file by its ID.
    Args:
        ticket_id (int): The ID of the ticket to update.
        new_status (str): The new status to set.
    Returns:
        response (Response): An object containing status, message, and data if successful.
        data (dict): The modified object.
    """
    read_response = read_json_file()
    if read_response.status != 200:
        return read_response
    
    if len(read_response.data) == 0:
        return Response(404, "Aucun ticket à modifier.", None)
    
    data = read_response.data
    ticket_found = False
    updated_item = None
    for item in data:
        if item.get("id") == ticket_id:
            item["status"] = new_status
            ticket_found = True
            updated_item = item
            break

    if not ticket_found:
        return Response(404, f"Ticket d'id : {ticket_id} introuvable.", None)

    try:
        #utf-8 et ensure_ascii=False nécessaires pour supporter les accents
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        return Response(200, f"Le statut du ticket d'id : {ticket_id} a été mis à jour.", updated_item)
   
    except FileNotFoundError:
        return Response(404, f"Fichier {filepath} introuvable.", None)
    
    except json.JSONDecodeError:
        return Response(400, "Format invalide.", None)
    
    except Exception as e:
        return Response(500, f"Erreur lors de l'écriture du fichier: {str(e)}", None)
    