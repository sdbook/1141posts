from fastapi import FastAPI, Form, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import HTTPException, status
from fastapi.staticfiles import StaticFiles

#宣告一個fastAPI應用
app = FastAPI()

from starlette.middleware.sessions import SessionMiddleware
app.add_middleware(
    SessionMiddleware,
    secret_key="your-secret-key",
	max_age=None, #86400,  # 1 day
    same_site="lax",  # Options: 'lax', 'strict', 'none'
    https_only=False,  # Set to True in production with HTTPS,
)

#example of using dependency function for login check
def get_current_user(request: Request):
	user_id = request.session.get("user")
	if not user_id:
		raise HTTPException(status_code=401, detail="Not authenticated")
	return user_id


@app.get("/")
async def home(request: Request, user:str =Depends(get_current_user)): #use Depends on chkRole with constant parameter
	return {"message": f"Welcome back, {user}!"}

@app.get("/logout")
async def logout(request: Request):
	request.session.clear()
	return RedirectResponse(url="/loginForm.html")

@app.post("/login") #receive login data from form post
async def login(
	request: Request,
	username: str = Form(...),
	password: str = Form(...),
):
	#make your own credential check
	if username=='user' and password == 'pass':
		request.session["user"] = username
		return RedirectResponse(url="/", status_code=302)
	return HTMLResponse("Invalid credentials <a href='/loginForm.html'>login again</a>", status_code=401)

app.mount("/", StaticFiles(directory="www"))