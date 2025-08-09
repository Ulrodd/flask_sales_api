from flask import Blueprint, request, jsonify
from sqlalchemy import and_
from .db import SessionLocal
from .models import Product, Sale, Customer
from datetime import datetime

api_bp = Blueprint('api', __name__)

# GET /products
@api_bp.route('/products', methods=['GET'])
def get_products():
    session = SessionLocal()
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    products = session.query(Product).offset((page-1)*per_page).limit(per_page).all()
    result = [{"id": p.id, "name": p.name, "price": float(p.price)} for p in products]
    session.close()
    return jsonify(result)

# POST /products
@api_bp.route('/products', methods=['POST'])
def add_product():
    session = SessionLocal()
    data = request.json
    product = Product(name=data.get('name'), price=data.get('price'))
    session.add(product)
    session.commit()
    session.refresh(product)
    session.close()
    return jsonify({"id": product.id, "name": product.name, "price": float(product.price)}), 201

# GET /sales
@api_bp.route('/sales', methods=['GET'])
def get_sales():
    session = SessionLocal()
    try:
        page = int(request.args.get("page", 1))
        per_page = min(int(request.args.get("per_page", 10)), 200)

        start = request.args.get("start")
        end = request.args.get("end")
        min_amount = request.args.get("min_amount", type=float)
        max_amount = request.args.get("max_amount", type=float)

        q = session.query(Sale)

        # Joindre Product UNE SEULE FOIS si filtre prix
        if min_amount is not None or max_amount is not None:
            q = q.join(Product)
            if min_amount is not None:
                q = q.filter(Product.price >= min_amount)
            if max_amount is not None:
                q = q.filter(Product.price <= max_amount)

        if start:
            q = q.filter(Sale.date >= start)
        if end:
            q = q.filter(Sale.date <= end)

        rows = q.offset((page - 1) * per_page).limit(per_page).all()
        data = [{
            "id": s.id,
            "invoice_no": s.invoice_no,
            "date": s.date.isoformat() if getattr(s, "date", None) else None,
            "quantity": s.quantity,
            "product_id": s.product_id,
            "customer_id": s.customer_id
        } for s in rows]
        return jsonify({"items": data, "page": page, "per_page": per_page})
    finally:
        session.close()

# POST /sales
@api_bp.route('/sales', methods=['POST'])
def add_sale():
    session = SessionLocal()
    data = request.json
    sale = Sale(
        invoice_no=data.get('invoice_no'),
        date=datetime.strptime(data.get('date'), '%Y-%m-%d').date(),
        quantity=data.get('quantity'),
        product_id=data.get('product_id'),
        customer_id=data.get('customer_id')
    )
    session.add(sale)
    session.commit()
    session.refresh(sale)
    session.close()
    return jsonify({"id": sale.id}), 201

# PUT /customers/<id>
@api_bp.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    session = SessionLocal()
    customer = session.query(Customer).get(id)
    if not customer:
        session.close()
        return jsonify({"error": "Customer not found"}), 404
    data = request.json
    customer.name = data.get('name', customer.name)
    customer.country = data.get('country', customer.country)
    session.commit()
    session.close()
    return jsonify({"message": "Customer updated"})

# DELETE /sales/<id>
@api_bp.route('/sales/<int:id>', methods=['DELETE'])
def delete_sale(id):
    session = SessionLocal()
    sale = session.query(Sale).get(id)
    if not sale:
        session.close()
        return jsonify({"error": "Sale not found"}), 404
    session.delete(sale)
    session.commit()
    session.close()
    return jsonify({"message": "Sale deleted"})
