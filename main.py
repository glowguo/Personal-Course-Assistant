# main.py - FastAPI 应用总指挥官
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
import os

# 从我们的工具箱里，导入需要的工具
from sva import ultimate_text_analyzer, save_results_as_chart, SYNONYMS_CONFIG

# 1. 创建FastAPI应用实例
app = FastAPI()

# 2. 定义请求体的数据模型 (Pydantic)
class AnalyzeRequest(BaseModel):
    keywords: List[str]

# 3. 定义我们的API端点 (Endpoint)
@app.post("/api/v1/analyze")
async def analyze_trends(request: AnalyzeRequest):
    # a. 定义数据文件的路径
    #    (这里假设 weekly_task.py 会生成一个固定的最新文件名)
    headlines_file_path = "36kr_headlines.txt" 
    
    # b. 读取文本内容
    try:
        with open(headlines_file_path, 'r', encoding='utf-8') as f:
            text_to_analyze = f.read()
    except FileNotFoundError:
        return {"error": f"Data file not found at {headlines_file_path}"}

    # c. 调用我们的分析引擎
    analysis_result = ultimate_text_analyzer(
        text_to_analyze, 
        request.keywords, 
        SYNONYMS_CONFIG
    )
    
    # d. 调用我们的绘图引擎
    chart_path = save_results_as_chart(analysis_result)
    
    # e. 将生成的图表文件，作为响应直接返回
    return FileResponse(chart_path, media_type='image/png')

# 可以在根路径定义一个简单的“心跳”检测
@app.get("/")
def read_root():
    return {"Hello": "World"}