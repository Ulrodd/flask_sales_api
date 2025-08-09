# API Flask – Backend REST PostgreSQL

![Flask](https://img.shields.io/badge/Flask-2.x-green)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-blue)

## Description
API REST modulaire connectée à PostgreSQL pour exposer des données de ventes.  
Fonctionnalités : endpoints CRUD, pagination, filtres dynamiques.

## Stack technique
- Flask (API REST)
- SQLAlchemy (ORM)
- PostgreSQL

## Installation et configuration
```bash
git clone https://github.com/Ulrodd/flask_sales_api.git
cd flask_sales_api
pip install -r requirements.txt

# Créer un fichier .env à la racine du projet :
echo "DATABASE_URL=postgresql://airflow:airflow@postgres:5432/airflow" > .env
```
Notes :
- Si l’API tourne dans le même réseau Docker que l’ETL : `host=postgres` fonctionne.
- Si l’API tourne sur la machine hôte : utiliser le host/port publiés (`localhost:5432`) et adapter l’URL.

## Lancement
```bash
# Mode développement
python run.py

# En Docker
docker run -p 8080:5000 flask_sales_api

# Production avec WSGI
gunicorn "app:create_app()" --bind 0.0.0.0:5000
```
Accéder à : http://localhost:8080

## Endpoints

### Produits
```bash
# GET /products — Liste paginée
curl "http://localhost:5000/products?page=1&per_page=20"

# POST /products — Création
curl -X POST http://localhost:5000/products \
  -H "Content-Type: application/json" \
  -d '{"name":"Widget","price":9.99}'
```

### Ventes
```bash
# GET /sales — Liste filtrable + pagination
curl "http://localhost:5000/sales?start=2025-08-01&end=2025-08-09&page=1&per_page=50"
curl "http://localhost:5000/sales?min_amount=5&max_amount=20"

# POST /sales — Création
curl -X POST http://localhost:5000/sales \
  -H "Content-Type: application/json" \
  -d '{"invoice_no":"536365","date":"2025-08-09","quantity":3,"product_id":1,"customer_id":12345}'

# DELETE /sales/<id> — Suppression
curl -X DELETE http://localhost:5000/sales/10
```

### Clients
```bash
# PUT /customers/<id> — Mise à jour partielle
curl -X PUT http://localhost:5000/customers/12345 \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","country":"France"}'
```

## Arborescence
```plaintext
flask_sales_api/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── db.py
│   └── routes.py
├── run.py
├── .env
├── requirements.txt
└── README.md
```

## Remarques
- Le serveur Flask intégré convient uniquement au développement.
- En production, utiliser gunicorn ou un autre serveur WSGI.
- Assurez-vous que `DATABASE_URL` pointe vers la base PostgreSQL alimentée par l’ETL Airflow.

## Auteur
LinkedIn : https://www.linkedin.com/in/fahd
