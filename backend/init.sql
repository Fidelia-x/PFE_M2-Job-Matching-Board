-- Activer l'extension nécessaire
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE offres_emploi (
    id_offres_emploi SERIAL PRIMARY KEY,
    titre VARCHAR(255),
    description TEXT,
    competences TEXT[],       -- Tableau de mots-clés
    contract TEXT,
    diplome_requis TEXT,
    localisation TEXT,
    salaire_min FLOAT,
    salaire_max FLOAT,
    education TEXT,
    experience_years INTEGER,
    source_url TEXT,
    source_platform TEXT,
    company TEXT NOT NULL,
    languages TEXT[],
    date_du_poste TIMESTAMP DEFAULT NOW(),

    embedding vector(100)    -- La colonne IA
);

CREATE TABLE cv_candidats (
    id_cv SERIAL PRIMARY KEY,
    nom_candidat TEXT,
    competences_detectees TEXT[],
    email TEXT,
    phone TEXT,
    localisation TEXT,
    experience_years INTEGER,
    education_level TEXT,
    certifications TEXT[],
    languages TEXT[],
    date_de_lanalyse TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    cv_embedding vector(100),
);