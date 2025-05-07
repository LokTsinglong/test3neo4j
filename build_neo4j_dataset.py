from build_node_relation import DataToNeo4j
import pandas as pd
test_data=pd.read_excel("test_data_Demo.xls",header=0)
# 采用excel文件读取，缺少依赖
# ImportError: Missing optional dependency 'xlrd'. Install xlrd >= 2.0.1 for xls Excel support Use pip or conda to install xlrd.
# pip install xlrd>=2.0.1
def data_extraction():
    #取出甲方名称到list
    node_buy_key=[]
    # 这里的[]是一个空列表，用于存储甲方名称
    for i in range(0,len(test_data)):
        node_buy_key.append(test_data['甲方名称'][i])
    
    node_sell_key=[]
    for j in range(0,len(test_data)):
        node_sell_key.append(test_data['乙方名称'][j])
    
    # 去除掉重复的发票名称
    node_buy_key=list(set(node_buy_key))
    node_sell_key=list(set(node_sell_key))

    node_list_value=[]
    for i in range(0,len(test_data)):
        for n in range(1,len(test_data.columns)):
            node_list_value.append(test_data[test_data.columns[n]][i])
            # 太奇怪了这里
    
    # 对第三列金额去重
    node_list_value=list(set(node_list_value))
    # 强制类型转换
    node_list_value=[str(i) for i in node_list_value]

    return node_buy_key,node_sell_key,node_list_value
    # data_extraction函数到此搞定

# 做一个小测试
# for n in test_data.columns:
#     print(n)
# print(test_data.columns[2])

# 关系提取的函数
def relation_extraction():
    links_dict={}
    sell_list=[]
    buy_list=[]
    money_list=[]
    for i in range(0,len(test_data)):
        sell_list.append(test_data['乙方名称'][i])
        buy_list.append(test_data['甲方名称'][i])
        money_list.append(test_data['金额'][i])
    
    # 强制类型转换
    sell_list=[str(i) for i in sell_list]
    buy_list=[str(i) for i in buy_list] 
    money_list=[str(i) for i in money_list]

    # 将三个list组合成一个字典
    links_dict['buy']=buy_list
    links_dict['sell']=sell_list    
    links_dict['money']=money_list

    # 将字典转化为DataFrame
    df_data=pd.DataFrame(links_dict)
    # 这里的df_data就是关系数据了
    print(df_data)

    return df_data
    # relation_extraction函数到此搞定

create_data=DataToNeo4j()
# 调用外部py子函数，先把图数据库建立好
create_data.create_node(data_extraction()[0],data_extraction()[1])
create_data.create_relation(relation_extraction())


