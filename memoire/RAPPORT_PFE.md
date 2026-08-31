# [NOM DE L'ÉCOLE]

**[Formation / Titre visé, ex. : Master Data Engineer — Titre RNCP Niveau 7]**

---

# Projet de Fin d'Études

En vue de l'obtention du **[Nom exact du diplôme]**

## SkillGap AI : une plateforme de matching CV — offres d'emploi et de recommandation de formations assistée par IA

---

Présenté par
**Fidélia SOWAKOUDE**

Réalisé [au sein de / dans le cadre de] **[Nom de l'entreprise / du contexte du projet, si applicable]**

Encadrant(e) : **[Nom de l'encadrant·e]**

**[Mois AAAA] – [Mois AAAA]**

---
---

## Remerciements

*[À compléter — section personnelle : remerciements à l'encadrant·e, à l'école/l'entreprise d'accueil, aux proches, et un mot de conclusion personnel sur le parcours accompli.]*

---

## Table des matières

- Introduction générale
- **1. Introduction générale du projet**
  - 1.1 Contexte du projet
  - 1.2 Problématique
  - 1.3 Enjeux
  - 1.4 Objectifs du projet
- **2. Analyse des besoins et spécifications**
  - 2.1 Identification des besoins fonctionnels
  - 2.2 Exigences non fonctionnelles et contraintes techniques
  - 2.3 Choix technologiques et justification
  - 2.4 Cartographie des besoins et fonctionnalités
- **3. Conception et architecture**
  - 3.1 Présentation générale de l'architecture
  - 3.2 Présentation des composants du pipeline
  - 3.3 Architecture applicative avec Streamlit
  - 3.4 Orchestration et automatisation avec Airflow
  - 3.5 Gestion des coûts API et stratégie de cache
  - 3.6 Sécurité et contrôle d'accès
- **4. Collecte des données**
  - 4.1 Sources de données et méthodes de collecte
  - 4.2 Préparation des fichiers et vérification des doublons
- **5. Stockage et modélisation des données**
  - 5.1 Schéma relationnel retenu
  - 5.2 Modèle pgvector
  - 5.3 Stratégie de cache des recommandations
  - 5.4 Accès aux données pour les étapes ultérieures
- **6. Extraction et structuration des compétences (CV & offres)**
  - 6.1 Parsing des CV
  - 6.2 Extraction des compétences depuis les offres
  - 6.3 Normalisation et nettoyage
- **7. Machine Learning : matching sémantique et skill-gap**
  - 7.1 Préparation des données textuelles
  - 7.2 Génération des embeddings et similarité vectorielle
  - 7.3 Formule de matching
  - 7.4 Calcul du skill-gap et classification
  - 7.5 Score d'impact et priorisation
- **8. Intégration de l'intelligence artificielle générative (Mistral)**
  - 8.1 Choix du fournisseur LLM et comparatif
  - 8.2 Le client Mistral partagé
  - 8.3 Génération des recommandations personnalisées
  - 8.4 Stratégie de cache pour l'optimisation des coûts API
- **9. Développement de l'interface utilisateur (Streamlit)**
  - 9.1 Structure générale de l'application
  - 9.2 Page d'analyse et résultats
  - 9.3 Page Tendances
  - 9.4 Page Recommandations et routage via st.session_state
  - 9.5 Authentification et gestion des utilisateurs
- **10. Automatisation avec Airflow**
  - 10.1 Configuration du DAG de collecte et transformation
  - 10.2 Visualisation du DAG
  - 10.3 Avantages de l'automatisation pour le projet
- **11. Difficultés rencontrées et solutions**
  - 11.1 Problèmes de réseau Docker
  - 11.2 Confusion environnement d'exécution
  - 11.3 Robustesse du traitement des données JSON
  - 11.4 Choix techniques revus
- Conclusion générale et perspectives
- Bibliographie

## Table des figures

- Figure 3.1 — Page d'accueil de SkillGap
- Figure 3.2 — Page de connexion
- Figure 9.1 — Dépôt du CV sur la page Matching
- Figure 9.2 — Résultat d'analyse du matching CV
- Figure 9.3 — Page Offres trouvées
- Figure 9.4 — Page Tendances du marché
- Figure 9.5 — Page Recommandations de formations
- Figure 9.6 — Assistant IA conversationnel

---

## Introduction générale

La recherche d'un premier poste ou d'une reconversion dans le secteur de la data se heurte aujourd'hui à un paradoxe : le marché de l'emploi n'a jamais publié autant d'offres, mais un candidat individuel a rarement les moyens de savoir, précisément, ce qui le sépare du poste qu'il vise. Les offres sont dispersées entre plusieurs plateformes, les intitulés de compétences varient d'une entreprise à l'autre, et rien ne relie mécaniquement le contenu d'un CV aux exigences réelles du marché à un instant donné.

SkillGap AI est né de cette observation. Le projet ne se contente pas de centraliser des offres d'emploi : il analyse sémantiquement un CV, le compare au marché réel via une base d'offres vectorisées, en déduit les compétences manquantes les plus déterminantes, puis referme la boucle en proposant des formations vérifiées et un accompagnement conversationnel pour combler ces écarts.

Ce rapport suit la table des matières validée pour ce mémoire : le contexte et les objectifs du projet, l'analyse des besoins, la conception et l'architecture technique, le pipeline de collecte des données, le stockage et la modélisation des données, l'extraction des compétences, le moteur de matching sémantique, les fonctionnalités d'intelligence artificielle générative, l'application Streamlit, l'automatisation Airflow, et enfin les difficultés rencontrées. Une attention particulière est portée, tout au long du document, à la distinction entre ce qui est effectivement implémenté et vérifié dans le code du projet, et ce qui a été envisagé, évalué puis écarté ou reporté — un choix délibéré de rigueur plutôt que d'exhaustivité apparente. Chaque fois que la structure attendue de ce rapport suppose un composant qui n'a finalement pas été retenu pour la version actuelle de SkillGap AI (par exemple une source de données par scraping, ou un schéma de base entièrement normalisé), ce chapitre l'indique explicitement et explique la solution réellement mise en œuvre à la place, ainsi que la raison de cet écart.

---

# 1. Introduction générale du projet

## 1.1 Contexte du projet

Le secteur de la data (data analyst, data engineer, data scientist, MLOps...) connaît en France une croissance soutenue de la demande, portée par la généralisation des usages de la donnée et de l'intelligence artificielle dans les entreprises. Cette dynamique s'accompagne d'un paradoxe bien documenté : la multiplication des offres ne facilite pas la recherche d'emploi, elle la complique. Les candidats doivent composer avec des intitulés de poste hétérogènes, des référentiels de compétences qui varient d'une entreprise à l'autre, et l'absence d'un outil qui leur dise, concrètement, où se situe l'écart entre leur profil actuel et un poste visé.

SkillGap AI répond à ce constat en proposant une plateforme qui ne se contente pas d'agréger des offres, mais qui les met en relation directe avec le profil réel du candidat, via une analyse sémantique de son CV.

## 1.2 Problématique

Comment permettre à un candidat de comprendre, de façon quantifiée et actionnable, ce qui le sépare des offres d'emploi correspondant à son projet professionnel — et de savoir précisément quoi apprendre en priorité pour combler cet écart ?

## 1.3 Enjeux

- **Objectiver le matching** : remplacer la recherche par mots-clés, peu fiable dès que les intitulés de compétences varient, par une comparaison sémantique du contenu réel du CV et des offres.
- **Rendre l'écart actionnable** : ne pas se contenter d'un score de compatibilité, mais identifier précisément les compétences manquantes les plus déterminantes et donner un chemin concret pour les acquérir.
- **Rester honnête sur les données proposées** : ne jamais présenter au candidat une formation ou une ressource inventée — un enjeu de confiance central dès lors qu'on introduit de l'IA générative dans le parcours.
- **Automatiser la fraîcheur des données** : le marché de l'emploi évolue en continu ; la pertinence du matching dépend directement de la régularité de la collecte des offres.

## 1.4 Objectifs du projet

1. Centraliser des offres d'emploi réelles issues d'une source publique fiable (France Travail), avec un pipeline de collecte automatisé et reproductible.
2. Développer un moteur de matching sémantique CV ↔ offres, fondé sur des embeddings vectoriels plutôt que sur une simple correspondance de mots-clés.
3. Calculer, pour chaque candidat, un classement objectif des compétences qui lui manquent le plus fréquemment par rapport aux offres auxquelles il correspond.
4. Proposer des ressources de formation réelles et vérifiées pour combler ces écarts, sans recourir à du contenu généré par IA sur des faits vérifiables.
5. Accompagner le candidat au-delà du résultat brut, via un assistant conversationnel capable d'expliquer son score et de le conseiller, ancré sur son profil réel.
6. Automatiser l'ensemble du pipeline de données (collecte → transformation → chargement → vectorisation) pour que la plateforme reste à jour sans intervention manuelle quotidienne.

---

# 2. Analyse des besoins et spécifications

## 2.1 Identification des besoins fonctionnels

### 2.1.1 Analyse du skill-gap et personnalisation des recommandations

Le cœur fonctionnel de SkillGap AI est la détection d'écart de compétences (« skill-gap ») : pour chaque offre comparée au CV du candidat, le système distingue les compétences déjà maîtrisées de celles qui manquent, puis agrège ces écarts à l'échelle de l'ensemble des offres pertinentes pour dégager une priorité d'apprentissage. Cette analyse alimente directement la personnalisation des recommandations (Chapitre 8) : chaque compétence manquante prioritaire donne lieu à une formation vérifiée et à un projet pratique généré par IA, plutôt qu'à une liste générique de cours sans lien avec le profil réel du candidat.

### 2.1.2 Accessibilité et rapidité de l'analyse CV/offre

Le candidat doit pouvoir obtenir un résultat de matching sans étape d'installation ni de configuration : dépôt d'un fichier PDF ou DOCX par glisser-déposer (ou collage direct du texte, prévu pour faciliter les tests), extraction du texte côté serveur, puis affichage du score de correspondance en quelques secondes. Le choix technique qui sert directement ce besoin est décrit en 2.3 : un seul modèle d'embeddings chargé une fois par processus, une recherche de similarité déléguée à PostgreSQL/pgvector plutôt qu'à un calcul Python côté application, et une interface Streamlit qui affiche un résultat dès que la requête SQL revient, sans étape de compilation ni de build côté client.

### 2.1.3 Automatisation du pipeline de collecte des offres

La pertinence du matching dépend directement de la fraîcheur des offres en base. Le besoin identifié ici est celui d'un pipeline qui tourne sans intervention manuelle quotidienne : collecte, nettoyage, chargement et vectorisation des nouvelles offres doivent s'enchaîner automatiquement, avec une traçabilité des exécutions et une capacité de reprise en cas d'échec partiel. C'est ce besoin qui justifie le choix d'Apache Airflow comme orchestrateur (voir 2.3.4 et Chapitre 10) plutôt qu'un simple script planifié par cron.

## 2.2 Exigences non fonctionnelles et contraintes techniques

### 2.2.1 Sécurité et conformité (données CV, RGPD)

Le CV et les informations qu'il contient (identité, coordonnées, parcours) sont des données à caractère personnel au sens du RGPD. Plusieurs choix de conception en découlent directement :

- **Minimisation des données transmises à des tiers.** Le texte brut du CV n'est jamais transmis à un service tiers pour les fonctionnalités génératives récurrentes (recommandations de formation, conversation avec l'assistant IA) : seuls les labels de compétences déjà extraits sont envoyés au fournisseur de LLM. Une exception assumée existe : l'extraction automatique du poste visé (Chapitre 8) envoie jusqu'à 4000 caractères du texte du CV à Mistral pour cette tâche ponctuelle — ce qui est documenté ici pour rester rigoureux plutôt que de prétendre à une confidentialité absolue vis-à-vis du CV.
- **Consentement explicite.** Le formulaire d'inscription conditionne la création de compte à l'acceptation explicite d'une case à cocher « J'accepte les conditions d'utilisation et la politique de confidentialité », plutôt que de considérer le consentement comme acquis par défaut.
- **Protection des identifiants de connexion.** Les mots de passe ne sont jamais stockés en clair : ils sont hachés avec `bcrypt` (sel aléatoire propre à chaque utilisateur), et seul le hash est conservé en base (`frontend/back_service/auth_service.py`).
- **Limite assumée sur le droit à l'oubli.** À ce stade du projet, il n'existe pas encore de fonctionnalité permettant à un utilisateur de supprimer lui-même son compte et les données associées (CV, historique de matching) : c'est une limite de conformité RGPD identifiée mais non résolue, documentée en Chapitre 11 et en conclusion plutôt que passée sous silence.
- **Secrets hors du dépôt de code.** Le fichier `.env` (identifiants de base de données, clé API Mistral, identifiants MinIO) est exclu du dépôt Git ; les secrets sont injectés par variables d'environnement dans chaque conteneur Docker.

### 2.2.2 Scalabilité et robustesse

Le projet est conçu pour un volume d'offres de l'ordre de quelques dizaines de milliers de lignes (six intitulés de poste ciblés, collecte sur la France entière) — un volume qui reste dans le domaine de confort d'une instance PostgreSQL unique. Deux choix garantissent que cette architecture reste robuste face à la croissance du volume plutôt que de nécessiter une refonte à court terme :

- **Index approximatif HNSW sur la colonne `embedding`** (`USING hnsw (embedding vector_cosine_ops)`), qui garde un temps de réponse de recherche par similarité sous-linéaire même lorsque le nombre d'offres en base augmente, contrairement à un parcours séquentiel de toute la table.
- **Upsert plutôt qu'insertion aveugle** (`ON CONFLICT (source_url) DO UPDATE`) lors du chargement, qui empêche la table de grossir artificiellement à chaque exécution du pipeline avec des doublons d'une même offre déjà connue.

La robustesse du pipeline face à des données d'entrée imparfaites (champs absents de la réponse API, structure JSON incomplète) est traitée en détail au Chapitre 4 (§4.2.2).

### 2.2.3 Disponibilité et performance

SkillGap AI est un projet de fin d'études porté par une seule personne, exécuté en développement via Docker Compose sur une machine unique : il n'y a pas d'exigence de disponibilité de type SLA de production (pas de réplication, pas de bascule automatique en cas de panne). Les choix de performance qui ont néanmoins été faits portent sur l'expérience perçue par l'utilisateur :

- Les statistiques coûteuses à recalculer (tendances du marché, taux d'adéquation du CV au marché) sont mises en cache côté application via `@st.cache_data(ttl=600)` (10 minutes), pour éviter de repasser sur l'ensemble des offres ou de ré-encoder le CV à chaque interaction de l'utilisateur avec l'interface (voir 3.5).
- Le matching lui-même ne considère que les offres publiées dans les 30 derniers jours (`WHERE date_du_poste >= NOW() - INTERVAL '30 days'`), ce qui garde la table balayée par la recherche vectorielle à une taille raisonnable et la réponse rapide, en plus de garantir la pertinence des résultats (voir 2.2.4 et Chapitre 7).
- Le chargement des offres (upsert) et leur vectorisation sont deux étapes découplées : la vectorisation ne retraite que les lignes dont `embedding IS NULL`, jamais l'ensemble de la table, ce qui évite un recalcul coûteux et inutile à chaque exécution quotidienne du pipeline.

### 2.2.4 Maintenance et évolutivité du pipeline

Trois décisions structurent la maintenabilité du pipeline dans la durée :

- **Un référentiel de compétences unique et partagé** (`scripts/skills_reference.py`, fonction `extract_skills()`), utilisé à la fois par le chargement des offres et par le matching CV. Ajouter une compétence à ce référentiel la rend immédiatement disponible des deux côtés, sans risque de désynchronisation entre le vocabulaire des offres et celui des CV.
- **Des scripts partagés entre l'application et Airflow.** Les modules de `scripts/` (matching, extraction de compétences, chargement, vectorisation) sont montés à la fois dans le conteneur Streamlit et dans les conteneurs Airflow (`docker-compose.yml`), pour que la même logique métier serve dans les deux contextes plutôt que d'être dupliquée.
- **Des étapes de pipeline idempotentes et rejouables indépendamment**, découpées en DAGs distincts (Chapitre 3 §3.4 et Chapitre 10) : une étape en échec peut être rejouée seule, sans devoir relancer l'intégralité de la collecte depuis l'API externe.

## 2.3 Choix technologiques et justification

### 2.3.1 Docker & Docker Compose

Isolation et reproductibilité de chaque service (base de données, stockage objet, orchestration, application). L'ensemble de la stack (`postgres`, `pgadmin`, `minio`, `create-buckets`, `airflow-webserver`, `airflow-scheduler`, `streamlit`) démarre à l'identique sur n'importe quelle machine avec une seule commande (`docker compose up -d`), ce qui élimine la classe de bugs « ça marche chez moi ».

### 2.3.2 PostgreSQL + pgvector

Une seule base relationnelle (image `pgvector/pgvector:pg17`) sert à la fois de stockage classique (offres, utilisateurs) et de moteur de recherche vectorielle (colonne `embedding vector(384)`), évitant de maintenir un moteur de recherche dédié séparé (type Pinecone, Weaviate ou Qdrant) pour un volume de données qui ne le justifie pas encore.

### 2.3.3 Streamlit (choix vs FastAPI, compromis assumé)

Streamlit a été retenu pour construire l'intégralité de l'interface interactive en Python pur, sans développer de frontend séparé — cohérent avec un projet porté par une seule personne dans un temps contraint : une même personne écrit la logique métier et l'écran qui l'affiche, sans synchronisation d'API entre deux bases de code.

Ce choix a un coût assumé, documenté plutôt que dissimulé : le dépôt contient une ébauche de service **FastAPI** (`backend/main.py`), pensée au départ comme couche API séparée entre le stockage et l'interface. Son bloc de service est aujourd'hui commenté dans `docker-compose.yml` et son code se limite à deux routes de santé (`/` et `/sante`) — la logique métier n'y a finalement pas été portée. Le compromis assumé est le suivant : Streamlit interroge PostgreSQL en direct depuis le même processus qui affiche l'interface, ce qui accélère l'itération sur un projet solo, mais ne permettrait pas, en l'état, de servir un futur client mobile ou une intégration tierce sans réintroduire cette couche API — un axe d'évolution identifié en conclusion plutôt qu'un manque non anticipé.

### 2.3.4 Airflow

Orchestration et planification du pipeline de collecte/transformation/chargement, avec reprise sur erreur (`retries`, `retry_delay`) et traçabilité complète des exécutions (statut, durée, logs par tâche) via l'interface web. Alternative à un enchaînement de scripts cron sans visibilité ni gestion de dépendances entre étapes.

### 2.3.5 MinIO (stockage objet)

Stockage objet compatible S3, utilisé pour organiser le pipeline de données selon une architecture en médaillon (bronze / silver / gold — voir Chapitre 3), sans dépendre d'un cloud provider payant en développement. Les buckets `bronze`, `silver` et `gold` sont créés automatiquement au démarrage par le service `create-buckets`.

### 2.3.6 Mistral API (LLM) — comparatif vs Gemini/Groq/OpenRouter/Ollama

Le choix du fournisseur de LLM générateur (recommandations, chat, extraction du poste visé) s'est fait par comparaison de plusieurs options :

- **Google Gemini** a été la seule alternative évaluée de façon concrète, en parallèle de Mistral, avant de trancher. Les deux offrent un accès gratuit exploitable pour ce projet. Le choix s'est porté sur Mistral pour trois raisons : une meilleure adéquation au traitement du français (pertinent puisque l'ensemble du contenu candidat — CV, conversation — est en français), une politique de confidentialité plus simple à désactiver sur le tier gratuit (l'entraînement sur les données utilisateur peut être désactivé directement depuis la console, sans devoir lier de moyen de paiement comme l'exige Gemini pour les utilisateurs européens), et un SDK déjà en place dans le projet.
- **Groq** et **OpenRouter** ont été considérés à un niveau plus superficiel, en tant qu'hébergeurs/agrégateurs de modèles tiers plutôt que fournisseurs de modèle propre : leur intérêt principal (latence d'inférence très basse pour Groq, choix étendu de modèles pour OpenRouter) ne correspondait pas à un besoin identifié pour ce projet, dont les appels sont ponctuels (une génération par écart de compétence, un message de chat à la fois) et non sensibles à la latence d'inférence brute. Ils n'ont pas fait l'objet d'une intégration technique.
- **Ollama** (exécution locale de modèles open source) a été écarté pour une raison d'infrastructure plutôt que de qualité de modèle : il suppose une ressource de calcul locale (GPU ou CPU dimensionné) dédiée en permanence dans la stack Docker Compose, ce qui va à l'encontre du choix assumé de s'appuyer sur des API managées pour rester léger à faire tourner sur une machine de développement standard.

Le SDK Mistral est aujourd'hui appelé directement depuis chaque service ayant besoin de génération (`frontend/back_service/mistral_client.py`, `recommendation_service.py`, `chat_service.py`, `cv_parser.py`) plutôt que derrière une couche d'abstraction générique multi-fournisseurs : il n'existe pas, dans le code actuel, de fonction `call_llm()` agnostique du fournisseur — un seul fournisseur étant utilisé en production, cette abstraction n'a pas été jugée nécessaire à ce stade. C'est un axe de refactorisation possible si un second fournisseur devait être ajouté (voir conclusion).

## 2.4 Cartographie des besoins et fonctionnalités

| Besoin | Solution fonctionnelle | Technologie associée |
|---|---|---|
| Authentification | Formulaire de connexion/inscription, mots de passe hachés | `bcrypt`, PostgreSQL |
| Centralisation des offres | Pipeline automatisé de collecte et chargement | France Travail API, Airflow, MinIO |
| Matching sémantique | Comparaison d'embeddings CV/offres | `sentence-transformers`, pgvector |
| Détection des écarts | Comparaison ensembliste des compétences par offre | Référentiel `skills_reference.py`, Python |
| Recommandations de formation | Catalogue vérifié + génération de projets pratiques | Catalogue statique, Mistral AI |
| Assistant conversationnel | Chat contextualisé sur le profil du candidat | Mistral AI (chat, streaming) |
| Exploration du marché | Tableaux de bord agrégés | Altair, `market_stats.py` |
| Automatisation | Pipeline planifié et rejouable | Apache Airflow |

---

# 3. Conception et architecture

## 3.1 Présentation générale de l'architecture

### 3.1.1 Choix de l'approche (pipeline ELT via Airflow)

Le pipeline suit une architecture en médaillon (bronze / silver / gold), orchestrée par Airflow. Le principe général est celui d'un pipeline **ELT** au sens large adopté par les architectures lakehouse modernes : la donnée brute est d'abord extraite et déposée telle quelle (bronze), avant d'être progressivement transformée en place à travers les zones successives (silver, puis gold). Une nuance mérite d'être signalée pour rester rigoureux : contrairement à un ELT strict où le chargement dans l'entrepôt final précéderait la transformation, SkillGap AI nettoie et structure les données (silver) avant de les charger dans PostgreSQL (gold) — une variante que l'on peut qualifier d'ETL organisé selon la même logique de zones que les architectures ELT/lakehouse, choisie parce qu'elle simplifie le chargement final (un upsert sur des colonnes déjà typées plutôt que sur du JSON brut).

### 3.1.2 Vue globale de l'architecture (schéma Docker Compose)

```
France Travail (API)
        │
        ▼
  [Airflow: ingestion_dags]  ──▶  MinIO/bronze (JSON brut)
        │
        ▼
[Airflow: transformation_silver_dag]  ──▶  MinIO/silver (Parquet nettoyé)
        │
        ▼
   [Airflow: dag_load_to_gold]
        │  ├─ chargement + upsert  ──▶  PostgreSQL (offres_emploi)
        │  └─ vectorisation manquante ──▶  colonne embedding (pgvector)
        ▼
  [Airflow: dag_master (@daily)] orchestre les 3 DAGs ci-dessus,
  puis (re)crée l'index HNSW de similarité cosinus
        │
        ▼
   Application Streamlit  ◀────────────  Mistral AI (recommandations, chat)
   (lit directement PostgreSQL)
```

![Page d'accueil de SkillGap](figures/fig_accueil.png)
*Figure 3.1 — Page d'accueil de SkillGap*

![Page de connexion](figures/fig_connexion.png)
*Figure 3.2 — Page de connexion*

## 3.2 Présentation des composants du pipeline

### 3.2.1 Collecte des données (France Travail, WTTJ)

SkillGap AI s'appuie en production sur une source de données unique et assumée : l'API publique **France Travail**. Une seconde source, **Welcome to the Jungle (WTTJ)**, a été explicitement évaluée en amont du développement mais n'a pas abouti à un scraper mis en production — le détail de cette évaluation et les raisons de cet arbitrage font l'objet du Chapitre 4 (§4.1.2), pour ne pas dupliquer l'explication ici.

### 3.2.2 Stockage initial dans PostgreSQL/MinIO

Le stockage initial de la donnée collectée se fait dans **MinIO**, pas directement dans PostgreSQL : chaque lot d'offres brutes récupéré depuis l'API est déposé tel quel (JSON) dans le bucket `bronze`. PostgreSQL n'intervient qu'en bout de chaîne, au moment du chargement en zone `gold` (§3.2.3 et Chapitre 5) : c'est le stockage définitif et interrogeable de l'application, mais pas le point d'entrée du pipeline. Ce séquencement (stockage brut d'abord, base relationnelle ensuite) permet de rejouer les étapes de transformation et de chargement sans avoir à re-solliciter l'API en cas d'évolution des règles de nettoyage.

### 3.2.3 Transformation des données

#### 3.2.3.1 Transformation pour l'analyse de matching

Le script `scripts/transform_datafr.py` lit les fichiers JSON bruts de la zone bronze et construit un jeu de données structuré : titre, description, compétences et langues détectées, type de contrat, niveau de diplôme requis, localisation, fourchette salariale (extraite par expression régulière du champ texte de l'API), secteur d'activité. Le résultat est enregistré au format Parquet dans le bucket `silver`. L'étape est idempotente : un fichier déjà transformé n'est pas retraité.

#### 3.2.3.2 Préparation des données pour le modèle vectoriel (embeddings)

La préparation des données destinées au modèle vectoriel se fait en deux temps distincts, volontairement découplés : le chargement dans `offres_emploi` (colonnes texte/structurées) d'abord, puis le calcul des embeddings ensuite, par `scripts/vectorisateur_data.py`, qui sélectionne les offres dont l'`embedding` est encore vide, encode leur description avec le modèle `paraphrase-multilingual-MiniLM-L12-v2` par lots de 32, et met à jour la base en masse (`execute_values`). Ce découpage (chargement ≠ vectorisation) permet de relancer l'un sans l'autre, et de ne jamais recalculer un embedding déjà existant.

## 3.3 Architecture applicative avec Streamlit

L'application est structurée en trois couches : les **vues** (`frontend/views/`, une page par fonctionnalité), les **services métier** (`frontend/back_service/`, logique réutilisable indépendante de l'affichage) et les **scripts partagés** (`scripts/`, utilisés à la fois par l'application et par les tâches Airflow — c'est le cas de `matching_cv.py` et `skills_reference.py`). Le routage entre les pages est détaillé au Chapitre 9 (§9.4).

## 3.4 Orchestration et automatisation avec Airflow

Le pipeline de données est découpé en quatre DAGs distincts plutôt qu'un unique script monolithique, pour que chaque étape reste indépendamment rejouable : `ingestion_dags` (collecte), `transformation_silver_dag` (nettoyage bronze → silver), `dag_load_to_gold` (chargement + vectorisation), et `master_pipeline_full_workflow` (orchestrateur quotidien). Le détail de la configuration et de l'exécution de ces DAGs est présenté au Chapitre 10.

## 3.5 Gestion des coûts API et stratégie de cache

Chaque appel à l'API Mistral (génération de conseils/projets, extraction du poste visé, message de chat) a un coût, même faible sur le tier gratuit — et surtout une latence perçue par l'utilisateur. La stratégie de cache retenue se situe **au niveau applicatif Streamlit**, pas dans une table PostgreSQL dédiée : le décorateur `@st.cache_data(ttl=600, show_spinner=False)` mémorise, pendant 10 minutes et par combinaison exacte d'arguments d'entrée, le résultat des fonctions coûteuses (`_cached_skill_advice()` dans `views/recommendation.py`, `_cached_market_fit_stats()` dans `views/matching.py`). Concrètement, pour un même ensemble de compétences manquantes, les recommandations générées par Mistral ne sont recalculées qu'une fois toutes les 10 minutes, et non à chaque re-rendu de la page (un modèle Streamlit ré-exécute son script à chaque interaction utilisateur).

Ce choix a été fait plutôt qu'une table de cache persistée en base (de type `recommendations_cache`), pour une raison de proportion : le cache en mémoire de processus suffit à absorber l'essentiel des appels redondants sur une session utilisateur, sans ajouter de logique d'invalidation ni de schéma supplémentaire pour un gain marginal à ce stade (le cache Streamlit ne survit pas à un redémarrage du conteneur ni ne se partage entre plusieurs instances de l'application, ce qui serait la limite à lever si SkillGap AI devait être déployé à plusieurs répliques).

## 3.6 Sécurité et contrôle d'accès

L'inscription et la connexion reposent sur un formulaire Streamlit classique (`frontend/views/authentification.py`), adossé à une table `users` PostgreSQL (`id`, `nom`, `prenom`, `email`, `password_hash`, `role`, `created_at`). Les mots de passe ne sont jamais stockés en clair : ils sont hachés avec `bcrypt`, avec un sel aléatoire propre à chaque utilisateur (`auth_service.py`). L'adresse e-mail est normalisée (minuscules, espaces retirés) avant toute comparaison, pour éviter les doublons de compte liés à la casse.

L'accès aux pages de l'application est conditionné à l'état `logged_in` de la session Streamlit, vérifié de façon centralisée dans `show_page()` (`frontend/app.py`) plutôt que page par page : un utilisateur non connecté ne peut atteindre que l'accueil, la connexion ou l'inscription, quelle que soit la valeur de `st.session_state.page`.

Le champ `role` de la table `users` existe dans le schéma (valeur par défaut `'candidat'`) mais n'est aujourd'hui lu par aucune logique d'autorisation : il n'y a qu'un seul niveau d'accès effectif dans l'application actuelle.

---

# 4. Collecte des données

## 4.1 Sources de données et méthodes de collecte

### 4.1.1 Présentation de la source France Travail (API officielle)

#### 4.1.1.1 Description des données accessibles via l'API

L'API partenaire France Travail (`api.francetravail.io/partenaire/offresdemploiv2`) expose, pour chaque offre, un ensemble de champs riches : intitulé, description complète, compétences et langues attendues (sous forme de libellés structurés), type de contrat, qualification/diplôme requis, expérience, localisation, fourchette de salaire (le plus souvent sous forme de texte libre), secteur d'activité de l'entreprise (NAF), et l'URL de l'offre.

#### 4.1.1.2 Authentification et envoi de requêtes

L'authentification se fait par OAuth2 en `client_credentials` (`get_access_token()` dans `scripts/recup_france_travail.py`) : `CLIENT_ID` et `CLIENT_SECRET` sont stockés comme variables Airflow (`Variable.get(...)`) plutôt qu'en dur dans le code, et échangés contre un jeton d'accès auprès de `entreprise.francetravail.fr/connexion/oauth2/access_token`, avec le scope `api_offresdemploiv2 o2dsoffre`. Ce jeton est ensuite passé en en-tête `Authorization: Bearer` sur chaque appel à l'endpoint de recherche.

#### 4.1.1.3 Script de collecte

Le script interroge l'endpoint de recherche pour six intitulés de métier ciblés (`data engineer`, `data analyst`, `data scientist`, `machine learning engineer`, `MLOps`, `développeur python`), sans restriction géographique. La pagination se fait par tranches de 149 résultats (`recup_all_pages()`), en avançant tant que la page renvoyée contient le nombre maximal de résultats — un code HTTP 206 signalant des résultats partiels, 200 la dernière page. Chaque lot est déposé dans MinIO via `S3Hook` (§4.2.1), et un rapport de collecte récapitulatif (nombre d'offres par métier) est généré en fin d'exécution dans `bronze/rapports/`.

### 4.1.2 Présentation de la source Welcome to the Jungle (scraping)

#### 4.1.2.1 Analyse du robots.txt et démarche éthique

Avant d'envisager tout scraping de Welcome to the Jungle, la démarche a suivi la pratique éthique standard en la matière : consultation du `robots.txt` et des conditions d'utilisation du site, pour vérifier qu'une collecte automatisée de pages d'offres publiques serait compatible avec la politique du site plutôt que de la contourner silencieusement. Cette analyse a mis en évidence une protection anti-bot robuste (AWS WAF) placée en amont du site, qui bloque de façon systématique jusqu'aux requêtes les plus simples vers des ressources pourtant publiques. Plutôt que de chercher à contourner ce dispositif — au prix d'une fragilité technique permanente et d'un risque vis-à-vis des conditions d'utilisation de la plateforme — la décision a été prise d'arrêter l'exploration de cette source à ce stade de diagnostic, avant l'écriture d'un quelconque script de scraping de production.

#### 4.1.2.2 Sources écartées (HelloWork — blacklist scraper ; Adzuna — couverture faible)

Deux autres sources ont été considérées puis écartées durant la même phase d'évaluation des alternatives à l'API France Travail :

- **HelloWork**, dont les mécanismes de détection bloquent (blacklistent) rapidement toute activité identifiée comme non humaine, pour les mêmes raisons de robustesse anti-bot que WTTJ.
- **Adzuna**, dont l'API d'agrégation d'offres, bien qu'accessible, présentait une couverture insuffisante pour le périmètre de métiers data ciblé par le projet en France — un volume d'offres trop faible pour justifier l'effort d'intégration.

#### 4.1.2.3 Pourquoi aucun script de scraping n'a été mis en production

Par souci de transparence, ce mémoire précise qu'aucun script de scraping fonctionnel pour WTTJ, HelloWork ou Adzuna n'a été écrit ni committé dans le dépôt du projet : l'évaluation ci-dessus a conclu, avant la phase d'implémentation, que le rapport effort/robustesse de ces sources ne justifiait pas leur intégration au regard d'une source officielle, documentée et stable comme l'API France Travail. C'est une décision de type « fail fast » assumée — écarter une piste sur la base d'un diagnostic rapide plutôt que d'investir du temps de développement dans un scraper fragile — plutôt qu'un développement resté inachevé. SkillGap AI fonctionne donc aujourd'hui avec une source de données unique, ce qui est documenté comme limite du projet en conclusion.

## 4.2 Préparation des fichiers et vérification des doublons

### 4.2.1 Format et structuration des données collectées

Chaque lot d'offres collectées est déposé dans le bucket MinIO `bronze` sous la forme d'un objet JSON structuré : `{"metadata": {...}, "nb_offres": N, "offres": [...]}`, fidèle à la réponse brute de l'API. Ce choix — conserver la donnée brute avant toute transformation — permet de rejouer les étapes suivantes du pipeline (§3.2.3) sans avoir à re-solliciter l'API en cas d'évolution des règles de nettoyage. La déduplication des offres n'intervient pas à ce stade : elle est gérée plus loin, au chargement en base, par une contrainte d'unicité sur `source_url` (Chapitre 5) et par l'upsert (`ON CONFLICT ... DO UPDATE`), une offre déjà connue étant mise à jour plutôt que dupliquée.

### 4.2.2 Gestion des erreurs et données défensives (cas KeyError: 'libelle')

La réponse de l'API France Travail n'est pas uniformément structurée d'une offre à l'autre : certains champs imbriqués (compétences, langues, salaire, formations) sont parfois absents, `null`, ou ne respectent pas exactement le schéma attendu. Un accès naïf du type `item['libelle']` sur une liste de compétences produit alors une `KeyError` dès la première offre incomplète rencontrée, et interrompt tout le traitement du lot.

`scripts/transform_datafr.py` traite ce risque de façon défensive plutôt que de laisser l'exception se propager :

```python
def extract_libelles(x):
    if not isinstance(x, list):
        return []
    return [item['libelle'] for item in x if isinstance(item, dict) and 'libelle' in item]
```

Chaque élément est vérifié individuellement (`isinstance(item, dict)` et présence de la clé) avant l'accès, et les éléments non conformes sont silencieusement ignorés plutôt que de faire échouer l'extraction de toute l'offre. Le même principe s'applique au champ salaire, lu via `salary_data.get('libelle') or salary_data.get('commentaire', "")` plutôt que par accès direct, et aux colonnes globalement absentes du DataFrame source (`get_col(...)`, avec valeur de repli `'Non précisé'`). Cette robustesse défensive est ce qui permet au pipeline de continuer à fonctionner malgré l'hétérogénéité réelle des données renvoyées par une API tierce externe, plutôt que de s'arrêter à la première offre atypique.

---

# 5. Stockage et modélisation des données

## 5.1 Objectif du schéma relationnel

Le schéma relationnel effectivement utilisé en production (`database/init.sql`) repose sur deux tables principales :

```sql
CREATE TABLE offres_emploi (
    id_offres_emploi SERIAL PRIMARY KEY,
    id_france_travail VARCHAR(50),
    titre VARCHAR(255),
    description TEXT,
    competences TEXT[],
    languages TEXT[],
    contract TEXT,
    diplome_requis TEXT,
    education TEXT,
    localisation TEXT,
    salaire_min FLOAT,
    salaire_max FLOAT,
    experience_years INTEGER,
    source_url TEXT,
    source_platform TEXT,
    company TEXT NOT NULL,
    secteur_activite TEXT,
    date_du_poste TIMESTAMP DEFAULT NOW(),
    embedding vector(384)
);

CREATE TABLE cv_candidats (
    id_cv SERIAL PRIMARY KEY,
    nom_candidat TEXT,
    competences_detectees TEXT[],
    ...
    cv_embedding vector(384)
);
```

Une conception « manuel de référence » du même besoin aurait pu reposer sur un schéma pleinement normalisé, avec des tables `cv_skills` et `job_skills` (association many-to-many entre compétences et CV/offres) et une table `matches` matérialisant chaque résultat de matching. Ce n'est **pas** le schéma retenu pour SkillGap AI. Le choix effectivement fait est un schéma dénormalisé, où les compétences sont stockées directement comme un tableau PostgreSQL (`competences TEXT[]`) au sein de la ligne de l'offre ou du CV, plutôt que dans une table de jointure séparée.

Ce choix a été fait pour des raisons de simplicité et de proportion au volume du projet : à l'échelle de quelques dizaines de milliers d'offres, un `TEXT[]` filtré côté application (voir Chapitre 7, comparaison ensembliste `matched_skills`/`missing_skills`) évite d'introduire des jointures SQL supplémentaires et une table de correspondance à maintenir, pour un bénéfice qui ne se ferait sentir qu'à un volume de données bien supérieur ou si l'on avait besoin d'interroger la fréquence d'une compétence directement en SQL (aujourd'hui calculée en Python, `rank_missing_skills()`). Un passage à un schéma normalisé `cv_skills` / `job_skills` (et une table `matches` persistant l'historique des analyses, aujourd'hui non conservé — chaque matching est recalculé à la volée et vit seulement dans `st.session_state`) est identifié comme évolution possible en conclusion, si le besoin de requêtage analytique sur les compétences venait à grandir.

Autre point de transparence : la table `cv_candidats` est bien créée par le script d'initialisation, mais n'est aujourd'hui alimentée par aucun code applicatif — aucune insertion n'y est faite lors d'un matching. Le CV du candidat est traité entièrement en mémoire, le temps de la session Streamlit (texte extrait, compétences détectées, vecteur), sans persistance en base. `cv_candidats` reste donc, en l'état, une table préparée pour une fonctionnalité future (historique des CV analysés) plutôt qu'un composant actif du pipeline actuel.

## 5.2 Modèle pgvector : stockage des embeddings

L'extension `pgvector` (activée via `CREATE EXTENSION IF NOT EXISTS vector`) ajoute le type `vector(384)` directement utilisable comme type de colonne PostgreSQL. Les deux tables ci-dessus portent chacune une colonne d'embedding (`embedding` pour les offres, `cv_embedding` — prévue mais non utilisée en pratique pour les raisons ci-dessus — pour les CV), dimensionnée à 384 pour correspondre à la sortie du modèle `paraphrase-multilingual-MiniLM-L12-v2` (Chapitre 7). Un index de similarité approximative HNSW (`vector_cosine_ops`) est (re)créé quotidiennement par le DAG orchestrateur sur la colonne `embedding` des offres, pour que la recherche par similarité cosinus reste rapide même lorsque le volume d'offres augmente.

## 5.3 Table `recommendations_cache` : structure et rôle

Il n'existe pas, dans le schéma actuel de SkillGap AI, de table PostgreSQL nommée `recommendations_cache` ou équivalente. La stratégie de mise en cache des recommandations générées par IA est implémentée à un autre niveau de l'architecture, décrit en détail au Chapitre 3 (§3.5) et au Chapitre 8 (§8.4) : un cache en mémoire de processus, côté application Streamlit (`@st.cache_data`), plutôt qu'une table persistée. Ce chapitre fait volontairement le lien entre les deux plutôt que de dupliquer l'explication : le rôle qu'une table `recommendations_cache` aurait joué (éviter de regénérer un contenu identique) est bien assuré dans SkillGap AI, mais par un mécanisme applicatif à durée de vie plus courte (10 minutes, non partagé entre plusieurs instances) plutôt que par une persistance en base.

## 5.4 Accès aux données pour les étapes ultérieures

Toutes les étapes situées en aval du chargement accèdent à la même base `job_matching` via une fonction de connexion centralisée, `get_db_connection()` (`scripts/matching_cv.py`), réutilisée par le matching CV (Chapitre 7), les statistiques de marché (`market_stats.py`, Chapitre 9) et la gestion des utilisateurs (`gestion_table_user.py`, Chapitre 9). `register_vector(conn)` (module `pgvector.psycopg2`) est systématiquement appelé sur chaque connexion qui manipule des embeddings, condition nécessaire pour que psycopg2 sache sérialiser/désérialiser le type `vector` de PostgreSQL.

---

# 6. Extraction et structuration des compétences (CV & offres)

## 6.1 Parsing des CV avec pdfplumber

Le candidat dépose un fichier PDF ou DOCX (`frontend/back_service/cv_parser.py`). Pour un PDF, `pdfplumber` extrait le texte page par page (`page.extract_text()`), les pages étant concaténées avec un saut de ligne ; pour un DOCX, `python-docx` (`Document`) parcourt les paragraphes non vides. `extract_cv_text()` orchestre ce choix selon l'extension du fichier et lève une `ValueError` explicite si le format n'est pas supporté, ou si aucun texte n'a pu être extrait — cas typique d'un PDF scanné (image) sans couche de texte, non géré par cette version du projet (pas d'OCR).

## 6.2 Extraction des compétences depuis les offres d'emploi

Contrairement à une lecture directe du champ `competences` renvoyé par l'API France Travail (dont le vocabulaire est hétérogène et ne correspond pas nécessairement à un référentiel exploitable pour un matching), les compétences finalement stockées en base sont **re-extraites depuis le texte de la description** de l'offre, au moment du chargement (`clean_competences()` dans `scripts/load_to_postgres.py`, qui appelle `extract_skills()` du référentiel partagé — voir 6.3 et Chapitre 3 §2.2.4). Ce choix garantit que les compétences des offres et celles détectées dans les CV sont exprimées avec exactement le même vocabulaire, condition nécessaire à une comparaison ensembliste fiable (Chapitre 7).

## 6.3 Normalisation et nettoyage des données de compétences

Le référentiel partagé (`scripts/skills_reference.py`) couvre **96 compétences uniques**, réparties en 8 catégories : langages backend, langages frontend, bases de données (« Data Stores »), cloud & infrastructure, data engineering, IA/ML, no-code, méthodologies & outils. La fonction `extract_skills(text)` détecte, dans un texte libre (CV ou description d'offre), les compétences connues, et retourne une liste dédupliquée et capitalisée pour l'affichage.

La détection utilise une expression régulière à frontières personnalisées plutôt qu'une simple recherche de sous-chaîne ou `\b...\b` classique, pour trois raisons concrètes rencontrées en pratique sur des textes français réels :

- Des mots-clés courts comme `go` donneraient de faux positifs sur n'importe quel texte contenant ces lettres (ex. dans « al**go**rithme ») avec une recherche naïve.
- `\b` seul ne suffit pas pour des compétences finissant par un symbole (`c++`, `c#`, `.net`) : il n'existe pas de frontière de mot entre deux caractères non-alphanumériques, donc un motif `\bc\+\+\b` ne matche jamais. Le référentiel utilise donc `(?<!\w)...(?!\w)` à la place.
- Les descriptions d'offres contiennent de nombreuses lettres accentuées (« goût », « référent »...). Utiliser `\w` (Unicode par défaut en Python 3) plutôt que `[a-z0-9]` évite qu'un mot comme « goût » soit vu à tort comme « go » + frontière + « ût », ce qui aurait fait matcher `go` par erreur. Le caractère `&`, fréquent dans les sigles français (« R&D »), est également traité comme une frontière invalide pour la même raison.

---

# 7. Machine Learning : matching sémantique et skill-gap

## 7.1 Préparation des données textuelles (CV et offres)

Côté offres, le texte encodé est la `description` complète stockée en base (Chapitre 5). Côté CV, c'est le texte intégral extrait par `cv_parser.py` (Chapitre 6). Aucune étape de nettoyage supplémentaire (suppression de stop-words, lemmatisation) n'est appliquée avant l'encodage : le modèle d'embeddings retenu (§7.2) est un modèle de phrases pré-entraîné, conçu pour être robuste à du texte brut plutôt que d'exiger un prétraitement classique de type bag-of-words.

## 7.2 Génération des embeddings et similarité vectorielle (pgvector)

Le modèle `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` encode chaque texte en un vecteur de 384 dimensions. Il est chargé une seule fois par processus (`get_model()`, singleton paresseux) plutôt que rechargé à chaque appel, ce modèle pesant plusieurs centaines de Mo. C'est un modèle multilingue, adapté au français, suffisamment léger pour tourner sans GPU dédié — un choix fait au profit de la simplicité opérationnelle plutôt que de la performance maximale d'un modèle plus lourd.

Le cœur du matching (`scripts/matching_cv.py`, fonction `find_best_matches`) encode le texte du CV, puis délègue la recherche de similarité directement à PostgreSQL via l'opérateur de distance cosinus de `pgvector` :

```sql
SELECT titre, company, ..., 1 - (embedding <=> %s::vector) AS similarity_score
FROM offres_emploi
WHERE date_du_poste >= NOW() - INTERVAL '30 days'
  AND embedding IS NOT NULL
ORDER BY similarity_score DESC
LIMIT %s;
```

Seules les offres publiées dans les 30 derniers jours sont considérées, pour garantir la pertinence du résultat par rapport au marché réel du moment (une offre plus ancienne est susceptible d'être déjà pourvue).

## 7.3 Formule de matching

Le score de correspondance affiché au candidat (« Meilleure correspondance », Chapitre 9) est **uniquement** la similarité cosinus entre le vecteur du CV et celui de l'offre (`1 - (embedding <=> cv_vector)`), ramenée en pourcentage. SkillGap AI n'implémente pas, dans sa version actuelle, une formule de matching hybride pondérant explicitement une composante de similarité vectorielle et une composante de couverture de compétences (par exemple 60 % / 40 %) : ce n'est pas le calcul réellement effectué par `find_best_matches()`.

La comparaison de compétences (`matched_skills` / `missing_skills`, §7.4) est calculée **en parallèle** du score, sur les mêmes offres retournées, mais n'entre à aucun moment dans le calcul du score affiché — elle sert exclusivement à l'affichage du détail par offre et à la priorisation des recommandations. Une évolution vers une formule hybride, combinant explicitement le score sémantique et un taux de couverture de compétences pondéré (par exemple pour réduire l'écart entre deux offres à similarité proche mais couverture de compétences très différente), est une piste d'amélioration identifiée mais non implémentée à ce stade — elle est reprise en conclusion.

## 7.4 Calcul du skill-gap et classification (compétences acquises / manquantes)

Pour chaque offre retournée par la recherche vectorielle, les compétences détectées dans le CV (`cv_skills`, un `set()`) sont comparées ensemblistement à celles de l'offre (`offer_skills`, issues de la colonne `competences`), produisant deux listes distinctes par offre :

```python
matched_skills = [s for s in offer_skills if s in cv_skills]
missing_skills = [s for s in offer_skills if s not in cv_skills]
```

C'est cette classification, offre par offre, qui alimente l'affichage des étiquettes de compétences colorées sur chaque carte d'offre (Chapitre 9).

## 7.5 Score d'impact et priorisation (« What to learn first »)

La fonction `rank_missing_skills()` agrège les écarts de compétences sur l'ensemble des offres matchées, en comptant chaque compétence **une seule fois par offre** (`set(offre["missing_skills"])`), pour ne pas gonfler artificiellement le score d'une compétence répétée plusieurs fois dans une même description. Le résultat est un classement par fréquence : « cette compétence manque dans X % des offres correspondant à votre profil ».

Ce classement alimente directement deux endroits de l'interface (Chapitre 9) :

- la tuile « Compétence à acquérir en priorité » sur la page Matching (le premier élément du classement) ;
- le bloc « Quoi apprendre en priorité », qui affiche les trois compétences manquantes les plus fréquentes, chacune accompagnée d'un score d'impact indicatif (« points de correspondance estimés »), calculé comme `max(1, round(pct / 5))` — une estimation illustrative de l'effet potentiel sur le score global, et non une simulation exacte recalculée en ré-encodant le CV sans cette compétence, ce qui serait coûteux à faire à chaque affichage.

`get_profile_summary()` centralise ces mêmes calculs (score du meilleur match, nombre d'offres compatibles à ≥ 70 %, compétences manquantes prioritaires) dans une seule fonction réutilisable, pour que les tuiles KPI de la page Matching et le contexte transmis à l'assistant IA (Chapitre 8) restent rigoureusement cohérents entre eux plutôt que recalculés séparément à deux endroits du code.

---

# 8. Intégration de l'intelligence artificielle générative (Mistral)

C'est la partie du projet qui distingue le plus nettement SkillGap AI d'un simple moteur de matching : transformer un écart de compétences détecté en un chemin d'action concret, sans jamais sacrifier la fiabilité de l'information au profit de la fluidité de l'IA générative.

## 8.1 Choix du fournisseur LLM et comparatif

Le choix du fournisseur (Mistral, comparé à Gemini, Groq, OpenRouter et Ollama) est détaillé au Chapitre 2 (§2.3.6) pour éviter la redondance ; il n'est que rappelé ici : Mistral a été retenu pour son adéquation au français, une politique de confidentialité plus simple à désactiver sur le tier gratuit, et un SDK déjà intégré au projet.

## 8.2 Le client Mistral partagé

Contrairement à une architecture multi-fournisseurs pensée dès le départ, l'appel au LLM ne passe pas par un wrapper générique de type `call_llm(provider, ...)` agnostique du fournisseur : il n'existe qu'un point d'accès partagé, `get_client()` dans `frontend/back_service/mistral_client.py`, qui instancie un client Mistral singleton (paresseux, réutilisé par tous les back-services) à partir de la variable d'environnement `MISTRAL_API_KEY`, et retourne `None` si cette clé est absente — chaque appelant devant alors dégrader proprement (masquer la fonctionnalité IA plutôt que planter l'application) au lieu de laisser une exception remonter jusqu'à l'utilisateur.

Chaque service consomme ce client directement pour son propre besoin :

- `cv_parser.extract_target_role()` — extraction factuelle du poste visé, avec consigne explicite de ne rien inventer si l'information n'est pas présente dans le texte.
- `recommendation_service.get_skill_advice()` — génération de conseils et de projets pratiques (§8.3).
- `chat_service.stream_chat_reply()` — conversation en streaming, ancrée sur le profil du candidat (§8.3).

Un principe de conception a guidé tout ce chapitre : **un LLM ne doit jamais être la source d'un fait vérifiable qu'il pourrait halluciner.** Demander à un modèle de langage de nommer une formation réelle l'expose à inventer un cours, un organisme ou un lien qui n'existent pas — un risque inacceptable pour un outil censé accompagner un vrai parcours professionnel.

Le catalogue de formations (`scripts/training_catalog.py`) a donc été construit à l'inverse de tout appel au LLM pour ce besoin précis : une entrée par compétence, curée manuellement, avec un lien **vérifié individuellement en HTTP (code 200)** avant intégration. Le catalogue couvre l'intégralité des 96 compétences du référentiel, avec un filet de sécurité générique (une recherche sur une plateforme de formation stable) pour toute compétence qui ne serait pas encore couverte si le référentiel venait à s'étendre.

## 8.3 Génération des recommandations personnalisées (mini-missions pratiques)

À l'inverse du nom d'une formation, suggérer une idée de projet pour pratiquer une compétence est un contenu **génératif**, sans « bonne réponse » factuelle à inventer — c'est le cas d'usage confié à Mistral (`get_skill_advice()`). Pour chaque compétence manquante, le modèle (`mistral-small-latest`, appelé avec `response_format={"type": "json_object"}` pour garantir une sortie structurée) produit un conseil court et un projet structuré (titre, 2 à 3 étapes concrètes, livrable attendu), avec une consigne explicite lui interdisant d'inventer des détails vérifiables (nom précis d'un jeu de données, URL, version d'un outil) — il doit rester général plutôt que de fabriquer une fausse précision. Seuls les **labels** de compétences manquantes sont envoyés dans le prompt, jamais le texte du CV.

L'assistant conversationnel (`chat_service.stream_chat_reply()`, page `frontend/views/assistant_ia.py`) permet au candidat de poser des questions libres sur son profil, ses compétences ou le marché de l'emploi, avec une réponse **streamée** token par token (générateur Python consommé par l'interface Streamlit). Il est délibérément **cadré, sans être restreint** : le prompt système l'oriente vers les sujets carrière/compétences/emploi tout en le laissant répondre à des questions plus générales, plutôt que de les refuser systématiquement. Son originalité tient à l'ancrage sur les données réelles du candidat : score de correspondance, compétences manquantes les plus fréquentes, et intitulé du poste visé — ce dernier étant lui-même extrait automatiquement du texte du CV. Le panneau « Contexte utilisé », visible à l'écran, rend cet ancrage transparent pour l'utilisateur plutôt que de le laisser deviner sur quelles données l'assistant s'appuie.

## 8.4 Stratégie de cache pour l'optimisation des coûts API

Comme détaillé au Chapitre 3 (§3.5), l'optimisation des coûts d'appel API repose sur `@st.cache_data(ttl=600, show_spinner=False)` appliqué à `_cached_skill_advice()` : pour un même tuple ordonné de compétences manquantes, Mistral n'est interrogé qu'une fois par tranche de 10 minutes, quel que soit le nombre de fois où le candidat revisite la page Recommandations dans cet intervalle. L'historique de conversation de l'assistant IA, lui, n'est volontairement pas mis en cache (chaque message doit produire une réponse fraîche) et ne persiste que le temps de la session (`st.session_state.chat_messages`), réinitialisé à chaque nouveau matching.

---

# 9. Développement de l'interface utilisateur (Streamlit)

## 9.1 Structure générale de l'application

`frontend/app.py` est le point d'entrée unique de l'application. Il initialise l'état de session (`page`, `logged_in`, `matching_done`, `dark_mode`), initialise la base de données au premier démarrage du processus (`init_db_once()`, mis en cache via `@st.cache_resource` pour ne s'exécuter qu'une fois), puis délègue l'affichage à `show_page()`, une fonction de routage centralisée (voir §9.4). Les modules de style, de services métier et de vues sont explicitement rechargés (`importlib.reload(...)`) à chaque exécution, pour que le rechargement à chaud de Streamlit en développement (`fileWatcherType=poll`) prenne en compte les modifications de code sans redémarrer le conteneur.

## 9.2 Page d'analyse et résultats

La page **Matching** (`frontend/views/matching.py`) est le point d'entrée du parcours candidat : une zone de dépôt (glisser-déposer PDF/DOCX, avec une option avancée de collage de texte pour les tests), puis, après analyse, un bloc de résultats composé de tuiles KPI — score de meilleure correspondance affiché sous forme d'anneau de progression SVG, nombre d'offres compatibles (score ≥ 70 %), et compétence à acquérir en priorité. Chaque offre affichée porte des **étiquettes de compétences colorées** (`render_skill_pills()`, Chapitre 7) : vert pour une compétence déjà maîtrisée, rouge pour une compétence manquante — un score d'alignement qualitatif immédiatement lisible sans devoir lire le détail texte de l'offre. Le bloc « Quoi apprendre en priorité » (§7.5) referme la boucle vers une formation vérifiée pour chacune des trois compétences les plus déterminantes.

![Dépôt du CV](figures/fig_matching_depot.png)
*Figure 9.1 — Dépôt du CV sur la page Matching*

![Résultat du matching](figures/fig_matching_resultats.png)
*Figure 9.2 — Résultat d'analyse du matching CV*

La page **Offres trouvées** (`frontend/views/offres.py`) liste, de façon paginée, les offres correspondant au profil du candidat, accessible uniquement après qu'un matching a été effectué (un écran d'invitation s'affiche sinon). Chaque offre y reprend le même système d'étiquettes colorées.

![Page Offres trouvées](figures/fig_offres.png)
*Figure 9.3 — Page Offres trouvées*

## 9.3 Page Tendances (KPIs marché : compétences demandées, distribution des scores, évolution temporelle)

Indépendante du profil du candidat, la page **Tendances** (`frontend/views/tendences.py`, logique agrégée dans `frontend/back_service/market_stats.py`) balaie l'ensemble des offres en base pour donner une vision du marché : compétences les plus demandées (top 8, via `Counter` sur la colonne `competences`), types de contrats les plus fréquents (regroupement des contrats au-delà du top 4 sous « Autres » pour rester lisible sur un diagramme), répartition par secteur d'activité, évolution du nombre d'offres publiées dans le temps, fourchettes salariales par métier (le métier recherché n'étant pas conservé tel quel en base, il est reconstitué à la volée par mots-clés sur le titre — `_classify_metier()`), et répartition géographique (ville, reconstruite par nettoyage du champ localisation brut de l'API — `_clean_city()`, qui fusionne arrondissements et numéros de département sous le nom de ville). Les graphiques sont produits avec **Altair**. Cette page est mise en cache 10 minutes (§3.5) pour éviter de rebalayer toute la table à chaque interaction.

![Page Tendances du marché](figures/fig_tendances.png)
*Figure 9.4 — Page Tendances du marché*

## 9.4 Page Recommandations et routage via st.session_state

La navigation entre les pages ne repose pas sur un mécanisme de routage HTTP classique (Streamlit ne fournit pas d'URL par page dans cette architecture single-page) : elle repose entièrement sur `st.session_state.page`, une chaîne de caractères (`'accueil'`, `'login'`, `'signup'`, `'matching'`, `'offres'`, `'tendences'`, `'recommendation'`, `'assistant_ia'`) lue par la fonction `show_page()` de `app.py`, qui affiche la vue correspondante et appelle `st.rerun()` après chaque changement pour forcer un nouveau rendu immédiat. Chaque bouton de navigation de l'application (ex. « Voir les recommandations » sur la page Matching) se contente de modifier cette variable de session puis de déclencher un nouveau rendu, plutôt que de naviguer vers une nouvelle URL.

La page **Recommandations** (`frontend/views/recommendation.py`) applique ce même principe d'accès conditionnel qu'Offres trouvées : elle n'est utile qu'après un matching, et affiche, pour chaque compétence manquante prioritaire (plafonnées à `MAX_SKILLS`), la formation vérifiée correspondante (§8.2) ainsi que le conseil et le projet pratique générés par Mistral (§8.3), mis en cache (§8.4).

![Page Recommandations](figures/fig_recommandations.png)
*Figure 9.5 — Page Recommandations de formations*

![Assistant IA](figures/fig_assistant_ia.png)
*Figure 9.6 — Assistant IA conversationnel*

## 9.5 Authentification et gestion des utilisateurs

Les écrans de connexion et d'inscription (`frontend/views/authentification.py`) valident le format de l'e-mail côté client avant tout appel serveur (`is_valid_email()`), affichent des messages d'erreur explicites et distincts selon la cause (email invalide, email déjà utilisé, identifiants incorrects, erreur serveur) plutôt qu'un message générique, et redirigent vers le tableau de bord (`st.session_state.page = 'dashboard'` puis Matching par défaut) après succès. Le bouton « Mot de passe oublié ? » affiche aujourd'hui une confirmation de type `st.toast(...)` sans déclencher d'envoi réel — une limite documentée au Chapitre 11 et en conclusion plutôt que dissimulée. Le bouton « Continuer avec Google » est également un bouton non fonctionnel à ce stade (pas d'intégration OAuth réelle) — une extension identifiée en conclusion.

---

# 10. Automatisation avec Airflow

## 10.1 Configuration du DAG de collecte et transformation

### 10.1.1 Paramètres généraux

Chaque DAG est défini avec des `default_args` communs — un propriétaire (`owner`), une politique de nouvelle tentative (`retries: 1`, `retry_delay` de 2 à 5 minutes selon le DAG) — et `catchup=False`, pour ne pas déclencher rétroactivement d'exécutions manquées entre la `start_date` déclarée et aujourd'hui.

### 10.1.2 Définition des tâches

- `ingestion_dags` — une tâche unique, `run_france_travail_collecte`, qui exécute `scripts.recup_france_travail.run_collecte`.
- `transformation_silver_dag` — une tâche unique, `run_transformation_silver`, qui exécute `scripts.transform_datafr.transform_and_save_all`.
- `dag_load_to_gold` — deux tâches séquentielles : `load_silver_to_postgres` (`scripts.load_to_postgres.load_silver_to_gold`) puis `vectorize_offres` (`scripts.vectorisateur_data.vectorize_missing_offers`).
- `master_pipeline_full_workflow` — l'orchestrateur : trois `TriggerDagRunOperator` (un par DAG ci-dessus, avec `wait_for_completion=True` et `allowed_states=['success']`, donc en échec si le DAG déclenché échoue), suivis d'un `PostgresOperator` qui recrée l'index HNSW.

### 10.1.3 Dépendances des tâches

Au sein de `dag_load_to_gold` : `load_task >> task_vectorize` (la vectorisation ne peut démarrer qu'une fois le chargement terminé, puisqu'elle a besoin des lignes déjà présentes en base). Au sein du DAG orchestrateur : `trigger_scrapping >> trigger_ingestion >> trigger_vectorization >> create_index_task`, une chaîne strictement séquentielle où chaque étape attend le succès complet de la précédente avant de démarrer.

## 10.2 Visualisation du DAG

Le DAG `master_pipeline_full_workflow` s'exécute quotidiennement (`schedule_interval='@daily'`) et déclenche les trois DAGs précédents en séquence stricte, avant de (re)créer, si besoin, l'index de similarité cosinus HNSW sur la colonne `embedding` — une opération idempotente (`CREATE INDEX IF NOT EXISTS`) rejouée chaque jour à coût nul une fois l'index déjà en place. L'interface web Airflow (accessible sur le port 8080) permet de visualiser ce graphe de dépendances, le statut de chaque exécution, sa durée, et les logs détaillés par tâche.

## 10.3 Avantages de l'automatisation pour le projet

L'automatisation garantit que la base reste alimentée sans intervention manuelle quotidienne, avec une traçabilité complète des exécutions. Les exécutions observées sur la période du projet montrent un pipeline globalement fiable, avec un taux d'échec ponctuel normal pour un système dépendant d'une API tierce externe.

Une limite assumée : le pipeline ne gère pas la suppression des offres devenues obsolètes côté source — une offre n'est mise à jour que si elle réapparaît dans une collecte, jamais explicitement retirée si elle disparaît de l'API. C'est pour cette raison que le moteur de matching (Chapitre 7) filtre systématiquement sur une fenêtre de 30 jours plutôt que de faire confiance à l'intégralité de la table.

---

# 11. Difficultés rencontrées et solutions

## 11.1 Problèmes de réseau Docker (service name vs localhost)

Une source récurrente d'erreurs de connexion en développement a été la confusion entre l'adresse réseau à utiliser depuis l'intérieur d'un conteneur Docker et celle utilisée depuis la machine hôte. Une connexion PostgreSQL ou MinIO codée avec `localhost` fonctionne lorsqu'un script est exécuté directement sur la machine de développement, mais échoue systématiquement une fois exécuté à l'intérieur d'un conteneur Airflow ou Streamlit, où `localhost` désigne le conteneur lui-même et non le service voisin. La solution retenue a été d'utiliser systématiquement les **noms de service Docker Compose** (`postgres`, `job_minio:9000`) comme nom d'hôte dans la configuration de connexion utilisée en conteneur — Docker Compose résolvant ces noms via son réseau interne — tout en conservant, en commentaire dans le code (`scripts/matching_cv.py`), l'alternative `localhost` pour un usage hors conteneur ponctuel.

## 11.2 Confusion environnement d'exécution (local vs conteneurisé)

Dans le prolongement de la difficulté précédente, plusieurs scripts (`scripts/matching_cv.py`, `scripts/vectorisateur_data.py`) ont dû être écrits pour pouvoir être importés à la fois depuis le processus Streamlit (monté en volume, `PYTHONPATH=/app:/pylibs`) et depuis les conteneurs Airflow (montés séparément dans `/opt/airflow/scripts`, avec un ajout explicite de chemin en tête de chaque fichier de DAG : `sys.path.insert(0, os.path.abspath(...))`). Cette double contrainte a nécessité de garder les imports relatifs au paquet `scripts` cohérents entre les deux contextes d'exécution, plutôt que de dupliquer la logique métier dans chaque environnement.

## 11.3 Robustesse du traitement des données JSON

Comme détaillé au Chapitre 4 (§4.2.2), l'hétérogénéité de la réponse JSON de l'API France Travail (champs absents, valeurs `null`, structures imbriquées incomplètes selon les offres) a nécessité de remplacer les accès directs (`item['libelle']`) par des accès défensifs (`isinstance()` + `.get()` avec valeurs de repli), après plusieurs interruptions de traitement de lot causées par une seule offre atypique au milieu de centaines d'offres valides.

## 11.4 Choix techniques revus (ex : abandon SMTP, simplification)

Plusieurs choix techniques initialement envisagés ont été révisés en cours de projet, par souci de proportion entre l'effort d'implémentation et la valeur apportée à ce stade :

- **Envoi d'e-mail transactionnel (vérification de compte, réinitialisation de mot de passe) via SMTP** — envisagé, puis abandonné au profit d'une validation du seul format de l'e-mail (`is_valid_email()`) et d'une confirmation d'interface sans envoi réel (`st.toast`, Chapitre 9 §9.5), pour rester concentré sur les fonctionnalités cœur du produit (matching, skill-gap, recommandations) dans le temps imparti — une limite documentée plutôt que masquée.
- **Découplage API REST (FastAPI) / interface** — une ébauche a été commencée (`backend/`, Chapitre 2 §2.3.3) puis mise de côté au profit d'un accès direct de Streamlit à PostgreSQL, pour accélérer l'itération sur un projet porté par une seule personne.
- **Formule de matching hybride pondérée (similarité + couverture de compétences)** — envisagée dans la conception initiale, non implémentée dans la version actuelle du score (Chapitre 7 §7.3), au profit d'un score de similarité vectorielle seul, la comparaison de compétences restant un affichage parallèle plutôt qu'une composante du score.
- **Sources de données additionnelles par scraping (WTTJ, HelloWork, Adzuna)** — évaluées puis écartées avant implémentation (Chapitre 4 §4.1.2), au profit d'une source unique mais officielle et stable.

---

## Conclusion générale et perspectives

SkillGap AI répond à l'objectif initial du projet : transformer un CV en un diagnostic objectif de positionnement sur le marché de l'emploi data, puis en un plan d'action concret pour progresser. Le pipeline de collecte et de traitement des données est entièrement automatisé et orchestré par Airflow ; le moteur de matching s'appuie sur une comparaison sémantique réelle plutôt que sur une simple recherche par mots-clés ; les recommandations de formation reposent sur des ressources vérifiées plutôt que sur du contenu généré à l'aveugle ; et l'assistant conversationnel apporte un accompagnement personnalisé ancré sur les données réelles du candidat.

Le projet assume également, tout au long de ce rapport, ses limites actuelles : une seule source de données en production (choix justifié face aux protections anti-bot des alternatives évaluées — WTTJ, HelloWork, Adzuna), un score de matching fondé sur la seule similarité vectorielle plutôt que sur une formule hybride pondérée, un schéma de compétences dénormalisé plutôt que des tables `cv_skills`/`job_skills`/`matches` distinctes, une stratégie de cache applicative plutôt qu'une table `recommendations_cache` persistée, pas d'API REST active malgré une base de code préparée en ce sens, une couverture de tests encore partielle, et l'absence de supervision applicative en production.

**Perspectives d'évolution :**
- Étendre la couverture de tests automatisés et mettre en place une intégration continue.
- Ajouter une supervision applicative temps réel du pipeline et de l'application.
- Finaliser l'authentification (vérification d'e-mail réelle, réinitialisation de mot de passe fonctionnelle, droit à l'oubli conforme au RGPD).
- Persister l'historique des conversations de l'assistant IA et des analyses de matching (table `matches`) au-delà de la session en cours.
- Envisager l'ajout d'une seconde source de données officielle (API) pour diversifier le volume d'offres sans recourir au scraping.
- Explorer une formule de matching hybride pondérant explicitement similarité vectorielle et couverture de compétences.
- Réintroduire une couche API (FastAPI) découplée de l'interface, si un client mobile ou une intégration tierce devenait nécessaire.
- Explorer un système de retour utilisateur sur la pertinence des recommandations, pour ajuster le classement des écarts de compétences dans le temps.

---

## Bibliographie

*[À compléter avec les sources effectivement citées/consultées, au format imposé par votre école. Pistes à intégrer :]*

- Documentation officielle de l'API France Travail. https://francetravail.io/. Consulté en 2026.
- Documentation officielle de pgvector. https://github.com/pgvector/pgvector. Consulté en 2026.
- Documentation officielle de sentence-transformers. https://www.sbert.net/. Consulté en 2026.
- Documentation officielle d'Apache Airflow. https://airflow.apache.org/docs/. Consulté en 2026.
- Documentation officielle de Mistral AI. https://docs.mistral.ai/. Consulté en 2026.
- Documentation officielle de Streamlit. https://docs.streamlit.io/. Consulté en 2026.
- Documentation officielle de MinIO. https://min.io/docs/. Consulté en 2026.
- Règlement général sur la protection des données (RGPD) — Règlement (UE) 2016/679.
