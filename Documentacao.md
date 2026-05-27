# NetAdmin — Documentação Técnica

### Painel de Monitoramento de Redes com Teoria dos Grafos

---

## Visão Geral do Projeto

O **NetAdmin** é um painel administrativo web desenvolvido com **Flask** (Python) para monitoramento e gerenciamento de redes computacionais. O projeto utiliza **Teoria dos Grafos** como base matemática para representar a topologia de uma rede — ou seja, como os dispositivos estão conectados entre si — e aplica algoritmos clássicos de busca e otimização sobre essa estrutura.

A interface simula ferramentas reais de NOC _(Network Operations Center)_, como Grafana, Zabbix e Cisco DNA Center, com tema escuro e visualização dinâmica da rede.

**Tecnologias utilizadas:**

| Camada       | Tecnologia                 |
| ------------ | -------------------------- |
| Backend      | Python 3 + Flask           |
| Grafos       | NetworkX                   |
| Visualização | Matplotlib                 |
| Persistência | JSON (sem banco de dados)  |
| Frontend     | HTML, CSS, JavaScript puro |

---

## Como o Projeto Funciona

O fluxo completo do sistema segue estas etapas:

```
network.json
     │
     ▼
graph_generator.py          ← lê o JSON e monta o grafo com NetworkX
     │
     ▼
app.py (Flask)              ← executa BFS, DFS e Dijkstra sobre o grafo
     │
     ├── renderiza imagem PNG (Matplotlib) → static/images/graph.png
     │
     └── envia dados para os templates HTML
              │
              ▼
         Dashboard (navegador)
```

Toda vez que a rede é alterada (adição/remoção de nós ou arestas), o sistema:

1. Relê o `network.json`
2. Reconstrói o grafo em memória
3. Reexecuta os algoritmos
4. Gera uma nova imagem da topologia
5. Retorna os dados atualizados para a interface

---

## Conceito Principal — O que é um Grafo no Projeto

Em matemática, um **grafo** é uma estrutura composta por:

- **Vértices (nós):** os elementos da rede — roteadores, servidores, usuários, switches
- **Arestas (arestas):** as conexões entre esses elementos — cabos, links de rede
- **Pesos:** o custo de cada conexão — latência, distância, banda

No projeto, o grafo é **não-direcionado** (as conexões funcionam nos dois sentidos) e **ponderado** (cada conexão tem um custo numérico).

### O que é um Grafo no Projeto

Um grafo **G** é formado por:

```
G = (V, E)

V = conjunto de vértices (nós da rede)
E = conjunto de arestas (conexões entre nós)
```

No NetAdmin, isso se traduz diretamente para:

```
V = { Core, R1, R2, R3, Server, User1, User2, User3, User4 }

E = { (Core, R1), (Core, R2), (R1, R3), (R2, Server),
      (R3, User1), (R3, User2), (R2, User3), (R2, User4) }
```

### Exemplo no Projeto

O arquivo `network.json` é a fonte de dados do grafo. Cada nó tem um `id` e um `type`, e cada aresta conecta dois nós com um `weight` (peso):

```json
{
  "nodes": [
    { "id": "Core", "type": "router" },
    { "id": "R1", "type": "router" },
    { "id": "R2", "type": "router" },
    { "id": "Server", "type": "server" },
    { "id": "User1", "type": "user" }
  ],
  "edges": [
    { "source": "Core", "target": "R1", "weight": 2 },
    { "source": "Core", "target": "R2", "weight": 4 },
    { "source": "R2", "target": "Server", "weight": 5 }
  ]
}
```

---

## Arestas (Edges)

Uma **aresta** representa uma conexão física ou lógica entre dois dispositivos da rede. No projeto, as arestas são **bidirecionais** — se `Core` se conecta a `R1`, então `R1` também se conecta a `Core`.

No código, as arestas são carregadas assim:

```python
# graph_generator.py

def load_graph():
    with open("network.json", "r") as f:
        data = json.load(f)

    G = nx.Graph()  # Grafo não-direcionado

    for node in data["nodes"]:
        G.add_node(node["id"], type=node["type"])

    for edge in data["edges"]:
        G.add_edge(
            edge["source"],   # nó de origem
            edge["target"],   # nó de destino
            weight=edge["weight"]  # custo da conexão
        )

    return G
```

`nx.Graph()` cria um grafo **não-direcionado**: ao adicionar `(Core → R1)`, o NetworkX automaticamente também registra `(R1 → Core)`.

---

## Pesos

O **peso** de uma aresta representa o custo de atravessar aquela conexão. Dependendo do contexto da rede, o peso pode significar:

- Latência (tempo de resposta em ms)
- Distância física entre equipamentos
- Custo de utilização do link
- Número de saltos necessários

No projeto, os pesos são números inteiros definidos no `network.json` e usados pelo algoritmo de Dijkstra para encontrar o **caminho de menor custo total** entre dois pontos da rede.

**Exemplo:** para ir de `Core` até `Server`, existem dois caminhos possíveis:

```
Caminho 1: Core → R1 → R3 → ...       (não alcança Server diretamente)
Caminho 2: Core → R2 → Server         custo = 4 + 5 = 9
```

O Dijkstra calcula todos os caminhos possíveis e retorna o de menor custo.

---

## Interpretação do Grafo

O grafo gerado pelo Matplotlib usa cores para diferenciar visualmente os tipos de dispositivo:

| Cor                  | Tipo     | Representa                            |
| -------------------- | -------- | ------------------------------------- |
| 🔵 Azul `#38bdf8`    | `router` | Roteador — interliga sub-redes        |
| 🟢 Verde `#22c55e`   | `server` | Servidor — provê serviços             |
| 🟡 Amarelo `#f59e0b` | `user`   | Estação de usuário / cliente          |
| 🟣 Roxo `#a855f7`    | `switch` | Switch — comutação de pacotes         |
| 🔴 Vermelho (aresta) | —        | Menor caminho calculado pelo Dijkstra |

No código, essa diferenciação é feita agrupando os nós por tipo antes de desenhá-los:

```python
# graph_generator.py

NODE_STYLES = {
    "router":  {"color": "#38bdf8", "shape": "o", "size": 2800},
    "server":  {"color": "#22c55e", "shape": "s", "size": 3000},
    "user":    {"color": "#f59e0b", "shape": "o", "size": 2200},
    "switch":  {"color": "#a855f7", "shape": "D", "size": 2400},
    "default": {"color": "#94a3b8", "shape": "o", "size": 2000},
}

# Agrupa nós por tipo para desenhar com cores diferentes
type_groups = {}
for node, data in G.nodes(data=True):
    t = data.get("type", "default")
    if t not in type_groups:
        type_groups[t] = []
    type_groups[t].append(node)

# Desenha cada grupo com seu estilo visual
for ntype, nodes in type_groups.items():
    style = NODE_STYLES.get(ntype, NODE_STYLES["default"])
    nx.draw_networkx_nodes(
        G, pos,
        nodelist=nodes,
        node_color=style["color"],
        node_size=style["size"],
        node_shape=style["shape"],
        ax=ax
    )
```

---

## Como Ler a Topologia

A imagem gerada mostra:

- **Círculos/quadrados coloridos:** cada dispositivo da rede
- **Linhas cinzas:** conexões normais entre dispositivos
- **Linhas vermelhas (espessas):** o menor caminho calculado pelo Dijkstra
- **Números nas arestas:** o peso/custo de cada conexão

### Exemplo

Para a rede padrão do projeto, a topologia representa:

```
                    [Core]
                   /      \
                 (2)       (4)
                 /            \
              [R1]            [R2]──(2)──[User3]
               |              |  \
              (3)            (5)  (4)
               |              |     \
              [R3]         [Server] [User4]
             /    \
           (2)    (3)
           /        \
        [User1]   [User2]
```

O menor caminho de `Core` até `Server` é:

```
Core ──(4)──> R2 ──(5)──> Server    custo total = 9
```

Esse caminho é destacado em **vermelho** na imagem da topologia.

---

## Como os Algoritmos São Usados

Os três algoritmos são executados na função `get_algorithms()` do arquivo `app.py`, toda vez que uma página é carregada ou o usuário clica em **Calcular** no painel do Dijkstra:

```python
# app.py

def get_algorithms(G):
    source = "Core"   # nó de origem padrão
    target = "Server" # nó de destino padrão

    results = {}

    # BFS
    results["bfs"] = list(nx.bfs_tree(G, source).nodes())

    # DFS
    results["dfs"] = list(nx.dfs_tree(G, source).nodes())

    # Dijkstra
    if nx.has_path(G, source, target):
        results["shortest_path"] = nx.dijkstra_path(G, source, target, weight="weight")
        results["cost"]          = nx.dijkstra_path_length(G, source, target, weight="weight")

    return results
```

---

## 1. BFS — Breadth First Search (Busca em Largura)

### O que é

O BFS explora o grafo **nível por nível**, a partir de um nó inicial. Ele visita primeiro todos os vizinhos diretos do nó inicial, depois os vizinhos dos vizinhos, e assim por diante. Utiliza uma **fila (queue)** internamente.

### Para que serve na rede

- Descobrir **todos os dispositivos acessíveis** a partir de um ponto
- Encontrar o caminho com o **menor número de saltos** (sem considerar pesos)
- Mapear a "distância em hops" de um nó central para os demais

### Como funciona (passo a passo)

Partindo de `Core` na rede padrão:

```
Nível 0: Core
Nível 1: R1, R2          (vizinhos diretos de Core)
Nível 2: R3, Server, User3, User4   (vizinhos de R1 e R2)
Nível 3: User1, User2    (vizinhos de R3)

Resultado BFS: [Core, R1, R2, R3, Server, User3, User4, User1, User2]
```

### Código no projeto

```python
# app.py — dentro de get_algorithms()

results["bfs"] = list(nx.bfs_tree(G, source).nodes())
```

`nx.bfs_tree(G, source)` retorna uma **árvore BFS** — um subgrafo que contém apenas as arestas percorridas durante a busca em largura. `.nodes()` extrai a lista de nós visitados, na ordem em que foram descobertos.

### Implementação manual equivalente

Para entender o que o NetworkX faz internamente:

```python
from collections import deque

def bfs_manual(grafo, inicio):
    visitados = []
    fila = deque([inicio])
    vistos = {inicio}

    while fila:
        no_atual = fila.popleft()     # retira o primeiro da fila
        visitados.append(no_atual)

        for vizinho in grafo.neighbors(no_atual):
            if vizinho not in vistos:
                vistos.add(vizinho)
                fila.append(vizinho)  # adiciona no final da fila

    return visitados
```

---

## 2. DFS — Depth First Search (Busca em Profundidade)

### O que é

O DFS explora o grafo **indo o mais fundo possível** em cada ramo antes de voltar e explorar outros. Utiliza uma **pilha (stack)** internamente — ou recursão.

### Para que serve na rede

- Detectar **ciclos** na rede (conexões redundantes)
- Verificar se a rede é **conexa** (todos os dispositivos se comunicam)
- Encontrar todos os caminhos possíveis entre dois pontos

### Como funciona (passo a passo)

Partindo de `Core` na rede padrão:

```
1. Visita Core
2. Vai fundo por R1 → R3 → User1
3. Volta para R3 → User2
4. Volta para Core → R2 → Server
5. Continua R2 → User3
6. Continua R2 → User4

Resultado DFS: [Core, R1, R3, User1, User2, R2, Server, User3, User4]
```

Note como o DFS desce por um caminho inteiro antes de explorar o próximo — diferente do BFS que explora por camadas.

### Código no projeto

```python
# app.py — dentro de get_algorithms()

results["dfs"] = list(nx.dfs_tree(G, source).nodes())
```

`nx.dfs_tree(G, source)` retorna a **árvore DFS** — o subgrafo das arestas percorridas em profundidade. `.nodes()` extrai os nós na ordem de visita.

### Implementação manual equivalente

```python
def dfs_manual(grafo, inicio):
    visitados = []
    pilha = [inicio]
    vistos = set()

    while pilha:
        no_atual = pilha.pop()        # retira o topo da pilha

        if no_atual not in vistos:
            vistos.add(no_atual)
            visitados.append(no_atual)

            for vizinho in grafo.neighbors(no_atual):
                if vizinho not in vistos:
                    pilha.append(vizinho)  # empilha para visitar depois

    return visitados
```

### BFS vs DFS — Comparação direta

|                        | BFS                      | DFS                             |
| ---------------------- | ------------------------ | ------------------------------- |
| Estrutura interna      | Fila (FIFO)              | Pilha (LIFO)                    |
| Ordem de visita        | Por níveis (camadas)     | Por profundidade (ramos)        |
| Garante menor caminho? | Sim (em grafos sem peso) | Não                             |
| Uso na rede            | Mapear alcançabilidade   | Detectar ciclos e conectividade |

---

## 3. Dijkstra — Menor Caminho com Pesos

### O que é

O algoritmo de Dijkstra encontra o **caminho de menor custo total** entre dois nós em um grafo ponderado. Ao contrário do BFS (que minimiza o número de saltos), o Dijkstra minimiza a **soma dos pesos** das arestas percorridas.

Foi criado pelo cientista da computação **Edsger W. Dijkstra** em 1956 e é amplamente usado em roteamento de redes (protocolo OSPF, por exemplo).

### Para que serve na rede

- Encontrar a **rota mais eficiente** entre dois dispositivos
- Base para protocolos de roteamento reais (OSPF, IS-IS)
- Calcular a latência mínima entre pontos da rede

### Como funciona (passo a passo)

Para `Core → Server` na rede padrão:

```
Distâncias iniciais:
  Core=0, R1=∞, R2=∞, R3=∞, Server=∞, User1=∞ ...

Passo 1 — processa Core (menor distância=0):
  Core → R1: 0+2 = 2   ✓ atualiza R1=2
  Core → R2: 0+4 = 4   ✓ atualiza R2=4

Passo 2 — processa R1 (menor distância=2):
  R1 → R3: 2+3 = 5     ✓ atualiza R3=5

Passo 3 — processa R2 (menor distância=4):
  R2 → Server: 4+5 = 9 ✓ atualiza Server=9
  R2 → User3:  4+2 = 6 ✓
  R2 → User4:  4+4 = 8 ✓

Passo 4 — processa R3 (menor distância=5):
  R3 → User1: 5+2 = 7  ✓
  R3 → User2: 5+3 = 8  ✓

Resultado: Core → R2 → Server  com custo total = 9
```

### Código no projeto

```python
# app.py — dentro de get_algorithms()

if nx.has_path(G, source, target):

    # Retorna a lista de nós do caminho de menor custo
    path = nx.dijkstra_path(G, source, target, weight="weight")

    # Retorna o custo total (soma dos pesos)
    cost = nx.dijkstra_path_length(G, source, target, weight="weight")

    results["shortest_path"] = path   # ex: ["Core", "R2", "Server"]
    results["cost"] = cost            # ex: 9
```

O parâmetro `weight="weight"` instrui o NetworkX a usar o atributo `weight` das arestas como custo — o mesmo valor definido no `network.json`.

### Rota dinâmica (seleção pelo usuário)

O painel também permite que o usuário selecione **qualquer origem e destino** para calcular o menor caminho em tempo real. Isso é feito via uma requisição AJAX para a rota `/api/dijkstra`:

```python
# app.py — rota da API

@app.route("/api/dijkstra")
def api_dijkstra():
    source = request.args.get("source")  # ex: "R1"
    target = request.args.get("target")  # ex: "User2"

    G = load_graph()

    # Validações
    if source == target:
        return jsonify({"error": "Origem e destino devem ser diferentes."})

    if not nx.has_path(G, source, target):
        return jsonify({"error": f"Sem caminho entre '{source}' e '{target}'."})

    # Calcula o caminho
    path = nx.dijkstra_path(G, source, target, weight="weight")
    cost = nx.dijkstra_path_length(G, source, target, weight="weight")

    # Regenera o grafo com o novo caminho destacado em vermelho
    draw_graph(G, path)

    return jsonify({
        "path":  path,   # ["R1", "R3", "User2"]
        "cost":  cost,   # 6
        "hops":  len(path) - 1,  # 2
    })
```

No frontend, o JavaScript recebe o resultado e atualiza a interface sem recarregar a página:

```javascript
// templates/index.html

function calcDijkstra() {
  const source = document.getElementById("dijk-source").value;
  const target = document.getElementById("dijk-target").value;

  fetch(`/api/dijkstra?source=${source}&target=${target}`)
    .then((r) => r.json())
    .then((d) => {
      // Renderiza os nós do caminho na interface
      let html = "";
      d.path.forEach((node, i) => {
        html += `<span class="path-node highlight">${node}</span>`;
        if (i < d.path.length - 1) html += `<span> → </span>`;
      });
      document.getElementById("dijkstra-path").innerHTML = html;

      // Atualiza custo e número de saltos
      document.getElementById("dijkstra-cost").textContent = d.cost;
      document.getElementById("dijkstra-hops").textContent = d.hops;

      // Recarrega a imagem do grafo com o novo caminho em vermelho
      const img = document.getElementById("topology-img");
      img.src = "/static/images/graph.png?t=" + d.graph_ts;
    });
}
```

### Como o caminho é destacado no grafo

Após o cálculo, o `draw_graph()` recebe o caminho e desenha as arestas do percurso em vermelho com espessura maior:

```python
# graph_generator.py

def draw_graph(G, shortest_path=None):

    # Identifica as arestas que fazem parte do menor caminho
    path_edges = []
    if shortest_path and len(shortest_path) > 1:
        path_edges = list(zip(shortest_path, shortest_path[1:]))
        # ex: ["Core","R2","Server"] → [("Core","R2"), ("R2","Server")]

    # Arestas normais (cinza)
    normal_edges = [
        e for e in G.edges()
        if e not in path_edges and (e[1], e[0]) not in path_edges
    ]
    nx.draw_networkx_edges(G, pos, edgelist=normal_edges,
                           edge_color="#334155", width=2)

    # Arestas do caminho mínimo (vermelho, mais espessas)
    if path_edges:
        nx.draw_networkx_edges(G, pos, edgelist=path_edges,
                               edge_color="#ef4444", width=4)
```

---

## Resumo dos Algoritmos

| Algoritmo | Usa pesos? | Garante ótimo?     | Complexidade     | Uso no projeto               |
| --------- | ---------- | ------------------ | ---------------- | ---------------------------- |
| BFS       | Não        | Menor nº de saltos | O(V + E)         | Mapa de alcançabilidade      |
| DFS       | Não        | Não                | O(V + E)         | Verificação de conectividade |
| Dijkstra  | Sim        | Menor custo total  | O((V + E) log V) | Roteamento de pacotes        |

> **V** = número de vértices (nós) · **E** = número de arestas (conexões)

---

_Projeto desenvolvido com Flask, NetworkX e Matplotlib — Teoria dos Grafos aplicada a redes computacionais._
