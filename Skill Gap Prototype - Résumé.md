# Skill Gap Prototype — Résumé de conception

Prototype interactif (`Skill Gap Prototype.dc.html`) pour l'app Streamlit de comparaison de compétences, poste cible : **Data Analyst**.

## Arborescence des pages

1. **Connexion** — email/mot de passe, point d'entrée unique.
2. **Matching CV** (page d'accueil, fusionne l'ancien Dashboard) :
   - Étape 1 : dépôt du CV (zone drag & drop) + bouton "Lancer le matching".
   - Étape 2 (après analyse) : radar chart (profil actuel vs cible), jauge de correspondance au poste, score global, écarts critiques, listes "compétences maîtrisées" / "à développer", tableau détaillé par compétence, bandeau vers Recommandations.
3. **Offres trouvées** — liste d'offres d'emploi correspondant au profil (titre, entreprise, ville, contrat, salaire, % de correspondance). Accessible seulement après le matching CV (sinon rappel + bouton de redirection).
4. **Tendances du marché** :
   - Compétences les plus demandées (barres).
   - Types de contrats les plus demandés (CDI/CDD/Freelance/Stage).
   - Offres publiées dans le temps (graphe en barres, 6 mois).
   - Fourchettes salariales par métier (barres de plage).
   - Demande par ville (cartes : offres, salaire moyen, compétences top).
5. **Recommandations** — formations suggérées par écart de compétence (nom, organisme, durée), accessible seulement après matching.
6. **Assistant IA** — placeholder "Bientôt disponible".
7. **Guide de conception** — page intégrée résumant arborescence, wireframes, interactions, composants visuels et style guide.

## Header commun (toutes les pages)

Titre + sous-titre de page, recherche globale, icône notifications, bouton "+ Nouveau matching".

## Menu profil (sidebar)

Avatar + nom d'utilisateur en bas de la sidebar → popover : Paramètres, Langue, Mode sombre (toggle), Déconnexion. Remplace l'ancien bloc "Déconnexion / Mode sombre" affiché en dur.

## Mode sombre

Toggle dans le menu profil. Palette claire et sombre définies via variables CSS (voir style guide), même teinte primaire ajustée pour le contraste.

## Composants visuels

- **Radar chart** (SVG) : profil actuel (plein) vs profil cible (pointillés).
- **Jauge circulaire (donut)** : taux de correspondance / préparation.
- **Barres de progression doubles** : niveau actuel (couleur) + repère niveau cible.
- **Graphe en barres** : évolution du nombre d'offres publiées.
- **Barres de plage** : fourchettes salariales par métier.
- Écarts signalés par **couleur uniquement** (vert = acquis, ambre = à combler, rouge = critique) — pas d'icône d'alerte.

## Style guide — couleurs

**Clair**
- Fond `#FAF7F2`, cartes `#FFFFFF`, secondaire `#F3EEE6`, bordures `#ECE3D6`
- Texte `#2B2620`, texte secondaire `#5B5346`, texte discret `#8A7F6E`
- Primaire `#B5654A` / texte sur primaire `#FFF8F3`
- Vert `oklch(0.58 0.12 150)`, ambre `oklch(0.72 0.14 78)`, rouge `oklch(0.58 0.17 26)`

**Sombre**
- Fond `#211C17`, cartes `#2A241D`, secondaire `#2F281F`, bordures `#3D352A`
- Texte `#F3ECE2`, texte secondaire `#CBBFAE`, texte discret `#9C8E7A`
- Primaire `#C97D5D` / texte sur primaire `#211C17`
- Vert/ambre/rouge : mêmes teintes que le clair, luminosité augmentée pour le contraste

**Typographie** : Inter (Helvetica en repli), 1 seule famille.

## Décisions UX notables

- Le matching CV doit être lancé avant d'accéder aux Offres et aux Recommandations (pas de données affichées sans analyse).
- Jamais plus de 3 cartes KPI par ligne.
- Couleur seule (sans icône) pour les alertes de gap, pour un rendu sobre et professionnel.

## Export

Version autonome (offline, sans dépendances) livrée en téléchargement : `Skill Gap Prototype - Standalone.html`.
