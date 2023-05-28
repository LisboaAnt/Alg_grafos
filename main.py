#Importante!!!!
#Antônio Lisboa De cravalho - 535865
#São as 6 da manhã e vou dar uma pequena explicada de como funciona:
#Ele inicia pelo vertice com maior grau de saida, se empatar acho q inicia por ordem alfabetica
#Depois de iniciar ele busca o proximo vertice Branco, se tiver mais de um ele pega na ordem
#Usei inicialmente seu codigo como base, mas não deu pra continuar com ele, só aproveitei a recursão
#Usei o tk(canvas) para fazer a janela, não conseguir colocar o tipo da seta em cima dela por isso das cores(ficou melhor)
#Espero que esteja tudo funcionando, Amém

import math
import tkinter as tk

def ler_graph(file_name):
    graph = {}
    with open(file_name, 'r') as file:
        for line in file:
            vertices = line.strip().split()
            if len(vertices) == 2:
                u, v = vertices
                if u not in graph:
                    graph[u] = []
                graph[u].append(v)
    return graph #retorna um dicionário representando o grafo, Cada chave do dicionário é um vértice do grafo e o valor associado é uma lista de vértices adjacentes

def get_grau_saida(graph):#Recebe um grafo representado por um dicionário e retorna um dicionario com os graus de saida de cada vértice
    out_degrees = {}
    for u in graph:
        out_degrees[u] = len(graph[u])
    return out_degrees #graus de saída de cada vértice

def get_ordenado_saida(graph): #Recebe um grafo representado por um dicionario
    out_degrees = get_grau_saida(graph)
    sorted_vertices = sorted(out_degrees.keys(), key=lambda v: out_degrees[v], reverse=True)
    return sorted_vertices #retorna uma lista de vertices ordenados por seus graus de saida em ordem decrescente

def dfs(graph): #Realiza uma busca em profundidade
    def dfs_visit(u):
        nonlocal mark, seta_tipo
        cor[u] = 'CINZA'
        mark += 1
        d[u] = mark
        if u in graph:
            for v in graph[u]:
                if cor[v] == 'BRANCO':
                    seta_tipo[(u, v)] = 'Árvore'
                    dfs_visit(v)
                elif cor[v] == 'CINZA':
                    seta_tipo[(u, v)] = 'Retorno'
                elif d[u] < d[v]:
                    seta_tipo[(u, v)] = 'Avanço'
                else:
                    seta_tipo[(u, v)] = 'Cruzamento'
        cor[u] = 'PRETO'
        mark += 1
        f[u] = mark

    cor = {}
    d = {}
    f = {}
    mark = 0
    seta_tipo = {}

    sorted_vertices = get_ordenado_saida(graph)

    for u in sorted_vertices:
        cor[u] = 'BRANCO'

    for u in sorted_vertices:
        if cor[u] == 'BRANCO':
            dfs_visit(u)

    return d, f, seta_tipo

def distribute_circularly(num_vertices, radius, center_x, center_y): #Distribui os vertices de um grafo circularmente ao redor de um ponto central
    coordinates = []
    angle = 2 * math.pi / num_vertices
    for i in range(num_vertices):
        x = center_x + radius * math.cos(i * angle)
        y = center_y + radius * math.sin(i * angle)
        coordinates.append((x, y))
    return coordinates

def draw_graph(graph, edge_types, d, f): 
    #Utiliza a biblioteca tkinter para desenhar o grafo na tela
    #Recebe como entrada o grafo, os tipos de arestas, e as informacoes de descoberta e finalizacao de cada vertice obtidos pela funcao dfs
    window = tk.Tk()
    canvas = tk.Canvas(window, width=500, height=500)
    canvas.pack()

    num_vertices = len(graph)
    center_x = 250
    center_y = 250
    radius = 200
    vertex_coords = distribute_circularly(num_vertices, radius, center_x, center_y)

    vertex_objects = {}
    for i, vertex in enumerate(graph):
        x, y = vertex_coords[i]
        vertex_objects[vertex] = canvas.create_oval(x-15, y-15, x+15, y+15, fill='white', outline='black')
        canvas.create_text(x, y, text=vertex)

    animation_speed = 0.9  # Velocidade da animação (em segundos)
    lines = []
    for edge, edge_type in edge_types.items():
        u, v = edge
        x1, y1 = vertex_coords[list(graph.keys()).index(u)]
        x2, y2 = vertex_coords[list(graph.keys()).index(v)]
        if edge_type == 'Árvore':
            color = 'green'
        elif edge_type == 'Retorno':
            color = 'red'
        elif edge_type == 'Avanço':
            color = 'blue'
        else:
            color = 'orange'
        
        line = canvas.create_line(x1, y1, x2, y2, fill=color, arrow=tk.LAST, state='hidden')
        lines.append(line)

    def show_next_line():
        nonlocal current_line
        if current_line < len(lines):
            canvas.itemconfigure(lines[current_line], state='normal')
            current_line += 1
            window.after(int(animation_speed * 1000), show_next_line)

    def show_previous_line():
        nonlocal current_line
        if current_line > 0:
            current_line -= 1
            canvas.itemconfigure(lines[current_line], state='hidden')

    def show_d_f_values():
        x = 10
        y = canvas.winfo_height() + 480

        d_text = "d: "
        f_text = "f: "

        for u in d:
            d_text += f"{d[u]} "
            f_text += f"{f[u]} "

        canvas.create_text(x, y, text=d_text, anchor="sw")
        canvas.create_text(x, y - 15, text=f_text, anchor="sw")

        canvas.create_text(+250,+480,text="Use 'a' para vançar e 'd' para voltar a animação",anchor="sw")

        #for u in graph:
        #print(u,"= ", "d:", d[u], "f:", f[u])
        canvas.create_text(350,80, text="""
        Árvore = Verde
        Retorno = Vermelho
        Avanço = Azul
        Cruzamento = Laranja
        """,anchor="sw")
        #Mostra na tela d e f de cada vertice
        ii = 5
        for u in graph:
            ii +=15
            canvas.create_text(+10,ii,text=u+" {"+"d: "+str(d[u])+ " f: "+str(f[u])+"}",anchor="sw")


    def bind_keys(event):
        if event.keysym == 'd':
            show_next_line()
        elif event.keysym == 'a':
            show_previous_line()
    
    canvas.bind('<Key>', bind_keys)
    canvas.focus_set()

    current_line = 0
    show_next_line()
    show_d_f_values()

    window.mainloop()

graph = ler_graph("grafo.txt")
d, f, edge_types = dfs(graph)
draw_graph(graph, edge_types, d, f)

