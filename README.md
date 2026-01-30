# ticket-management

## Installation

Lien vers le frontend : https://github.com/gaetan-pardon/ticket-management-front  

Dans le dossier backend :  
```pip install uvicorn```  
```pip install fastapi```  

Dans le dossier frontend :  
```npm install```

## Lancement de l'API
  
```cd backend```  
```./launch.bat```

## Lancement du frontend
  
```cd frontend```  
```npm run dev```   

Frontend accessible depuis localhost:5173.

## Endpoints  

**Get Endpoints**  
http://localhost:8000/tickets  
http://localhost:8000/tickets/count-status
http://localhost:8000/tickets/priority/{priority}
http://localhost:8000/tickets/status/{status}

**POST Endpoints**  
http://localhost:8000/tickets/{id}

**DELETE Endpoints**  
http://localhost:8000/tickets/{id}

**PATCH Endpoints**  
http://localhost:8000/tickets/{id}
