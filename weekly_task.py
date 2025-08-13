import os
import subprocess
from datetime import datetime

def run_news_tracker():
    """运行新闻采集器，如果失败则返回None。"""
    date_str = datetime.now().strftime('%Y-%m-%d')
    output_file = f"36kr_headlines_{date_str}.txt"
    print(f"[采集] 运行 news_tracker.py，输出文件：{output_file}")
    
    try:
        # 我们需要让 news_tracker.py 接受 --output 参数
        subprocess.run(
            ["python", "news_tracker.py", "--output", output_file], 
            check=True,  # check=True 会在命令失败时抛出异常
            capture_output=True, # 捕获子进程的输出
            text=True # 以文本形式捕获
        )
        print(f"[采集] 成功完成！")
        return output_file
    except subprocess.CalledProcessError as e:
        # 捕获异常，打印错误信息，然后返回None
        print(f"[采集] 失败！错误信息如下：")
        print(e.stderr) # 打印子进程的标准错误输出
        return None

def run_sva_analysis(input_file):
    """运行文本分析器。"""
    date_str = datetime.now().strftime('%Y-%m-%d')
    report_file = f"report_{date_str}.png"
    keywords = ["数字化", "人工智能", "SaaS", "创新", "资本"] # 你可以按需修改
    print(f"[分析] 运行 sva.py，输入文件：{input_file}，关键词：{keywords}，输出图表：{report_file}")
    
    try:
        subprocess.run(
            ["python", "sva.py", input_file, "--keywords", *keywords, "--output", report_file],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"[分析] 成功完成！")
        return report_file
    except subprocess.CalledProcessError as e:
        print(f"[分析] 失败！错误信息如下：")
        print(e.stderr)
        return None

if __name__ == "__main__":
    print("--- 开始执行每周自动化任务 ---")
    
    # 1. 采集数据
    headlines_file = run_news_tracker()
    
    # 2. 只有在采集成功时，才进行分析 (熔断机制)
    if headlines_file and os.path.exists(headlines_file):
        report_file = run_sva_analysis(headlines_file)
        if report_file:
            print(f"\n[成功] 自动化任务完成！")
            print(f"新闻数据：{headlines_file}")
            print(f"分析报告：{report_file}")
        else:
            print(f"\n[失败] 分析步骤执行失败。")
    else:
        print(f"\n[失败] 数据采集步骤失败，任务中止。")