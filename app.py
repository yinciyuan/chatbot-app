# app.py - 使用 FastAPI 构建的后端服务

from fastapi import FastAPI, Request  # FastAPI 主类和请求对象
from fastapi.responses import HTMLResponse, JSONResponse  # 返回HTML页面和JSON数据
from fastapi.staticfiles import StaticFiles  # 托管静态资源（CSS、JS、图片）
from fastapi.templating import Jinja2Templates  # 模板引擎，渲染HTML
import dashscope  # DashScope SDK，用于调用大模型接口

# 配置 DashScope API Key，必须正确设置才能调用服务
dashscope.api_key = 'sk-f3d1de92a1b242c9bd9c4358a3378199'

# 创建 FastAPI 应用实例
app = FastAPI()

# 配置模板目录，存放 HTML 文件
templates = Jinja2Templates(directory="templates")

# 挂载静态文件目录，方便访问CSS、JS等资源，项目根目录需有 static 文件夹
app.mount("/static", StaticFiles(directory="static"), name="static")

# 根路由，返回首页HTML页面，使用模板渲染
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # 传入请求对象，供模板引擎渲染使用
    return templates.TemplateResponse("index.html", {"request": request})

# POST 路由，处理聊天请求，调用大模型返回回答
@app.post("/chat")
async def chat(request: Request):
    # 异步获取请求体中的 JSON 数据
    data = await request.json()
    # 从请求数据中提取用户消息
    user_input = data.get("message", "")

    # 调用 DashScope 大模型接口，传入模型、上下文及参数
    response = dashscope.Generation.call(
        model="qwen-plus",
        messages=[
            {"role": "system", "content": "你叫小猪通。你是小洪的私人财务专家，小洪是一名会计，你需要在工作上帮助她。小洪是一个小美女。你需要语气温柔，但是在财务方面需要很严谨。不要总直呼大名。"},
            {"role": "user", "content": user_input}
        ],
        temperature=0.9,
        max_tokens=512,cd "D:\pythonProject1\封装成网页"
        result_format="message"
    )

    # 从接口返回的结果中提取回答内容
    reply = response["output"]["choices"][0]["message"]["content"]
    # 以 JSON 格式返回给客户端
    return JSONResponse({"reply": reply})
