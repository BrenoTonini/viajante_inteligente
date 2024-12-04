from flask import Flask, render_template_string, request, session
import networkx as nx
import matplotlib.pyplot as plt
import io
import base64
import random
import json

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

# Função para criar o grafo
def create_graph(numero_de_pontos):
    G = nx.DiGraph()

   
    G.add_nodes_from(range(1, numero_de_pontos + 1))

    # Adicionando arestas com pesos aleatórios
    for i in range(1, numero_de_pontos):
        for j in range(i + 1, numero_de_pontos + 1):
            peso = random.randint(1, 10)
            G.add_edge(i, j, weight=peso)

    # Gerando a visualização do grafo
    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 4))
    nx.draw(G, pos, with_labels=True, node_size=600, node_color="red", font_size=12, font_weight="bold", arrowsize=10, arrows = False,)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Salvando a imagem do grafo
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Convertendo para base64
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    return img_base64, G

# Função para serializar o grafo
def serialize_graph(G):
    edges = []
    for u, v, data in G.edges(data=True):
        edges.append((u, v, data['weight']))
    return json.dumps({'nodes': list(G.nodes), 'edges': edges})

# Função para desserializar o grafo
def deserialize_graph(serialized_graph):
    data = json.loads(serialized_graph)
    G = nx.DiGraph()
    G.add_nodes_from(data['nodes'])
    for u, v, weight in data['edges']:
        G.add_edge(u, v, weight=weight)
    return G

@app.route('/', methods=['GET', 'POST'])
def index():
    graph_img = None
    numero_de_pontos = 10 
    if request.method == 'POST':
        pontos = int(request.form['pontos'])  
        graph_img, G = create_graph(pontos)  
        serialized_graph = serialize_graph(G)  
        session['G'] = serialized_graph

    return render_template_string('''<!DOCTYPE html>
    <html>
        <head>
            <title>TRABALHO GRAPH</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f9;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    flex-direction: column;
                }

                .container {
                    width: 80%;
                    max-width: 1000px;
                    padding: 20px;
                    background-color: rgba(255, 255, 255, 0.8);
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                }

                h3 {
                    background-color : rgb(102, 216, 74)
                    display: center;
                    padding-left: 250px;
                    font-size: 24px;
                    color: #333;
                    margin-bottom: 20px;
                }

                .graph img {
                    max-width: 100%;
                    height: auto;
                    border-radius: 8px;
                    margin-top: 20px;
                }

                .form-container {
                    margin-top: 20px;
                }

                select, button {
                    padding: 10px;
                    font-size: 16px;
                    border: 2px solid #0099cc;
                    border-radius: 8px;
                    background-color: #f0faff;
                    margin-top: 10px;
                    width: 100%;
                }

                button {
                    background-color: #04AA6D;
                    color: white;
                    cursor: pointer;
                }

                button:hover {
                    background-color: #028a56;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h3>Seu melhor trajeto é nossa preocupação</h3>
                {% if graph_img %}
                    <div class="graph">
                        <img src="data:image/png;base64,{{ graph_img }}" alt="Grafo">
                    </div>
                {% endif %}
                <div class="form-container">
                    <form method="POST">
                        <label for="pontos">Quantos pontos deseja ter em seu trajeto?</label>
                        <select name="pontos" id="pontos">
                            {% for i in range(2, numero_de_pontos + 1) %}
                                <option value="{{ i }}">Ponto {{ i }}</option>
                            {% endfor %}
                        </select>
                        <button type="submit">Gerar</button>
                    </form>
                </div>
            </div>
        </body>
    </html>
    ''', graph_img=graph_img, numero_de_pontos=numero_de_pontos)

if __name__ == '__main__':
    app.run(debug=True)
