**!! Atenção: Renomeie o seu repositório para (Tema)_(NomeDoProjeto). !!** 

Temas:
 - Greed

# NomedoProjeto

**Número da Lista**: X<br>
**Conteúdo da Disciplina**: Greed<br>

## Alunos

|Matrícula | Aluno |
| -- | -- |
| 21/1062179  |  Marcelo de Araújo Lopes |
| 17/0020339  |  Paulo Lucca |

## Sobre 
Descreva os objetivos do seu projeto e como ele funciona. 

## Screenshots
Adicione 3 ou mais screenshots do projeto em funcionamento.

## Instalação 
**Linguagem**: xxxxxx<br>
**Framework**: (caso exista)<br>
Descreva os pré-requisitos para rodar o seu projeto e os comandos necessários.

## Uso 
Explique como usar seu projeto caso haja algum passo a passo após o comando de execução.

## Algoritmo: Interval Partitioning

Cada turma é quebrada em blocos (turma × dia de aula), e cada bloco é um intervalo
`[início, fim)`. A alocação é **por bloco**: a mesma turma pode ficar em salas
diferentes em dias diferentes, como já acontece no SIGAA.

Guloso (`alocacao.py`):

1. Ordena os blocos por dia e hora de início (no empate, a turma maior primeiro).
2. Para cada bloco, olha as salas livres naquele horário que comportam as vagas da turma.
3. Escolhe uma sala já aberta naquele dia, se houver; senão, abre a menor sala que serve.
4. Se nenhuma sala serve, o bloco entra no relatório de não alocados.

**Lower bound.** A profundidade `d` é o maior número de blocos acontecendo ao
mesmo tempo. Qualquer alocação precisa de pelo menos `d` salas, porque esses
blocos se sobrepõem dois a dois.

**Prova de otimalidade (caso clássico, salas sem limite de capacidade).** Suponha
que o guloso abra a sala `k` para um bloco `b`. Ele só abre uma sala nova quando
as `k − 1` salas já abertas estão ocupadas no início de `b`. Como os blocos são
processados por hora de início, cada um desses `k − 1` blocos começou antes de
`b` e ainda não terminou, então todos contêm o instante em que `b` começa. Junto
com `b`, são `k` blocos sobrepostos, logo `k ≤ d`. O guloso nunca usa mais que `d`
salas, e nenhuma solução usa menos, então ele é ótimo.

Com capacidade, a sala aberta pode não servir para a turma, e o guloso pode passar
de `d`. Nos dados de 2026.2, os 430 blocos são todos alocados, com pico de 30 salas
num dia contra um lower bound de 28.

## Outros 
Quaisquer outras informações sobre seu projeto podem ser descritas abaixo.




