"""Catalogue de formations curé manuellement, indexé par compétence (mêmes
labels que scripts.skills_reference.SKILL_CATEGORIES / extract_skills — ex.
"Sql", "Power bi", "Ci/cd", ".net"), utilisé par la page Recommandations pour
suggérer des ressources concrètes en fonction des écarts détectés lors du
matching CV.

Volontairement statique (pas de génération par LLM) : le nom exact d'une
formation, son organisme et sa durée sont des faits vérifiables, pas du
contenu créatif — un LLM peut halluciner un cours qui n'existe pas. Priorisé
sur les compétences les plus fréquentes dans offres_emploi (requête faite au
lancement du projet) plutôt que sur l'intégralité du référentiel.
"""

TRAINING_CATALOG = {
    "Sql": [
        {"nom": "Utilisez SQL avec MySQL", "organisme": "OpenClassrooms", "duree": "15h"},
    ],
    "Agile": [
        {"nom": "Les fondamentaux de l'agilité", "organisme": "LinkedIn Learning", "duree": "2h"},
    ],
    "Python": [
        {"nom": "Découvrez le langage Python", "organisme": "OpenClassrooms", "duree": "15h"},
    ],
    "Java": [
        {"nom": "Apprenez à programmer en Java", "organisme": "OpenClassrooms", "duree": "20h"},
    ],
    "Ci/cd": [
        {"nom": "Comprendre l'intégration et le déploiement continus (CI/CD)", "organisme": "GitLab Docs", "duree": "auto-formation"},
    ],
    "Devops": [
        {"nom": "DevOps Culture and Mindset", "organisme": "Coursera (UC Davis)", "duree": "10h"},
    ],
    "Git": [
        {"nom": "Pro Git (livre officiel gratuit)", "organisme": "Git-scm.com", "duree": "auto-formation"},
    ],
    "Angular": [
        {"nom": "Tour of Heroes (tutoriel officiel)", "organisme": "Angular.dev", "duree": "auto-formation"},
    ],
    "Docker": [
        {"nom": "Docker for Beginners", "organisme": "Docker Docs", "duree": "auto-formation"},
    ],
    "Kubernetes": [
        {"nom": "Kubernetes Basics (tutoriel officiel)", "organisme": "Kubernetes.io", "duree": "auto-formation"},
    ],
    "Gitlab": [
        {"nom": "GitLab Learn", "organisme": "GitLab Docs", "duree": "auto-formation"},
    ],
    "Azure": [
        {"nom": "Microsoft Azure Fundamentals (AZ-900)", "organisme": "Microsoft Learn", "duree": "10h"},
    ],
    "Postgresql": [
        {"nom": "PostgreSQL Tutorial", "organisme": "postgresqltutorial.com", "duree": "auto-formation"},
    ],
    "Aws": [
        {"nom": "AWS Cloud Practitioner Essentials", "organisme": "AWS Skill Builder", "duree": "6h"},
    ],
    "Scrum": [
        {"nom": "Professional Scrum Master I (PSM I) — préparation", "organisme": "Scrum.org", "duree": "auto-formation"},
    ],
    "React": [
        {"nom": "Apprendre React (tutoriel officiel)", "organisme": "React.dev", "duree": "auto-formation"},
    ],
    "Javascript": [
        {"nom": "JavaScript (guide du langage)", "organisme": "MDN Web Docs", "duree": "auto-formation"},
    ],
    ".net": [
        {"nom": ".NET — Get Started", "organisme": "Microsoft Learn", "duree": "auto-formation"},
    ],
    "Power bi": [
        {"nom": "Power BI Fundamentals", "organisme": "Microsoft Learn", "duree": "8h"},
    ],
    "Linux": [
        {"nom": "Introduction to Linux (LFS101x)", "organisme": "Linux Foundation / edX", "duree": "40h"},
    ],
    "C#": [
        {"nom": "C# Fundamentals", "organisme": "Microsoft Learn", "duree": "10h"},
    ],
    "Php": [
        {"nom": "PHP The Right Way", "organisme": "Communauté PHP", "duree": "auto-formation"},
    ],
    "Jenkins": [
        {"nom": "Jenkins Tutorials", "organisme": "Jenkins.io", "duree": "auto-formation"},
    ],
    "Typescript": [
        {"nom": "TypeScript Handbook", "organisme": "TypeScriptLang.org", "duree": "auto-formation"},
    ],
    "Gcp": [
        {"nom": "Google Cloud Digital Leader", "organisme": "Google Cloud Skills Boost", "duree": "10h"},
    ],
}


def get_trainings_for_skill(skill):
    return TRAINING_CATALOG.get(skill, [])
