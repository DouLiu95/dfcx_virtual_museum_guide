from py2neo import Node, Relationship, Graph
from component.question_classfier import *
from component.question_parser import *
import random

class ArtGraph:
    def __init__(self):
        self.g = Graph(
            scheme="bolt",
            host="localhost",
            port=7687,
            auth=("neo4j", "000000"))
        self.node_name_list = ['Paintings','Keyword','Country','Genre','Material','Collection','Person','Exhibition','Movement','City']
        self.Paintings = []
        self.Keyword = []
        self.Country = []
        self.Genre = []
        self.Material = []
        self.Collection = []
        self.Person = []
        self.Exhibition = []
        self.Movement  = []
        self.City = []
        self.num_limit = 20
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()
        with open('dict/Paintings.txt', encoding="utf-8") as f:
            self.Paintings = [i.strip() for i in f.readlines()]

        with open('dict/Keyword.txt', encoding="utf-8") as f:
            self.Keyword = [i.strip() for i in f.readlines()]

        with open('dict/Country.txt', encoding="utf-8") as f:
            self.Country = [i.strip() for i in f.readlines()]

        with open('dict/Genre.txt', encoding="utf-8") as f:
            self.Genre = [i.strip() for i in f.readlines()]

        with open('dict/Material.txt', encoding="utf-8") as f:
            self.Material = [i.strip() for i in f.readlines()]

        with open('dict/Collection.txt', encoding="utf-8") as f:
            self.Collection = [i.strip() for i in f.readlines()]



        with open('dict/Person.txt', encoding="utf-8") as f:
            self.Person = [i.strip() for i in f.readlines()]

        with open('dict/Exhibition.txt', encoding="utf-8") as f:
            self.Exhibition = [i.strip() for i in f.readlines()]

        with open('dict/Movement.txt', encoding="utf-8") as f:
            self.Movement = [i.strip() for i in f.readlines()]

        with open('dict/City.txt', encoding="utf-8") as f:
            self.City = [i.strip() for i in f.readlines()]
        # print(self.Paintings)

        self.exhibit_checked = []
        self.exhibit_unchecked = ['Two moors', 'King Caspar', 'Don Miguel de Castro, Emissary of Congo',
                                  'Diego Bemba, a Servant of Don Miguel de Castro',
                                  'Pedro Sunda, a Servant of Don Miguel de Castro',
                                  'Map of Paranambucae', 'Portrait of a Black Woman', 'Portrait of a Man',
                                  'Man in a Turban',
                                  'Head of a Boy in a Turban', 'Doritos',
                                  'The New Utopia Begins Here: Hermina Huiswoud',
                                  'The Unspoken Truth', 'Ilona', 'Head of a Boy', 'The Market in Dam Square']

        self.preference = {'Paintings': 1,
                           'Person': 1,
                           'Collection': 1,
                           'Exhibition': 1,
                           'Genre': 1,
                           'Keyword': 1,
                           'Movement': 1,
                           'Material': 1,
                           'Exhibit': len(self.exhibit_unchecked)}
        self.preference_list = ['Paintings','Keyword','Genre','Material','Collection','Person','Exhibition','Movement']

    def build_nodes(self):
        # kinds of nodes
        Paintings = []
        Keyword = []
        Country = []
        Genre = []
        Material = []
        Collection = []
        Person = []
        Exhibition = []
        Movement = []
        City = []
        nodes_list=[Paintings,Keyword,Country,Genre,Material,Collection,Person,Exhibition,Movement,City]
        # kinds of relations
        in_collection = [] #collection-[]-paintings
        keyword = [] # paintings-[]-depicts
        has_genre = [] # paintings - [] - genre
        has_material = [] # paintings - [] - material
        country = [] # paintings - [] - country

        for index,nodes in enumerate(self.node_name_list):
            print(nodes)
            sparql_for_name = "MATCH (n:"+str(nodes)+") RETURN n"
            nodes_data_all = self.g.run(str(sparql_for_name)).data()
            for node in nodes_data_all:
                try:
                    nodes_list[index].append(node['n']['name'])

                except :
                    pass

            # if nodes == 'Paintings':
            #     with open('./dict/' + str('title') + '.txt', 'w+', encoding="utf-8") as f:
            #         f.write('\n'.join(list(title)))
        # write the txt of data
            with open('./dict/'+str(nodes)+'.txt', 'w+',encoding="utf-8") as f:
                f.write('\n'.join(list(nodes_list[index])))


    def show_exhibit(self,exhibit_in_dialog):
        if exhibit_in_dialog in self.Paintings:
            sparql_for_name = "MATCH (n:Paintings) WHERE n.name = '" + str(exhibit_in_dialog) +"' RETURN n"
            data = self.g.run(str(sparql_for_name)).data()
            print(data)
            return data
        # elif exhibit_in_dialog in self.Paintings_title:
        #     sparql_for_name = "MATCH (n:Paintings) WHERE n.title = '" + str(exhibit_in_dialog) + "' RETURN n"
        #     data = self.g.run(str(sparql_for_name)).data()
        #     print(data)
        #     return data
        elif exhibit_in_dialog in self.Person:
            sparql_for_name = "MATCH (n:Person) WHERE n.name = '" + str(exhibit_in_dialog) + "' RETURN n"
            data = self.g.run(str(sparql_for_name)).data()
            print(data)
            return data
        else:
            return None

    def search_by_nodeId(self, nodeid):
        sparql_with_nodeid = "MATCH (n) WHERE id(n) = "+str(nodeid)+" RETURN n"
        data = self.g.run(str(sparql_with_nodeid)).data()
        print(data)
        return data

    def update_exhibit(self,exhibit_name):
        if exhibit_name in self.exhibit_unchecked:
            self.exhibit_unchecked.remove(exhibit_name)
            self.exhibit_checked.append(exhibit_name)
            self.preference['Exhibit'] = len(self.exhibit_unchecked)

    def update_user_preference(self,item):

        if item in self.Paintings and self.preference['Paintings'] <=10:
            self.preference['Paintings'] +=1
        if item in self.Collection and self.preference['Collection'] <=10:
            self.preference['Collection'] +=1
        if item in self.Exhibition and self.preference['Exhibition'] <=10:
            self.preference['Exhibition'] +=1
        if item in self.Genre and self.preference['Genre'] <=10:
            self.preference['Genre'] +=1
        if item in self.Keyword and self.preference['Keyword'] <=10:
            self.preference['Keyword'] +=1
        if item in self.Movement and self.preference['Movement'] <=10:
            self.preference['Movement'] +=1
        if item in self.Material and self.preference['Mterial'] <=10:
            self.preference['Mterial'] +=1
        if item in self.Person and self.preference['Person'] <=10:
            self.preference['Person'] +=1

    def decide_label_preference(self):
        target = random.randint(0,sum(self.preference.values()))
        sum_ = 0
        for k, v in self.preference.items():
            sum_ += v
            if sum_ >= target:
                return k

    def answer_prettify(self, question):
        data = self.classifier.classify(question)
        print('classified question is:',data)
        try:

            sqls = self.parser.parser_main(data)
            if not sqls:
                return None
            else:

                answer_neo4j = self.g.run(str(sqls[0]['sql'][0])).data()
                return answer_neo4j
        except:
            return None
        '''
        can not find anything related
        Return None and then either the ask for clarification or say sorry to the user
        '''


if __name__ == '__main__':
    handler = ArtGraph()
    # handler.build_nodes()
    # handler.create_graphrels()
    # handler.export_data()
    data = handler.show_exhibit('Rembrandt')
    print(data)
    print('Done')
    print(handler.decide_label_preference())
# graph.schema.node_labels

# graph.schema.relationship_types
