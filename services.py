from get_connection import get_connection


# 1
async def register(username,telegram_id):
    conn = await get_connection()
    try:
        user = await conn.fetchrow("""
        select id from users where username = $1 and telegram_id = $2""",username,int(telegram_id))
        if not user:
            await conn.execute("""Insert into users(username, telegram_id)values($1,$2)""", username, telegram_id)
            print("User registred successfully!")
            user = await conn.fetchrow("""
                select id from users where username = $1 and telegram_id = $2""",username,int(telegram_id))
            return user
    except Exception as error:
        print("Registration error: ", error)
    finally:
        await conn.close()

# 2
async def get_user(username):
    conn = await get_connection()
    try:
        user = await conn.fetchrow("""select id,username, telegram_id from users where username = $1""", username)
        return user
    except Exception as error:
        print("Get user error: ", error)
    finally:
        await conn.close()


# 3

async def add_transaction(user_id, amount, type, description):
    conn = await get_connection()
    try:
        balance = await conn.execute("""Select balance from users where id = $1""",user_id)
        bal = balance["balance"]
        if type == 'income':
            bal += int(amount)
        else:
            bal -= int(amount)

        await conn.execute("""
        update users set balance = $1 where id = $2""",bal, user_id)
        await conn.execute("""INSERT INTO transactions (user_id, type, amount, description) VALUES ($1, $2, $3, $4)""",user_id, type, amount, description)
        return bal
    except Exception as error:
        print("Add transaction error: ",error)
    finally:
        await conn.close()



# 4

async def get_balance(user_id):
    conn = await get_connection()
    try:
        income = await conn.fetchrow(
            """SELECT SUM(amount) as total from transactions where user_id = $1 and type = $2 """,user_id, 'income')

        expense = await conn.fetchrow(
            """SELECT SUM(amount) AS total from transactions where user_id = $1 and type = $2 """,user_id, 'expense')
        balance = income - expense
        return balance
    except Exception as error:
        print("Get balance error: ",error)
    finally:
        await conn.close()






# 5

async def transaction_history(user_id):
    conn = await get_connection()
    try:
        history = await conn.fetch(
            "SELECT type, amount, description, created_at from transactions where user_id = $1 ORDER BY created_at DESC ",user_id)
        return history
    finally:
        await conn.close()


    





