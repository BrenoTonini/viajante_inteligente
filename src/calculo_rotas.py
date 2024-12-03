import random

def calcular_distancia(matriz, rota):
    """
    calcula a distância total de uma rota com base na matriz de distâncias.
    """
    distancia_total = 0
    n = len(rota)
    for i in range(n - 1):
        origem = rota[i]
        destino = rota[i + 1]
        distancia_total += matriz[origem][destino]
    # conecta o último nó de volta ao primeiro (nó 0)
    distancia_total += matriz[rota[-1]][rota[0]]
    return distancia_total

def two_opt(matriz, rota):
    """
    aplica o algoritmo 2-opt para melhorar a rota.
    """
    n = len(rota)
    melhor_rota = rota[:]
    melhor_distancia = calcular_distancia(matriz, melhor_rota)

    # tenta todas as combinações de swaps 2-opt
    for i in range(1, n - 1):  # começa a partir de 1, porque o nó 0 deve ficar fixa
        for j in range(i + 1, n - 1):  # não pode alterar o último nó, que é o 0
            nova_rota = melhor_rota[:]
            nova_rota[i + 1:j + 1] = reversed(melhor_rota[i + 1:j + 1])
            nova_distancia = calcular_distancia(matriz, nova_rota)
            
            if nova_distancia < melhor_distancia:
                melhor_rota = nova_rota[:]
                melhor_distancia = nova_distancia

    return melhor_rota, melhor_distancia

def gerar_rota_inicial(n):
    """
    gera uma rota inicial aleatória com o nó 0 fixado no início e no final.
    """
    rota_inicial = list(range(1, n))  # exclui o 0
    random.shuffle(rota_inicial)
    # coloca o nó 0 no início e no final da rota
    rota_inicial = [0] + rota_inicial + [0]
    return rota_inicial

def otimizar_rota(matriz, n_tentativas):
    """
    tenta otimizar a rota por várias tentativas, retornando a melhor rota.
    """
    melhor_rota = None
    melhor_distancia = float('inf')
    
    for _ in range(n_tentativas):
        rota_inicial = gerar_rota_inicial(len(matriz))
        rota_otimizada, distancia_otimizada = two_opt(matriz, rota_inicial)
        
        if distancia_otimizada < melhor_distancia:
            melhor_rota = rota_otimizada
            melhor_distancia = distancia_otimizada

    return melhor_rota, melhor_distancia
