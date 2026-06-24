from lodestar_veritas.graph import LodestarGraph


def main():
    graph = LodestarGraph()

    print("=" * 70)
    print("            Lodestar Veritas - Agentic RAG CLI")
    print("=" * 70)

    while True:
        query = input("\nAsk a question (or type 'exit'): ").strip()

        if query.lower() in {"exit", "quit"}:
            print("\nGoodbye.")
            break

        state = graph.run(
            query=query,
            file_paths=[],
        )

        print("\n" + "=" * 70)
        print("ANSWER")
        print("=" * 70)
        print(state.answer)

        print("\nSources")
        print("-" * 70)

        if state.sources:
            for source in state.sources:
                print(source)
        else:
            print("No sources available.")

        print("\nConfidence")
        print("-" * 70)
        print(state.confidence)

        print("\nVerification")
        print("-" * 70)
        print(state.verification)

        print("\nGuardrails")
        print("-" * 70)
        print(state.guardrails)

        print("\nWorkflow Events")
        print("-" * 70)

        for event in state.events:
            print("•", event)

        print("\n" + "=" * 70)


if __name__ == "__main__":
    main()