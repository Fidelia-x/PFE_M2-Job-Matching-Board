"""Référentiel de compétences partagé entre le pipeline d'ingestion des offres
(scripts.load_to_postgres) et le matching CV (scripts.matching_cv), pour que
les deux côtés détectent les compétences avec exactement le même vocabulaire.
"""

import re

SKILL_CATEGORIES = {
    'Langages pour le Backend': [
        'python', 'java', 'scala', 'go', 'node.js', 'fastapi', 'flask', 'r',
        'kotlin', 'swift', 'rust', 'php', 'ruby', 'perl', 'c++', 'c#', '.net', 'asp.net',
    ],
    'Langages pour le Frontend': [
        'javascript', 'typescript', 'react', 'vue', 'html', 'css', 'angular', 'svelte',
        'next.js', 'tailwind', 'bootstrap', 'sass',
    ],
    'Data Stores': [
        'postgresql', 'mongodb', 'mysql', 'redis', 'elasticsearch', 'snowflake', 'oracle',
        'cassandra', 'dynamodb', 'bigquery', 'redshift', 'clickhouse',
    ],
    'Cloud & Infra': [
        'sql', 'aws', 'gcp', 'azure', 'docker', 'kubernetes', 'snowflake', 'terraform',
        'ansible', 'jenkins', 'linux', 'nginx', 'github actions', 'gitlab', 'ci/cd',
    ],
    'Data Engineering': ['dbt', 'airflow', 'spark', 'kafka', 'hadoop', 'databricks', 'talend', 'nifi'],
    'IA/ML': [
        'tensorflow', 'pytorch', 'scikit-learn', 'llm', 'rag', 'mlops', 'langchain',
        'keras', 'opencv', 'nlp', 'hugging face',
    ],
    'No-Code': [
        'airtable', 'make', 'bubble', 'power bi', 'zapier', 'tableau', 'metabase', 'webflow', 'excel', 'notion',
        'qlikview', 'spss', 'looker',
    ],
    'Méthodologies & outils': ['agile', 'scrum', 'devops', 'git', 'jira', 'confluence', 'salesforce', 'sap'],
}


def extract_skills(text):
    """Détecte, dans un texte libre (description d'offre ou texte de CV), les
    compétences connues de SKILL_CATEGORIES. Retourne une liste dédupliquée,
    capitalisée pour l'affichage.

    Utilise des frontières basées sur \\w plutôt qu'une simple recherche de
    sous-chaîne : des mots-clés courts comme 'go' donneraient sinon des faux
    positifs sur n'importe quel texte contenant ces lettres (ex. 'go' dans
    "algorithme"). \\b seul ne suffit pas non plus pour des compétences
    finissant par un symbole ('c++', 'c#', '.net') : il n'y a pas de
    frontière de mot entre deux caractères non-mot, donc \\bc\\+\\+\\b ne
    matche jamais. On utilise donc (?<!\\w)...(?!\\w) à la place.

    \\w (pas [a-z0-9]) est important : les textes de description contiennent
    beaucoup de lettres accentuées ('goût', 'référent'...), qui ne sont pas
    dans [a-z0-9] mais font bien partie du mot. Avec [a-z0-9], "goût" était
    vu comme "go" + frontière + "ût", et 'go' matchait à tort. \\w (Unicode
    par défaut en Python 3) reconnaît correctement les lettres accentuées
    comme faisant partie du mot.

    Le '&' est aussi traité comme une frontière invalide : des sigles très
    courants dans les offres françaises ('R&D') collent un '&' directement
    au mot-clé sans espace, ce qui ferait matcher 'r' isolé sinon.
    """
    text = str(text).lower()
    found = []
    for skills in SKILL_CATEGORIES.values():
        for skill in skills:
            label = skill.capitalize()
            if label in found:
                continue
            pattern = r"(?<![\w&])" + re.escape(skill) + r"(?![\w&])"
            if re.search(pattern, text):
                found.append(label)
    return found
