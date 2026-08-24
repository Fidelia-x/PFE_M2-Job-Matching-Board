import re
from collections import Counter
from datetime import datetime

import pandas as pd

from scripts.matching_cv import get_db_connection

_MONTHS_FR = ['Jan', 'Fév', 'Mars', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sept', 'Oct', 'Nov', 'Déc']

# Les offres sont collectées via des recherches par mots-clés (voir scripts.recup_france_travail.JOBS),
# mais le métier recherché n'est pas conservé en base : on le retrouve en repassant sur le titre.
_METIER_KEYWORDS = [
    ('Data Analyst', ['data analyst', 'analyste data']),
    ('Data Scientist', ['data scientist']),
    ('Data Engineer', ['data engineer']),
    ('MLOps', ['mlops']),
    ('ML Engineer', ['machine learning']),
    ('Développeur Python', ['python']),
]


def _load_offers():
    conn = get_db_connection()
    try:
        return pd.read_sql("""
            SELECT titre, contract, localisation, competences, salaire_min, salaire_max, date_du_poste, secteur_activite
            FROM offres_emploi
        """, conn)
    finally:
        conn.close()


def _classify_metier(titre):
    titre_lower = str(titre).lower()
    for label, keywords in _METIER_KEYWORDS:
        if any(kw in titre_lower for kw in keywords):
            return label
    return None


def _clean_city(localisation):
    """'75 - Paris 9e Arrondissement' -> 'Paris' (fusionne arrondissements et
    dépts sous le nom de ville pour l'agrégation)."""
    if not localisation:
        return None
    ville = re.sub(r'^\s*\d+\s*-\s*', '', str(localisation))
    ville = re.sub(r'\s+\d+\w*\s+Arrondissement$', '', ville, flags=re.IGNORECASE)
    return ville.strip() or None


def _top_skills(df, limit=8):
    counter = Counter()
    for skills in df['competences'].dropna():
        counter.update(skills)
    return dict(counter.most_common(limit))


def _contract_types(df, top_n=4):
    """Regroupe les types de contrats au-delà de top_n dans 'Autres' — sans ça,
    un diagramme à disques se retrouve avec des parts de 2-9 offres illisibles
    (ex. 'CDD Tremplin', 'CDD Insertion') à côté du CDI qui domine largement."""
    normalized = df['contract'].dropna().apply(lambda c: c.split(' - ')[0].strip())
    counts = normalized.value_counts()
    if len(counts) <= top_n:
        return counts.to_dict()
    result = counts.iloc[:top_n].to_dict()
    result['Autres'] = int(counts.iloc[top_n:].sum())
    return result


def _sector_distribution(df, top_n=8):
    """Secteur d'activité de l'entreprise (NAF, via l'API France Travail) —
    même repli top_n + 'Autres' que _contract_types, la longue traîne de
    secteurs à 1-2 offres serait illisible sinon."""
    sectors = df['secteur_activite'].dropna()
    sectors = sectors[sectors.str.strip() != '']
    if sectors.empty:
        return {}
    counts = sectors.value_counts()
    if len(counts) <= top_n:
        return counts.to_dict()
    result = counts.iloc[:top_n].to_dict()
    result['Autres'] = int(counts.iloc[top_n:].sum())
    return result


def _postings_over_time(df):
    """Nombre d'offres par mois de publication, depuis le 1er janvier de
    l'année en cours (les données remontent en fait à 2023, mais tout
    afficher noie le graphique et rend les tout premiers mois, avec très peu
    d'offres collectées, difficiles à comparer aux mois récents)."""
    dated = df.dropna(subset=['date_du_poste'])
    start_of_year = datetime(datetime.now().year, 1, 1)
    dated = dated[dated['date_du_poste'] >= start_of_year]
    grouped = dated.groupby(dated['date_du_poste'].dt.to_period('M')).size()
    return {f"{_MONTHS_FR[period.month - 1]} {period.year}": int(count) for period, count in grouped.items()}


def current_month_label():
    """Même format de clé que _postings_over_time, pour que la vue puisse
    repérer le dernier point du graphique quand c'est le mois en cours (donc
    un décompte partiel, pas comparable aux mois complets précédents)."""
    now = datetime.now()
    return f"{_MONTHS_FR[now.month - 1]} {now.year}"


def _salary_ranges_by_metier(df):
    salaried = df[(df['salaire_min'] > 0) & (df['salaire_max'] > 0)].copy()
    salaried['metier'] = salaried['titre'].apply(_classify_metier)
    salaried = salaried.dropna(subset=['metier'])
    if salaried.empty:
        return []
    grouped = salaried.groupby('metier').agg(mn=('salaire_min', 'mean'), mx=('salaire_max', 'mean'))
    ranges = [
        {"metier": metier, "min": round(row['mn'] / 1000), "max": round(row['mx'] / 1000)}
        for metier, row in grouped.iterrows()
    ]
    return sorted(ranges, key=lambda r: r['min'])


# Découpage administratif officiel (18 régions depuis 2016) : la BDD ne
# stocke pas la région, seule la localisation brute ("75 - Paris") — on la
# déduit du code département en préfixe.
_DEPARTMENT_TO_REGION = {
    '01': 'Auvergne-Rhône-Alpes', '03': 'Auvergne-Rhône-Alpes', '07': 'Auvergne-Rhône-Alpes',
    '15': 'Auvergne-Rhône-Alpes', '26': 'Auvergne-Rhône-Alpes', '38': 'Auvergne-Rhône-Alpes',
    '42': 'Auvergne-Rhône-Alpes', '43': 'Auvergne-Rhône-Alpes', '63': 'Auvergne-Rhône-Alpes',
    '69': 'Auvergne-Rhône-Alpes', '73': 'Auvergne-Rhône-Alpes', '74': 'Auvergne-Rhône-Alpes',
    '21': 'Bourgogne-Franche-Comté', '25': 'Bourgogne-Franche-Comté', '39': 'Bourgogne-Franche-Comté',
    '58': 'Bourgogne-Franche-Comté', '70': 'Bourgogne-Franche-Comté', '71': 'Bourgogne-Franche-Comté',
    '89': 'Bourgogne-Franche-Comté', '90': 'Bourgogne-Franche-Comté',
    '22': 'Bretagne', '29': 'Bretagne', '35': 'Bretagne', '56': 'Bretagne',
    '18': 'Centre-Val de Loire', '28': 'Centre-Val de Loire', '36': 'Centre-Val de Loire',
    '37': 'Centre-Val de Loire', '41': 'Centre-Val de Loire', '45': 'Centre-Val de Loire',
    '2A': 'Corse', '2B': 'Corse',
    '08': 'Grand Est', '10': 'Grand Est', '51': 'Grand Est', '52': 'Grand Est',
    '54': 'Grand Est', '55': 'Grand Est', '57': 'Grand Est', '67': 'Grand Est',
    '68': 'Grand Est', '88': 'Grand Est',
    '02': 'Hauts-de-France', '59': 'Hauts-de-France', '60': 'Hauts-de-France',
    '62': 'Hauts-de-France', '80': 'Hauts-de-France',
    '75': 'Île-de-France', '77': 'Île-de-France', '78': 'Île-de-France', '91': 'Île-de-France',
    '92': 'Île-de-France', '93': 'Île-de-France', '94': 'Île-de-France', '95': 'Île-de-France',
    '14': 'Normandie', '27': 'Normandie', '50': 'Normandie', '61': 'Normandie', '76': 'Normandie',
    '16': 'Nouvelle-Aquitaine', '17': 'Nouvelle-Aquitaine', '19': 'Nouvelle-Aquitaine',
    '23': 'Nouvelle-Aquitaine', '24': 'Nouvelle-Aquitaine', '33': 'Nouvelle-Aquitaine',
    '40': 'Nouvelle-Aquitaine', '47': 'Nouvelle-Aquitaine', '64': 'Nouvelle-Aquitaine',
    '79': 'Nouvelle-Aquitaine', '86': 'Nouvelle-Aquitaine', '87': 'Nouvelle-Aquitaine',
    '09': 'Occitanie', '11': 'Occitanie', '12': 'Occitanie', '30': 'Occitanie', '31': 'Occitanie',
    '32': 'Occitanie', '34': 'Occitanie', '46': 'Occitanie', '48': 'Occitanie', '65': 'Occitanie',
    '66': 'Occitanie', '81': 'Occitanie', '82': 'Occitanie',
    '44': 'Pays de la Loire', '49': 'Pays de la Loire', '53': 'Pays de la Loire',
    '72': 'Pays de la Loire', '85': 'Pays de la Loire',
    '04': "Provence-Alpes-Côte d'Azur", '05': "Provence-Alpes-Côte d'Azur",
    '06': "Provence-Alpes-Côte d'Azur", '13': "Provence-Alpes-Côte d'Azur",
    '83': "Provence-Alpes-Côte d'Azur", '84': "Provence-Alpes-Côte d'Azur",
    '971': 'Guadeloupe', '972': 'Martinique', '973': 'Guyane', '974': 'La Réunion', '976': 'Mayotte',
}
_DEPARTMENT_CODE_RE = re.compile(r'^\s*(2[AB]|\d{2,3})\s*-')


def _region_from_localisation(localisation):
    if not localisation:
        return None
    match = _DEPARTMENT_CODE_RE.match(str(localisation))
    if not match:
        return None
    return _DEPARTMENT_TO_REGION.get(match.group(1))


def _canonical_city_labels(ville_series):
    """Une partie des localisations sont en MAJUSCULES ('75 - PARIS') alors que
    la majorité est correctement casée ('75 - Paris') : sans regroupement,
    'Paris' et 'PARIS' sont comptés comme deux villes distinctes, ce qui dilue
    leurs offres. On regroupe par forme insensible à la casse et on garde la
    graphie la plus fréquente comme libellé affiché."""
    best_by_lower = {}
    for variant, count in ville_series.value_counts().items():
        key = variant.lower()
        if key not in best_by_lower or count > best_by_lower[key][1]:
            best_by_lower[key] = (variant, count)
    return ville_series.map(lambda v: best_by_lower[v.lower()][0])


def _with_clean_city(df):
    """Localisation nettoyée + regroupée (arrondissements et casse fusionnés
    sous un même nom de ville) — utilisé par _city_demand et
    _city_contract_distribution, qui ont besoin du même regroupement."""
    with_city = df.copy()
    with_city['ville'] = with_city['localisation'].apply(_clean_city)
    with_city = with_city.dropna(subset=['ville'])
    with_city['ville'] = _canonical_city_labels(with_city['ville'])
    return with_city[with_city['ville'] != 'France']


def _city_demand(df, limit=8):
    with_city = _with_clean_city(df)
    return with_city['ville'].value_counts().head(limit).to_dict()


def _region_demand(df, limit=12):
    regions = df['localisation'].apply(_region_from_localisation).dropna()
    if regions.empty:
        return {}
    return regions.value_counts().head(limit).to_dict()


def _city_contract_distribution(df, top_cities=6, top_contracts=4):
    """Croise ville x type de contrat sur les villes les plus actives, pour
    visualiser comment se répartissent CDI/CDD/... dans chacune (même repli
    top_n + 'Autres' que _contract_types, pour rester lisible)."""
    with_city = _with_clean_city(df)
    with_city = with_city.dropna(subset=['contract']).copy()
    with_city['contrat'] = with_city['contract'].apply(lambda c: c.split(' - ')[0].strip())

    top_villes = with_city['ville'].value_counts().head(top_cities).index
    scoped = with_city[with_city['ville'].isin(top_villes)].copy()
    if scoped.empty:
        return []

    contract_counts = scoped['contrat'].value_counts()
    if len(contract_counts) > top_contracts:
        keep = set(contract_counts.head(top_contracts).index)
        scoped['contrat'] = scoped['contrat'].where(scoped['contrat'].isin(keep), 'Autres')

    grouped = scoped.groupby(['ville', 'contrat']).size().reset_index(name='offres')
    return grouped.to_dict(orient='records')


def get_active_offers_this_week():
    """Nombre d'offres dont la date de publication tombe dans les 7 derniers
    jours — volume d'offres actives collectées par le pipeline de scraping
    cette semaine (pas de colonne de date de collecte distincte en base, on
    se base sur date_du_poste comme _postings_over_time)."""
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT COUNT(*) FROM offres_emploi
            WHERE date_du_poste >= NOW() - INTERVAL '7 days'
        """)
        return cur.fetchone()[0]
    finally:
        conn.close()


def get_market_trends():
    """Charge les offres une seule fois et calcule toutes les statistiques de
    la page Tendances à partir des vraies données de offres_emploi.

    Une offre publiée il y a plus de 30 jours est probablement close côté
    France Travail (rien dans le pipeline ne le confirme ni ne la supprime de
    la base, voir load_to_postgres.py — c'est un simple upsert), donc les
    photographies de l'état actuel du marché (compétences, contrats,
    salaires, villes, régions, secteurs) l'excluent. Seule la courbe
    _postings_over_time fait exception : c'est un historique de publication,
    pas un état courant, une offre ancienne doit continuer à compter dans le
    mois où elle a été publiée."""
    df = _load_offers()
    fresh = df[df['date_du_poste'] >= pd.Timestamp.now() - pd.Timedelta(days=30)]
    return {
        "top_skills": _top_skills(fresh),
        "contract_types": _contract_types(fresh),
        "postings_over_time": _postings_over_time(df),
        "salary_ranges": _salary_ranges_by_metier(fresh),
        "city_demand": _city_demand(fresh),
        "region_demand": _region_demand(fresh),
        "city_contract_distribution": _city_contract_distribution(fresh),
        "sector_distribution": _sector_distribution(fresh),
    }
