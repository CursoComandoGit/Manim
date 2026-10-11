# Aula bônus 1: Complemento de dois

Animações do vídeo bônus 1 (anunciado na aula 6): como o computador guarda números negativos e por que,
com complemento de dois, a subtração vira uma soma comum.

## Renderizar

Dentro desta pasta:

```bash
uv run manim -pqh bonus1.py AulaCompleta   # vídeo inteiro, 1080p60 (~3:56)
uv run manim -pql bonus1.py SeteMenosCinco # uma cena, baixa qualidade
```

## Cenas (ordem do `AulaCompleta`)

Abertura · Resumo · Pergunta · SinalMagnitude · SomaSinalMagnitude · CircuitosComplexos · Genialidade ·
PesoNegativo · CincoPositivo · CincoNegativo · Truque · PorQueMelhor · SeteMenosCinco · CincoMenosCinco ·
Vantagem · Final · Creditos

- `PesoNegativo`, `CincoPositivo` e `CincoNegativo` usam a mesma fita (`self.fita_pesos`) no vídeo inteiro.
  Renderizadas sozinhas, cada uma cria a sua.
- `SomaBinaria` monta as contas armadas: os vai-uns aparecem em roxo sobre a próxima coluna, e o bit que
  transborda fica fora da fita, à esquerda do resultado, antes de ser descartado.
- A frase do roteiro "Na aula 6, comentamos como representar números na base 2" não tem animação
  (pedido do roteiro).

## Padronização

Cores, fontes (Manrope e DejaVu Sans Mono), fundo `#1E1E1E`, `Code`/cards e a vinheta final seguem o
documento de padronização e as aulas anteriores.
