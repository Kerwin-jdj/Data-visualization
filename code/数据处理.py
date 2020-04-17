import pandas as pd
import numpy as np
import re

df = pd.read_csv(r"D:\scrapy文件\job.csv")

# 数据清洗
print("去重之前的记录数", df.shape)
# 清洗之前的记录数
df.drop_duplicates(subset=["公司", "职位"], inplace=True)
print("清洗之后的记录数", df.shape)
# 清洗之后的记录数

# 对"职位"进行处理
# 职位名如python和Python是一样的，统一为小写即可
# print(df["职位"].value_counts())
df['职位'] = df['职位'].str.lower()


def get_title(x):
    # 去掉所有空格
    temp1 = re.sub(r'\s', '', x)
    # 去掉括号中的内容，英文的括号要加反斜杠
    temp2 = re.sub(r'\(.*?\)', '', temp1)
    # #去掉括号中的内容，中文括号
    title = re.sub(r'（.*?）', '', temp2)
    return title


df['职位'] = df['职位'].apply(get_title)

# 定义了一个想要替换的目标岗位title_list，将其转换为ndarray数组。
title_list = ['人工智能', 'ai', '数据分析', '数据挖掘', '深度学习',
              '机器学习', '爬虫', '大数据', '数据库', '嵌入式', '前端',
              '后端', 'web', '算法工程师', '开发工程师', '系统工程师',
              '架构师', '软件工程师', '运维', '测试', '安全', '运营']
title_list = np.array(title_list)


# 定义一个函数，若某条记录包含title_list数组中的某个关键词，
# 就将该条记录替换为这个关键词，多个关键词则取第一个即可。
def rename(x):
    index = [i in x for i in title_list]
    if sum(index) > 0:
        return title_list[index][0]
    else:
        return x


df["职位"] = df["职位"].apply(rename)
index = [df["职位"].str.count(i) for i in title_list]
index = np.array(index).sum(axis=0) > 0
df = df[index]  # 把没有归类的数据全部丢弃
df.loc[:, "职位"] = df["职位"].apply(lambda x: re.sub("ai", "人工智能", x))  # ai即为人工智能
# print(df["职位"].value_counts())


# 对"工资"字段处理
# 处理工资水平字段。针对工资水平字段“20-30万/年”、“2.5-3万/月”和“3.5-4.5千/月”这样的格式，将数据格式转换为“元/月”，求出工资的平均值。
# 针对20万以上/年和100元/天的数据，由于样本量较小，丢弃这些数据
index1 = df["工资"].str[-1].isin(["年", "月"])
index2 = df["工资"].str[-3].isin(["万", "千"])
df = df[index1 & index2]


def get_salary(x):
    if x[-3] == "万":
        temp = [float(i) * 10000 for i in re.findall(r"\d+\.?\d*", x)]
    elif x[-3] == "千":
        temp = [float(i) * 1000 for i in re.findall(r"\d+\.?\d*", x)]
    if x[-1] == "年":
        temp = [i / 12 for i in temp]
    return temp


salary = df["工资"].apply(get_salary)
df["最低工资"] = salary.str[0]
df["最高工资"] = salary.str[1]
df["平均工资"] = df[["最低工资", "最高工资"]].mean(axis=1)


# print(df["平均工资"])

# 工作地点去掉"-"后的区级单位
def get_location(x):
    temp1 = re.sub(r'\s', '', x)
    temp2 = temp1.split("-")
    return temp2[0]


df["工作地点"] = df["工作地点"].apply(get_location)


# print(df["工作地点"].value_counts())

# 对"工作经验"处理
def get_experience(x):
    # 去掉数据中的空格、制表符
    temp1 = re.sub(r'\s', '', x)
    # 将"招*人"替换成"无需经验""
    temp2 = re.sub(r"招\d+人", "无需经验", temp1)
    # 将不是数字开头的字符串，例如"本科"替换为"无需经验""
    experience = re.sub(r'^\D+', '无需经验', temp2)
    return experience


df["工作经验"] = df["工作经验"].apply(get_experience)


# print(df["工作经验"].value_counts())

# 对"学历"处理
def get_education(x):
    # 去掉数据中的空格、制表符
    temp1 = re.sub(r'\s', '', x)
    # 将"招*人"替换成"不限""
    temp2 = re.sub(r"招.*人", "不限", temp1)
    # 将数字开头的字符串，例如"2年经验"替换为"不限""
    education = re.sub(r"0.*", "不限", temp2)
    return education


df["学历"] = df["学历"].apply(get_education)


# print(df["学历"].value_counts())
print(df.info())

df.to_csv("处理好的数据.csv")