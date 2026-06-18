\c job_matching

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS offres_emploi (
    id_offres_emploi SERIAL PRIMARY KEY,
    id_france_travail VARCHAR(50),
    titre VARCHAR(255),
    description TEXT,
    competences TEXT[],       -- Tableau de mots-clés
    languages TEXT[],
    contract TEXT,
    diplome_requis TEXT,
    education TEXT,
    localisation TEXT,
    salaire_min FLOAT,
    salaire_max FLOAT,
    experience_years INTEGER,
    source_url TEXT,
    source_platform TEXT,
    company TEXT NOT NULL,
    date_du_poste TIMESTAMP DEFAULT NOW(),

    embedding vector(384)    -- La colonne IA
);

CREATE UNIQUE INDEX idx_unique_source_url ON offres_emploi (source_url);

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
    date_de_lanalyse TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    cv_embedding vector(384)
);