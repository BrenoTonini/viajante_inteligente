# MVP - Viajante Inteligente  

Este repositório contém o desenvolvimento de um **MVP** (Minimum Viable Product) como parte de um trabalho avaliativo da disciplina de **Sistemas Web**. O objetivo do trabalho era construir um MVP para solucionar um problema **não trivial**, e o escolhido foi o **Problema do Caixeiro Viajante** (*Travelling Salesman Problem - TSP*).  

---

## **Objetivo do Projeto**  

O projeto busca resolver o problema do Caixeiro Viajante de forma prática, permitindo que o usuário:  
1. Insira os pontos a serem visitados por meio de uma interface web.  
2. Visualize o grafo que representa os pontos e suas conexões.  
3. Execute um algoritmo para calcular uma rota eficiente que passe por todos os pontos, retornando ao ponto inicial.  

A interface web está sendo desenvolvida utilizando o **Flask**, um microframework Python, visando simplicidade e uma interação intuitiva.  

---

## **Contexto do Problema**  

O **Problema do Caixeiro Viajante** é um desafio clássico na ciência da computação e na matemática. Ele consiste em determinar a menor rota que permita visitar todas as cidades (ou pontos) exatamente uma vez, retornando ao ponto de origem. Esse problema é conhecido por sua **complexidade computacional**, especialmente à medida que o número de pontos aumenta, sendo classificado como **NP-difícil**.  

---

## **Motivação e Proposta Didática**  

Este trabalho avaliativo visa explorar:  
- A aplicação de conceitos aprendidos na disciplina de Sistemas Web.  
- A construção de um MVP funcional para um problema não trivial.
- O uso de tecnologias web, como Flask, para criar uma interface acessível e dinâmica.  

---

## **Tecnologias Utilizadas**

- **Linguagem**: Python
- **Bibliotecas**:  
    - [`flask`](https://flask.palletsprojects.com/en/stable/): para criação da interface web.  
    - [`matplotlib`](https://matplotlib.org/): para visualização gráfica do grafo e das rotas (planejado).  
    - [`networkx`](https://networkx.org/): para modelar e manipular o grafo de pontos (planejado).  
