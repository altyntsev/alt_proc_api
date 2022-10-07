import alt_proc_path
from _import import *
import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder

import _global

import event.info
import event.list
import event.emit
import status.main
import task.save
import task.info
import task.list
import task.set_status
import proc.info
import proc.list
import cmds.set_status

app = FastAPI(dependencies=[Depends(auth.get_login)])
_global.app = app

app.include_router(event.info.router)
app.include_router(event.list.router)
app.include_router(event.emit.router)
app.include_router(status.main.router)
app.include_router(task.save.router)
app.include_router(task.info.router)
app.include_router(task.list.router)
app.include_router(task.set_status.router)
app.include_router(proc.info.router)
app.include_router(proc.list.router)
app.include_router(cmds.set_status.router)

app.add_middleware(CORSMiddleware, allow_origins=_global.cfg.cors, allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error = exc.errors()[0]
    msg = error['msg'] + ':' + error['loc'][-1]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": msg}),
    )


@app.on_event("startup")
async def startup_event():
    await _global.db.connect()


@app.get("/")
async def root():
    return RedirectResponse('/redoc')


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=_global.cfg.port,
                reload=True, reload_dirs=[_global.main_dir])
