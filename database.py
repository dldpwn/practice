
import sqlite3
import hashlib
import hmac
import os
from pathlib import Path

# 프로젝트 폴더에 데이터베이스 파일 생성
DB_PATH = Path(__file__).resolve().parent / "NutriDay.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def hash_password(password, salt=None):
    """비밀번호를 원문 그대로 저장하지 않고 해시 처리."""
    if salt is None:
        salt = os.urandom(16)

    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        600_000
    )
    return salt.hex(), hashed.hex()


def verify_password(password, salt_hex, hash_hex):
    """입력한 비밀번호가 등록된 비밀번호와 일치하는지 확인."""
    salt = bytes.fromhex(salt_hex)
    _, calculated_hash = hash_password(password, salt)
    return hmac.compare_digest(calculated_hash, hash_hex)


def init_db():
    """필요한 테이블을 처음 생성."""
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL COLLATE NOCASE UNIQUE,
                salt TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS profiles (
                user_id INTEGER PRIMARY KEY,
                age INTEGER,
                height REAL,
                weight REAL,
                activity_level TEXT,
                food_preferences TEXT,
                excluded_foods TEXT,
                FOREIGN KEY (user_id)
                    REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS meal_plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                plan_date TEXT NOT NULL,
                plan_data TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id)
                    REFERENCES users(id) ON DELETE CASCADE
            );
        """)


def register_user(username, password):
    """회원가입. 성공하면 (True, 메시지)를 반환."""
    username = username.strip()

    if len(username) < 4 or len(username) > 30:
        return False, "아이디는 4~30자로 입력해 주세요."

    if not username.replace("_", "").isalnum():
        return False, "아이디에는 영문, 숫자, 밑줄(_)만 사용할 수 있어요."

    if len(password) < 10:
        return False, "비밀번호는 10자 이상으로 설정해 주세요."

    salt, password_hash = hash_password(password)

    try:
        with get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO users (username, salt, password_hash)
                VALUES (?, ?, ?)
                """,
                (username, salt, password_hash)
            )
            user_id = cursor.lastrowid

            conn.execute(
                "INSERT INTO profiles (user_id) VALUES (?)",
                (user_id,)
            )

        return True, "회원가입이 완료됐어요."

    except sqlite3.IntegrityError:
        return False, "이미 사용 중인 아이디예요."


def authenticate_user(username, password):
    """로그인 성공 시 사용자 ID를 반환하고 실패 시 None 반환."""
    with get_connection() as conn:
        user = conn.execute(
            """
            SELECT id, salt, password_hash
            FROM users
            WHERE username = ?
            """,
            (username.strip(),)
        ).fetchone()

    if user is None:
        return None

    if verify_password(password, user["salt"], user["password_hash"]):
        return user["id"]

    return None


def save_profile(user_id, age, height, weight,
                 activity_level, food_preferences, excluded_foods):
    """해당 사용자 본인의 프로필 저장."""
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE profiles
            SET age = ?, height = ?, weight = ?,
                activity_level = ?, food_preferences = ?,
                excluded_foods = ?
            WHERE user_id = ?
            """,
            (
                age, height, weight, activity_level,
                food_preferences, excluded_foods, user_id
            )
        )


def load_profile(user_id):
    """해당 사용자 본인의 프로필 조회."""
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM profiles WHERE user_id = ?",
            (user_id,)
        ).fetchone()


def save_meal_plan(user_id, plan_date, plan_data):
    """식단 정보를 문자열 형태로 저장."""
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO meal_plans (user_id, plan_date, plan_data)
            VALUES (?, ?, ?)
            """,
            (user_id, plan_date, plan_data)
        )


def load_meal_plans(user_id):
    """해당 사용자 본인의 식단 기록만 조회."""
    with get_connection() as conn:
        return conn.execute(
            """
            SELECT id, plan_date, plan_data, created_at
            FROM meal_plans
            WHERE user_id = ?
            ORDER BY created_at DESC
            """,
            (user_id,)
        ).fetchall()


# 앱을 실행할 때 테이블을 준비
init_db()
