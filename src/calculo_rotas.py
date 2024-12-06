import numpy as np

class Ponto:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    # Distância entre dois pontos
    def dist(self, outro):
        diff_x = self.x - outro.x
        diff_y = self.y - outro.y
        return np.sqrt(diff_x ** 2 + diff_y ** 2)

    def __repr__(self):
        return f"({self.x:.1f}, {self.y:.1f})"


# Função para calcular o comprimento de uma rota
def comprimento_rota(caminho):
    n = len(caminho)
    comprimento = caminho[-1].dist(caminho[0])  # Distância entre o último e o primeiro ponto
    for i in range(n - 1):
        comprimento += caminho[i].dist(caminho[i + 1])
    return comprimento


# Função para realizar a troca de bordas no algoritmo 2-opt
def trocar_bordas(caminho, i, j):
    caminho[i+1:j+1] = reversed(caminho[i+1:j+1])
    return caminho


# Função para criar uma rota aleatória de n pontos
def criar_rota_aleatoria(n):
    pontos = []
    for _ in range(n):
        x = np.random.uniform(0, 1000)
        y = np.random.uniform(0, 1000)
        pontos.append(Ponto(x, y))
    return pontos


# Função para otimizar a rota com o algoritmo 2-opt
def otimizar_rota(caminho):
    n = len(caminho)
    melhoria = True

    while melhoria:
        melhoria = False
        for i in range(n - 1):
            for j in range(i + 2, n):
                # Calculando o delta de comprimento ao realizar a troca de bordas
                delta_comprimento = -caminho[i].dist(caminho[i + 1]) - caminho[j].dist(caminho[(j + 1) % n]) + \
                                     caminho[i].dist(caminho[j]) + caminho[i + 1].dist(caminho[(j + 1) % n])

                # Se o comprimento da rota foi reduzido, realiza a troca de bordas
                if delta_comprimento < 0:
                    caminho = trocar_bordas(caminho, i, j)
                    melhoria = True
                    break
            if melhoria:
                break

    return caminho


# Teste do código
if __name__ == "__main__":
    # Criando uma rota aleatória com 10 pontos
    caminho = criar_rota_aleatoria(10)
    print("Rota original:")
    print(caminho)
    comprimento_inicial = comprimento_rota(caminho)
    print(f"Comprimento da rota original: {comprimento_inicial:.1f}")

    # Otimizando a rota
    caminho_otimizado = otimizar_rota(caminho)
    comprimento_otimizado = comprimento_rota(caminho_otimizado)
    print("\nRota otimizada:")
    print(caminho_otimizado)
    print(f"Comprimento da rota otimizada: {comprimento_otimizado:.1f}")
