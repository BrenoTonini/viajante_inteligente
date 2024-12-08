from flask import Flask, render_template_string, request, session
import networkx as nx
import matplotlib.pyplot as plt
import io
import base64
import random
import json
import numpy as np

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

# Classe Ponto
class Ponto:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def dist(self, outro):
        diff_x = self.x - outro.x
        diff_y = self.y - outro.y
        return np.sqrt(diff_x ** 2 + diff_y ** 2)

    def __repr__(self):
        return f"({self.x:.1f}, {self.y:.1f})"

# Funções auxiliares para otimização e criação de gráficos
def comprimento_rota(caminho):
    n = len(caminho)
    comprimento = caminho[-1].dist(caminho[0])
    for i in range(n - 1):
        comprimento += caminho[i].dist(caminho[i + 1])
    return comprimento

def trocar_bordas(caminho, i, j):
    caminho[i+1:j+1] = reversed(caminho[i+1:j+1])
    return caminho

def criar_rota_aleatoria(n):
    pontos = []
    for _ in range(n):
        x = np.random.uniform(0, 1000)
        y = np.random.uniform(0, 1000)
        pontos.append(Ponto(x, y))
    return pontos

def otimizar_rota(caminho):
    n = len(caminho)
    melhoria = True
    while melhoria:
        melhoria = False
        for i in range(n - 1):
            for j in range(i + 2, n):
                delta_comprimento = -caminho[i].dist(caminho[i + 1]) - caminho[j].dist(caminho[(j + 1) % n]) + \
                                     caminho[i].dist(caminho[j]) + caminho[i + 1].dist(caminho[(j + 1) % n])
                if delta_comprimento < 0:
                    caminho = trocar_bordas(caminho, i, j)
                    melhoria = True
                    break
            if melhoria:
                break
    return caminho

def create_graph(caminho):
    G = nx.DiGraph()
    pos = {}

    for idx, ponto in enumerate(caminho):
        G.add_node(idx, pos=(ponto.x, ponto.y))
        pos[idx] = (ponto.x, ponto.y)

    for i in range(len(caminho)):
        G.add_edge(i, (i + 1) % len(caminho), weight=caminho[i].dist(caminho[(i + 1) % len(caminho)]))

    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, with_labels=True, node_size=600, node_color="skyblue", font_size=12, font_weight="bold", arrowsize=15)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels={k: f"{v:.1f}" for k, v in edge_labels.items()})

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    return img_base64

@app.route('/', methods=['GET', 'POST'])
def index():
    graph_img = None
    numero_de_pontos = 10
    caminho = None

    if request.method == 'POST':
        if 'gerar' in request.form:
            pontos = int(request.form['pontos'])
            caminho = criar_rota_aleatoria(pontos)
            session['caminho'] = [(p.x, p.y) for p in caminho]
            graph_img = create_graph(caminho)
        elif 'organizar' in request.form:
            caminho = [Ponto(x, y) for x, y in session.get('caminho', [])]
            caminho_otimizado = otimizar_rota(caminho)
            session['caminho_otimizado'] = [(p.x, p.y) for p in caminho_otimizado]
            graph_img = create_graph(caminho_otimizado)

    return render_template_string('''<!DOCTYPE html>
    <html>
        <head>
            <title>Otimização de Rotas</title>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
            <style>
                body {
                    font-family: 'Arial', sans-serif;
                    background: linear-gradient(to right, #8360c3, #2ebf91);
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    color: #fff;
                }
                .container {
                    text-align: center;
                    background: rgba(255, 255, 255, 0.1);
                    padding: 30px;
                    border-radius: 15px;
                    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
                    width: 80%;
                    max-width: 800px;
                }
                h3 {
                    font-size: 2rem;
                    margin-bottom: 20px;
                    font-weight: bold;
                }
                .graph img {
                    width: 100%;
                    border-radius: 10px;
                    margin-bottom: 20px;
                }
                .form-container {
                    display: flex;
                    justify-content: space-around;
                    flex-wrap: wrap;
                    gap: 10px;
                }
                select, button {
                    padding: 12px 20px;
                    font-size: 16px;
                    border: none;
                    border-radius: 8px;
                    cursor: pointer;
                }
                select {
                    background: #fff;
                    color: #333;
                    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
                }
                button {
                    background: #04AA6D;
                    color: white;
                    transition: all 0.3s ease-in-out;
                }
                button:hover {
                    background: #028a56;
                }
                footer {
                    margin-top: 20px;
                    font-size: 14px;
                    color: #ddd;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h3><i class="fas fa-route"></i> Seu Melhor Trajeto</h3>
                {% if graph_img %}
                    <div class="graph">
                        <img src="data:image/png;base64,{{ graph_img }}" alt="Grafo">
                    </div>
                {% endif %}
                <div class="form-container">
                    <form method="POST">
                        <label for="pontos">Quantos pontos deseja ter em seu trajeto?</label>
                        <select name="pontos" id="pontos">
                            {% for i in range(2, 21) %}
                                <option value="{{ i }}">Ponto {{ i }}</option>
                            {% endfor %}
                        </select>
                        <button type="submit" name="gerar"><i class="fas fa-random"></i> Gerar Rota</button>
                    </form>
                    {% if session.get('caminho') %}
                        <form method="POST">
                            <button type="submit" name="organizar"><i class="fas fa-sort"></i> Organizar Rota</button>
                        </form>
                    {% endif %}
                </div>
                <footer>&copy; 2024 Seu Melhor Trajeto</footer>
            </div>
        </body>
    </html>
    ''', graph_img=graph_img)

if __name__ == '__main__':
    app.run(debug=True)
