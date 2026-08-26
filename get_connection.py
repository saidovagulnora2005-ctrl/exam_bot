import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()


async def get_connection():
    conn = await asyncpg.connect(
        host = "localhost",
        user = "postgres",
        database = "exam3_db",
        password = os.getenv("SQL_PASSWORD"),
        port = 5432,
    )
    return conn

async def init_tables():
    conn = await get_connection()
    try:
        await conn.execute("""
            create table if not exists users(
                id serial primary key,
                username varchar(20),
                balance numeric(9,2) default 0,
                telegram_id bigint unique
        );
            create table if not exists transactions(
                id serial primary key,
                type varchar(20) check(type = 'income' or type = 'expense'),
                description varchar(100),
                created_at timestamp default now(),
                amount numeric(9,2),
                due_date timestamp default now(),
                user_id bigint references users(id)
        );
""")
        print("Tables created successfully!")

    except Exception as error:
        print("Error in creating tables: ",error)
    finally:
        await conn.close()