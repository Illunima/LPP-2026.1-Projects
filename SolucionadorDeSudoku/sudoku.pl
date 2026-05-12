:- use_module(library(clpfd)).
 
sudoku(Rows) :- % Cria um tabuleiro de Sudoku a partir de uma lista de listas (Rows)
        length(Rows, 9), maplist(length_(9), Rows),
        append(Rows, Vs), Vs ins 1..9,
        maplist(all_distinct, Rows),
        transpose(Rows, Columns), maplist(all_distinct, Columns),
        Rows = [A,B,C,D,E,F,G,H,I],
        blocks(A, B, C), blocks(D, E, F), blocks(G, H, I).
 
length_(L, Ls) :- length(Ls, L).

blocks([], [], []).
blocks([A,B,C|Bs1], [D,E,F|Bs2], [G,H,I|Bs3]) :-
        all_distinct([A,B,C,D,E,F,G,H,I]),
        blocks(Bs1, Bs2, Bs3).

resolver_interativo :-
    writeln('Digite o tabuleiro como uma lista de listas (use _ para vazios):'),
    read(Rows),          % Lê o que você digitar no terminal
    sudoku(Rows),        % Aplica a lógica
    writeln('Solução encontrada:'),
    maplist(portray_clause, Rows).

problem(1, [[_,_,_,_,_,_,_,_,_],  % Exemplo de tabuleiro de Sudoku (use _ para vazios)
            [_,_,_,_,_,3,_,8,5],
            [_,_,1,_,2,_,_,_,_],
            [_,_,_,5,_,7,_,_,_],
            [_,_,4,_,_,_,1,_,_],
            [_,9,_,_,_,_,_,_,_],
            [5,_,_,_,_,_,_,7,3],
            [_,_,2,_,1,_,_,_,_],
            [_,_,_,_,4,_,_,_,9]]).

        