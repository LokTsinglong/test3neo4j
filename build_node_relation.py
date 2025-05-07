from py2neo import Node, Graph, Relationship, NodeMatcher

class DataToNeo4j(object):
    def __init__(self):
        link=Graph("http://localhost:7474", auth=("neo4j", "123456"))
        self.graph=link
        self.buy="buy"
        self.sell="sell"
        self.graph.delete_all()
        self.matcher=NodeMatcher(self.graph)
    
    def create_node(self, node_buy_key,node_sell_key):
        for name in node_buy_key:
            buy_node=Node(self.buy, name=name)
            self.graph.create(buy_node)
        for name in node_sell_key:
            sell_node=Node(self.sell, name=name)
            self.graph.create(sell_node)

    def create_relation(self, df_data):
        m=0
        try:   
            for m in range(0,len(df_data)):
                # 打印关系里的buy和sell，where是匹配条件
                # dataframe里面都是字符串类型的
                # 注意_.name是py2neo的语法，字段搜索
                print(list(self.matcher.match(self.buy).where("_.name="+"'"+df_data['buy'][m]+"'")))
                print(list(self.matcher.match(self.sell).where("_.name="+"'"+df_data['sell'][m]+"'")))
                rel =Relationship(self.matcher.match(self.buy).where("_.name="+"'"+df_data['buy'][m]+"'").first(), df_data['money'][m], self.matcher.match(self.sell).where("_.name="+"'"+df_data['sell'][m]+"'").first())
                self.graph.create(rel)
        except AttributeError as e:
            print( e,m)
