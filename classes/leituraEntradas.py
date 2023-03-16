def ler_instancia_cvrp(arquivo_instancia):
    # Inicializar os vetores de informações
    nome = ""
    comentario = ""
    tipo = ""
    dimensao = 0
    capacidade = 0
    coordenadas = {}
    demandas = {}
    deposito = 0
    
    # Abrir o arquivo da instância
    with open(arquivo_instancia, "r") as f:
        # Ler as linhas do arquivo
        linhas = f.readlines()
        
        # Loop sobre as linhas
        for linha in linhas:
            # Verificar o tipo de informação
            if linha.startswith("NAME"):
                nome = linha.split(":")[1].strip()
            elif linha.startswith("COMMENT"):
                comentario = linha.split(":")[1].strip()
            elif linha.startswith("TYPE"):
                tipo = linha.split(":")[1].strip()
            elif linha.startswith("DIMENSION"):
                dimensao = int(linha.split(":")[1].strip())
            elif linha.startswith("CAPACITY"):
                capacidade = int(linha.split(":")[1].strip())
            elif linha.startswith("NODE_COORD_SECTION"):
                # Ler as coordenadas dos nós
                for i in range(dimensao):
                    linha_coordenadas = linhas[linhas.index(linha) + 1 + i]
                    no, x, y = linha_coordenadas.strip().split()
                    coordenadas[int(no)] = (float(x), float(y))
            elif linha.startswith("DEMAND_SECTION"):
                # Ler as demandas dos nós
                for i in range(dimensao):
                    linha_demandas = linhas[linhas.index(linha) + 1 + i]
                    no, demanda = linha_demandas.strip().split()
                    demandas[int(no)] = int(demanda)
            elif linha.startswith("DEPOT_SECTION"):
                # Ler o nó do depósito
                deposito = int(linhas[linhas.index(linha) + 1].strip())
    
    # Retornar as informações da instância como um dicionário
    return {
        "nome": nome,
        "comentario": comentario,
        "tipo": tipo,
        "dimensao": dimensao,
        "capacidade": capacidade,
        "coordenadas": coordenadas,
        "demandas": demandas,
        "deposito": deposito
    }

instancia = ler_instancia_cvrp("instancias/A/A-n32-k5.vrp")
coordenadas = instancia["coordenadas"][1]
print(coordenadas)
print(instancia["demandas"])