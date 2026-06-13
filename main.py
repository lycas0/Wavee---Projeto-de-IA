from src.agent.agente import Agente


def main():
    agente = Agente()

    print("=== Wavee - Agente de Recomendação Musical ===")
    print("Digite uma palavra, frase ou trecho (ou 'sair' para encerrar)\n")

    while True:
        entrada = input("Você: ").strip()

        if entrada.lower() in ("sair", "exit", "quit"):
            break

        if not entrada:
            continue

        resultado = agente.agir(entrada)

        print(f"\nGênero identificado: {resultado['genero']}")
        print("Probabilidades por gênero:")
        for genero, prob in sorted(resultado["probabilidades"].items(), key=lambda x: -x[1]):
            print(f"  {genero}: {prob:.2%}")

        print("\nRecomendações:")
        for m in resultado["musicas"]:
            print(f"  - {m.nome} ({m.cantor})")

        print()

    agente.encerrar()
    print("Até mais!")


if __name__ == "__main__":
    main()