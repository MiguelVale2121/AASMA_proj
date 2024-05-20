def extrair_valores(lista_de_dicionarios):
        valores = []
        for dicionario in lista_de_dicionarios:
            for valor in dicionario.values():
                valores.append(valor)
        return valores
    
def convert_dicKeys_to_tuple(dic):
    return tuple(dic.keys())[0]

def inverse_position(pos):
    if pos == "up":
        return "down"
    elif pos == "down":
        return "up"
    elif pos == "left":
        return "right"
    elif pos == "right":
        return "left"