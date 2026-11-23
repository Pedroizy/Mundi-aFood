# MundiçaFood - Sistema de Gerenciamento de Pedidos de Restaurante (Grupo 10)

Projeto desenvolvido para a disciplina **Paradigmas de Programação – Aula 07**, da **UNINASSAU**, sob orientação do **Prof. Marco Rogério**[cite: 1, 2, 23, 24].

---

## 1. Identificação dos Integrantes

* `Pedro Antonio da Silva Izidio` — `01705873`
`Desenvolvedor, designer, techlead, PO`

---

## 2. Descrição do Problema e da Solução Desenvolvida

### Problema
Um restaurante precisa controlar pedidos, produtos do cardápio, quantidades, valores das vendas, regras de desconto, status de preparo/entrega e disponibilidade de itens.

### Solução
Foi desenvolvido um sistema em linha de comando (CLI) em **Python** seguindo o **paradigma imperativo**[cite: 25]. O programa gerencia o estado mutável da aplicação em memória (cardápio, pedidos, contadores de IDs e vendas), valida entradas do usuário, bloqueia pedidos com itens indisponíveis, calcula subtotais, descontos e totais, atualiza o status do pedido sequencialmente e gera relatórios de vendas[cite: 24, 26].

---

## 3. Paradigma de Programação e Linguagem Escolhida

* **Paradigma:** **Imperativo**[cite: 25]
* **Linguagem de Programação:** **Python 3**

### Onde e como o paradigma imperativo aparece no código[cite: 26]
1. **Variáveis e coleções de estado mutável:** `cardapio`, `pedidos`, `proximo_id_produto` e `proximo_id_pedido` armazenam o estado atual do sistema e são atualizados conforme as operações ocorrem.
2. **Sequenciamento explícito e controle de fluxo:** as funções executam passos ordenados (validar item -> calcular valores -> aplicar desconto -> atualizar estado/lista) com estruturas condicionais (`if/elif/else`) e laços de repetição (`while`, `for`)[cite: 24, 26].
3. **Procedimentos/funções com alteração de estado:** funções como cadastro de produto, registro de pedido e atualização de status modificam diretamente as estruturas de dados do sistema.

---

## 4. Funcionalidades Implementadas

* **Cadastro de produtos do cardápio:** adição de itens com ID, nome, preço e status de disponibilidade.
* **Controle de disponibilidade (Desafio adicional):** bloqueio de inclusão de itens marcados como indisponíveis em novos pedidos.
* **Registro de pedidos com múltiplos itens:** vinculação de cliente e de um ou mais produtos/quantidades a um pedido[cite: 24].
* **Cálculo de subtotal, desconto e valor total:** soma dos itens, aplicação de regra de desconto definida e cálculo do valor final[cite: 24].
* **Atualização de status do pedido:** transição controlada entre `recebido`, `em preparação`, `pronto` e `entregue`[cite: 24].
* **Relatório de vendas:** consolidação dos pedidos e valores vendidos[cite: 24].
* **Dados iniciais de teste:** carga prévia de cardápio (incluindo item indisponível) e pedidos de exemplo para facilitar testes e demonstração[cite: 26].

---

## 5. Estrutura de Pastas e Arquivos

```text
sistema-restaurante-grupo10/
├── main.py          # Código-fonte principal do sistema (paradigma imperativo)
└── README.md        # Documentação oficial do projeto
