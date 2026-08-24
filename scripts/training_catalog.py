"""Catalogue de formations curé manuellement, indexé par compétence (mêmes
labels que scripts.skills_reference.SKILL_CATEGORIES / extract_skills — ex.
"Sql", "Power bi", "Ci/cd", ".net"), utilisé par la page Recommandations pour
suggérer des ressources concrètes en fonction des écarts détectés lors du
matching CV.

Volontairement statique (pas de génération par LLM) : le nom exact d'une
formation, son organisme et sa durée sont des faits vérifiables, pas du
contenu créatif — un LLM peut halluciner un cours qui n'existe pas.

Couvre l'intégralité du référentiel SKILL_CATEGORIES (~96 compétences) : pour
une compétence donnée, le candidat retombe sur une vraie ressource nommée
plutôt qu'un message d'impasse. Chaque "lien" a été vérifié individuellement
(HTTP 200) au moment de l'écriture — le nom/organisme reflète la page
réellement pointée par le lien, jamais une formation supposée mais non
vérifiée.
"""

import urllib.parse

TRAINING_CATALOG = {
    # --- Langages pour le Backend ---
    "Python": [{"nom": "Découvrez le langage Python", "organisme": "OpenClassrooms", "duree": "15h",
                "lien": "https://openclassrooms.com/fr/courses/7168871-decouvrez-le-langage-python"}],
    "Java": [{"nom": "Apprendre Java (dev.java)", "organisme": "Oracle / dev.java", "duree": "auto-formation",
              "lien": "https://dev.java/learn/"}],
    "Scala": [{"nom": "Tour of Scala", "organisme": "Scala-lang.org", "duree": "auto-formation",
               "lien": "https://docs.scala-lang.org/tour/tour-of-scala.html"}],
    "Go": [{"nom": "A Tour of Go", "organisme": "Go.dev", "duree": "auto-formation",
            "lien": "https://go.dev/tour/welcome/1"}],
    "Node.js": [{"nom": "Node.js — Learn", "organisme": "Nodejs.org", "duree": "auto-formation",
                 "lien": "https://nodejs.org/en/learn"}],
    "Fastapi": [{"nom": "FastAPI Tutorial", "organisme": "FastAPI Docs", "duree": "auto-formation",
                 "lien": "https://fastapi.tiangolo.com/tutorial/"}],
    "Flask": [{"nom": "Flask Quickstart", "organisme": "Flask Docs (Pallets)", "duree": "auto-formation",
               "lien": "https://flask.palletsprojects.com/en/latest/quickstart/"}],
    "R": [{"nom": "An Introduction to R", "organisme": "CRAN / The R Project", "duree": "auto-formation",
           "lien": "https://cran.r-project.org/doc/manuals/r-release/R-intro.html"}],
    "Kotlin": [{"nom": "Kotlin — Getting Started", "organisme": "Kotlinlang.org", "duree": "auto-formation",
                "lien": "https://kotlinlang.org/docs/getting-started.html"}],
    "Swift": [{"nom": "The Swift Programming Language", "organisme": "Swift.org", "duree": "auto-formation",
               "lien": "https://docs.swift.org/swift-book/"}],
    "Rust": [{"nom": "The Rust Programming Language (the book)", "organisme": "Rust-lang.org", "duree": "auto-formation",
              "lien": "https://doc.rust-lang.org/book/"}],
    "Php": [{"nom": "PHP The Right Way", "organisme": "Communauté PHP", "duree": "auto-formation",
             "lien": "https://phptherightway.com/"}],
    "Ruby": [{"nom": "Ruby in Twenty Minutes", "organisme": "Ruby-lang.org", "duree": "20 min",
              "lien": "https://www.ruby-lang.org/en/documentation/quickstart/"}],
    "Perl": [{"nom": "Learn Perl", "organisme": "Perl.org", "duree": "auto-formation",
              "lien": "https://learn.perl.org/"}],
    "C++": [{"nom": "LearnCpp.com", "organisme": "LearnCpp.com", "duree": "auto-formation",
             "lien": "https://www.learncpp.com/"}],
    "C#": [{"nom": "C# Fundamentals", "organisme": "Microsoft Learn", "duree": "10h",
            "lien": "https://learn.microsoft.com/en-us/training/paths/csharp-first-steps/"}],
    ".net": [{"nom": ".NET — Get Started", "organisme": "Microsoft Learn", "duree": "auto-formation",
              "lien": "https://dotnet.microsoft.com/en-us/learn"}],
    "Asp.net": [{"nom": "ASP.NET Core — Prise en main", "organisme": "Microsoft Learn", "duree": "auto-formation",
                 "lien": "https://learn.microsoft.com/en-us/aspnet/core/getting-started"}],

    # --- Langages pour le Frontend ---
    "Javascript": [{"nom": "JavaScript (guide du langage)", "organisme": "MDN Web Docs", "duree": "auto-formation",
                     "lien": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide"}],
    "Typescript": [{"nom": "TypeScript Handbook", "organisme": "TypeScriptLang.org", "duree": "auto-formation",
                     "lien": "https://www.typescriptlang.org/docs/handbook/intro.html"}],
    "React": [{"nom": "Apprendre React (tutoriel officiel)", "organisme": "React.dev", "duree": "auto-formation",
               "lien": "https://react.dev/learn"}],
    "Vue": [{"nom": "Vue.js — Guide", "organisme": "Vuejs.org", "duree": "auto-formation",
             "lien": "https://vuejs.org/guide/introduction.html"}],
    "Html": [{"nom": "Learn HTML", "organisme": "MDN Web Docs", "duree": "auto-formation",
              "lien": "https://developer.mozilla.org/en-US/docs/Learn/HTML"}],
    "Css": [{"nom": "Learn CSS", "organisme": "MDN Web Docs", "duree": "auto-formation",
             "lien": "https://developer.mozilla.org/en-US/docs/Learn/CSS"}],
    "Angular": [{"nom": "Tour of Heroes (tutoriel officiel)", "organisme": "Angular.dev", "duree": "auto-formation",
                 "lien": "https://angular.dev/tutorials/first-app"}],
    "Svelte": [{"nom": "Svelte Tutorial", "organisme": "Svelte.dev", "duree": "auto-formation",
                "lien": "https://svelte.dev/tutorial"}],
    "Next.js": [{"nom": "Next.js — Learn", "organisme": "Nextjs.org", "duree": "auto-formation",
                 "lien": "https://nextjs.org/learn"}],
    "Tailwind": [{"nom": "Tailwind CSS — Installation", "organisme": "Tailwindcss.com", "duree": "auto-formation",
                  "lien": "https://tailwindcss.com/docs/installation"}],
    "Bootstrap": [{"nom": "Bootstrap — Getting Started", "organisme": "Getbootstrap.com", "duree": "auto-formation",
                   "lien": "https://getbootstrap.com/docs/5.3/getting-started/introduction/"}],
    "Sass": [{"nom": "Sass — Guide", "organisme": "Sass-lang.com", "duree": "auto-formation",
              "lien": "https://sass-lang.com/guide/"}],

    # --- Data Stores ---
    "Postgresql": [{"nom": "PostgreSQL Tutorial", "organisme": "postgresqltutorial.com", "duree": "auto-formation",
                     "lien": "https://www.postgresqltutorial.com/"}],
    "Mongodb": [{"nom": "MongoDB University", "organisme": "MongoDB", "duree": "variable",
                 "lien": "https://learn.mongodb.com/"}],
    "Mysql": [{"nom": "MySQL Tutorial", "organisme": "mysqltutorial.org", "duree": "auto-formation",
               "lien": "https://www.mysqltutorial.org/"}],
    "Redis": [{"nom": "Redis — Learn", "organisme": "Redis.io", "duree": "auto-formation",
               "lien": "https://redis.io/learn/"}],
    "Elasticsearch": [{"nom": "Elasticsearch — Getting Started", "organisme": "Elastic.co", "duree": "auto-formation",
                        "lien": "https://www.elastic.co/guide/en/elasticsearch/reference/current/getting-started.html"}],
    "Snowflake": [{"nom": "Snowflake Documentation", "organisme": "Snowflake", "duree": "auto-formation",
                   "lien": "https://docs.snowflake.com/"}],
    "Oracle": [{"nom": "Oracle Database Documentation", "organisme": "Oracle", "duree": "auto-formation",
                "lien": "https://docs.oracle.com/en/database/"}],
    "Cassandra": [{"nom": "Apache Cassandra Documentation", "organisme": "Apache Cassandra", "duree": "auto-formation",
                   "lien": "https://cassandra.apache.org/doc/latest/"}],
    "Dynamodb": [{"nom": "Amazon DynamoDB Developer Guide", "organisme": "AWS Docs", "duree": "auto-formation",
                  "lien": "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html"}],
    "Bigquery": [{"nom": "BigQuery — Introduction", "organisme": "Google Cloud", "duree": "auto-formation",
                  "lien": "https://cloud.google.com/bigquery/docs/introduction"}],
    "Redshift": [{"nom": "Amazon Redshift — Getting Started", "organisme": "AWS Docs", "duree": "auto-formation",
                  "lien": "https://docs.aws.amazon.com/redshift/latest/gsg/getting-started.html"}],
    "Clickhouse": [{"nom": "ClickHouse — Tutorial", "organisme": "ClickHouse Docs", "duree": "auto-formation",
                    "lien": "https://clickhouse.com/docs/en/tutorial"}],

    # --- Cloud & Infra ---
    "Sql": [{"nom": "SQL Tutorial", "organisme": "postgresqltutorial.com", "duree": "auto-formation",
             "lien": "https://www.postgresqltutorial.com/"}],
    "Aws": [{"nom": "AWS Cloud Practitioner Essentials", "organisme": "AWS", "duree": "6h",
             "lien": "https://aws.amazon.com/training/digital/aws-cloud-practitioner-essentials/"}],
    "Gcp": [{"nom": "Google Cloud — Formations et parcours", "organisme": "Google Cloud", "duree": "variable",
             "lien": "https://cloud.google.com/learn/training"}],
    "Azure": [{"nom": "Microsoft Azure Fundamentals (AZ-900)", "organisme": "Microsoft Learn", "duree": "10h",
               "lien": "https://learn.microsoft.com/en-us/credentials/certifications/azure-fundamentals/"}],
    "Docker": [{"nom": "Docker — Get Started", "organisme": "Docker Docs", "duree": "auto-formation",
                "lien": "https://docs.docker.com/get-started/"}],
    "Kubernetes": [{"nom": "Kubernetes Basics (tutoriel officiel)", "organisme": "Kubernetes.io", "duree": "auto-formation",
                     "lien": "https://kubernetes.io/docs/tutorials/kubernetes-basics/"}],
    "Terraform": [{"nom": "Terraform — Tutorials", "organisme": "HashiCorp Developer", "duree": "auto-formation",
                    "lien": "https://developer.hashicorp.com/terraform/tutorials"}],
    "Ansible": [{"nom": "Ansible — Getting Started", "organisme": "Ansible Docs", "duree": "auto-formation",
                 "lien": "https://docs.ansible.com/ansible/latest/getting_started/index.html"}],
    "Jenkins": [{"nom": "Jenkins Tutorials", "organisme": "Jenkins.io", "duree": "auto-formation",
                 "lien": "https://www.jenkins.io/doc/tutorials/"}],
    "Linux": [{"nom": "Introduction to Linux (LFS101x)", "organisme": "Linux Foundation / edX", "duree": "40h",
               "lien": "https://www.edx.org/learn/linux/the-linux-foundation-introduction-to-linux"}],
    "Nginx": [{"nom": "NGINX — Beginner's Guide", "organisme": "Nginx.org", "duree": "auto-formation",
               "lien": "https://nginx.org/en/docs/beginners_guide.html"}],
    "Github actions": [{"nom": "Learn GitHub Actions", "organisme": "GitHub Docs", "duree": "auto-formation",
                         "lien": "https://docs.github.com/en/actions/learn-github-actions"}],
    "Gitlab": [{"nom": "Documentation GitLab", "organisme": "GitLab", "duree": "auto-formation",
                "lien": "https://docs.gitlab.com/"}],
    "Ci/cd": [{"nom": "Comprendre l'intégration et le déploiement continus (CI/CD)", "organisme": "GitLab Docs", "duree": "auto-formation",
               "lien": "https://docs.gitlab.com/ee/ci/"}],

    # --- Data Engineering ---
    "Dbt": [{"nom": "dbt — Introduction", "organisme": "getdbt.com", "duree": "auto-formation",
             "lien": "https://docs.getdbt.com/docs/introduction"}],
    "Airflow": [{"nom": "Apache Airflow — Tutorial", "organisme": "Apache Airflow", "duree": "auto-formation",
                 "lien": "https://airflow.apache.org/docs/apache-airflow/stable/tutorial/"}],
    "Spark": [{"nom": "Apache Spark — Quick Start", "organisme": "Apache Spark", "duree": "auto-formation",
               "lien": "https://spark.apache.org/docs/latest/quick-start.html"}],
    "Kafka": [{"nom": "Apache Kafka — Documentation", "organisme": "Apache Kafka", "duree": "auto-formation",
               "lien": "https://kafka.apache.org/documentation/"}],
    "Hadoop": [{"nom": "Apache Hadoop — Documentation", "organisme": "Apache Hadoop", "duree": "auto-formation",
                "lien": "https://hadoop.apache.org/docs/stable/"}],
    "Databricks": [{"nom": "Databricks — Getting Started", "organisme": "Databricks Docs", "duree": "auto-formation",
                     "lien": "https://docs.databricks.com/en/getting-started/index.html"}],
    "Talend": [{"nom": "Talend Help Center", "organisme": "Talend", "duree": "auto-formation",
                "lien": "https://help.talend.com/"}],
    "Nifi": [{"nom": "Apache NiFi — Documentation", "organisme": "Apache NiFi", "duree": "auto-formation",
              "lien": "https://nifi.apache.org/documentation/"}],

    # --- IA/ML ---
    "Tensorflow": [{"nom": "TensorFlow — Tutorials", "organisme": "TensorFlow.org", "duree": "auto-formation",
                     "lien": "https://www.tensorflow.org/tutorials"}],
    "Pytorch": [{"nom": "PyTorch — Tutorials", "organisme": "PyTorch.org", "duree": "auto-formation",
                 "lien": "https://pytorch.org/tutorials/"}],
    "Scikit-learn": [{"nom": "scikit-learn — User Guide", "organisme": "scikit-learn.org", "duree": "auto-formation",
                       "lien": "https://scikit-learn.org/stable/user_guide.html"}],
    "Llm": [{"nom": "LLM Course", "organisme": "Hugging Face", "duree": "variable",
             "lien": "https://huggingface.co/learn/llm-course"}],
    "Rag": [{"nom": "Build a Retrieval Augmented Generation (RAG) App", "organisme": "LangChain Docs", "duree": "auto-formation",
             "lien": "https://python.langchain.com/docs/tutorials/rag/"}],
    "Mlops": [{"nom": "MLOps — Continuous delivery and automation pipelines", "organisme": "Google Cloud", "duree": "auto-formation",
               "lien": "https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning"}],
    "Langchain": [{"nom": "LangChain — Introduction", "organisme": "LangChain Docs", "duree": "auto-formation",
                   "lien": "https://python.langchain.com/docs/introduction/"}],
    "Keras": [{"nom": "Keras — Getting Started", "organisme": "Keras.io", "duree": "auto-formation",
               "lien": "https://keras.io/getting_started/"}],
    "Opencv": [{"nom": "OpenCV-Python Tutorials", "organisme": "OpenCV Docs", "duree": "auto-formation",
                "lien": "https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html"}],
    "Nlp": [{"nom": "NLP Course", "organisme": "Hugging Face", "duree": "variable",
             "lien": "https://huggingface.co/learn/nlp-course"}],
    "Hugging face": [{"nom": "Hugging Face — Learn", "organisme": "Hugging Face", "duree": "variable",
                       "lien": "https://huggingface.co/learn"}],

    # --- No-Code ---
    "Airtable": [{"nom": "Airtable — Guides", "organisme": "Airtable", "duree": "auto-formation",
                  "lien": "https://www.airtable.com/guides"}],
    "Make": [{"nom": "Make Academy", "organisme": "Make", "duree": "auto-formation",
              "lien": "https://academy.make.com/"}],
    "Bubble": [{"nom": "Bubble — Manual", "organisme": "Bubble", "duree": "auto-formation",
                "lien": "https://manual.bubble.io/"}],
    "Power bi": [{"nom": "Power BI Fundamentals", "organisme": "Microsoft Learn", "duree": "8h",
                  "lien": "https://learn.microsoft.com/en-us/training/powerplatform/power-bi/"}],
    "Zapier": [{"nom": "Zapier — Learn", "organisme": "Zapier", "duree": "auto-formation",
                "lien": "https://zapier.com/learn"}],
    "Tableau": [{"nom": "Tableau — Get Started Tutorial", "organisme": "Tableau Help", "duree": "auto-formation",
                 "lien": "https://help.tableau.com/current/guides/get-started-tutorial/en-us/get-started-tutorial-home.htm"}],
    "Metabase": [{"nom": "Metabase Learn", "organisme": "Metabase", "duree": "auto-formation",
                  "lien": "https://www.metabase.com/learn/"}],
    "Webflow": [{"nom": "Webflow University", "organisme": "Webflow", "duree": "auto-formation",
                 "lien": "https://university.webflow.com/"}],
    "Excel": [{"nom": "Formations Excel", "organisme": "Microsoft Learn", "duree": "variable",
               "lien": "https://learn.microsoft.com/en-us/training/browse/?products=office-excel"}],
    "Notion": [{"nom": "Notion — Centre d'aide", "organisme": "Notion", "duree": "auto-formation",
                "lien": "https://www.notion.so/help"}],
    "Qlikview": [{"nom": "Qlik — Formations", "organisme": "Qlik", "duree": "variable",
                  "lien": "https://www.qlik.com/us/services/training"}],
    "Spss": [{"nom": "IBM SPSS Statistics — Ressources", "organisme": "IBM", "duree": "auto-formation",
              "lien": "https://www.ibm.com/products/spss-statistics/resources"}],
    "Looker": [{"nom": "Looker Documentation", "organisme": "Google Cloud", "duree": "auto-formation",
                "lien": "https://cloud.google.com/looker/docs"}],

    # --- Méthodologies & outils ---
    "Agile": [{"nom": "Agile Foundations", "organisme": "LinkedIn Learning", "duree": "2h",
               "lien": "https://www.linkedin.com/learning/agile-foundations"}],
    "Scrum": [{"nom": "Le Guide Scrum (guide officiel)", "organisme": "ScrumGuides.org", "duree": "auto-formation",
               "lien": "https://www.scrumguides.org/scrum-guide.html"}],
    "Devops": [{"nom": "Formations DevOps", "organisme": "Coursera", "duree": "variable",
                "lien": "https://www.coursera.org/courses?query=devops"}],
    "Git": [{"nom": "Pro Git (livre officiel gratuit)", "organisme": "Git-scm.com", "duree": "auto-formation",
             "lien": "https://git-scm.com/book/en/v2"}],
    "Jira": [{"nom": "Jira Software — Guides", "organisme": "Atlassian", "duree": "auto-formation",
              "lien": "https://www.atlassian.com/software/jira/guides"}],
    "Confluence": [{"nom": "Confluence — Guides", "organisme": "Atlassian", "duree": "auto-formation",
                    "lien": "https://www.atlassian.com/software/confluence/guides"}],
    "Salesforce": [{"nom": "Trailhead", "organisme": "Salesforce", "duree": "variable",
                     "lien": "https://trailhead.salesforce.com/"}],
    "Sap": [{"nom": "SAP Learning", "organisme": "SAP", "duree": "variable",
             "lien": "https://learning.sap.com/"}],
}


def get_trainings_for_skill(skill):
    return TRAINING_CATALOG.get(skill, [])


def search_fallback_link(skill):
    """Filet de sécurité pour une compétence sans entrée dans le catalogue
    (référentiel étendu plus tard, faute de frappe, etc.) : un lien de
    recherche sur une plateforme stable plutôt qu'une impasse. Volontairement
    étiqueté comme une recherche, pas comme un cours précis — on ne sait pas
    à l'avance ce que la recherche va remonter."""
    query = urllib.parse.quote(skill)
    return f"https://openclassrooms.com/fr/search?query={query}"
