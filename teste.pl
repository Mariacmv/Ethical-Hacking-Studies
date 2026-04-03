%fatos
mochila(verde).
mochila(azul).
mochila(vermelho).
mochila(amarelo).
mochila(branco).
nome(otavio).
nome(will).
nome(denis).
nome(joao).
nome(lenin).
mes(janeiro).
mes(agosto).
mes(dezembro).
mes(setembro).
mes(maio).
jogo(cacapalavras).
jogo(tresoumais).
jogo(forca).
jogo(logica).
jogo(cubovermelho).
materia(geografia).
materia(historia).
materia(matematica).
materia(portugues).
materia(biologia).
suco(limao).
suco(maracuja).
suco(morango).
suco(uva).
suco(laranja).

alldifferent([]).
alldifferent([H|T]) :-
    \+ member(H, T),
    alldifferent(T).

%modelo define a estrutura, como os elementos se relacionam
modelo(L) :- % * significa uma regra
    L = [ %separação do modelo com as lógicas
        (M1,N1,MS1,J1,MA1,S1),
        (M2,N2,MS2,J2,MA2,S2),
        (M3,N3,MS3,J3,MA3,S3),
        (M4,N4,MS4,J4,MA4,S4),
        (M5,N5,MS5,J5,MA5,S5)
    ],

    permutation([verde,azul,vermelho,amarelo,branco], [M1,M2,M3,M4,M5]),
    permutation([otavio,will,denis,joao,lenin], [N1,N2,N3,N4,N5]),
    permutation([janeiro,agosto,dezembro,setembro,maio], [MS1,MS2,MS3,MS4,MS5]),
    permutation([cacapalavras,tresoumais,forca,logica,cubovermelho], [J1,J2,J3,J4,J5]),
    permutation([geografia,historia,matematica,portugues,biologia], [MA1,MA2,MA3,MA4,MA5]),
    permutation([limao,maracuja,morango,uva,laranja], [S1,S2,S3,S4,S5]),

    member((_,joao,_,_,historia,_), L), % *joão gosta de história. _ representa que não importa os outros elementos
    member((_,_,_,_,biologia,morango), L), % *O garoto que gosta de biologia gosta de suco de morango
    nth1(Iset, L, (_,_,setembro,_,_,_)), % *O menino que nasceu no mês de setembro está ao lado de quem gosta de suco de laranja
    ( %*
    	(Iset > 1, I1 is Iset - 1, nth1(I1, L, (_, _, _, _, _, laranja))); %confere do lado esquerdo. Confere se a posição é válida e confere se o vizinho à esquerda é "laranja"
    	(Iset < 5, I2 is Iset + 1, nth1(I2, L, (_, _, _, _, _, laranja))) %confere do lado direito. Confere se a posição é válida e confere se o vizinho à esquerda é "laranja"
    ),
    nth1(Ibra, L, (branco, _, _, _, _, _)), % *nth -> enésimo, refere-se à posição genérica em uma sequência. Encontra onde está "branco"
    Ibra < 5, %não está na posição 5
    I2b is Ibra + 1, %posição exatamente à direita
    nth1(I2b, L, (_, will, _, _, _, _)), %will esteja na posição 2

    (
    	nth1(1, L, (_, otavio, _,_,_,_)); % *"otavio" está em uma das pontas, ou seja, na primeira
    	nth1(5, L, (_, otavio, _,_,_,_))  %ou na última
    ),
    nth1(Iazul, L, (azul,_,_,_,_,_)),% *mochila azul está à esquerda de quem nasceu em maio
    nth1(Jmaio, L, (_,_,maio,_,_,_)),
    Iazul < Jmaio, % azul está antes de maio

    nth1(3, L, (_, _, _, _, _, morango)), % *morango está na terceira posição
    nth1(1, L, (_, _, _, _, _, limao)), % *limão está na primeira posição
    nth1(5, L, (_, lenin, _, _, _, _)). % *lenin está na quinta posição


%main
main :-
    modelo(L), 
    write(L),nl. %imprime o modelo
    %write(L), nl, !. utilize o exclamação para mostrar apenas a primeira solução
    %fail.
main.
