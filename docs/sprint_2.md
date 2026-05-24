# Sprint 2

## Padroes GoF aplicados

- Strategy: `ItemDiscountStrategy`, `CustomerDiscountStrategy` e
  `PaymentStrategy` removem condicionais de desconto e pagamento.
- Observer: `NotificationService` publica eventos para observers de email,
  SMS, gerente de conta e pontos de fidelidade.
- Factory Method: `OrderFactory` cria `OrderDraft` e concentra a variacao de
  montagem de pedidos.
- Repository: `OrderRepositoryInterface` segue isolando SQLite da regra de
  negocio.

## SOLID

- OCP: novas regras entram por novas estrategias, observers e factories.
- DIP: `Sis` recebe abstracoes por construtor e nao depende de concretos para
  persistencia, pagamento, notificacao, estoque, relatorio ou criacao de
  pedido.
- LSP: `PedEspecial` deixou de herdar `Sis`; agora delega para uma instancia
  configurada por composicao, eliminando a substituicao problematica.

## UML

O diagrama Mermaid esta em `docs/diagrama_sprint2.mmd`.

## Validacoes

- `pytest -q`
- `mypy --strict src`
- `ruff check .`
- `radon cc . -s -a`
