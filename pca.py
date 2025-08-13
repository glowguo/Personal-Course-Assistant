import csv

def get_courses(year=None, course_type=None):
    """
    根据指定的学年和/或课程类型，从CSV文件中获取课程列表。
    参数:
        year (str, optional): 筛选的学年，如 "第一学年"。默认为 None。
        course_type (str, optional): 筛选的课程类型，如 "专业主修课程（必修）"。默认为 None。
    返回:
        list: 包含课程名称的列表。
    """
    courses = []
    try:
        with open('courses.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # 跳过标题行
            for row in reader:
                # 确保行数据完整，避免索引错误
                if len(row) < 6:
                    continue

                # 检查筛选条件
                # 如果参数为 None，则视为匹配成功；否则，检查列内容是否相等
                year_match = (year is None) or (row[5] == year)
                type_match = (course_type is None) or (row[1] == course_type)

                # 只有所有条件都匹配，才添加课程
                if year_match and type_match:
                    courses.append(row[0].strip())
        return courses
    except FileNotFoundError:
        print("错误：courses.csv 文件未找到！")
        return []

# --- 主程序部分 ---

# 示例1：查找第一学年的所有课程
print("--- 示例1: 第一学年全部课程 ---")
first_year_courses = get_courses(year="第一学年")
for course in first_year_courses:
    print(f"待办：[ ] {course}")

print("\n" + "="*30 + "\n") # 打印分隔符

# 示例2：查找所有“专业主修课程（必修）”
print("--- 示例2: 所有专业主修课程（必修） ---")
required_major_courses = get_courses(course_type="专业主修课程（必修）")
for course in required_major_courses:
    print(f"待办：[ ] {course}")

print("\n" + "="*30 + "\n")

# 示例3：查找第一学年的“共同专业基础课程（必修）”
print("--- 示例3: 第一学年共同专业基础课程（必修） ---")
first_year_common_courses = get_courses(year="第一学年", course_type="共同专业基础课程（必修）")
for course in first_year_common_courses:
    print(f"待办：[ ] {course}")