"""
Projeto 10: Sistema de Gerenciamento de Pedidos de Restaurante
Disciplina: Paradigmas de Programação - UNINASSAU (Aula 07)
Paradigma: Imperativo (estado mutável, sequenciamento explícito, condicionais e laços)
"""

STATUS_VALIDOS = ["recebido", "em preparação", "pronto", "entregue"]

# Regra de desconto: 10% para subtotais a partir de R$ 50,00; 5% a partir de R$ 30,00; abaixo disso, 0%
LIMITE_DESCONTO_ALTO = 50.00
PERCENTUAL_DESCONTO_ALTO = 0.10

LIMITE_DESCONTO_MEDIO = 30.00
PERCENTUAL_DESCONTO_MEDIO = 0.05

# Estado global mutável do sistema
cardapio = [
    {"id": 1, "nome": "Hambúrguer Artesanal", "preco": 32.00, "disponivel": True},
    {"id": 2, "nome": "Batata Frita Média", "preco": 18.00, "disponivel": True},
    {"id": 3, "nome": "Refrigerante Lata", "preco": 7.50, "disponivel": True},
    {"id": 4, "nome": "Salmão Grelhado", "preco": 58.00, "disponivel": False},  # Indisponível para teste
]

pedidos = [
    {
        "id": 1,
        "cliente": "Ana Souza",
        "itens": [
            {
                "produto_id": 1,
                "nome": "Hambúrguer Artesanal",
                "preco_unitario": 32.00,
                "quantidade": 2,
            },
            {
                "produto_id": 3,
                "nome": "Refrigerante Lata",
                "preco_unitario": 7.50,
                "quantidade": 2,
            },
        ],
        "subtotal": 79.00,
        "desconto": 7.90,
        "total": 71.10,
        "status": "em preparação",
    },
    {
        "id": 2,
        "cliente": "Carlos Lima",
        "itens": [
            {
                "produto_id": 2,
                "nome": "Batata Frita Média",
                "preco_unitario": 18.00,
                "quantidade": 1,
            },
        ],
        "subtotal": 18.00,
        "desconto": 0.00,
        "total": 18.00,
        "status": "entregue",
    },
]

proximo_id_produto = 5
proximo_id_pedido = 3


def buscar_produto_por_id(produto_id: int) -> dict | None:
    """Busca um produto no cardápio mutável pelo ID."""
    for produto in cardapio:
        if produto["id"] == produto_id:
            return produto
    return None


def buscar_pedido_por_id(pedido_id: int) -> dict | None:
    """Busca um pedido na lista mutável de pedidos pelo ID."""
    for pedido in pedidos:
        if pedido["id"] == pedido_id:
            return pedido
    return None


def ler_inteiro_positivo(mensagem: str) -> int | None:
    """Lê um número inteiro positivo com validação de entrada."""
    valor_str = input(mensagem).strip()
    if not valor_str.isdigit():
        print("Entrada inválida. Digite um número inteiro positivo.")
        return None
    valor = int(valor_str)
    if valor <= 0:
        print("O valor deve ser maior que zero.")
        return None
    return valor


def ler_preco_positivo(mensagem: str) -> float | None:
    """Lê um valor decimal positivo para preço."""
    valor_str = input(mensagem).strip().replace(",", ".")
    try:
        valor = float(valor_str)
    except ValueError:
        print("Preço inválido. Digite um valor numérico (ex.: 25.50).")
        return None

    if valor <= 0:
        print("O preço deve ser maior que zero.")
        return None
    return round(valor, 2)


def cadastrar_produto() -> None:
    """Cadastra um novo produto no cardápio atualizando o estado global."""
    global proximo_id_produto

    print("\n--- CADASTRAR PRODUTO NO CARDÁPIO ---")
    nome = input("Nome do produto: ").strip()
    if not nome:
        print("O nome do produto não pode ficar vazio.")
        return

    preco = ler_preco_positivo("Preço unitário (R$): ")
    if preco is None:
        return

    disp_input = input("Está disponível? (s/n) [padrão: s]: ").strip().lower()
    if disp_input in ("", "s", "sim"):
        disponivel = True
    elif disp_input in ("n", "nao", "não"):
        disponivel = False
    else:
        print("Opção de disponibilidade inválida. Use 's' ou 'n'.")
        return

    novo_produto = {
        "id": proximo_id_produto,
        "nome": nome,
        "preco": preco,
        "disponivel": disponivel,
    }
    cardapio.append(novo_produto)
    proximo_id_produto += 1
    print(f"Produto '{nome}' cadastrado com sucesso (ID #{novo_produto['id']}).")


def alternar_disponibilidade_produto() -> None:
    """Altera o status de disponibilidade de um produto existente no cardápio."""
    listar_cardapio()
    produto_id = ler_inteiro_positivo("Digite o ID do produto para alterar disponibilidade: ")
    if produto_id is None:
        return

    produto = buscar_produto_por_id(produto_id)
    if produto is None:
        print("Produto não encontrado.")
        return

    # Modifica diretamente o estado booleano do produto
    produto["disponivel"] = not produto["disponivel"]
    novo_estado = "Disponível" if produto["disponivel"] else "Indisponível"
    print(f"Disponibilidade de '{produto['nome']}' alterada para: {novo_estado}.")


def calcular_valores_pedido(itens: list[dict]) -> tuple[float, float, float]:
    """Calcula subtotal, desconto conforme regra de negócio e valor total."""
    subtotal = 0.0
    for item in itens:
        subtotal += item["preco_unitario"] * item["quantidade"]
    subtotal = round(subtotal, 2)

    # Regra de desconto por faixa de subtotal
    if subtotal >= LIMITE_DESCONTO_ALTO:
        percentual = PERCENTUAL_DESCONTO_ALTO
    elif subtotal >= LIMITE_DESCONTO_MEDIO:
        percentual = PERCENTUAL_DESCONTO_MEDIO
    else:
        percentual = 0.0

    desconto = round(subtotal * percentual, 2)
    total = round(subtotal - desconto, 2)
    return subtotal, desconto, total


def registrar_pedido() -> None:
    """Registra um novo pedido permitindo adicionar vários produtos disponíveis."""
    global proximo_id_pedido

    print("\n--- REGISTRAR NOVO PEDIDO ---")
    cliente = input("Nome do cliente: ").strip()
    if not cliente:
        print("Nome do cliente não pode ficar vazio.")
        return

    itens_pedido: list[dict] = []
    adicionando_itens = True

    while adicionando_itens:
        listar_cardapio()
        produto_id = ler_inteiro_positivo("Digite o ID do produto para adicionar: ")
        if produto_id is None:
            continue

        produto = buscar_produto_por_id(produto_id)
        if produto is None:
            print("Produto não encontrado no cardápio.")
            continue

        # Desafio adicional: impedir pedido de itens indisponíveis
        if not produto["disponivel"]:
            print(
                f"Bloqueado: '{produto['nome']}' está INDISPONÍVEL no momento e não pode ser pedido."
            )
            continue

        quantidade = ler_inteiro_positivo("Quantidade desejada: ")
        if quantidade is None:
            continue

        # Se o produto já foi adicionado neste pedido, acumula a quantidade
        item_existente = None
        for item in itens_pedido:
            if item["produto_id"] == produto["id"]:
                item_existente = item
                break

        if item_existente is not None:
            item_existente["quantidade"] += quantidade
        else:
            itens_pedido.append(
                {
                    "produto_id": produto["id"],
                    "nome": produto["nome"],
                    "preco_unitario": produto["preco"],
                    "quantidade": quantidade,
                }
            )

        print(f"Adicionado: {quantidade}x {produto['nome']}.")
        continuar = input("Adicionar outro produto ao pedido? (s/n): ").strip().lower()
        if continuar not in ("s", "sim"):
            adicionando_itens = False

    if len(itens_pedido) == 0:
        print("Pedido cancelado: nenhum item disponível foi adicionado.")
        return

    subtotal, desconto, total = calcular_valores_pedido(itens_pedido)

    novo_pedido = {
        "id": proximo_id_pedido,
        "cliente": cliente,
        "itens": itens_pedido,
        "subtotal": subtotal,
        "desconto": desconto,
        "total": total,
        "status": "recebido",
    }

    pedidos.append(novo_pedido)
    proximo_id_pedido += 1

    print("\nPedido registrado com sucesso!")
    print(
        f"Pedido #{novo_pedido['id']} | Cliente: {novo_pedido['cliente']} | "
        f"Status: {novo_pedido['status']}"
    )
    print(
        f"Subtotal: R$ {subtotal:.2f} | Desconto: R$ {desconto:.2f} | "
        f"Total a pagar: R$ {total:.2f}"
    )


def atualizar_status_pedido() -> None:
    """Atualiza o status do pedido sequencialmente (recebido -> em preparação -> pronto -> entregue)."""
    listar_pedidos()
    pedido_id = ler_inteiro_positivo("Digite o ID do pedido para atualizar o status: ")
    if pedido_id is None:
        return

    pedido = buscar_pedido_por_id(pedido_id)
    if pedido is None:
        print("Pedido não encontrado.")
        return

    status_atual = pedido["status"]
    indice_atual = STATUS_VALIDOS.index(status_atual)

    if indice_atual >= len(STATUS_VALIDOS) - 1:
        print(f"O Pedido #{pedido['id']} já está '{status_atual}' (status final).")
        return

    proximo_status = STATUS_VALIDOS[indice_atual + 1]
    confirmacao = (
        input(
            f"Avançar Pedido #{pedido['id']} de '{status_atual}' para '{proximo_status}'? (s/n): "
        )
        .strip()
        .lower()
    )

    if confirmacao in ("s", "sim"):
        pedido["status"] = proximo_status
        print(f"Status do Pedido #{pedido['id']} atualizado para '{proximo_status}'.")
    else:
        print("Atualização de status cancelada.")


def listar_cardapio() -> None:
    """Percorre a lista mutável do cardápio e exibe preços e disponibilidade."""
    print("\n--- CARDÁPIO ---")
    if not cardapio:
        print("Nenhum produto cadastrado no momento.")
        return

    for produto in cardapio:
        situacao = "Disponível" if produto["disponivel"] else "Indisponível"
        print(
            f"[{produto['id']}] {produto['nome']} - "
            f"R$ {produto['preco']:.2f} ({situacao})"
        )


def listar_pedidos() -> None:
    """Percorre a lista mutável de pedidos e exibe resumo, status e valores."""
    print("\n--- PEDIDOS REGISTRADOS ---")
    if not pedidos:
        print("Nenhum pedido registrado no momento.")
        return

    for pedido in pedidos:
        print(
            f"\nPedido #{pedido['id']} | Cliente: {pedido['cliente']} | "
            f"Status: {pedido['status']} | Subtotal: R$ {pedido['subtotal']:.2f} | "
            f"Desconto: R$ {pedido['desconto']:.2f} | Total: R$ {pedido['total']:.2f}"
        )
        for item in pedido["itens"]:
            subtotal_item = item["preco_unitario"] * item["quantidade"]
            print(
                f"   - {item['quantidade']}x {item['nome']} "
                f"(R$ {item['preco_unitario']:.2f} un.) = R$ {subtotal_item:.2f}"
            )


def gerar_relatorio_vendas() -> None:
    """Consolida métricas de pedidos e valores de vendas a partir da lista de pedidos."""
    print("\n--- RELATÓRIO DE VENDAS ---")
    total_pedidos = len(pedidos)
    if total_pedidos == 0:
        print("Nenhum pedido registrado para gerar relatório.")
        return

    total_subtotal = 0.0
    total_descontos = 0.0
    total_liquido = 0.0
    contagem_status = {status: 0 for status in STATUS_VALIDOS}

    for pedido in pedidos:
        total_subtotal += pedido["subtotal"]
        total_descontos += pedido["desconto"]
        total_liquido += pedido["total"]
        status_atual = pedido["status"]
        if status_atual in contagem_status:
            contagem_status[status_atual] += 1

    print(f"Total de pedidos registrados: {total_pedidos}")
    for status in STATUS_VALIDOS:
        print(f"  - Status '{status}': {contagem_status[status]}")
    print(f"Soma dos subtotais: R$ {total_subtotal:.2f}")
    print(f"Total de descontos concedidos: R$ {total_descontos:.2f}")
    print(f"Valor total de vendas (líquido): R$ {total_liquido:.2f}")


def exibir_menu() -> None:
    """Exibe as opções do sistema no terminal."""
    print("\n=== MUNDIÇAFOOD - DO TAMANHO DA SUA FOME! (SystemPDV) ===")
    print("1 - Listar cardápio")
    print("2 - Cadastrar produto no cardápio")
    print("3 - Alternar disponibilidade de produto")
    print("4 - Registrar novo pedido")
    print("5 - Listar pedidos")
    print("6 - Atualizar status do pedido")
    print("7 - Gerar relatório de vendas")
    print("0 - Sair")


def executar_sistema() -> None:
    """Controla o fluxo principal do programa por laço de repetição e estruturas condicionais."""
    executando = True

    while executando:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            listar_cardapio()
        elif opcao == "2":
            cadastrar_produto()
        elif opcao == "3":
            alternar_disponibilidade_produto()
        elif opcao == "4":
            registrar_pedido()
        elif opcao == "5":
            listar_pedidos()
        elif opcao == "6":
            atualizar_status_pedido()
        elif opcao == "7":
            gerar_relatorio_vendas()
        elif opcao == "0":
            executando = False
            print("Encerrando o sistema...")
        else:
            print("Opção inválida. Escolha uma opção do menu.")


if __name__ == "__main__":
    executar_sistema()