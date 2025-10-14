from psycopg_pool import AsyncConnectionPool #使用connection pool


async def getList(conn):
	async with conn.cursor() as cur:
		sql="select id,title from posts order by id desc;"
		await cur.execute(sql)
		rows = await cur.fetchall()
		return rows

async def getPost(conn, id):
	async with conn.cursor() as cur:
		sql="select id,title, content from posts where id=%s;"
		await cur.execute(sql,(id,))
		row = await cur.fetchone()
		return row