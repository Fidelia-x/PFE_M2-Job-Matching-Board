from fastapi import FastAPI

app = FastAPI(
    title="Job Matching API",
    description="API de matching CV ↔ Offres d'emploi",
    version="1.0.0"
)

# Route de santé — vérifie que l'API tourne
@app.get("/")
def root():
    return {"message": "Job Matching API opérationnelle"}

@app.get("/sante")
def sante():
    return {"status": "ok"}