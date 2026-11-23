"""
Projeto 10: Sistema de Gerenciamento de Pedidos de Restaurante
Disciplina: Paradigmas de Programação - UNINASSAU (Aula 07)
Paradigma: Imperativo (estado mutável, sequenciamento explícito, condicionais e laços)
"""

STATUS_VALIDOS = ["recebido", "em preparação", "pronto", "entregue"]

# Estado mutável global do sistema (base do paradigma imperativo)
cardapio = [
    {"id": 1, "nome": "Hambúrguer Artesanal", "preco": 32.00, "disponivel": True},
    {"id": 2, "nome": "Batata Frita Média", "preco": 18.00, "disponivel": True},
    {"id": 3, "nome": "Refrigerante Lata", "preco": 7.50, "disponivel": True},
    {"id": 4, "nome": "Salmão Grelhado", "preco": 58.00, "disponivel": False},  # Dados de teste: indisponível
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
            f"Pedido #{pedido['id']} | Cliente: {pedido['cliente']} | "
            f"Status: {pedido['status']} | Subtotal: R$ {pedido['subtotal']:.2f} | "
            f"Desconto: R$ {pedido['desconto']:.2f} | Total: R$ {pedido['total']:.2f}"
        )
        for item in pedido["itens"]:
            subtotal_item = item["preco_unitario"] * item["quantidade"]
            print(
                f"   - {item['quantidade']}x {item['nome']} "
                f"(R$ {item['preco_unitario']:.2f} un.) = R$ {subtotal_item:.2f}"
            )


def exibir_menu() -> None:
    """Exibe as opções disponíveis no terminal."""
    print("\n=== SISTEMA DE PEDIDOS - RESTAURANTE (GRUPO 10) ===")
    print("1 - Listar cardápio")
    print("2 - Listar pedidos")
    print("0 - Sair")


def executar_sistema() -> None:
    """Controla o fluxo principal por laço de repetição e estruturas condicionais."""
    executando = True

    while executando:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            listar_cardapio()
        elif opcao == "2":
            listar_pedidos()
        elif opcao == "0":
            executando = False
            print("Encerrando o sistema...")
        else:
            print("Opção inválida. Digite 1, 2 ou 0.")


if __name__ == "__main__":
    executar_sistema()