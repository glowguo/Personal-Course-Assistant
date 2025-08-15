# main.py - The FastAPI Application
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# 导入我们sva.py里的核心逻辑
# 注意：我们需要对sva.py稍作改造，让它的函数可以被导入
from sva import ultimate_text_analyzer, save_chart_to_cos, s3_client, BUCKET_NAME, LATEST_PATH_FILE

# 1. 初始化FastAPI应用
app = FastAPI()

# 2. 定义请求体的数据模型 (Pydantic会自动进行数据校验)
class AnalyzeRequest(BaseModel):
    keywords: list[str]

# 3. 定义我们的API Endpoint
@app.post("/api/v1/analyze")
async def analyze_trends(request: AnalyzeRequest):
    try:
        # 4. 从COS读取数据
        path_object = s3_client.get_object(Bucket=BUCKET_NAME, Key=LATEST_PATH_FILE)
        data_file_path = path_object['Body'].read().decode('utf-8').strip()
        data_object = s3_client.get_object(Bucket=BUCKET_NAME, Key=data_file_path)
        text_to_analyze = data_object['Body'].read().decode('utf-8')

        # 5. 调用核心分析逻辑
        analysis_result = ultimate_text_analyzer(text_to_analyze, request.keywords)

        # 6. 生成图表并上传
        report_key = save_chart_to_cos(analysis_result)
        
        # 7. 生成预签名URL
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': report_key},
            ExpiresIn=300
        )
        
        # 8. 返回成功的响应
        return {
            "code": 0, "message": "Success",
            "data": { "chart_url": presigned_url, "analysis_results": analysis_result }
        }

    except Exception as e:
        # 抛出HTTP异常，FastAPI会自动处理成标准的错误响应
        raise HTTPException(status_code=500, detail=str(e))