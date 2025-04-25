import requests
import psycopg2

TOTH = 'toth'

POSTGRES_HOST = 'localhost'
POSTGRES_PORT = 5432
POSTGRES_USER = 'postgres'
POSTGRES_PASSWORD = 'postgres'
POSTGRES_DATABASE = 'postgres'

TABLE_NAME = f'{TOTH.lower()}_cosmetics'
J0P7MF_URL = 'http://makeup-api.herokuapp.com/api/v1/products.json'

def create_table(conn, table_name):
    print("Adatbázis tábla létrehozása...")
    cursor = conn.cursor()

    cursor.execute(f'''
        DROP TABLE IF EXISTS {table_name}
    ''')
    #név (name), ár (price), leírás (description), terméktípus (product_type)
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            price NUMERIC,
            description TEXT,
            product_type VARCHAR(50)
        )
    ''')
    conn.commit()
    cursor.close()

def insert_products(conn, products, table_name):
    print("Adatok beszúrása adatbázisba...")
    cursor = conn.cursor()
    for product in products:
        cursor.execute(f'''
                INSERT INTO {table_name} (
                    name, price, description, product_type
                ) VALUES 
                    (%s, %s, %s, %s)
            ''', (
                product['name'], 
                product['price'],
                product['description'],
                product['product_type']
            )
        )
    conn.commit()
    print("Adatok sikeresen beszúrva.")
    cursor.close()

def connect_db():
    conn = psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        dbname=POSTGRES_DATABASE
    )
    return conn

def fetch_products(url):
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return resp.json()

def main() -> None:
    print("Adatok letöltése...")
    try:
        termekek = fetch_products(J0P7MF_URL)
    except:
        print("Hiba történt a termékek letöltésekor.")
        return
    try:
        with connect_db() as conn:
            create_table(conn, TABLE_NAME)
            insert_products(conn, termekek, TABLE_NAME)
    except Exception as e:
        print(f"Hiba történt az adatbázis műveletek során.")
        return

if __name__ == "__main__":
    main()
