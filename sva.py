import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import string
import argparse
import matplotlib
matplotlib.use('Agg') # <-- **核心修复**：在导入pyplot之前，设置后端
import matplotlib.pyplot as plt # 1. 导入 matplotlib

# ... (NLTK下载部分保持不变) ...
print("Ensuring NLTK data is available...")
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
print("NLTK data check complete.")

def analyze_text_with_nlp(text_content, keywords_to_check):
    # ... (这个函数本身的内容完全不变) ...
    lower_text = text_content.lower()
    no_punc_text = lower_text.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(no_punc_text)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(word) for word in filtered_tokens]
    word_counts = {}
    for stem in stemmed_tokens:
        word_counts[stem] = word_counts.get(stem, 0) + 1
    strategic_counts = {}
    for keyword in keywords_to_check:
        keyword_stem = stemmer.stem(keyword)
        count = word_counts.get(keyword_stem, 0)
        strategic_counts[keyword] = count
    return strategic_counts

# 2. 新增一个专门用于可视化的函数
def save_results_as_chart(results, output_filename):
    """将分析结果保存为一张条形图。"""
    
    # 准备图表数据
    keywords = list(results.keys())
    counts = list(results.values())
    
    # 创建图表
    plt.figure(figsize=(12, 7)) # 设置画布大小，让图表更清晰
    plt.bar(keywords, counts, color='skyblue')
    
    # 添加图表元素
    plt.title('Strategic Keyword Frequency Analysis', fontsize=16)
    plt.xlabel('Keywords', fontsize=12)
    plt.ylabel('Frequency Count', fontsize=12)
    plt.xticks(rotation=45, ha="right") # 旋转X轴标签，防止重叠
    
    # 优化布局并保存图表
    plt.tight_layout() # 自动调整布局，确保所有标签都能显示
    try:
        plt.savefig(output_filename)
        print(f"\nChart saved successfully to: {output_filename}")
    except Exception as e:
        print(f"\nError saving chart: {e}")

def main():
    parser = argparse.ArgumentParser(description="使用NLTK分析文本中的战略词汇频率，并生成可视化图表。")
    parser.add_argument("file_path", help="要分析的文本文件的路径。")
    parser.add_argument("--keywords", required=True, nargs='+', help="要检查的关键词列表（用空格分隔）。")
    # 3. 添加一个可选参数，用于指定图表输出路径
    parser.add_argument("--output", default="analysis_report.png", help="可视化图表的输出文件名。默认为 'analysis_report.png'。")
    
    args = parser.parse_args()
    
    try:
        with open(args.file_path, 'r', encoding='utf-8') as file:
            text_to_analyze = file.read()
    except FileNotFoundError:
        print(f"错误：文件未找到 -> {args.file_path}")
        return
        
    analysis_result = analyze_text_with_nlp(text_to_analyze, args.keywords)
    
    print(f"\n--- 分析报告: {args.file_path} ---")
    for keyword, count in analysis_result.items():
        print(f"概念 '{keyword}' (词干分析): {count} 次")
        
    # 4. 调用新的可视化函数
    # 只在有分析结果时才创建图表
    if analysis_result:
        save_results_as_chart(analysis_result, args.output)

if __name__ == "__main__":
    main()