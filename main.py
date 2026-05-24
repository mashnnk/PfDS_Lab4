import time
import pandas as pd
from sqlalchemy import create_engine, text

# --- Налаштування підключення ---
DB_USER     = "user"
DB_PASSWORD = "password"
DB_HOST     = "localhost"
DB_PORT     = 3306
DB_NAME     = "my_database"

CONNECTION_STRING = (
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

MAX_RETRIES = 10
RETRY_DELAY = 10  # секунд


def connect_with_retry() -> pd.DataFrame:
    """Підключається до БД, повторює спробу кожні 10 секунд (до 10 разів)."""
    engine = create_engine(CONNECTION_STRING)

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f"[{attempt}/{MAX_RETRIES}] Підключення до бази даних...")
            with engine.connect() as conn:
                df = pd.read_sql(text("SELECT * FROM titanic"), conn)
            print("Підключення успішне!\n")
            return df

        except Exception as e:
            print(f"База ще не готова: {e}")
            if attempt < MAX_RETRIES:
                print(f"Повтор через {RETRY_DELAY} секунд...\n")
                time.sleep(RETRY_DELAY)
            else:
                print("Вичерпано всі спроби. Завершення.")
                raise


if __name__ == "__main__":
    df = connect_with_retry()

    print(f"Рядків: {len(df)}, Колонок: {len(df.columns)}")
    print(f"Колонки: {df.columns.tolist()}\n")
    print(df.to_string())
