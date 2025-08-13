import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import string # 引入string库，更高效地处理标点

# --- 首次运行时需要下载NLTK的数据包 ---
try:
    stopwords.words('english')
except LookupError:
    print("Downloading NLTK data (stopwords)...")
    nltk.download('stopwords')
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("Downloading NLTK data (punkt)...")
    nltk.download('punkt')
# -----------------------------------------


def analyze_text_with_nlp(text_content, keywords_to_check):
    """
    使用NLTK库，对文本进行专业的词频分析。
    
    该函数会进行以下处理：
    1. 转换为小写
    2. 移除所有标点符号
    3. 智能分词 (Tokenization)
    4. 移除停用词 (Stopwords)
    5. 词干提取 (Stemming)
    
    参数:
        text_content (str): 要分析的完整文本。
        keywords_to_check (list): 你关心的战略关键词列表（单数形式）。
        
    返回:
        dict: 一个包含每个关键词词干及其计数的字典。
    """
    
    # 1. 转换为小写
    lower_text = text_content.lower()
    
    # 2. 移除标点 (更高效的方式)
    no_punc_text = lower_text.translate(str.maketrans('', '', string.punctuation))
    
    # 3. 智能分词
    tokens = word_tokenize(no_punc_text)
    
    # 4. 移除停用词
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    
    # 5. 词干提取
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(word) for word in filtered_tokens]
    
    # 6. 统计词干频率
    word_counts = {}
    for stem in stemmed_tokens:
        word_counts[stem] = word_counts.get(stem, 0) + 1
        
    # 7. 检查我们关心的战略词汇的词干频率
    strategic_counts = {}
    for keyword in keywords_to_check:
        # 我们也需要检查关键词本身的词干
        keyword_stem = stemmer.stem(keyword)
        count = word_counts.get(keyword_stem, 0)
        strategic_counts[keyword] = count
        
    return strategic_counts

# --- 使用我们升级后的工具 ---

text_snippet = """
A platform is a business model that creates value by facilitating exchanges 
between two or more interdependent groups, usually consumers and producers. 
In order to make these exchanges happen, platforms harness and create large, 
scalable networks of users and resources that can be accessed on demand. 
Platforms create communities and markets with network effects that allow 
users to interact and transact. The key is the network effect.
"""
# 依然只需要提供单数形式
strategic_keywords_to_analyze = ['platform', 'network', 'exchange', 'user', 'value', 'market']

analysis_result = analyze_text_with_nlp(text_snippet, strategic_keywords_to_analyze)

print("--- 战略词汇频率分析 (V3.0 with NLTK) ---")
for keyword, count in analysis_result.items():
    print(f"概念 '{keyword}' (词干分析): {count} 次")