import sqlite3
import os
from datetime import datetime

# Creamos el directorio de la base de datos si no existe
os.makedirs('data', exist_ok=True)
DB_PATH = 'data/banco.db'


def init_db():
    """Inicializar la base de datos"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Crear tabla de usuarios
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            user_id INTEGER PRIMARY KEY,
            nombre TEXT,
            saldo REAL,
            fecha_registro TEXT,
            interacciones INTEGER DEFAULT 0
        )
        ''')

        # Crear tabla de movimientos
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS movimientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            descripcion TEXT,
            monto REAL,
            fecha TEXT,
            FOREIGN KEY (user_id) REFERENCES usuarios(user_id)
        )
        ''')

        # Crear tabla de préstamos simulados
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS prestamos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            monto REAL,
            plazo INTEGER,
            tasa REAL,
            cuota REAL,
            total REAL,
            fecha TEXT,
            FOREIGN KEY (user_id) REFERENCES usuarios(user_id)
        )
        ''')

        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Error al inicializar la base de datos: {e}")
        return False


def get_user(user_id):
    """Obtener información del usuario"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE user_id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        return user
    except sqlite3.Error as e:
        print(f"Error al obtener usuario: {e}")
        return None


def create_user(user_id, nombre="Usuario"):
    """Crear un nuevo usuario con saldo inicial generado por movimientos simulados"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Insertar usuario con saldo inicial 0.0
        cursor.execute(
            'INSERT INTO usuarios (user_id, nombre, saldo, fecha_registro) VALUES (?, ?, ?, ?)',
            (user_id, nombre, 0.0, fecha)
        )

        # Movimientos simulados: ingresos y egresos básicos
        movimientos_simulados = [
            ("Depósito inicial", 10000.0),
            ("Compra supermercado", -1500.0),
            ("Transferencia recibida", 2500.0),
            ("Pago de servicio", -2000.0),
        ]

        for descripcion, monto in movimientos_simulados:
            # Insertar movimiento
            cursor.execute(
                'INSERT INTO movimientos (user_id, descripcion, monto, fecha) VALUES (?, ?, ?, ?)',
                (user_id, descripcion, monto, fecha)
            )

            # Actualizar saldo en tabla de usuarios
            cursor.execute(
                'UPDATE usuarios SET saldo = saldo + ? WHERE user_id = ?',
                (monto, user_id)
            )

        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Error al crear usuario: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return False


def update_interactions(user_id):
    """Actualizar contador de interacciones"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE usuarios SET interacciones = interacciones + 1 WHERE user_id = ?',
            (user_id,)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Error al actualizar interacciones: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return False


def get_balance(user_id):
    """Obtener saldo del usuario"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT saldo FROM usuarios WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        conn.close()

        if result:
            # Formatear el saldo como moneda
            return f"$ {result[0]:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        return "$ 0,00"
    except sqlite3.Error as e:
        print(f"Error al obtener saldo: {e}")
        if conn:
            conn.close()
        return "$ 0,00"


def save_transaction(user_id, descripcion, monto):
    """Guardar un movimiento en la cuenta"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Guardar movimiento
        cursor.execute(
            'INSERT INTO movimientos (user_id, descripcion, monto, fecha) VALUES (?, ?, ?, ?)',
            (user_id, descripcion, monto, fecha)
        )

        # Actualizar saldo
        cursor.execute(
            'UPDATE usuarios SET saldo = saldo + ? WHERE user_id = ?',
            (monto, user_id)
        )

        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Error al guardar transacción: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return False


def get_transactions(user_id, limit=5):
    """Obtener últimos movimientos"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT descripcion, monto, fecha FROM movimientos WHERE user_id = ? ORDER BY fecha DESC LIMIT ?',
            (user_id, limit)
        )
        movimientos = cursor.fetchall()
        conn.close()

        # Formatear los movimientos
        formatted_movimientos = []
        for mov in movimientos:
            descripcion, monto, fecha = mov
            signo = "🟢 +" if monto > 0 else "🔴 -"
            monto_fmt = f"$ {abs(monto):,.2f}".replace(
                ',', 'X').replace('.', ',').replace('X', '.')
            formatted_movimientos.append(
                f"{signo} {monto_fmt} - {descripcion}")

        return formatted_movimientos
    except sqlite3.Error as e:
        print(f"Error al obtener transacciones: {e}")
        if conn:
            conn.close()
        return []


def save_loan_simulation(user_id, monto, plazo, tasa, cuota, total):
    """Guardar simulación de préstamo"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute(
            'INSERT INTO prestamos (user_id, monto, plazo, tasa, cuota, total, fecha) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (user_id, monto, plazo, tasa, cuota, total, fecha)
        )

        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Error al guardar simulación de préstamo: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return False
