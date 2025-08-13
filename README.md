# 个人课程与文本分析助手 (Personal Course & Text Analyzer) V1.0

这是一个为信息系统与数字化创新 (IS & DI) 方向学习者打造的Python工具集，旨在通过自动化脚本提升学习与研究效率。本项目已完成V1.0的开发目标，具备了从文本分析到结果可视化的完整能力。

---

## ✨ 项目功能 (Features)

*   **个人课程助手 (`pca.py`)**: 从CSV文件读取和筛选课程信息。
*   **高级文本分析器 (`sva.py`)**:
    *   **专业NLP处理**: 集成NLTK库，实现智能分词、停用词移除和词干提取。
    *   **命令行驱动**: 通过`argparse`构建了灵活的命令行界面，实现代码与数据的完全分离。
    *   **数据可视化**: 集成Matplotlib，自动将分析结果生成清晰的条形图。

## 🚀 如何使用 (How to Use)

1.  确保你的电脑已安装 Python 环境及所需库。可以通过以下命令安装依赖：
    ```bash
    pip install nltk matplotlib
    ```
2.  克隆本仓库到本地。
3.  准备一个要分析的 `input.txt` 文件。
4.  在终端中运行 `sva.py` 脚本，并传入参数：

    **示例命令:**
    ```bash
    python sva.py input.txt --keywords platform network exchange --output report.png
    ```
    *   `input.txt`: 你要分析的源文本文件。
    *   `--keywords`: 你关心的核心词汇列表（用空格隔开）。
    *   `--output`: (可选) 你希望保存的图表文件名。

脚本将会在终端打印出词频报告，并生成一张名为 `report.png` 的可视化图表。

## ✅ V1.0 开发目标

- [x] 为 `sva.py` 引入更专业的NLP库（如 NLTK）。
- [x] 将两个脚本整合到一个更具交互性的命令行界面 (CLI) 中。
- [x] 探索将分析结果进行可视化的可能性（如使用 Matplotlib）。