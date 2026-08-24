"""Tests unitaires pour les fonctions pures de matching_cv.py (pas de DB, pas
d'appel réseau — contrairement à test_matching_cv.py qui teste find_best_matches
en conditions réelles). Lancer avec : pytest scripts/test_matching_helpers.py
"""

from matching_cv import rank_missing_skills, get_profile_summary


def _offer(score, missing_skills):
    """Construit une offre minimale, avec seulement les champs dont
    rank_missing_skills/get_profile_summary ont besoin."""
    return {"score": score, "missing_skills": missing_skills}


# --- rank_missing_skills ---

def test_rank_missing_skills_empty_offers():
    assert rank_missing_skills([]) == []


def test_rank_missing_skills_no_gaps():
    offers = [_offer(0.9, []), _offer(0.8, [])]
    assert rank_missing_skills(offers) == []


def test_rank_missing_skills_single_offer_full_percentage():
    offers = [_offer(0.7, ["Sql", "Python"])]
    result = rank_missing_skills(offers)
    assert dict(result) == {"Sql": 100, "Python": 100}


def test_rank_missing_skills_sorted_by_frequency_desc():
    offers = [
        _offer(0.8, ["Sql", "Docker"]),
        _offer(0.7, ["Sql"]),
        _offer(0.6, ["Sql", "Docker"]),
        _offer(0.5, []),
    ]
    result = rank_missing_skills(offers)
    # Sql manque dans 3/4 offres (75%), Docker dans 2/4 (50%) : Sql doit être en tête.
    assert result[0] == ("Sql", 75)
    assert result[1] == ("Docker", 50)


def test_rank_missing_skills_duplicate_within_same_offer_counts_once():
    # missing_skills dupliqué dans UNE offre ne doit compter que pour 1 occurrence
    # (rank_missing_skills fait un set() par offre), pas gonfler le pourcentage.
    offers = [_offer(0.7, ["Sql", "Sql", "Sql"]), _offer(0.6, [])]
    result = rank_missing_skills(offers)
    assert dict(result) == {"Sql": 50}


# --- get_profile_summary ---

def test_get_profile_summary_empty_offers():
    assert get_profile_summary([]) == {}


def test_get_profile_summary_score_from_best_offer():
    offers = [_offer(0.66, ["Sql"]), _offer(0.40, ["Sql"])]
    summary = get_profile_summary(offers)
    assert summary["score"] == 66


def test_get_profile_summary_compatible_count_threshold():
    # round() plutôt que troncature : 0.695 -> 70% (compatible), 0.694 -> 69% (non).
    offers = [_offer(0.695, []), _offer(0.694, []), _offer(0.80, [])]
    summary = get_profile_summary(offers)
    assert summary["compatible_count"] == 2


def test_get_profile_summary_missing_skills_capped_at_top_n():
    offers = [_offer(0.7, ["A", "B", "C", "D"])]
    summary = get_profile_summary(offers, top_n_skills=2)
    assert len(summary["missing_skills"]) == 2
