from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.staticfiles import StaticFiles

from routers import pages, charts

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(pages.router)
app.include_router(charts.router)


@app.exception_handler(HTTPException)
async def not_found_handler(request: Request, exc: HTTPException):
    if exc.status_code == 404:
        return pages.templates.TemplateResponse(request, "pages/404.html", {}, status_code=404)
    raise exc

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)
