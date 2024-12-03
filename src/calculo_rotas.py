import random

def calcular_distancia_total(rota, matriz_distancias):
    distancia_total = 0
    for i in range(len(rota)):
        distancia_total += matriz_distancias[rota[i - 1]][rota[i]]
    return distancia_total

def realizar_troca_2_opt(rota, i, k):
    nova_rota = rota[:i] + rota[i:k + 1][::-1] + rota[k + 1:]
    return nova_rota

def algoritmo_caixeiro_2_opt(matriz_distancias):
    numero_nos = len(matriz_distancias)
    
    # gera uma rota inicial com o nó 0 fixado no início e no final
    rota_atual = list(range(1, numero_nos))
    random.shuffle(rota_atual)
    rota_atual = [0] + rota_atual + [0]

    melhor_distancia = calcular_distancia_total(rota_atual, matriz_distancias)
    melhorou = True

    while melhorou:
        melhorou = False
        # tenta melhorar a rota com o algoritmo 2-opt
        for i in range(1, len(rota_atual) - 2):
            for k in range(i + 1, len(rota_atual) - 1):
                nova_rota = realizar_troca_2_opt(rota_atual, i, k)
                nova_distancia = calcular_distancia_total(nova_rota, matriz_distancias)

                # se for melhor, atualiza a rota e a distância
                if nova_distancia < melhor_distancia:
                    rota_atual = nova_rota
                    melhor_distancia = nova_distancia
                    melhorou = True
                    break
            if melhorou:
                break

    return rota_atual, melhor_distancia


# EXEMPLO DE USO:
# matriz_distancias = [
#     [0, 10, 15, 20],
#     [10, 0, 35, 25],
#     [15, 35, 0, 30],
#     [20, 25, 30, 0]
# ]

# melhor_rota, melhor_distancia = algoritmo_caixeiro_2_opt(matriz_distancias)
# print("Melhor rota encontrada:", melhor_rota)
# print("Distância total:", melhor_distancia)