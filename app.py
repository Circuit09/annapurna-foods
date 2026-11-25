from contextlib import asynccontextmanager
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path
import sqlite3

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

ROOT = Path(__file__).parent
DB = ROOT / "annapurna.db"


def connect():
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys=ON")
    return db


def init_db():
    with connect() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS products(id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE, price_paise_per_kg INTEGER NOT NULL CHECK(price_paise_per_kg>=0));
        CREATE TABLE IF NOT EXISTS materials(id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE);
        CREATE TABLE IF NOT EXISTS sales(id INTEGER PRIMARY KEY, day TEXT NOT NULL, product_id INTEGER NOT NULL REFERENCES products(id), grams INTEGER NOT NULL CHECK(grams>0), price_paise_per_kg INTEGER NOT NULL, total_paise INTEGER NOT NULL);
        CREATE TABLE IF NOT EXISTS purchases(id INTEGER PRIMARY KEY, day TEXT NOT NULL, material_id INTEGER NOT NULL REFERENCES materials(id), quantity INTEGER NOT NULL CHECK(quantity>0), unit TEXT NOT NULL, amount_paise INTEGER NOT NULL CHECK(amount_paise>=0));
        CREATE TABLE IF NOT EXISTS expenses(id INTEGER PRIMARY KEY, day TEXT NOT NULL, category TEXT NOT NULL, description TEXT NOT NULL, amount_paise INTEGER NOT NULL CHECK(amount_paise>=0));
        CREATE TABLE IF NOT EXISTS inventory(id INTEGER PRIMARY KEY, kind TEXT NOT NULL CHECK(kind IN ('raw','finished')), item_id INTEGER NOT NULL, opening_grams INTEGER NOT NULL CHECK(opening_grams>=0), UNIQUE(kind,item_id));
        CREATE TABLE IF NOT EXISTS production(id INTEGER PRIMARY KEY, day TEXT NOT NULL, product_id INTEGER NOT NULL REFERENCES products(id), grams INTEGER NOT NULL CHECK(grams>0));
        CREATE TABLE IF NOT EXISTS sale_deductions(sale_id INTEGER PRIMARY KEY REFERENCES sales(id), product_id INTEGER NOT NULL REFERENCES products(id), grams INTEGER NOT NULL);
        """)


@asynccontextmanager
async def lifespan(app):
    init_db()
    yield


app = FastAPI(title="Annapurna Foods Business Manager", lifespan=lifespan)


class ProductIn(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    price_per_kg: str = Field(pattern=r"^\d+(\.\d{1,2})?$")


class MaterialIn(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class OpeningIn(BaseModel):
    kind: str
    item_id: int = Field(gt=0)
    grams: int = Field(ge=0)


class SaleIn(BaseModel):
    day: date
    product_id: int = Field(gt=0)
    grams: int = Field(gt=0)


class PurchaseIn(BaseModel):
    day: date
    material_id: int = Field(gt=0)
    quantity: int = Field(gt=0)
    unit: str = Field(min_length=1, max_length=20)
    amount: str = Field(pattern=r"^\d+(\.\d{1,2})?$")


class ExpenseIn(BaseModel):
    day: date
    category: str = Field(min_length=1, max_length=80)
    description: str = Field(min_length=1, max_length=240)
    amount: str = Field(pattern=r"^\d+(\.\d{1,2})?$")


class ProductionIn(BaseModel):
    day: date
    product_id: int = Field(gt=0)
    grams: int = Field(gt=0)


def paise(value):
    try:
        return int(Decimal(value) * 100)
    except InvalidOperation:
        raise HTTPException(422, "Invalid money amount")


def rows(db, query, args=()):
    return [dict(r) for r in db.execute(query, args).fetchall()]


@app.get("/")
def homepage():
    return FileResponse(ROOT / "index.html")

@app.get("/static/{name}")
def static_asset(name: str):
    if name not in {"style.css", "manager.css", "manager.js"}:
        raise HTTPException(404, "Not found")
    return FileResponse(ROOT / name)


@app.get("/manager")
def manager():
    return FileResponse(ROOT / "manager.html")


@app.get("/api/catalog")
def catalog():
    with connect() as db:
        return {"products": rows(db, "SELECT * FROM products ORDER BY name"), "materials": rows(db, "SELECT * FROM materials ORDER BY name")}


@app.post("/api/products")
def add_product(data: ProductIn):
    try:
        with connect() as db:
            cur = db.execute("INSERT INTO products(name,price_paise_per_kg) VALUES(?,?)", (data.name.strip(), paise(data.price_per_kg)))
            return {"id": cur.lastrowid}
    except sqlite3.IntegrityError as exc:
        raise HTTPException(409, "Product name already exists") from exc


@app.post("/api/materials")
def add_material(data: MaterialIn):
    try:
        with connect() as db:
            cur = db.execute("INSERT INTO materials(name) VALUES(?)", (data.name.strip(),))
            return {"id": cur.lastrowid}
    except sqlite3.IntegrityError as exc:
        raise HTTPException(409, "Material name already exists") from exc


@app.post("/api/inventory/opening")
def opening(data: OpeningIn):
    if data.kind not in ("raw", "finished"):
        raise HTTPException(422, "Kind must be raw or finished")
    with connect() as db:
        table = "materials" if data.kind == "raw" else "products"
        if not db.execute(f"SELECT id FROM {table} WHERE id=?", (data.item_id,)).fetchone():
            raise HTTPException(404, "Inventory item not found")
        db.execute("INSERT INTO inventory(kind,item_id,opening_grams) VALUES(?,?,?) ON CONFLICT(kind,item_id) DO UPDATE SET opening_grams=excluded.opening_grams", (data.kind, data.item_id, data.grams))
    return {"saved": True}


@app.post("/api/sales")
def sale(data: SaleIn):
    with connect() as db:
        product = db.execute("SELECT * FROM products WHERE id=?", (data.product_id,)).fetchone()
        if not product:
            raise HTTPException(404, "Product not found")
        total = (data.grams * product["price_paise_per_kg"] + 500) // 1000
        cur = db.execute("INSERT INTO sales(day,product_id,grams,price_paise_per_kg,total_paise) VALUES(?,?,?,?,?)", (data.day.isoformat(), data.product_id, data.grams, product["price_paise_per_kg"], total))
        db.execute("INSERT INTO sale_deductions(sale_id,product_id,grams) VALUES(?,?,?)", (cur.lastrowid, data.product_id, data.grams))
        return {"id": cur.lastrowid, "total_paise": total}


@app.post("/api/purchases")
def purchase(data: PurchaseIn):
    with connect() as db:
        cur = db.execute("INSERT INTO purchases(day,material_id,quantity,unit,amount_paise) VALUES(?,?,?,?,?)", (data.day.isoformat(), data.material_id, data.quantity, data.unit, paise(data.amount)))
        return {"id": cur.lastrowid}


@app.post("/api/expenses")
def expense(data: ExpenseIn):
    with connect() as db:
        cur = db.execute("INSERT INTO expenses(day,category,description,amount_paise) VALUES(?,?,?,?)", (data.day.isoformat(), data.category.strip(), data.description.strip(), paise(data.amount)))
        return {"id": cur.lastrowid}


@app.post("/api/production")
def production(data: ProductionIn):
    with connect() as db:
        if not db.execute("SELECT id FROM products WHERE id=?", (data.product_id,)).fetchone():
            raise HTTPException(404, "Product not found")
        cur = db.execute("INSERT INTO production(day,product_id,grams) VALUES(?,?,?)", (data.day.isoformat(), data.product_id, data.grams))
        return {"id": cur.lastrowid}


@app.get("/api/stock")
def stock():
    with connect() as db:
        return {"finished": rows(db, "SELECT p.id,p.name,COALESCE(i.opening_grams,0)+COALESCE((SELECT SUM(grams) FROM production WHERE product_id=p.id),0)-COALESCE((SELECT SUM(grams) FROM sale_deductions WHERE product_id=p.id),0) AS grams FROM products p LEFT JOIN inventory i ON i.kind='finished' AND i.item_id=p.id"), "raw": rows(db, "SELECT m.id,m.name,COALESCE(i.opening_grams,0)+COALESCE((SELECT SUM(CASE unit WHEN 'kg' THEN quantity*1000 WHEN 'g' THEN quantity ELSE 0 END) FROM purchases WHERE material_id=m.id),0) AS grams FROM materials m LEFT JOIN inventory i ON i.kind='raw' AND i.item_id=m.id")}


@app.get("/api/dashboard")
def dashboard():
    today = date.today().isoformat()
    with connect() as db:
        sales = db.execute("SELECT COALESCE(SUM(total_paise),0) FROM sales WHERE day=?", (today,)).fetchone()[0]
        purchases = db.execute("SELECT COALESCE(SUM(amount_paise),0) FROM purchases WHERE day=?", (today,)).fetchone()[0]
        expenses = db.execute("SELECT COALESCE(SUM(amount_paise),0) FROM expenses WHERE day=?", (today,)).fetchone()[0]
        return {"day": today, "sales_paise": sales, "purchases_paise": purchases, "expenses_paise": expenses, "provisional_balance_paise": sales-expenses, "profit_note": "Provisional indicator only; purchases are cash outflow, not cost of goods sold. Product costing is not implemented.", "stock": stock()["finished"]}
