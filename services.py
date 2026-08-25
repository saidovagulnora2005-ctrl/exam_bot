from get_connection import get_connection

async def register(username,telegram_id):
    conn = await get_connection()
    try:
        user = await conn.fetchrow(""""
        select id from users whete username = $1 and telegram_id = $2""",username,telegram_id)
        if not user:
            await conn.execute("""
        insert into users(username)values(username)
    """, username)
            print("User registred successfully!")

    except Exception as error:
        print("Registration error: ", error)

    finally:
        await conn.close()


async def get_user(username):
    conn = await get_connection()
    try:
        user = await conn.fetchrow("""
    select username from users where username = $1
""", username)
    except Exception as error:
        print("Get user error: ", error)
    finally:
        await conn.close()



async def incomes(amount):
    conn = await get_connection()





