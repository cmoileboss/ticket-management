## Les prompts

Explique-moi comment utiliser fastAPI et uvicorn pour faire une API Python. Quel est le rôle de ces frameworks ? 

Très bonne question, et très importante pour bien comprendre ton projet 👌 
Je vais t’expliquer pas à pas, sans code, et en séparant bien les rôles de FastAPI et Uvicorn. 

 

1. Qu’est-ce qu’une API, dans ton contexte ? 

Avant de parler des outils, il faut comprendre ce que tu construis. 

Ton API est un intermédiaire entre : 

ton frontend React 

tes données (le fichier JSON) 

👉 React ne sait pas lire directement un fichier JSON côté serveur. 
👉 Il envoie des requêtes HTTP (demande de données, création de ticket, etc.). 
👉 L’API reçoit ces requêtes, traite la logique, et renvoie des réponses. 

 

2. Le rôle de FastAPI 

FastAPI est un framework Python qui te permet de créer une API web. 

🔹 À quoi sert FastAPI concrètement ? 

FastAPI te permet de : 

définir les routes de ton API (ex : récupérer tous les tickets) 

décrire ce que l’API accepte (paramètres, données envoyées) 

décrire ce que l’API renvoie (réponses) 

gérer les erreurs (ticket non trouvé, données invalides, etc.) 

👉 En résumé : 
FastAPI = la logique et les règles de ton API 

 

🔹 FastAPI travaille avec le protocole HTTP 

FastAPI est basé sur les règles du web : 

des URL (ex : /tickets) 

des méthodes HTTP : 

demander des données 

en créer 

en modifier 

en supprimer 

Quand React fait une requête : 

FastAPI reçoit la requête 

il exécute la bonne logique 

il prépare une réponse structurée (souvent en JSON) 

 

🔹 FastAPI ne lance pas le serveur tout seul 

C’est un point clé à comprendre. 

FastAPI : 

décrit l’API 

organise les routes 

définit le comportement 

Mais il n’écoute pas le réseau tout seul. 

👉 Il a besoin d’un serveur web pour fonctionner réellement. 

 

3. Le rôle de Uvicorn 

Uvicorn est un serveur web. 

🔹 À quoi sert Uvicorn ? 

Uvicorn : 

lance ton application FastAPI 

écoute les requêtes HTTP sur un port 

transmet les requêtes à FastAPI 

renvoie les réponses au client (React, navigateur, etc.) 

👉 Sans Uvicorn : 

ton API existe “sur le papier” 

mais personne ne peut s’y connecter 

 

🔹 Analogie simple 

Imagine un restaurant : 

FastAPI = le chef et les recettes 
(il sait quoi faire quand une commande arrive) 

Uvicorn = la salle et les serveurs 
(il reçoit les clients et transmet les commandes au chef) 

Les deux sont indispensables, mais ils n’ont pas le même rôle. 

 

4. Comment FastAPI et Uvicorn travaillent ensemble 

Voici le cycle complet : 

Uvicorn démarre 

Il charge ton application FastAPI 

Il ouvre un port (ex : 8000) 

React envoie une requête HTTP 

Uvicorn reçoit la requête 

Uvicorn la transmet à FastAPI 

FastAPI : 

analyse la requête 

exécute la logique (lecture du JSON, filtrage, etc.) 

prépare une réponse 

Uvicorn renvoie la réponse à React 

👉 FastAPI ne parle jamais directement au réseau 
👉 Uvicorn ne décide jamais de la logique 

 

5. Pourquoi FastAPI est très utilisé en projet scolaire 

FastAPI est apprécié car : 

il est simple à comprendre 

il force une structure claire 

il est très proche des standards du web 

il génère automatiquement une documentation interactive 

👉 Cette documentation te permet de : 

tester ton API sans React 

comprendre les routes 

vérifier les réponses 

C’est un énorme avantage pédagogique. 

 

6. Pourquoi Uvicorn est souvent choisi avec FastAPI 

Uvicorn est : 

rapide 

léger 

parfaitement compatible avec FastAPI 

largement utilisé en production et en apprentissage 

👉 Dans la majorité des projets FastAPI : 

FastAPI = framework 

Uvicorn = serveur 

C’est un duo presque “officiel”. 

 

7. Ce qu’il faut absolument retenir 

Si tu dois l’expliquer à l’oral ou à l’écrit : 

FastAPI : 

définit ton API 

gère les routes 

applique la logique métier 

Uvicorn : 

lance l’application 

écoute les requêtes HTTP 

fait le lien entre le réseau et FastAPI 

 

Si tu veux, la prochaine fois je peux t’expliquer : 

comment penser les routes REST 

comment structurer ton projet FastAPI 

comment React communique avec l’API 

ou comment tester ton API sans frontend 

Dis-moi 

 

 

 

 

 

 

(index):1 Access to fetch at 'http://localhost:8000/tickets' from origin 'http://localhost:5173' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource. 

Très bien, cette erreur est fondamentale quand on relie un frontend React à une API 👍 
Je vais t’expliquer calmement, sans code, en partant du principe que tu découvres le sujet. 

 

1. Ce que dit exactement le message 

Prenons le message tel quel : 

Access to fetch at 'http://localhost:8000/tickets' from origin 'http://localhost:5173' has been blocked by CORS policy 

👉 Le navigateur te dit : 

« Une page web ouverte sur localhost:5173 » 

« essaie d’appeler une API sur localhost:8000 » 

« et je bloque la requête » 

 

No 'Access-Control-Allow-Origin' header is present on the requested resource 

👉 Et il précise pourquoi : 

l’API n’autorise pas explicitement cette origine 

 

2. Pourquoi cette erreur n’existe pas côté serveur 

Point très important : 

👉 Ce n’est PAS une erreur FastAPI 
👉 Ce n’est PAS une erreur Uvicorn 

C’est une sécurité du navigateur. 

Si tu fais la requête avec : 

Postman 

curl 

la documentation FastAPI 
👉 ça fonctionne souvent sans problème 

Mais : 

le navigateur applique des règles de sécurité supplémentaires 

 

3. Le principe de CORS (explication simple) 

CORS signifie Cross-Origin Resource Sharing. 

En clair : 

Un site web n’a pas le droit d’appeler une autre origine 
sauf si le serveur l’autorise explicitement. 

 

🔹 Qu’est-ce qu’une “origine” ? 

Une origine est définie par 3 éléments : 

le protocole (http / https) 

le domaine (localhost) 

le port 

Donc : 

http://localhost:5173 ≠ http://localhost:8000 

👉 Même si c’est le même ordinateur, le navigateur considère que ce sont deux origines différentes. 

 

4. Pourquoi cette règle existe 

Sans CORS : 

un site malveillant pourrait appeler n’importe quelle API 

récupérer des données privées 

agir à la place de l’utilisateur 

👉 CORS est une protection, pas un bug. 

 

5. Ce que le navigateur attend de ton API 

Le navigateur dit à ton API : 

« Dis-moi explicitement si tu acceptes des requêtes venant de http://localhost:5173. » 

Et ton API doit répondre : 

« Oui, j’accepte cette origine. » 

Cela se fait via un en-tête HTTP : 

Access-Control-Allow-Origin 

Mais pour l’instant : 

FastAPI ne l’envoie pas 

donc le navigateur bloque la réponse 

 

6. Pourquoi ça arrive dans ton projet précis 

Dans ton cas : 

React tourne sur : localhost:5173 

FastAPI tourne sur : localhost:8000 

👉 Configuration classique en développement 
👉 Mais CORS doit être configuré explicitement 

FastAPI, par défaut : 

n’autorise aucune origine externe 

même si c’est ton propre frontend 

 

7. Comment raisonner pour corriger le problème 

Sans parler de code, la logique est la suivante : 

Tu identifies qui appelle l’API 

React sur localhost:5173 

Tu décides si tu fais confiance à cette origine 

oui, c’est ton frontend 

Tu configures ton API pour : 

autoriser cette origine 

autoriser certaines méthodes (GET, POST, etc.) 

autoriser certains en-têtes 

👉 Cette configuration est côté API, jamais côté React. 

 

8. Erreur fréquente chez les débutants (important) 

Beaucoup pensent : 

“Je vais corriger ça côté React” 

❌ Faux 

React ne peut pas lever une règle de sécurité du navigateur 

seule l’API peut dire : 

« J’autorise cette origine » 

 

9. Ce que cette erreur prouve (bonne nouvelle) 

Cette erreur montre que : 

ton frontend fonctionne 

ta requête fetch est bien envoyée 

ton API est joignable 

FastAPI répond 

👉 Le navigateur bloque après la réponse du serveur 
👉 C’est donc une question de configuration, pas de logique métier 

 

10. Résumé à mémoriser pour ton projet 

Tu peux retenir cette phrase clé : 

Une erreur CORS signifie que le navigateur protège l’utilisateur, et que l’API doit autoriser explicitement l’origine du frontend. 

Dans ton cas : 

origine frontend : http://localhost:5173 

API : http://localhost:8000 

autorisation manquante → blocage 

 

Si tu veux, je peux ensuite t’expliquer : 

comment FastAPI gère CORS conceptuellement 

ce qu’est une requête preflight (OPTIONS) et pourquoi elle existe 

comment configurer CORS proprement en développement 

ou comment éviter ces problèmes en production 

Dis-moi ce que tu veux approfondir 👌

## Nos erreurs

Lors du premier lancement de notre frontend, nous avons rencontré l'erreur suivante :  
```Access to fetch at 'http://localhost:8000/tickets' from origin 'http://localhost:5173' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.```  
Toutes nos requêtes étaient bloquées par la CORS policy. Après quelques recherches sur internet, nous avons compris qu'il fallait configurer un middleware afin d'accepter les requêtes venant de localhost:5173, où est hébergée notre site.  
  
Lors de la consommation de l'endpoint PATCH permettant de modifier le statut d'un ticket, nous avons rencontré l'erreur "Unprocessable content". Cela signifiait que le frontend n'envoyait pas le bon type de données.
Afin de comprendre le problème, nous avons dû refaire notre gestion d'erreurs et la centraliser dans le controleur avec les exceptions_handlers. Nous avons alors compris que la valeur que nous recevions, une ENUM, n'était pas sérialisable. Il a donc fallu créer une requête StatusUpdate dans le dossier models et l'utiliser en argument de l'endpoint.

## Erreur de l'IA

Nous n'avons pas rencontré d'erreur lors de notre utilisation des LLM.