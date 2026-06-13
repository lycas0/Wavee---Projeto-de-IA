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
    
        musicas_recomendadas = resultado["musicas"] #guardar o resultado para usar como lista de opções para o usuário

        print(f"\nGênero identificado: {resultado['genero']}")
        print("Probabilidades por gênero:")
        for genero, prob in sorted(resultado["probabilidades"].items(), key=lambda x: -x[1]):
            print(f"  {genero}: {prob:.2%}")

        #print("\nRecomendações:")
        #for m in resultado["musicas"]:
            #print(f"  - {m.nome} ({m.cantor})")

        print("\nRecomendações:")
        for i, m in enumerate (musicas_recomendadas, start=1):
            print(f"  [{i}] - {m.nome} ({m.cantor})")

        print()

        #usando a função registrar_feedback na main
        if musicas_recomendadas:
            try:
                escolha = int(input("Digite o número da música que você deseja ouvir, ou digite 0 se não deseja ouvir nenhuma: ").strip())

                if 1 <= escolha <= len(musicas_recomendadas):
                    musica_escolhida = musicas_recomendadas[escolha - 1] 

                    print(f"Tocando: {musica_escolhida.nome}")

                    agente.registrar_feedback(
                        entrada_texto=entrada,
                        genero_nome=resultado['genero'],
                        musica_id=musica_escolhida.id,
                        gostou=True
                    ) #aqui o agente guarda a interação e aprende com ela 
                else:
                    print("Nenhuma música foi selecionada")

            except ValueError:
                print("\nOpção inválida, volte para a busca")
                

    agente.encerrar()
    print("Até mais!")


if __name__ == "__main__":
    main()