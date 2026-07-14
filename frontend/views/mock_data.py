"""Données factices pour les pages non encore reliées au backend (front seul)."""

SKILL_AXES = [
    {"name": "Python", "current": 82, "target": 75},
    {"name": "SQL", "current": 74, "target": 80},
    {"name": "Machine Learning", "current": 55, "target": 65},
    {"name": "Data Visualisation", "current": 68, "target": 70},
    {"name": "Statistiques", "current": 60, "target": 65},
    {"name": "Cloud (AWS/GCP)", "current": 32, "target": 55},
]


def get_mock_skill_gap():
    skills = []
    for axis in SKILL_AXES:
        gap = axis["target"] - axis["current"]
        if gap <= 0:
            status = "success"
        elif gap <= 15:
            status = "warning"
        else:
            status = "danger"
        skills.append({**axis, "gap": gap, "status": status})

    score = round(
        100 * sum(min(s["current"], s["target"]) / s["target"] for s in skills) / len(skills)
    )

    return {
        "skills": skills,
        "score": score,
        "acquired": [s["name"] for s in skills if s["status"] == "success"],
        "to_develop": [s for s in skills if s["status"] != "success"],
    }


MOCK_OFFERS = [
    {"titre": "Data Analyst", "entreprise": "Nova Insights", "ville": "Paris", "contrat": "CDI",
     "salaire": "38–45k€", "matching": 91},
    {"titre": "Analyste Business Intelligence", "entreprise": "Fluxo", "ville": "Lyon", "contrat": "CDI",
     "salaire": "36–42k€", "matching": 84},
    {"titre": "Data Analyst Junior", "entreprise": "Cartell", "ville": "Bordeaux", "contrat": "CDD",
     "salaire": "30–34k€", "matching": 78},
    {"titre": "Consultant Data / Reporting", "entreprise": "Kelio Group", "ville": "Nantes", "contrat": "Freelance",
     "salaire": "350–420€/j", "matching": 72},
    {"titre": "Data Analyst Marketing", "entreprise": "Verso Media", "ville": "Paris", "contrat": "CDI",
     "salaire": "37–43k€", "matching": 69},
]

MOCK_TRAININGS = [
    {"nom": "AWS Cloud Practitioner Essentials", "organisme": "AWS Skill Builder", "duree": "12h",
     "competence": "Cloud (AWS/GCP)"},
    {"nom": "Machine Learning Specialization", "organisme": "DeepLearning.AI", "duree": "3 semaines",
     "competence": "Machine Learning"},
    {"nom": "Statistiques appliquées à la data", "organisme": "OpenClassrooms", "duree": "20h",
     "competence": "Statistiques"},
    {"nom": "SQL avancé pour l'analyse de données", "organisme": "DataCamp", "duree": "8h",
     "competence": "SQL"},
]

MOCK_TOP_SKILLS = {"Python": 128, "SQL": 112, "Excel": 96, "Power BI": 74, "Machine Learning": 58, "AWS": 41}

MOCK_CONTRACT_TYPES = {"CDI": 62, "CDD": 18, "Freelance": 14, "Stage": 6}

MOCK_POSTINGS_OVER_TIME = {"Fév": 34, "Mars": 41, "Avr": 38, "Mai": 47, "Juin": 52, "Juil": 45}

MOCK_SALARY_RANGES = [
    {"metier": "Data Analyst", "min": 32, "max": 45},
    {"metier": "Data Scientist", "min": 42, "max": 58},
    {"metier": "Data Engineer", "min": 40, "max": 55},
    {"metier": "BI Analyst", "min": 34, "max": 46},
]

MOCK_CITY_DEMAND = [
    {"ville": "Paris", "offres": 214, "salaire_moyen": "42k€", "skills": ["Python", "SQL", "Power BI"]},
    {"ville": "Lyon", "offres": 68, "salaire_moyen": "38k€", "skills": ["SQL", "Excel", "Python"]},
    {"ville": "Nantes", "offres": 41, "salaire_moyen": "36k€", "skills": ["Power BI", "SQL"]},
    {"ville": "Bordeaux", "offres": 33, "salaire_moyen": "35k€", "skills": ["Python", "Excel"]},
    {"ville": "Toulouse", "offres": 29, "salaire_moyen": "37k€", "skills": ["SQL", "AWS"]},
    {"ville": "Lille", "offres": 22, "salaire_moyen": "35k€", "skills": ["Excel", "Power BI"]},
]
