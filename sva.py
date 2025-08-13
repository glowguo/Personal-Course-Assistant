import string
import argparse
import jieba
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# 终极版分析引擎配置
SYNONYMS_CONFIG = {
    '数字化': ['数字化', '数字经济', '数智', '数转', '数字产业', '数字基础设施', '数字治理', '数字转型', '数字平台'],
    '人工智能': ['人工智能', 'ai', '智能', '大模型', '机器学习', '深度学习', '算法', '智能化', '智能系统', '智能应用', '智能硬件', '智能制造'],
    'SaaS': ['saas', '软件服务', '云服务', '云平台', 'paas', 'iaas', '订阅制', '企业服务', '云计算', '云解决方案'],
    '创新': ['创新', '创意', '研发', '技术突破', '新技术', '新模式', '新业态', '创新驱动', '创新生态'],
    '产业': ['产业', '行业', '赛道', '领域', '生态', '产业链', '产业升级', '产业互联网', '产业数字化'],
    '创业': ['创业', '创企', '初创', '创投', '风险投资', '孵化', '创业者', '创业项目'],
    '资本': ['资本', '投资', '融资', '股权', '基金', 'vc', 'pe', '天使投资', '并购'],
    '平台': ['平台', '生态平台', '数字平台', '服务平台', '交易平台', '创新平台'],
    '大数据': ['大数据', '数据分析', '数据挖掘', '数据治理', '数据平台', '数据智能', '数据驱动'],
    '云计算': ['云计算', '云服务', '云平台', '云基础设施', '云解决方案', '云原生', '云安全'],
    '区块链': ['区块链', '分布式账本', '智能合约', '数字货币', '加密货币', '链上', '链下', '去中心化'],
    '元宇宙': ['元宇宙', '虚拟现实', '增强现实', '数字孪生', '虚拟空间', '虚拟人', '数字资产'],
    '自动化': ['自动化', '智能自动化', '流程自动化', '机器人', 'rpa', '自动控制', '自动系统'],
    '低代码': ['低代码', '无代码', '开发平台', '敏捷开发', '快速开发', '应用生成'],
    '5G': ['5g', '新基建', '通信技术', '无线网络', '高速网络', '物联网'],
    '物联网': ['物联网', 'iot', '智能设备', '传感器', '联网', '智能家居', '智能城市'],
    '智能制造': ['智能制造', '工业互联网', '工业4.0', '智能工厂', '数字工厂', '自动化生产'],
    '数字医疗': ['数字医疗', '智慧医疗', '医疗信息化', '远程医疗', '医疗ai', '健康管理'],
    '新能源': ['新能源', '光伏', '风能', '储能', '电池', '绿色能源', '能源转型'],
    '绿色科技': ['绿色科技', '环保', '碳中和', '绿色创新', '可持续', '节能减排'],
    '智能交通': ['智能交通', '自动驾驶', '车联网', '智慧出行', '交通数字化', '交通ai'],
    '数字金融': ['数字金融', '金融科技', 'fintech', '数字货币', '区块链金融', '智能投顾'],
    '云安全': ['云安全', '网络安全', '信息安全', '数据安全', '安全防护', '安全合规'],
}

def configure_matplotlib_for_chinese():
    # ... (此函数保持不变) ...
    try:
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
    except Exception:
        print("警告：未能找到可用的中文字体，图表中的中文可能显示为方框。")
    plt.rcParams['axes.unicode_minus'] = False

configure_matplotlib_for_chinese()

def ultimate_text_analyzer(text_content, keywords_to_check, synonym_map):
    """
    终极中文文本分析器，结合了Jieba分词和同义词扩展。
    """
    # 1. 精确分词
    # 移除标点和空格，并转为小写，以便匹配不区分大小写的同义词（如AI vs ai）
    punctuation = string.punctuation + " " + "　"
    processed_text = text_content.lower().translate(str.maketrans('', '', punctuation))
    tokens = jieba.cut(processed_text, cut_all=False)
    
    # 2. 创建一个反向映射：从同义词找到主关键词
    # 例如: {'ai': '人工智能', '大模型': '人工智能'}
    reverse_synonym_map = {}
    for main_keyword, syn_list in synonym_map.items():
        for synonym in syn_list:
            reverse_synonym_map[synonym.lower()] = main_keyword

    # 3. 统计主关键词的出现次数
    strategic_counts = {kw: 0 for kw in keywords_to_check}
    for word in tokens:
        if word in reverse_synonym_map:
            main_keyword = reverse_synonym_map[word]
            if main_keyword in strategic_counts:
                strategic_counts[main_keyword] += 1
                
    return strategic_counts

def save_results_as_chart(results, output_filename):
    # ... (此函数保持不变) ...
    keywords = list(results.keys())
    counts = list(results.values())
    plt.figure(figsize=(12, 7))
    plt.bar(keywords, counts, color='skyblue')
    plt.title('关键词频率分析报告', fontsize=16)
    plt.xlabel('关键词', fontsize=12)
    plt.ylabel('频率', fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(output_filename)
    print(f"\n图表已成功保存到: {output_filename}")

def main():
    parser = argparse.ArgumentParser(description="终极文本分析工具，支持同义词扩展。")
    # ... (main函数保持不变) ...
    parser.add_argument("file_path", help="要分析的文本文件的路径。")
    parser.add_argument("--keywords", required=True, nargs='+', help="要检查的主关键词列表。")
    parser.add_argument("--output", default="analysis_report.png", help="可视化图表的输出文件名。")
    
    args = parser.parse_args()
    
    try:
        with open(args.file_path, 'r', encoding='utf-8') as file:
            text_to_analyze = file.read()
    except FileNotFoundError:
        print(f"错误：文件未找到 -> {args.file_path}")
        return
        
    analysis_result = ultimate_text_analyzer(text_to_analyze, args.keywords, SYNONYMS_CONFIG)
    
    print(f"\n--- 分析报告: {args.file_path} ---")
    if not any(analysis_result.values()):
        print("未在文本中找到任何指定的关键词。")
    else:
        for keyword, count in analysis_result.items():
            print(f"概念 '{keyword}': {count} 次")
    
    if any(analysis_result.values()):
        save_results_as_chart(analysis_result, args.output)

if __name__ == "__main__":
    main()