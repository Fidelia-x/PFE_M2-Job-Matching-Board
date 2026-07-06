
# Projet de fin d'etude: SkillGap (Job Matching Board)

Ce projet est une plateforme de **Job Matching** basée sur l'intelligence artificielle. Elle permet aux candidats d'analyser leurs CV, d'identifier leurs lacunes en compétences par rapport au marché du travail et de trouver les offres qui leur correspondent le mieux.

## 🛠 Architecture Technique
Le projet repose sur une architecture conteneurisée avec **Docker** :

- **Frontend :** Streamlit (Interface interactive).
- **Backend :** Python (Gestion de la logique métier et authentification).
- **Base de données :** PostgreSQL avec l'extension **pgvector** (pour la recherche sémantique).
- **Stockage :** MinIO (Gestion des fichiers/CV).
- **Orchestration :** Apache Airflow (Pipelines de données).

## 📋 Prérequis

- Docker & Docker Compose
- Python 3.x

## 🔑 Variables d'environnement

Copiez le fichier `.env.example` en `.env` et ajustez les valeurs avant de démarrer les services :

- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` — accès PostgreSQL
- `MINIO_USER`, `MINIO_PASSWORD` — accès MinIO
- `CLIENT_ID`, `CLIENT_SECRET` — variables OAuth (si utilisées)

Un fichier d'exemple est fourni: `.env.example`.

## 🚀 Installation & Lancement

1. Clonez le projet :

```bash
git clone <git@github.com:Fidelia-x/PFE_M2-Job-Matching-Board.git>
cd PFE_M2-Job-Matching-Board
```
2. Lancez l'environnement complet :

```bash
docker-compose up -d
```
3. Accédez à l'interface : `http://localhost:8501`

### Commandes utiles & initialisation

Démarrer uniquement les services essentiels (rapide pour le dev) :

```bash
docker compose up -d postgres minio
docker compose up -d airflow-webserver airflow-scheduler
docker compose up -d fastapi streamlit
```

Consulter les logs d'un service :

```bash
docker compose logs -f airflow-webserver
docker compose logs -f job_streamlit
```

Exécuter les tests Python :

```bash
pip install -r backend/requirements.txt

```

## ✨ Fonctionnalités implémentées

- ✅ **Authentification :** Système de Signup/Login sécurisé relié à PostgreSQL.
- ✅ **Navigation :** Système de pages dynamique (Accueil, Dashboard, Matching).
- ✅ **Base de données :** Modèle relationnel `User` et `Offres d'emploi` opérationnel avec pgvector.
- ✅ **Conteneurisation :** Environnement de développement complet et stable.
- ✅ **Pipeline ETL (Airflow) :** Automatisation de la récupération des offres d'emploi (via API France Travail).Nettoyage et stockage automatisé dans MinIO et des vecteurs en Postgres/pgvector.

## 🚧 Roadmap : Fonctionnalités à venir
*Objectifs pour la suite du projet :*
### Priorité 1 — Produit coeur(à livrer en premier)

1. **Dashboard candidat & visualisations**

- Affichage du score de matching et détail compétences présentes / manquantes.
- Visualisations : radar skills, évolution des scores, répartition sectorielle.
- Interface pour consulter recommandations de formations.

2. **Recommandations de formations**

- Mapping des "skill gaps" vers cours/ressources (OpenClassrooms, Coursera, etc.).
- Génération de parcours d'apprentissage simples (3–6 étapes).

### Priorité 2 — Extensions/Bonus (phase 2)

3. **Assistant de carrière (Chatbot IA)**

- Agent conversationnel (LLM) pour réponses contextualisées et coaching.
- Stockage de l'historique des conversations pour personnalisation.

4. **Amélioration UI/UX & Auth**

- Finaliser le thème sombre et les illustrations.
- Ajouter OAuth (Google) pour inscription/connexion rapide.

5. **Monitoring & déploiement production**

- Logs centralisés, health checks, sauvegardes de la base.
- Déploiement CI/CD (ex : GitHub Actions, Render/Railway/VM/Kubernetes).

---

## 🌟 Valeur ajoutée (ce qui rend SkillGap unique)

- Matching basé sur l'analyse fine des CV (extraction de compétences) plutôt que sur mots-clés simples.
- Détection des "skill gaps" et recommandations de formations pratiques, reliées aux offres réelles du marché.
- Pipeline data-driven : Airflow + stockage MinIO + `pgvector` pour ré-entrainement / mise à jour régulière.
- Dashboard orienté coaching de carrière (parcours d'apprentissage, suivi d'évolution des compétences).

## 📝 Auteur

- **SOWAKOUDE Fidélia** - Projet de Fin d'Études (M2)