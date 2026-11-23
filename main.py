# Sequência oficial de estados permitidos para o ciclo de vida de um pedido
STATUS_VALIDOS = ["recebido", "em preparação", "pronto", "entregue"]

# Parâmetros da regra de desconto por faixa de subtotal
LIMITE_DESCONTO_ALTO = 50.00
PERCENTUAL_DESCONTO_ALTO = 0.10

LIMITE_DESCONTO_MEDIO = 30.00
PERCENTUAL_DESCONTO_MEDIO = 0.05

# --- ESTADO MUTÁVEL DO SISTEMA (PARADIGMA IMPERATIVO) ---
# Estas estruturas guardam o estado atual da aplicação e são modificadas ao longo da execução.
cardapio = [
    {"id": 1, "nome": "Hambúrguer Artesanal", "preco": 32.00, "disponivel": True},
    {"id": 2, "nome": "Batata Frita Média", "preco": 18.00, "disponivel": True},
    {"id": 3, "nome": "Refrigerante Lata", "preco": 7.50, "disponivel": True},
    {"id": 4, "nome": "Salmão Grelhado", "preco": 58.00, "disponivel": False},
]

pedidos = [
    {
        "id": 1,
        "cliente": "Alessandra (jujudopix)",
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
        "cliente": "Guilherme (Gabiru)",
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
    """Percorre o cardápio e retorna o dicionário do produto correspondente ou None."""
    for produto in cardapio:
        if produto["id"] == produto_id:
            return produto
    return None


def buscar_pedido_por_id(pedido_id: int) -> dict | None:
    """Percorre a lista de pedidos e retorna o dicionário do pedido correspondente ou None."""
    for pedido in pedidos:
        if pedido["id"] == pedido_id:
            return pedido
    return None


def ler_texto_obrigatorio(mensagem: str) -> str | None:
    """Lê uma string não vazia; retorna None se o usuário enviar apenas espaços."""
    texto = input(mensagem).strip()
    if not texto:
        print("Erro de validação: este campo não pode ficar vazio.")
        return None
    return texto


def ler_inteiro_positivo(mensagem: str) -> int | None:
    """Valida e converte entrada para número inteiro estritamente maior que zero."""
    entrada = input(mensagem).strip()
    if not entrada.isdigit():
        print("Erro de validação: digite apenas números inteiros positivos.")
        return None

    numero = int(entrada)
    if numero <= 0:
        print("Erro de validação: o valor deve ser maior que zero.")
        return None
    return numero


def ler_preco_positivo(mensagem: str) -> float | None:
    """Valida e converte entrada decimal (aceitando vírgula ou ponto) para preço > 0."""
    entrada = input(mensagem).strip().replace(",", ".")
    try:
        valor = float(entrada)
    except ValueError:
        print("Erro de validação: digite um valor numérico válido (ex.: 24.90).")
        return None

    if valor <= 0:
        print("Erro de validação: o preço deve ser maior que zero.")
        return None

    return round(valor, 2)


def ler_confirmacao(mensagem: str, padrao: bool | None = None) -> bool | None:
    """
    Lê confirmação de sim/não.
    Se 'padrao' for informado (True/False), pressionar Enter assume esse valor.
    Retorna None quando a entrada não é reconhecida.
    """
    resposta = input(mensagem).strip().lower()
    if resposta == "" and padrao is not None:
        return padrao
    if resposta in ("s", "sim"):
        return True
    if resposta in ("n", "nao", "não"):
        return False

    print("Erro de validação: responda com 's' (sim) ou 'n' (não).")
    return None


def cadastrar_produto() -> None:
    """Adiciona um novo produto à lista mutável 'cardapio' e incrementa o ID."""
    global proximo_id_produto

    print("\n--- CADASTRAR PRODUTO NO CARDÁPIO ---")
    nome = ler_texto_obrigatorio("Nome do produto: ")
    if nome is None:
        return

    preco = ler_preco_positivo("Preço unitário (R$): ")
    if preco is None:
        return

    disponivel = ler_confirmacao("Produto disponível inicialmente? (s/n) [Enter = s]: ", padrao=True)
    if disponivel is None:
        return

    novo_produto = {
        "id": proximo_id_produto,
        "nome": nome,
        "preco": preco,
        "disponivel": disponivel,
    }

    # Atualização explícita de estado global
    cardapio.append(novo_produto)
    proximo_id_produto += 1

    situacao = "Disponível" if disponivel else "Indisponível"
    print(f"Sucesso: [{novo_produto['id']}] {nome} - R$ {preco:.2f} ({situacao}).")


def alternar_disponibilidade_produto() -> None:
    """Inverte o estado booleano de disponibilidade de um produto existente."""
    listar_cardapio()
    if not cardapio:
        return

    produto_id = ler_inteiro_positivo("ID do produto para alterar disponibilidade: ")
    if produto_id is None:
        return

    produto = buscar_produto_por_id(produto_id)
    if produto is None:
        print(f"Erro: produto com ID #{produto_id} não encontrado.")
        return

    produto["disponivel"] = not produto["disponivel"]
    novo_estado = "Disponível" if produto["disponivel"] else "Indisponível"
    print(f"Status atualizado: '{produto['nome']}' agora está {novo_estado}.")


def calcular_valores_pedido(itens: list[dict]) -> tuple[float, float, float]:
    """Calcula subtotal, desconto por faixa de valor e total líquido de um pedido."""
    subtotal = 0.0
    for item in itens:
        subtotal += item["preco_unitario"] * item["quantidade"]
    subtotal = round(subtotal, 2)

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
    """Registra um novo pedido com múltiplos itens válidos e disponíveis."""
    global proximo_id_pedido

    print("\n--- REGISTRAR NOVO PEDIDO ---")
    cliente = ler_texto_obrigatorio("Nome do cliente: ")
    if cliente is None:
        return

    itens_pedido: list[dict] = []

    # Laço de controle para adicionar um ou mais produtos ao pedido
    while True:
        listar_cardapio()
        produto_id = ler_inteiro_positivo("Digite o ID do produto: ")
        if produto_id is None:
            continue

        produto = buscar_produto_por_id(produto_id)
        if produto is None:
            print(f"Erro: ID #{produto_id} não existe no cardápio.")
            continue

        # Desafio adicional: bloqueio de pedido de item indisponível
        if not produto["disponivel"]:
            print(
                f"Operação bloqueada: '{produto['nome']}' está INDISPONÍVEL e não pode ser adicionado."
            )
            continue

        quantidade = ler_inteiro_positivo("Quantidade: ")
        if quantidade is None:
            continue

        # Acumula quantidade caso o mesmo produto já tenha sido incluído neste pedido
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

        print(f"Item adicionado: {quantidade}x {produto['nome']}.")

        # Garante resposta válida de continuação antes de prosseguir
        while True:
            continuar = ler_confirmacao("Deseja adicionar outro produto? (s/n): ")
            if continuar is not None:
                break

        if not continuar:
            break

    if not itens_pedido:
        print("Pedido não registrado: nenhum item válido foi adicionado.")
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
    print(f"Pedido #{novo_pedido['id']} | Cliente: {cliente} | Status: {novo_pedido['status']}")
    print(f"Subtotal: R$ {subtotal:.2f} | Desconto: R$ {desconto:.2f} | Total: R$ {total:.2f}")


def atualizar_status_pedido() -> None:
    """Avança o status do pedido conforme a ordem definida em STATUS_VALIDOS."""
    listar_pedidos()
    if not pedidos:
        return

    pedido_id = ler_inteiro_positivo("Digite o ID do pedido para atualizar o status: ")
    if pedido_id is None:
        return

    pedido = buscar_pedido_por_id(pedido_id)
    if pedido is None:
        print(f"Erro: pedido #{pedido_id} não encontrado.")
        return

    status_atual = pedido["status"]
    if status_atual not in STATUS_VALIDOS:
        print(f"Erro de consistência: status '{status_atual}' inválido.")
        return

    indice_atual = STATUS_VALIDOS.index(status_atual)
    if indice_atual >= len(STATUS_VALIDOS) - 1:
        print(f"Aviso: Pedido #{pedido['id']} já se encontra no status final '{status_atual}'.")
        return

    proximo_status = STATUS_VALIDOS[indice_atual + 1]
    confirmar = ler_confirmacao(
        f"Confirmar alteração do Pedido #{pedido['id']} de '{status_atual}' para '{proximo_status}'? (s/n): "
    )
    if confirmar is None:
        return

    if confirmar:
        pedido["status"] = proximo_status
        print(f"Sucesso: Pedido #{pedido['id']} agora está '{proximo_status}'.")
    else:
        print("Alteração de status cancelada pelo usuário.")


def listar_cardapio() -> None:
    """Exibe todos os produtos do cardápio com preço e disponibilidade."""
    print("\n--- CARDÁPIO ---")
    if not cardapio:
        print("Nenhum produto cadastrado.")
        return

    for produto in cardapio:
        situacao = "Disponível" if produto["disponivel"] else "Indisponível"
        print(
            f"[{produto['id']}] {produto['nome']} - "
            f"R$ {produto['preco']:.2f} ({situacao})"
        )


def listar_pedidos() -> None:
    """Exibe os pedidos registrados com itens, valores e status atual."""
    print("\n--- PEDIDOS REGISTRADOS ---")
    if not pedidos:
        print("Nenhum pedido registrado.")
        return

    for pedido in pedidos:
        print(
            f"\nPedido #{pedido['id']} | Cliente: {pedido['cliente']} | "
            f"Status: {pedido['status']} | Subtotal: R$ {pedido['subtotal']:.2f} | "
            f"Desconto: R$ {pedido['desconto']:.2f} | Total: R$ {pedido['total']:.2f}"
        )
        for item in pedido["itens"]:
            total_item = item["preco_unitario"] * item["quantidade"]
            print(
                f"   - {item['quantidade']}x {item['nome']} "
                f"(R$ {item['preco_unitario']:.2f} un.) = R$ {total_item:.2f}"
            )


def gerar_relatorio_vendas() -> None:
    """Calcula e exibe o resumo de pedidos por status e totais financeiros."""
    print("\n--- RELATÓRIO DE VENDAS ---")
    if not pedidos:
        print("Nenhum pedido registrado até o momento.")
        return

    soma_subtotais = 0.0
    soma_descontos = 0.0
    soma_totais = 0.0
    contagem_status = {status: 0 for status in STATUS_VALIDOS}

    for pedido in pedidos:
        soma_subtotais += pedido["subtotal"]
        soma_descontos += pedido["desconto"]
        soma_totais += pedido["total"]
        if pedido["status"] in contagem_status:
            contagem_status[pedido["status"]] += 1

    print(f"Total de pedidos: {len(pedidos)}")
    for status in STATUS_VALIDOS:
        print(f"  - {status.capitalize()}: {contagem_status[status]}")
    print(f"Total bruto (subtotais): R$ {soma_subtotais:.2f}")
    print(f"Total de descontos aplicados: R$ {soma_descontos:.2f}")
    print(f"Total líquido de vendas: R$ {soma_totais:.2f}")


def exibir_menu() -> None:
    """Exibe as opções disponíveis no menu principal."""
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
    """Laço principal imperativo que lê comandos e despacha para as funções do sistema."""
    while True:
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
            print("Encerrando o sistema...")
            break
        else:
            print("Opção inválida. Escolha um número entre 0 e 7.")


if __name__ == "__main__":
    executar_sistema()