infos = [
    "João",
    "Paulo",
    "Brasil",
    "Desempregado",
    "Solteiro",
    "Ensino superior",
    "25"
]

nome, sobrenome, *_, escolaridade, idade = infos
print(f"{nome} {sobrenome} tem {escolaridade} e {idade} anos")