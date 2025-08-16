# ==============================================================================
# 科技趋势分析小程序 - 核心分析引擎 (sva.py)
# 版本: Library Edition for FastAPI Integration
# 作者: 郭柏柏 & IS/DI Mentor
# 最后更新: 2025-08-16
# 核心改造: 移除了云函数入口(main_handler)，使其成为一个可被导入的Python模块。
# ==============================================================================

# 1. --- 核心库导入 ---
import os
import string
from io import BytesIO
from datetime import datetime

# 2. --- 第三方依赖库导入 ---
import jieba
import boto3
import matplotlib

# 【关键配置】设置matplotlib后端
matplotlib.use('Agg')
import matplotlib.pyplot as plt


# 3. --- 全局配置与知识库 ---

# 从环境变量中安全地获取配置 (FastAPI应用启动时会加载)
BUCKET_NAME = os.environ.get('BUCKET_NAME')
REGION = os.environ.get('TENCENTCLOUD_REGION', 'ap-beijing')
LATEST_PATH_FILE = 'metadata/latest_headlines_path.txt'
REPORTS_DIR = 'reports/'

# 领域专家知识库
SYNONYMS_CONFIG = {
    '数字化': ['数字化', '数字经济', '数智', '数转', '数字产业', '数字基础设施', '数字治理', '数字转型', '数字平台'],
    '人工智能': ['人工智能', 'ai', '智能', '大模型', '机器学习', '深度学习', '算法', '智能化', '智能系统', '智能应用', '智能硬件', '智能制造'],
    'SaaS': ['saas', '软件服务', '云服务', '云平台', 'paas', 'iaas', '订阅制', '企业服务', '云计算', '云解决方案'],
    # ... (此处省略你其他的同义词)
}


# 4. --- 初始化与预配置 ---

# 在服务器环境中，boto3可以依赖于配置好的IAM角色或环境变量来自动获取凭证
s3_client = boto3.client('s3', region_name=REGION)

def configure_matplotlib_for_chinese():
    """配置Matplotlib以正确显示中文。"""
    try:
        # 确保你的Ubuntu服务器上安装了中文字体，例如：sudo apt-get install fonts-wqy-zenhei
        plt.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei', 'SimHei']
    except Exception:
        print("警告：未能找到可用的中文字体，图表中的中文可能显示为方框。")
    plt.rcParams['axes.unicode_minus'] = False

# 在模块加载时，就执行一次字体配置
configure_matplotlib_for_chinese()


# 5. --- 核心业务逻辑函数 (完全暴露给外部调用) ---

def ultimate_text_analyzer(text_content, keywords_to_check, synonym_map=SYNONYMS_CONFIG):
    """终极中文文本分析器，结合了Jieba分词和同义词扩展。"""
    punctuation = string.punctuation + " " + "　" + "\n"
    processed_text = text_content.lower().translate(str.maketrans('', '', punctuation))
    tokens = jieba.cut(processed_text, cut_all=False)
    
    reverse_synonym_map = {syn.lower(): main for main, syn_list in synonym_map.items() for syn in syn_list}
    
    strategic_counts = {kw: 0 for kw in keywords_to_check}
    for word in tokens:
        if word in reverse_synonym_map:
            main_keyword = reverse_synonym_map[word]
            if main_keyword in strategic_counts:
                strategic_counts[main_keyword] += 1
                
    return strategic_counts

def save_chart_to_cos(results):
    """将分析结果图表直接上传到COS，并返回其对象键(Key)。"""
    keywords = list(results.keys())
    counts = list(results.values())
    
    plt.figure(figsize=(12, 7))
    plt.bar(keywords, counts, color='#0052FF')
    plt.title('科技趋势关键词频率分析', fontsize=16, color='#1F2937')
    plt.xlabel('核心概念', fontsize=12)
    plt.ylabel('提及频率', fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    
    img_data = BytesIO()
    plt.savefig(img_data, format='png', bbox_inches='tight')
    img_data.seek(0)
    plt.close()
    
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    report_key = f"{REPORTS_DIR}report_{timestamp}.png"
    
    # 【重要】确保BUCKET_NAME被正确获取
    if not BUCKET_NAME:
        raise ValueError("Error: BUCKET_NAME environment variable not set.")
        
    s3_client.put_object(Bucket=BUCKET_NAME, Key=report_key, Body=img_data, ContentType='image/png')
    
    return report_key

# 【改造完成】已删除所有 main_handler 和 if __name__ == "__main__" 部分