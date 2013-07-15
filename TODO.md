TODO
====


Aplicacao
---------

Listener daemon +++
Evitar recursividade infinita na execucao de commands e listeners ++

CommandGroup (Recurso para registrar sequencia de commandos) ++++
- Tem slug, label, commands
- Interface para construção
  - Barra com lista de commands a esquerda
    - Criar include ou templatetag que retorna a mesma lista de commands da pagina inicial

  - Corpo
    - Os icones podem trocar de posicao
        - Tem sempre um icone no inicio e no fim que representa um espaço vazio para adicionar novos commands


    -------------  -------------  -------------  -------------  -------------  ------------- 
    |           |  |           |  |           |  |           |  |           |  |           | 
    |     +     |  |   luz     |  |   luz     |  |    luz    |  |    luz    |  |  Projetor | 
    |           |  |           |  |           |  |           |  |           |  |           | 
    | Add here  |  |  Entrada  |  |   Sala    |  |  Quarto   |  | Corredor  |  |    I/O    | 
    |           |  |           |  |           |  |           |  |           |  |           | 
    -------------  -------------  -------------  -------------  -------------  ------------- 





Arduino
-------

Completar 433 ++


Layout
------

Poder arrastar commands +
Guardar configuracoes +
Trocar cor dos commands
