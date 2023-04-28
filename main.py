import os
from models import request
from passages import savePassage
from passages import passageAnalysis
from fastapi import FastAPI

# 初始化，创建缓存目录：
if not os.path.exists('cache'):
    os.mkdir('cache')

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "This server is working normally."}


@app.post("/passage")
async def say_hello(req: request.SavePassageRequest):
    return savePassage.save_passage(req.content, req.token)


@app.post("/passage/{hash}")
async def action(hash: str, req: request.PassageRequest):
    if not os.path.exists(os.path.join('cache', hash)):
        return {
            "errno": 10001,
            "message": "hash对应的文件不存在，或者是文件读取异常"
        }
    return passageAnalysis.dispatch_action(req, hash)
