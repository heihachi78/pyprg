import psycopg2

TOTH = 'toth'

POSTGRES_HOST = 'localhost'
POSTGRES_PORT = 5432
POSTGRES_USER = 'postgres'
POSTGRES_PASSWORD = 'postgres'
POSTGRES_DATABASE = 'postgres'

TABLE_NAME = f'{TOTH.lower()}_cosmetics'

def connect_db():
    conn = psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        dbname=POSTGRES_DATABASE
    )
    return conn

def get_termek_tipusok(table_name):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute(f'select distinct t.product_type as tipus from {table_name} t order by t.product_type')
        rows = cursor.fetchall()
        cursor.close()
    return rows

def get_termekek(table_name, tipus):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute(f"select t.\"name\" as nev, t.price as ar from {table_name} t where t.product_type = '{tipus}' order by 1")
        rows = cursor.fetchall()
        cursor.close()
    return rows

    
def get_leiras(table_name, termek):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute(f"select t.\"description\" as leiras from {table_name} t where t.\"name\" = '{termek}'")
        rows = cursor.fetchone()
        cursor.close()
    return rows

def bekeres(max_ertek, msg = "Válassz egy számot: "):
    while True:
        try:
            valasztott = int(input(msg))
            if 0 <= valasztott < max_ertek:
                return valasztott
            raise ValueError
        except ValueError:
            print(f"Adj meg egy 0 és {max_ertek} közötti egész számot!")

def main():
    try:
        termek_tipusok = get_termek_tipusok(TABLE_NAME)
    except:
        print("Hiba történt az adatbázis lekérdezése során.")
        return

    print('Választható termék típusok:')
    for sorsz, tipus in enumerate(termek_tipusok):
        print(sorsz, tipus[0])
    valasztott_tipus = bekeres(len(termek_tipusok), "Válassz egy termék típust: ")

    try:
        termekek = get_termekek(TABLE_NAME, termek_tipusok[valasztott_tipus][0])
    except:
        print("Hiba történt a termékek lekérdezésekor.")
        return

    print('Választható termékek:')
    for sorsz, termek in enumerate(termekek):
        print(sorsz, termek[0], '(ára:', termek[1], ')')
    valasztott_termek = bekeres(len(termekek), "Válassz egy terméket: ")

    try:
        leiras = get_leiras(TABLE_NAME, termekek[valasztott_termek][0])
    except:
        print("Hiba történt az adatbázis lekérdezése során.")
        return

    print('A termék leírása:')
    print(leiras[0])

if __name__ == "__main__":
    main()