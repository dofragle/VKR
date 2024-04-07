import networkx as nx
import matplotlib.pyplot as plt

def convert_to_conll_data(conll_string):

    # Разделение строки на подстроки по символу перевода строки
    conll_lines = conll_string[0].split('\n')

    # Создание списка conll_data и добавление каждой подстроки в список
    conll_data = []
    for line in conll_lines:
        conll_data.append(line)
    conll_data.remove('')
    return conll_data

def conll_to_graph(conll_data):

    G = nx.DiGraph()
    root_id = None  # Переменная для хранения ID корня
    for line in conll_data:
        if line.strip():  # Пропускаем пустые строки
            parts = line.split('\t')
            token_id = int(parts[0])
            word = parts[1]
            parent_id = int(parts[6])
            dep_rel = parts[7]
            if parent_id != 0:  # Пропускаем корень
                G.add_node(parent_id, word=conll_data[parent_id-1].split('\t')[1])
                G.add_node(token_id, word=word)
                G.add_edge(parent_id, token_id, dep_rel=dep_rel)
            else:
                root_id = token_id
    # Если есть корень, добавляем его, если нет, создаем новый узел
    if root_id is not None:
        G.add_node(root_id, word=conll_data[root_id-1].split('\t')[1])
    else:
        root_id = 0
        G.add_node(root_id, word="ROOT")
    return G, root_id
    
def draw_dependency_tree(G):

    pos = nx.multipartite_layout(G, subset_key="level")
    plt.figure(figsize=(10, 6))
    node_labels = {node: G.nodes[node]['word'] for node in G.nodes()}
    nx.draw(G, pos, with_labels=True, labels=node_labels, node_size=7000, node_color='skyblue', font_size=10, font_weight='bold', arrows=False)
    labels = nx.get_edge_attributes(G, 'dep_rel')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()


def show_result(conll_string):
    # Преобразование в граф и отображение дерева
    G, root_id = conll_to_graph(convert_to_conll_data(conll_string))
    # Определение уровней вершин
    levels = nx.shortest_path_length(G, source=root_id)
    for node, level in levels.items():
        G.nodes[node]["level"] = level
    draw_dependency_tree(G)

