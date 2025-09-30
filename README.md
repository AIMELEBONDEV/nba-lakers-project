# 🏀 Analyse des Lakers – 5 dernières saisons NBA


## Introduction  
Ce projet est né d’une question simple : 

*Quels joueurs ont réellement porté les Lakers ces dernières années ?*  
*Comment la franchise a-t-elle évolué en termes de performances ?* 

Pour y répondre, j’ai construit un pipeline de données qui part de l’API officielle de la NBA, transforme les informations en format **Parquet**, puis les connecte à **Power BI** pour obtenir des analyses visuelles interactives.
La prochaine étape est de pouvoir stocké les données dans une base de données Microsoft serveur.

---
## Organisation du projet
- **Collecte** : scripts Python qui appellent l’API NBA (`nba_api`) pour récupérer les matchs, joueurs et saisons.  
- **Stockage** : données enregistrées en **Parquet** pour faciliter les mises à jour.  
- **Analyse** : tableaux de bord Power BI pour explorer l’évolution de la franchise et la contribution des joueurs.  



## Pipeline en bref
1. **Extraction** : via l’API NBA, récupération des matchs et statistiques joueurs.  
2. **Transformation** : nettoyage, structuration et sauvegarde en Parquet.  
3. **Visualisation** : intégration dans Power BI pour explorer l’histoire des Lakers.  


   <img width="937" height="356" alt="image" src="https://github.com/user-attachments/assets/b9117a91-842d-4455-9585-ea35f7d1be7f" />


## Analyse Franchise (Vue d’ensemble)  
Cette première partie met en avant le comportement global des Lakers sur les 5 dernières saisons :  
- Évolution des victoires/défaites.  
- Séries marquantes.  
- Tendances saison après saison.  
  
<img width="1284" height="722" alt="image" src="https://github.com/user-attachments/assets/68bf5ddd-d57f-411c-8cf9-6c0768d908a3" />
 

##  Analyse Joueurs (Contribution individuelle)  
La deuxième partie se concentre sur les joueurs :  
- Qui contribue le plus aux victoires ?  
- Quels profils ressortent selon les statistiques clés (points, rebonds, passes, etc.) ?  
- Comment la contribution des stars et du collectif évolue au fil des saisons ?
   

<img width="892" height="496" alt="image" src="https://github.com/user-attachments/assets/c555afdf-761f-44f7-bcd2-b8061e7e5ba5" />
 

## Résultats attendus
- Identifier les **joueurs clés** qui ont marqué la différence.  
- Comprendre l’évolution des **performances globales de la franchise pour orienter la nouvelle saison**.  
- Fournir un outil interactif avec Power BI pour analyser la NBA de manière dynamique. 

---
## Auteur 
Projet réalisé par Aimé ADJEGUEDE, passionné de data et de sport.

Cette analyse met en évidence une légère baisse de la performance des Lakers au cours des cinq dernières saisons, d’environ 4%, tant sur le plan offensif que défensif. Au niveau des joueurs, LeBron James et Anthony Davis ont joué un rôle majeur en contribuant significativement au nombre de points, aux passes décisives et à l’effort défensif. Le rapport Power BI illustre clairement ces contributions.

Ce rapport peut être utilisé par une franchise ou même par les Lakers pour suivre et évaluer les performances de leur équipe.

## La prochaine étape
La prochaine étape consistera à améliorer l’architecture en intégrant SQL Server comme entrepôt de données pour centraliser et gérer les informations. Si le projet évolue, l’intégration d’un CI/CD permettra de passer à une architecture professionnelle complète, et il sera envisageable de développer une application Django pour consommer et visualiser les données, facilitant ainsi le travail des équipes ou des journalistes.
