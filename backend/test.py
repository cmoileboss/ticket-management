from script import read_json_file
from script import write_json_file
from script import count_status


print(read_json_file())
print(count_status())

newObject = {
    "id": 3,
    "title": "Ajouter un filtre par priorité",
    "description": "Permettre de filtrer les tickets par priorité (Low, Medium, High) sur la page liste.",
    "priority": "Medium",
    "status": "In progress",
    "tags": ["feature", "ux"],
    "createdAt": "2026-01-15"
  }

write_json_file(newObject)