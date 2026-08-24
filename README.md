
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
pip install -r requirements.txt
pytest scripts/test_matching_helpers.py -v
```

## ✨ Fonctionnalités implémentées

- ✅ **Authentification :** Système de Signup/Login sécurisé relié à PostgreSQL.
- ✅ **Navigation :** Système de pages dynamique (Accueil, Dashboard, Matching).
- ✅ **Base de données :** Modèle relationnel `User` et `Offres d'emploi` opérationnel avec pgvector.
- ✅ **Conteneurisation :** Environnement de développement complet et stable.
- ✅ **Pipeline ETL (Airflow) :** Automatisation de la récupération des offres d'emploi (via API France Travail). Nettoyage et stockage automatisé dans MinIO et des vecteurs en Postgres/pgvector.
- ✅ **Matching CV :** Analyse sémantique du CV (embeddings + pgvector) contre les offres du marché, avec score de correspondance et détection des compétences manquantes par offre.
- ✅ **Recommandations de formations :** Catalogue de ~96 compétences (couverture complète du référentiel), chaque lien de formation vérifié manuellement plutôt que généré par IA — pour éviter les liens morts ou les formations inventées. Complété par un projet pratique généré par IA (titre, étapes, livrable) pour chaque compétence manquante.
- ✅ **Assistant IA (chatbot) :** Agent conversationnel (Mistral) ancré sur le profil réel du candidat (score, écarts de compétences, poste visé extrait automatiquement du CV) — sans jamais transmettre le CV brut aux services externes. Répond aussi aux questions générales sur la carrière et le marché de l'emploi.
- ✅ **Tendances du marché :** Compétences les plus demandées, fourchettes salariales, répartition géographique et sectorielle, calculés sur les données réelles en base.
- ✅ **Tests unitaires (pytest) :** Couverture de la logique de classement des écarts de compétences (`scripts/test_matching_helpers.py`).

## 🚧 Roadmap : Fonctionnalités à venir
*Objectifs pour la suite du projet :*

### Fait depuis la dernière mise à jour

- ~~Recommandations de formations~~ — fait : catalogue vérifié + génération de projets par IA.
- ~~Assistant de carrière (Chatbot IA)~~ — fait : conversationnel, ancré sur le profil, cadrage souple. Reste en mémoire de session uniquement (pas encore persisté en base pour reprendre une conversation après déconnexion).

### Priorité 1 — Produit coeur (à livrer en premier)

1. **Dashboard candidat & visualisations**

- Visualisations supplémentaires : radar skills, évolution du score dans le temps.

### Priorité 2 — Extensions/Bonus (phase 2)

2. **Amélioration UI/UX & Auth**

- Finaliser le thème sombre (quelques éléments — popover du menu profil notamment — restent en clair).
- Ajouter OAuth (Google) pour inscription/connexion rapide.

3. **Qualité & fiabilité**

- Étendre la couverture de tests unitaires au-delà de la logique de classement des écarts.
- CI (lancer les tests automatiquement sur chaque push).

4. **Monitoring & déploiement production**

- Logs centralisés, health checks, sauvegardes de la base.
- Déploiement CI/CD (ex : GitHub Actions, Render/Railway/VM/Kubernetes).

---

## 🌟 Valeur ajoutée (ce qui rend SkillGap unique)

- Matching basé sur l'analyse fine des CV (extraction de compétences) plutôt que sur mots-clés simples.
- Détection des "skill gaps" et recommandations de formations pratiques, reliées aux offres réelles du marché.
- Catalogue de formations vérifié manuellement (chaque lien testé) plutôt que généré par IA — évite les hallucinations sur des faits vérifiables (nom de cours, organisme).
- Assistant IA contextualisé sur le profil réel du candidat, sans jamais transmettre le CV brut aux services externes (confidentialité).
- Pipeline data-driven : Airflow + stockage MinIO + `pgvector` pour ré-entrainement / mise à jour régulière.
- Dashboard orienté coaching de carrière (parcours d'apprentissage, suivi d'évolution des compétences).

## 📝 Auteur

- **SOWAKOUDE Fidélia** - Projet de Fin d'Études (M2)