# Importa numpy como np:
import numpy as np
# Importa pyplot como plt:
import matplotlib.pyplot as plt
# Importa geradores_de_sequencias como gseq:
import geradores_de_sequencias as gseq
# Importa verificadores como ver:
import verificadores as ver

# config = {"tipo":, "titulo":, "rotulo_de_x":, "rotulo_de_y":, "grade":, "legenda":, "cor":}
# (X, Y, tipo='line', titulo=None, rotulo_de_x=None, rotulo_de_y=None, grade=True, legenda=None, cor='blue'):

# Y_t: Series pandas que representa uma sequência contínua;
# config: dicionário de configurações de uma sequência;
# t: eixo temporal.
def configura_sequencia_em_grafico(Y_t, config, t=None):
    # Se não for passado o eixo temporal t:
    if t is None:
        # Cria eixo das abscissas respectivo a ordem temporal:
        t =  np.arange(Y_t.size)
    
    # Cria desenho da sequência conforme solicitado:
    if config["tipo"] == "line":
        plt.plot(t, Y_t, label=config["legenda"], color=config["cor"])
    elif config["tipo"] == "scatter":
        plt.scatter(t, Y_t, label=config["legenda"], color=config["cor"], s=1, alpha=0.5)
    elif config["tipo"] == "bar":
        plt.bar(t, Y_t, label=config["legenda"], color=config["cor"])
    else:
        # Imprime aviso:
        print(f"Tipo de desenho \"{config["tipo"]}\" não suportado. Será usado o tipo \"line\".")
        plt.plot(t, Y_t, label=config["legenda"], color=config["cor"])

# seqs_Y_t: lista de Series pandas, das quais cada uma representa uma sequência contínua;
# config_seqs: lista de dicionários de configurações respectivas às sequências;
# config_graf: dicionário de configurações gerais do gráfico;
# t: eixo temporal.
def configura_grafico(seqs_Y_t, config_seqs, config_graf, t=None):
    # Se não for passado o eixo temporal t:
    if t is None:
        # Cria eixo das abscissas respectivo a ordem temporal:
        t =  np.arange(seqs_Y_t[0].size)

    # Para todas as configurações de sequências:
    for i, config_seq in enumerate(config_seqs):
        # Configura a sequência respesctiva no gráfico corrente:
        configura_sequencia_em_grafico(seqs_Y_t[i], config_seq, t)
    
    # Adiciona título e rótulos dos eixos se fornecidos:
    if config_graf["titulo"]:
        plt.title(config_graf["titulo"]) 
    if config_graf["rotulo_de_x"]:
        plt.xlabel(config_graf["rotulo_de_x"])
    if config_graf["rotulo_de_y"]:
        plt.ylabel(config_graf["rotulo_de_y"])

    # Exibe as legendas, se alguma foi fornecida:
    if config_seqs[0]["legenda"]:
        plt.legend()

    # Secciona o gráfico por linhas e colunas se solicitado:
    if config_graf["grade"]:
        plt.grid(True)

# seqs_Y_t: lista de Series pandas, das quais cada uma representa uma sequência contínua;
# config_seqs: lista de dicionários de configurações respectivas às sequências;
# config_graf: dicionário de configurações gerais do gráfico;
# t: eixo temporal.
def plota_grafico_de_sequencias(seqs_Y_t, config_seqs, config_graf, t=None):
    # Se não for passado o eixo temporal t:
    if t is None:
        # Cria eixo das abscissas respectivo a ordem temporal:
        t =  np.arange(seqs_Y_t[0].size)

    # Configura o gráfico respectivo:
    configura_grafico(seqs_Y_t, config_seqs, config_graf, t)
    # Exibe o gráfico:
    plt.show()

# axes: referência de subgráfico;
# Y_t: Series pandas que representa uma sequência contínua;
# config: dicionário de configurações de uma sequência;
# t: eixo temporal.
def configura_sequencia_em_subgrafico(axes, Y_t, config, t=None):
    # Se não for passado o eixo temporal t:
    if t is None:
        # Cria eixo das abscissas respectivo a ordem temporal:
        t =  np.arange(Y_t.size)
    
    # Cria desenho da sequência conforme solicitado:
    if config["tipo"] == "line":
        axes.plot(t, Y_t, label=config["legenda"], color=config["cor"])
    elif config["tipo"] == "scatter":
        axes.scatter(t, Y_t, label=config["legenda"], color=config["cor"], s=1, alpha=0.5)
    elif config["tipo"] == "bar":
        axes.bar(t, Y_t, label=config["legenda"], color=config["cor"])
    else:
        # Imprime aviso:
        print(f"Tipo de desenho \"{config['tipo']}\" não suportado. Será usado o tipo \"line\".")
        axes.plot(t, Y_t, label=config["legenda"], color=config["cor"])

# axes: referência de subgráfico;
# seqs_Y_t: lista de Series pandas, das quais cada uma representa uma sequência contínua;
# config_seqs: lista de dicionários de configurações respectivas às sequências de um subgráfico;
# config_graf: dicionário de configurações gerais do subgráfico;
# t: eixo temporal.
def configura_subgrafico(axes, seqs_Y_t, config_seqs, config_graf, t=None):
    # Se não for passado o eixo temporal t:
    if t is None:
        # Cria eixo das abscissas respectivo a ordem temporal:
        t =  np.arange(seqs_Y_t[0].size)

    # Para todas as sequências e suas configurações:
    for seq, config_seq in zip(seqs_Y_t, config_seqs):
        # Configura a sequência respesctiva no gráfico corrente:
        configura_sequencia_em_subgrafico(axes, seq, config_seq, t)
    
    # Adiciona título e rótulos dos eixos se fornecidos:
    if config_graf["titulo"]:
        axes.set_title(config_graf["titulo"]) 
    if config_graf["rotulo_de_x"]:
        axes.set_xlabel(config_graf["rotulo_de_x"])
    if config_graf["rotulo_de_y"]:
        axes.set_ylabel(config_graf["rotulo_de_y"])

    # Exibe as legendas, se alguma foi fornecida:
    if config_seqs[0]["legenda"]:
        axes.legend()

    # Secciona o gráfico por linhas e colunas se solicitado:
    if config_graf["grade"]:
        axes.grid(True)

# k: número de subgráficos;
# seqs_Y_t: lista de lista de Series pandas, das quais cada Series representa uma sequência contínua;
# config_seqs: lista de lista de dicionários de configurações respectivas às sequências de cada subgráfico;
# config_graf: lista de dicionários de configurações gerais dos subgráficos;
# t: eixo temporal.
def configura_grafico_de_subgraficos(k, seqs_Y_t, config_seqs, config_graf, t=None):
    # Se k não for inteiro:
    if not isinstance(k, int):
        # Levanta exceção de tipo:
        raise TypeError("O número de subgráficos k deve ser do tipo inteiro.")
    # Se k não for um natural não nulo:
    if k <= 0:
        # Levanta exceção de valor:
        raise ValueError("O número de subgráficos k deve ser um natural não nulo.")

    # Se não for passado o eixo temporal t:
    if t is None:
        # Cria eixo das abscissas respectivo a ordem temporal:
        t =  np.arange(seqs_Y_t[0][0].size)
        # t =  np.arange(len(seqs_Y_t[0][0]))

    # Se k for um:
    if k == 1:
        configura_grafico(seqs_Y_t[0], config_seqs[0], config_graf[0], t)
    # Senão, se k for dois:
    elif k == 2:
        # Cria vetor de gráficos:
        fig, axes = plt.subplots(1, 2, figsize=(15, 10))
        # Para todos os subgráficos:
        for i in range(0, 2):
            # Cria subgráfico:
            configura_subgrafico(axes[i], seqs_Y_t[i], config_seqs[i], config_graf[i], t)
    # Senão:
    else:
        # Inicia indicador de subgráfico:
        z = 0
        # Se k for ímpar:
        if k%2:
            # Se k é primo:
            if ver.eh_primo(k):
                # Pega os dois fatores dos quais o maior deles é o menor possível para ser maior
                # das possibilidades de pares de fatores que se multiplicados descrevem k+1:
                f = gseq.decomposicao_em_dupla_de_fatores_mais_proximos(k+1)
                # print(f"({f[0]}, {f[1]})")
                # Cria matriz de subgráficos:
                fig, axes = plt.subplots(f[0], f[1], figsize=(15, 10))
                # Para todas as linhas (exceto a última):
                for i in range(0, f[0]-1):
                    # Para todas as colunas:
                    for j in range(0, f[1]):
                       # Cria subgráfico:
                        configura_subgrafico(axes[i, j], seqs_Y_t[z], config_seqs[z], config_graf[z], t)
                        # Avança indicador:
                        z += 1
                # Para todas as colunas (exceto a última) da última linha:
                for j in range(0, f[1]-1):
                    # Cria subgráfico:
                    configura_subgrafico(axes[f[0]-1, j], seqs_Y_t[z], config_seqs[z], config_graf[z], t)
                    # Avança indicador:
                    z += 1
                # Desativa a exibição da última célula de subgráfico:
                axes[f[0]-1, f[1]-1].axis('off')
            # Senão:
            else:
                # Pega os dois fatores dos quais o maior deles é o menor possível para ser maior
                # das possibilidades de pares de fatores que se multiplicados descrevem k:
                f = gseq.decomposicao_em_dupla_de_fatores_mais_proximos(k)
                # print(f"({f[0]}, {f[1]})")
                # Cria matriz de subgráficos:
                fig, axes = plt.subplots(f[0], f[1], figsize=(15, 10))
                # Para todas as linhas:
                for i in range(0, f[0]):
                    # Para todas as colunas:
                    for j in range(0, f[1]):
                        # Cria subgráfico:
                        configura_subgrafico(axes[i, j], seqs_Y_t[z], config_seqs[z], config_graf[z], t)
                        # Avança indicador:
                        z += 1
        # Senão, se k par:
        else:
            # Pega os dois fatores dos quais o maior deles é o menor possível para ser maior
            # das possibilidades de pares de fatores que se multiplicados descrevem k:
            f = gseq.decomposicao_em_dupla_de_fatores_mais_proximos(k)
            # print(f"({f[0]}, {f[1]})")
            # Cria matriz de gráficos:
            fig, axes = plt.subplots(f[0], f[1], figsize=(15, 10))
            # Para todas as linhas:
            for i in range(0, f[0]):
                # Para todas as colunas:
                for j in range(0, f[1]):
                    # Cria subgráfico:
                    configura_subgrafico(axes[i, j], seqs_Y_t[z], config_seqs[z], config_graf[z], t)
                    # Avança indicador:
                    z += 1
    # Ajusta layout para evitar sobreposição de labels:
    plt.tight_layout()

# k: número de subgráficos;
# seqs_Y_t: lista de lista de Series pandas, das quais cada Series representa uma sequência contínua;
# config_seqs: lista de lista de dicionários de configurações respectivas às sequências de cada subgráfico;
# config_graf: lista de dicionários de configurações gerais dos subgráficos;
# t: eixo temporal.
def plota_grafico_de_subgraficos_de_sequencias(k, seqs_Y_t, config_seqs, config_graf, t=None):
     # Se não for passado o eixo temporal t:
    if t is None:
        # Cria eixo das abscissas respectivo a ordem temporal:
        t =  np.arange(seqs_Y_t[0][0].size)

    # Configura o gráfico respectivo:
    configura_grafico_de_subgraficos(k, seqs_Y_t, config_seqs, config_graf, t)
    # Exibe o gráfico:
    plt.show()
