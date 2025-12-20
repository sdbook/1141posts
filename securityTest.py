# main.py
from fastapi import FastAPI, Depends, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse,RedirectResponse

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")
from model.db import getDB
app = FastAPI()

#use session middleware for session mamagement
from starlette.middleware.sessions import SessionMiddleware
app.add_middleware(
    SessionMiddleware,
    secret_key="your-secret-key",
	max_age=None, #86400,  # 1 day
    same_site="lax",  # Options: 'lax', 'strict', 'none'
    https_only=False,  # Set to True in production with HTTPS,
)

#example of using dependency function for login check
def get_login_user(request: Request):
	user_id = request.session.get("user")
	#for not-login user, user_id will be None
	return user_id

@app.get("/")
async def root(request:Request,conn=Depends(getDB),user:str=Depends(get_login_user)):
	if user is None:
		#not login, redirect to loginForm
		return RedirectResponse(url="/loginForm.html", status_code=302)
	
	#return RedirectResponse(url="/homeVue.html", status_code=302)
	async with conn.cursor() as cur:
		sql="select id,title from posts order by id desc;"
		await cur.execute(sql)
		rows = await cur.fetchall()

	html="<hr/><ol>"
	for row in rows:
		html += f"<li>{row['title']}</li>"
	html += "</ol><hr />"


	html += f"""<h1>Hi {user}</h1>You are logged in. 
	<a href='/logout'>logout</a> <br/>
	新增資料:
	<form method="post" action="/addPost">
		<input type="text" name="title" />
		<input type="submit" />		
	</form>
	"""
	return HTMLResponse(html)
	#return templates.TemplateResponse("postList.html", {"request":request,"items": myList,"role": myRole})

@app.post("/addPost")
async def addPost(
	request:Request,
	title: str=Form(...),
	conn=Depends(getDB)
	):
	async with conn.cursor() as cur:
		sql=f"insert into posts (title) values ( '{title}')"
		print(sql)
		await cur.execute(sql)
		#sql=f"insert into post (title) values ( %s )"
		#await cur.execute(sql,(title,))

	return RedirectResponse(url="/", status_code=302)

@app.get("/logout")
async def logout(request: Request):
	request.session.clear()
	return RedirectResponse(url="/loginForm.html")

@app.post("/login") #receive login data from form post
async def login(
	request: Request,
	username: str = Form(...),
	password: str = Form(...),
	conn=Depends(getDB)
):
	#make your own credential check
	async with conn.cursor() as cur:
		sql=f"select * from users where id='{username}' and pwd='{password}';" 
		await cur.execute(sql)
		#sql="select * from user where id=%s and pwd=%s;"
		#await cur.execute(sql, (username,password))
		row = await cur.fetchone()
	if row: #has matched user
		request.session["user"] = row['name']
	else:
		request.session.clear()
		return HTMLResponse("Invalid credentials <a href='/loginForm.html'>login again</a>", status_code=401)
	return RedirectResponse(url="/", status_code=302)

app.mount("/", StaticFiles(directory="www"))