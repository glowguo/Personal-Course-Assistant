import spacy
from collections import Counter

try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    print("错误：spaCy英文模型 'en_core_web_sm' 未找到。")
    print("请在你的终端运行: python -m spacy download en_core_web_sm")
    exit() # 如果模型不存在，则退出程序

def analyze_text_with_spacy(text_content, keywords_to_check):
    """
    使用spaCy进行词形还原，分析文本中指定概念的出现频率。
    
    参数:
        text_content (str): 要分析的完整文本。
        keywords_to_check (list): 你关心的概念原型列表（如 'study', 'company'）。
        
    返回:
        dict: 一个包含每个概念及其总计数的字典。
    """
    
    # 1. 使用spaCy处理文本
    # nlp()返回一个Doc对象，它包含了文本的各种语言学注解
    doc = nlp(text_content.lower())
    
    # 2. 提取所有单词的原型 (lemma)
    # 我们只关心字母组成的单词，并排除代词和停用词（常见的、无分析意义的词）
    lemmas = [
        token.lemma_ for token in doc 
        if token.is_alpha and not token.is_stop
    ]
    
    # 3. 统计所有词形原型的频率
    lemma_counts = Counter(lemmas)
    
    # 4. 提取我们关心的概念的频率
    strategic_counts = {}
    for keyword in keywords_to_check:
        strategic_counts[keyword] = lemma_counts.get(keyword, 0)
        
    return strategic_counts

# --- 使用我们升级后的工具 ---

# a. 定义一个更复杂的文本，包含各种词形变化
text_snippet_advanced = """
Successful companies are studying the art of platform strategy. Their studies
show that a company's value is increasingly tied to the network it manages. 
This new business model involves exchanging traditional pipelines for platforms,
a change that many users are actively embracing. The study of these dynamics
is crucial for any modern producer or consumer.
"""
# 注意：这里我们只需要提供单词的原型
strategic_keywords_to_analyze = ['platform', 'network', 'exchange', 'user', 'value', 'study', 'company']

# b. 调用新函数，获取分析结果
analysis_result = analyze_text_with_spacy(text_snippet_advanced, strategic_keywords_to_analyze)

# c. 打印结果
print("--- 战略词汇频率分析 (V3.0 with spaCy) ---")
for keyword, count in analysis_result.items():
    print(f"概念 '{keyword}' (含所有变体): {count} 次")
