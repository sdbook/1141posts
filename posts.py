from psycopg_pool import AsyncConnectionPool #使用connection pool


async def getList(conn):
	async with conn.cursor() as cur:
		sql="select id,title from posts order by id desc;"
		await cur.execute(sql)
		rows = await cur.fetchall()
		return rows
	