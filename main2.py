import math
import tkinter as tk

def ler_grafo(nome_arquivo):
    grafo = {}
    with open(nome_arquivo, 'r') as arquivo:
        for linha in arquivo:
            vertices = linha.strip().split()
            if len(vertices) == 2:
                u, v = vertices
                if u not in grafo:
                    grafo[u] = []
                grafo[u].append(v)
    return grafo  # retorna um dicionário representando o grafo, cada chave do dicionário é um vértice do grafo e o valor associado é uma lista de vértices adjacentes

def obter_grau_saida(grafo):  # Recebe um grafo representado por um dicionário e retorna um dicionario com os graus de saída de cada vértice
    graus_saida = {}
    for u in grafo:
        graus_saida[u] = len(grafo[u])
    return graus_saida  # graus de saída de cada vértice

def obter_vertices_ordenados_saida(grafo):  # Recebe um grafo representado por um dicionario
    graus_saida = obter_grau_saida(grafo)
    vertices_ordenados = sorted(graus_saida.keys(), key=lambda v: graus_saida[v], reverse=True)
    return vertices_ordenados  # retorna uma lista de vertices ordenados por seus graus de saída em ordem decrescente

def dfs(grafo):  # Realiza uma busca em profundidade
    def dfs_visit(u):
        nonlocal cor, mark, seta_tipo
        cor[u] = 'CINZA'
        mark += 1
        d[u] = mark
        if u in grafo:
            for v in grafo[u]:
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

    vertices_ordenados = obter_vertices_ordenados_saida(grafo)

    for u in vertices_ordenados:
        cor[u] = 'BRANCO'

    for u in vertices_ordenados:
        if cor[u] == 'BRANCO':
            dfs_visit(u)

    return d, f, seta_tipo

def distribuir_circularmente(num_vertices, raio, centro_x, centro_y):  # Distribui os vertices de um grafo circularmente ao redor de um ponto central
    coordenadas = []
    angulo = 2 * math.pi / num_vertices
    for i in range(num_vertices):
        x = centro_x + raio * math.cos(i * angulo)
        y = centro_y + raio * math.sin(i * angulo)
        coordenadas.append((x, y))
    return coordenadas

def desenhar_grafo(grafo, tipos_aresta, d, f):
    # Utiliza a biblioteca tkinter para desenhar o grafo na tela
    # Recebe como entrada o grafo, os tipos de arestas, e as informacoes de descoberta e finalizacao de cada vertice obtidos pela funcao dfs
    janela = tk.Tk()
    canvas = tk.Canvas(janela, width=620, height=500)  # Janela
    canvas.pack()

    num_vertices = len(grafo)
    centro_x = 250
    centro_y = 250
    raio = 200
    coordenadas_vertices = distribuir_circularmente(num_vertices, raio, centro_x, centro_y)

    objetos_vertices = {}
    for i, vertice in enumerate(grafo):
        x, y = coordenadas_vertices[i]
        objetos_vertices[vertice] = canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill='white', outline='black')
        canvas.create_text(x, y, text=vertice)

    velocidade_animacao = 10  # Velocidade da animação (em segundos)
    linhas = []
    for aresta, tipo_aresta in tipos_aresta.items():  # mostra as setas na tela
        u, v = aresta
        x1, y1 = coordenadas_vertices[list(grafo.keys()).index(u)]
        x2, y2 = coordenadas_vertices[list(grafo.keys()).index(v)]
        if tipo_aresta == 'Árvore':
            cor = 'green'
        elif tipo_aresta == 'Retorno':
            cor = 'red'
        elif tipo_aresta == 'Avanço':
            cor = 'blue'
        else:
            cor = 'orange'

        linha = canvas.create_line(x1, y1, x2, y2, fill=cor, arrow=tk.LAST, state='hidden')
        linhas.append(linha)

    def mostrar_proxima_linha():
        nonlocal linha_atual
        if linha_atual < len(linhas):
            canvas.itemconfigure(linhas[linha_atual], state='normal')
            linha_atual += 1
            janela.after(int(velocidade_animacao * 1000), mostrar_proxima_linha)

    def mostrar_linha_anterior():
        nonlocal linha_atual
        if linha_atual > 0:
            linha_atual -= 1
            canvas.itemconfigure(linhas[linha_atual], state='hidden')

    def mostrar_valores_d_f():
        x = 10
        y = canvas.winfo_height() + 480

        texto_d = "d: "
        texto_f = " f: "

        for u in d:
            texto_d += f"{str(d[u]).zfill(2)} "
            texto_f += f"{str(f[u]).zfill(2)} "

        canvas.create_text(x, y, text=texto_f, anchor="sw")
        canvas.create_text(x, y - 15, text=texto_d, anchor="sw")

        canvas.create_text(+250, +480, text="Use 'a' para avançar e 'd' para voltar a animação", anchor="sw")

        canvas.create_text(350, 80, text="""
        Árvore = Verde
        Retorno = Vermelho
        Avanço = Azul
        Cruzamento = Laranja
        """, anchor="sw")

        # Mostra na tela d e f de cada vertice
        ii = 5
        for u in grafo:
            ii += 15
            canvas.create_text(+10, ii, text=u + " {" + "d: " + str(d[u]).zfill(2) + " f: " + str(f[u]) + "}", anchor="sw")

        # Mostra na tela o tipo de cada aresta
        canvas.create_text(+500, ii + 30, text="Tipos de Aresta:", anchor="sw")
        ii += 45
        for aresta, tipo in tipos_aresta.items():
            u, v = aresta
            canvas.create_text(+500, ii, text=f"{u} -> {v}: {tipo}", anchor="sw")
            ii += 15

    def vincular_teclas(evento):
        if evento.keysym == 'd':
            mostrar_proxima_linha()
        elif evento.keysym == 'a':
            mostrar_linha_anterior()

    canvas.bind('<Key>', vincular_teclas)
    canvas.focus_set()

    linha_atual = 0
    mostrar_proxima_linha()
    mostrar_valores_d_f()

    janela.mainloop()


grafo = ler_grafo("grafo.txt")
d, f, tipos_aresta = dfs(grafo)
desenhar_grafo(grafo, tipos_aresta, d, f)