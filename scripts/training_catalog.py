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

Chaque "lien" a été vérifié manuellement (HTTP 200) au moment de l'écriture —
le nom/organisme reflète la page réellement pointée par le lien, pas une
formation supposée mais non vérifiée.
"""

TRAINING_CATALOG = {
    "Sql": [
        {"nom": "SQL Tutorial", "organisme": "postgresqltutorial.com", "duree": "auto-formation",
         "lien": "https://www.postgresqltutorial.com/"},
    ],
    "Agile": [
        {"nom": "Agile Foundations", "organisme": "LinkedIn Learning", "duree": "2h",
         "lien": "https://www.linkedin.com/learning/agile-foundations"},
    ],
    "Python": [
        {"nom": "Découvrez le langage Python", "organisme": "OpenClassrooms", "duree": "15h",
         "lien": "https://openclassrooms.com/fr/courses/7168871-decouvrez-le-langage-python"},
    ],
    "Java": [
        {"nom": "Apprendre Java (dev.java)", "organisme": "Oracle / dev.java", "duree": "auto-formation",
         "lien": "https://dev.java/learn/"},
    ],
    "Ci/cd": [
        {"nom": "Comprendre l'intégration et le déploiement continus (CI/CD)", "organisme": "GitLab Docs", "duree": "auto-formation",
         "lien": "https://docs.gitlab.com/ee/ci/"},
    ],
    "Devops": [
        {"nom": "Formations DevOps", "organisme": "Coursera", "duree": "variable",
         "lien": "https://www.coursera.org/courses?query=devops"},
    ],
    "Git": [
        {"nom": "Pro Git (livre officiel gratuit)", "organisme": "Git-scm.com", "duree": "auto-formation",
         "lien": "https://git-scm.com/book/en/v2"},
    ],
    "Angular": [
        {"nom": "Tour of Heroes (tutoriel officiel)", "organisme": "Angular.dev", "duree": "auto-formation",
         "lien": "https://angular.dev/tutorials/first-app"},
    ],
    "Docker": [
        {"nom": "Docker — Get Started", "organisme": "Docker Docs", "duree": "auto-formation",
         "lien": "https://docs.docker.com/get-started/"},
    ],
    "Kubernetes": [
        {"nom": "Kubernetes Basics (tutoriel officiel)", "organisme": "Kubernetes.io", "duree": "auto-formation",
         "lien": "https://kubernetes.io/docs/tutorials/kubernetes-basics/"},
    ],
    "Gitlab": [
        {"nom": "Documentation GitLab", "organisme": "GitLab", "duree": "auto-formation",
         "lien": "https://docs.gitlab.com/"},
    ],
    "Azure": [
        {"nom": "Microsoft Azure Fundamentals (AZ-900)", "organisme": "Microsoft Learn", "duree": "10h",
         "lien": "https://learn.microsoft.com/en-us/credentials/certifications/azure-fundamentals/"},
    ],
    "Postgresql": [
        {"nom": "PostgreSQL Tutorial", "organisme": "postgresqltutorial.com", "duree": "auto-formation",
         "lien": "https://www.postgresqltutorial.com/"},
    ],
    "Aws": [
        {"nom": "AWS Cloud Practitioner Essentials", "organisme": "AWS", "duree": "6h",
         "lien": "https://aws.amazon.com/training/digital/aws-cloud-practitioner-essentials/"},
    ],
    "Scrum": [
        {"nom": "Le Guide Scrum (guide officiel)", "organisme": "ScrumGuides.org", "duree": "auto-formation",
         "lien": "https://www.scrumguides.org/scrum-guide.html"},
    ],
    "React": [
        {"nom": "Apprendre React (tutoriel officiel)", "organisme": "React.dev", "duree": "auto-formation",
         "lien": "https://react.dev/learn"},
    ],
    "Javascript": [
        {"nom": "JavaScript (guide du langage)", "organisme": "MDN Web Docs", "duree": "auto-formation",
         "lien": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide"},
    ],
    ".net": [
        {"nom": ".NET — Get Started", "organisme": "Microsoft Learn", "duree": "auto-formation",
         "lien": "https://dotnet.microsoft.com/en-us/learn"},
    ],
    "Power bi": [
        {"nom": "Power BI Fundamentals", "organisme": "Microsoft Learn", "duree": "8h",
         "lien": "https://learn.microsoft.com/en-us/training/powerplatform/power-bi/"},
    ],
    "Linux": [
        {"nom": "Introduction to Linux (LFS101x)", "organisme": "Linux Foundation / edX", "duree": "40h",
         "lien": "https://www.edx.org/learn/linux/the-linux-foundation-introduction-to-linux"},
    ],
    "C#": [
        {"nom": "C# Fundamentals", "organisme": "Microsoft Learn", "duree": "10h",
         "lien": "https://learn.microsoft.com/en-us/training/paths/csharp-first-steps/"},
    ],
    "Php": [
        {"nom": "PHP The Right Way", "organisme": "Communauté PHP", "duree": "auto-formation",
         "lien": "https://phptherightway.com/"},
    ],
    "Jenkins": [
        {"nom": "Jenkins Tutorials", "organisme": "Jenkins.io", "duree": "auto-formation",
         "lien": "https://www.jenkins.io/doc/tutorials/"},
    ],
    "Typescript": [
        {"nom": "TypeScript Handbook", "organisme": "TypeScriptLang.org", "duree": "auto-formation",
         "lien": "https://www.typescriptlang.org/docs/handbook/intro.html"},
    ],
    "Gcp": [
        {"nom": "Google Cloud — Formations et parcours", "organisme": "Google Cloud", "duree": "variable",
         "lien": "https://cloud.google.com/learn/training"},
    ],
}


def get_trainings_for_skill(skill):
    return TRAINING_CATALOG.get(skill, [])
