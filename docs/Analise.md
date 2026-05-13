# Análise Inicial do Sistema Legado

O sistema legado fornecido apresenta diversos problemas arquiteturais relacionados aos princípios SOLID, Clean Code e organização em camadas.

O objetivo desta análise é identificar violações arquiteturais existentes, compreender os impactos dessas decisões no processo de manutenção e preparar o sistema para uma futura refatoração orientada por testes.

Antes de iniciar qualquer modificação estrutural, foram criados testes de caracterização (Golden Master Tests) com o objetivo de preservar o comportamento original do sistema e evitar regressões funcionais durante o processo de refatoração.

# Violação do Princípio SRP (Single Responsibility Principle)

A classe `Sis` concentra múltiplas responsabilidades dentro de uma única estrutura, violando o princípio da responsabilidade única.

Responsabilidades identificadas:
- Persistência de dados em SQLite
- Processamento de pagamentos
- Cálculo de descontos
- Controle de status de pedidos
- Geração de relatórios
- Validação de estoque
- Envio de notificações

Trechos relacionados:
- `add_ped`
- `proc_pag`
- `gerar_rel`
- `validar_estoque`

Impacto arquitetural:
Alterações em funcionalidades específicas aumentam o risco de efeitos colaterais em partes não relacionadas do sistema, dificultando manutenção, testes e reutilização de código.

Exemplo:
Uma mudança no sistema de notificações exige alteração direta dentro da classe principal do sistema.

Solução planejada:
Separação das responsabilidades em camadas independentes utilizando:
- Services
- Repositories
- Notification Services
- Payment Strategies

# Violação do Princípio OCP (Open/Closed Principle)

O sistema atual depende fortemente de estruturas condicionais (`if/elif`) para definir comportamentos relacionados a pagamentos, descontos e tipos de cliente.

Trechos relacionados:
- Método `proc_pag`
- Método `add_ped`

Exemplo identificado:

```python
if m == 'cartao':
    ...
elif m == 'pix':
    ...
elif m == 'boleto':
    ...
```

Problema:
Sempre que um novo método de pagamento for adicionado, será necessário modificar o código existente, aumentando o risco de regressões.

Impacto arquitetural:
A arquitetura atual dificulta extensão do sistema sem alteração direta de classes existentes.

Solução planejada:
Aplicação do padrão Strategy para encapsular métodos de pagamento e descontos em estratégias independentes.

# Violação do Princípio LSP (Liskov Substitution Principle)

A classe `PedEspecial` herda da classe `Sis`, porém altera comportamentos fundamentais esperados da classe pai.

Trechos relacionados:
- Método `add_ped`
- Método `upd_st`

Problema identificado:
A subclasse modifica regras importantes do sistema original, como o fluxo de atualização de status e cálculo de valores, sem preservar o comportamento esperado da classe base.

Exemplo:
O método `upd_st` em `PedEspecial` ignora completamente validações e transições existentes na implementação original.

Impacto arquitetural:
Objetos da subclasse não podem substituir objetos da classe pai de forma segura, podendo gerar inconsistências no sistema.

Solução planejada:
Substituir herança inadequada por composição e estratégias específicas para comportamentos especiais.

# Violação do Princípio ISP (Interface Segregation Principle)

A estrutura atual concentra múltiplos comportamentos em uma única classe monolítica, obrigando clientes do sistema a dependerem de funcionalidades que não utilizam diretamente.

Problema identificado:
A classe `Sis` possui métodos relacionados a:
- pagamentos
- relatórios
- estoque
- notificações
- persistência
- pedidos

Impacto arquitetural:
A ausência de segregação aumenta acoplamento, dificulta manutenção e reduz reutilização de componentes específicos.

Exemplo:
Uma funcionalidade que necessita apenas de geração de relatórios depende indiretamente de métodos relacionados a pagamento e estoque.

Solução planejada:
Separação das responsabilidades em interfaces menores e especializadas, como:
- PaymentService
- ReportService
- InventoryService
- NotificationService

# Violação do Princípio DIP (Dependency Inversion Principle)

O sistema atual depende diretamente de implementações concretas, dificultando extensibilidade e testes isolados.

Trechos relacionados:
- SQLite diretamente na classe principal
- Impressões via `print`
- Regras de pagamento implementadas diretamente em condicionais

Problema identificado:
A classe `Sis` controla diretamente detalhes de infraestrutura e implementação, sem abstrações intermediárias.

Impacto arquitetural:
Mudanças em banco de dados, notificações ou pagamentos exigem alteração direta da lógica principal do sistema.

Exemplo:
A substituição do SQLite por outro banco exigiria modificações internas na classe principal.

Solução planejada:
Introdução de abstrações utilizando:
- Repositories
- Interfaces
- Injeção de dependência
- Serviços desacoplados