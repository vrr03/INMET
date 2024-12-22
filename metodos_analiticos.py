# Importa math:
import math
# Importa numpy como np:
import numpy as np
# Importa Polynomial de numpy.polynomial:
from numpy.polynomial import Polynomial
# Importa o módulo metodos_descritivos como mdes:
import metodos_descritivos as mdes
# Importa pandas como pd:
import pandas as pd
# Importa stats de scipy:
from scipy import stats
# Importa curve_fit de scipy.optimize:
from scipy.optimize import curve_fit
# Importa o módulo sys:
import sys

# df: dataframe;
# atr_temporal: nome do atributo que indica a ordem temporal;
# atr_imagem: nome do atributo a ser descrito como sequencia temporal.
def gera_sequencia_temporal_de_media_por_data(df, atr_temporal, atr_imagem):
    # Agrupa as tuplas pelas datas (sem horário) e calcula a média dos valores
    # dos campos referentes ao atributo imagem para cada grupo:
    media_por_dia = df.groupby(df[atr_temporal].dt.date)[atr_imagem].mean()
    # Retorna as médias ordenadas pelas datas em ordem crescente:
    return media_por_dia.sort_index()

# Y_t: sequência de dados cronológicos.
def eh_possivel_aplicar_Box_Cox(Y_t):
    # Para todos os dados:
    for dado in Y_t:
        # Se o dado é nulo (None ou NaN):
        if pd.isna(dado):
            # Retorna False.
            return False
        # Se o dado é menor ou igual a zero, ou muito próximo de zero:
        elif dado <= 0 or math.isclose(dado, 0):
            # Retorna False.
            return False
    # Se nenhum dado falhou nas condições, retorna True:
    return True

# Y_t: sequência de dados cronológicos.
# t: eixo temporal.
def tenta_aplicar_transformacao_Box_Cox(Y_t, t=None):
    # Se não for passado o eixo temporal t:
    if t is None:
        # Cria eixo das abscissas respectivo a ordem temporal:
        t = np.arange(Y_t.size)
     # Se é possível aplicar tranformação de Box-Cox:
    if eh_possivel_aplicar_Box_Cox(Y_t):
        # Aplica a transformação de Box-Cox:
        Z_t, valor_lambda = stats.boxcox(Y_t)
        # Retorna dupla de sequência transformada e o parâmetro da transformação:
        return (Z_t, valor_lambda)
    # Senão:
    else:
        # Retorna dupla com apenas a sequência original:
        return (Y_t, None)

# t: índice de ordem temporal;
# parâmetros: parâmetros que descrevem um polinômio harmônico. 
def polinomio_harmonico(t, *parametros):
    # Número de termos:
    h = (len(parametros)-1)//2
    # Período da sazonalidade:
    p = parametros[-1]
    # Inicia resultado com zero:
    resultado = 0
    # Para cada termo:
    for j in range(h):
        # Pega o coeficiente alfa_j:
        alfa = parametros[j]
        # Pega o coeficiente beta_j:
        beta = parametros[h+j]
        # Calcula lambda_j:
        lambda_j = (2*np.pi*(j+1))/p
        # Acumula resultado parcial do termo:
        resultado += alfa*np.cos(lambda_j*t) + beta*np.sin(lambda_j*t)
    # Retorna resultado final.
    return resultado

# Y_t: sequência de dados cronológicos.
# h: número de termos para a função de ajuste;
# p: comprimento de período relativo ao passo temporal de uma unidade;
# t: eixo temporal.
def ajusta_sequencia_de_polinomio_harmonico_para_sazonalidade(Y_t, h, p, t=None):
    # Se h não for inteiro:
    if not isinstance(h, int):
        # Levanta exceção de tipo:
        raise TypeError("O número de termos h deve ser do tipo inteiro.")
    # Se h não for um natural não nulo:
    if h <= 0:
        # Levanta exceção de valor:
        raise ValueError("O número de termos h deve ser um natural não nulo.")
    # Se p não for um float positivo não nulo:
    if p <= 0:
        # Levanta exceção de valor:
        raise ValueError("O comprimento de período p deve ser um número real positivo não nulo.")
    # Se não for passado o eixo temporal t:
    if t is None:
        # Cria eixo das abscissas respectivo a ordem temporal:
        t =  np.arange(Y_t.size)
        # Cria eixo temporal t usando o índice da Series:
        # t = Y_t.index.values
        # Observação sobre a linha comentada acima: essa forma de criar o eixo t
        # funciona se os índices da Série formam uma sequência númerica coerente
        # (correspondendo a uma ordem temporal contínua).
    
    # Calcula a média da sequência:
    media = Y_t.mean()
    # Calcula o desvio padrão da sequência:
    desvio_padrao = Y_t.std()
    
    # Inicia lista de parametros iniciais (com alfa ajustando amplitude e beta ajustando comprimento):
    # parametros_iniciais = [media if j < h else desvio_padrao for j in range(2*h)]
    parametros_iniciais = [media]*h + [desvio_padrao]*h
    # Adiciona o período aos parâmetros:
    parametros_iniciais.append(p)
    
    # Ajusta os parâmetros:
    parametros_ajustados, _ = curve_fit(polinomio_harmonico, t, Y_t, p0=parametros_iniciais)
    # Gera sequência (como numpy array) que descreve a sazonalidade ajustada para a Series:
    S_t = polinomio_harmonico(t, *parametros_ajustados)
    # Retorna a sequência de sazonalidade.
    return S_t
    
# Y_t_ss: sequência de dados cronológicos idealmente sem sazonalidade.
# g: grau do polinômio a ser ajustado;
# t: eixo temporal.
def ajusta_sequencia_de_polinomio_para_tendencia(Y_t_ss, g, t=None):
    # Se g não for inteiro:
    if not isinstance(g, int):
        # Levanta exceção de tipo:
        raise TypeError("O grau g deve ser do tipo inteiro.")
    # Se g não for um natural não nulo:
    if g <= 0:
        # Levanta exceção de valor:
        raise ValueError("O grau g deve ser um natural não nulo.")
    
    # Se não for passado o eixo temporal t:
    if t is None:
        # Cria eixo das abscissas respectivo a ordem temporal:
        t =  np.arange(Y_t_ss.size)

    # Ajusta os parâmetros de um polinômio de grau g para
    # representar a tendência da sequência de dados:
    coeficientes = Polynomial.fit(t, Y_t_ss, g).convert().coef

    # Gera sequência de tendência:
    T_t = np.polyval(coeficientes[::-1], t)

    # Retorna a sequência de tendência.
    return T_t

# Y_t_ss: sequência de dados cronológicos idealmente sem sazonalidade.
# g: grau limite dos polinômios a serem ajustados;
# t: eixo temporal.
def ajusta_sequencias_de_polinomios_para_tendencia(Y_t_ss, g, t=None):
    # Se g não for inteiro:
    if not isinstance(g, int):
        # Levanta exceção de tipo:
        raise TypeError("O grau limite g deve ser do tipo inteiro.")
    # Se g não for um natural não nulo:
    if g <= 0:
        # Levanta exceção de valor:
        raise ValueError("O grau limite g deve ser um natural não nulo.")

    # Se não for passado o eixo temporal t:
    if t is None:
        # Cria eixo das abscissas respectivo a ordem temporal:
        t =  np.arange(Y_t_ss.size)

    # Cria lista vazia para as sequências de tendência:
    seqs_T_t = []

    # Para todos os graus até (incluso) o grau limite:
    for k in range(1, g+1):
        # Ajusta os parâmetros de um polinômio de grau k para
        # representar a tendência da sequência de dados:
        coeficientes = Polynomial.fit(t, Y_t_ss, k).convert().coef
        # Gera sequência de tendência:
        T_t = np.polyval(coeficientes[::-1], t)
        # Insere a sequência:
        seqs_T_t.append(T_t)

    # Retorna a lista de sequências de tendência.
    return seqs_T_t

# t: índice de ordem temporal;
# alfa, beta e gama: parâmetros que descrevem a função de Gompertz. 
def funcao_de_curva_de_Gompertz(t, alfa, beta, gama):
    return alfa*np.exp(beta*np.exp(-gama*t))

# Y_t_ss: sequência de dados cronológicos idealmente sem sazonalidade.
# t: eixo temporal.
def ajusta_sequencia_de_uma_curva_de_Gompertz_para_tendencia(Y_t_ss, t=None):
    # Se não for passado o eixo temporal t:
    if t is None:
        # Cria eixo das abscissas respectivo a ordem temporal:
        t =  np.arange(Y_t_ss.size)

    # Limites para os parâmetros:
    limites = ([0, 0, 0], [np.inf, np.inf, np.inf])  # alfa, beta, gama

    # Inicializa parâmetros alfa e beta:
    alfa = max(Y_t_ss) # valor assintótico.
    beta = (alfa-Y_t_ss[0])/Y_t_ss[0] if Y_t_ss[0] != 0 else 1.0 # taxa de crescimento inicial.
    # Inicializa o parâmetro gama:
    delta_Y = Y_t_ss[1]-Y_t_ss[0] if Y_t_ss[1] != Y_t_ss[0] else 1.0
    gama = delta_Y/(alfa*beta) if beta != 0 else 1.0

    # Verificação para garantir que os parâmetros sejam válidos:
    if beta <= 0 or gama <= 0:
        # Ajuste os limites de gama e beta:
        beta = 1.0
        gama = 1.0
    
    # Ajusta os parâmetros de uma curva de Gompertz para representar a tendência:
    parametros_ajustados, _ = curve_fit(funcao_de_curva_de_Gompertz, t, Y_t_ss, p0=[alfa, beta, gama], bounds=limites, maxfev=10000)

    # Gera sequência que descreve a tendência ajustada para a Series:
    T_t = funcao_de_curva_de_Gompertz(t, *parametros_ajustados)
    # Retorna a sequência de tendência.
    return T_t

# t: índice de ordem temporal;
# alfa, beta e gama: parâmetros que descrevem uma curva logística.
def funcao_de_curva_logistica(t, alfa, beta, gama):
    return alfa/(1+beta*np.exp(-gama*t))

# Y_t_ss: sequência de dados cronológicos idealmente sem sazonalidade.
# t: eixo temporal.
def ajusta_sequencia_de_uma_curva_logistica_para_tendencia(Y_t_ss, t=None):
    # Se não for passado o eixo temporal t:
    if t is None:
        # Cria eixo das abscissas respectivo a ordem temporal:
        t =  np.arange(Y_t_ss.size)
    
    # Inicializa os parâmetros alfa e beta:
    alfa = max(Y_t_ss) # é o valor máximo da curva logística, ou seja, o valor assintótico
                            # que a função logística alcança quando t tende ao infinito.
    beta = (alfa-Y_t_ss[0])/Y_t_ss[0]

    # Inicializa gama a partir da derivada da função de curva logística:
    delta_Y = Y_t_ss[1]-Y_t_ss[0]  # taxa de variação inicial dos dados.
    # Estimativa inicial para gama a partir da derivada em t=0:
    gama = (delta_Y*(1+beta)**2)/(alfa*beta) if beta != 0 else 1.0

    # Ajusta os parâmetros de uma curva logística para representar a tendência:
    parametros_ajustados, _ = curve_fit(funcao_de_curva_logistica, t, Y_t_ss, p0=[alfa, beta, gama])

    # Gera sequência que descreve a tendência ajustada para a Series:
    T_t = funcao_de_curva_logistica(t, *parametros_ajustados)
    # Retorna a sequência de tendência.
    return T_t

# t: índice de ordem temporal;
# alfa e beta: parâmetros que descrevem uma curva exponencial.
def funcao_de_curva_exponencial(t, alfa, beta):
    return alfa*np.exp(beta*t)

# Y_t_ss: sequência de dados cronológicos idealmente sem sazonalidade.
# t: eixo temporal.
def ajusta_sequencia_de_uma_curva_exponencial_para_tendencia(Y_t_ss, t=None):
    # Se não for passado o eixo temporal t:
    if t is None:
        # Cria eixo das abscissas respectivo a ordem temporal:
        t =  np.arange(Y_t_ss.size)

    # Inicializa os parâmetros alfa e beta:
    alfa = Y_t_ss[0] # é o valor inicial no tempo t=0.
    # beta = (np.log(Y_t_ss[1])-np.log(Y_t_ss[0]))/(t[1]-t[0])
    beta = np.log(Y_t_ss[1]/Y_t_ss[0]) # simplificação (t[1]-t[0]=1).
    
    # Ajusta os parâmetros de uma curva exponencial para representar a tendência:
    parametros_ajustados, _ = curve_fit(funcao_de_curva_exponencial, t, Y_t_ss, p0=[alfa, beta])

    # Gera sequência que descreve a tendência ajustada para a Series:
    T_t = funcao_de_curva_exponencial(t, *parametros_ajustados)
    # Retorna a sequência de tendência.
    return T_t

# X_t: Series de observações;
# q: distância temporal à esquerda da (t+1)-ésima observação;
# s: distância temporal à direita da (t+1)-ésima observação;
# Alfa: vetor de pesos;
# n: número de observações.
def suaviza_sequencia_por_media_movel(X_t, q, s, Alfa, n=None):
    # Se alguma das distâncias temporais forem menores que zero:
    if q < 0 or s < 0:
        # Levanta exceção de valor:
        raise ValueError("As distâncias temporais devem ser naturais não nulos.")

    # Se o tamanho do vetor alfa for diferente do tamanho da janela:
    if len(Alfa) != q+s:
        # Levanta exceção de valor:
        raise ValueError(f"{len(Alfa)} != {q} + {s}.")

    # Se nao passou o número de observações:
    if n is None:
        # Pega o número de observações:
        n = X_t.size

    # Se não há observações:
    if n <= 0:
        # Levanta exceção de valor:
        raise ValueError("O número de observações deve ser um natural não nulo.")

    # Se o número de observações for menor que o tamanho da janela:
    if n < q+s:
        # Levanta exceção de valor:
        raise ValueError("O tamanho da janela deve ser menor que o número de observações.")

    # Inicia acumulador:
    acumulador = 0
    # Para todo alfa:
    for alfa in Alfa:
        # Acumula:
        acumulador += alfa
    # Se o acumulo de alfa for diferente de 1:
    if acumulador != 1:
        # Levanta exceção de valor:
        raise ValueError("A soma dos elementos do vetor alfa deve resultar em 1.")

    # Inicia série suavizada Y_t:
    Y_t = []

    # t+s <= n-1;
    #   t <= n-1-s.
    # t-q >= 0;
    #   t >= q.

    # Para todo t:
    for t in range(q, n-s):
        # Inicia acumulador:
        acumulador = 0
        # Para toda observação na janela:
        for j, x in enumerate(X_t[t-q:t+s]):
            # Acumula a suavização:
            acumulador += Alfa[j]*x
        # Salva a observação suavizada:
        Y_t.append(acumulador)
    
    # Retorna a sequência suavizada.
    return Y_t
    
    # {[i for i in range(1, n-s-q+1)], Y, tipo="line",
    # titulo=f"Suavização por Janela [{-q}, {s}]",
    # rotulo_de_x="Tempo", rotulo_de_y="Valor Suavizado",
    # grade=True, cor='blue'}

# X_t: Series de observações;
# q: distância temporal à esquerda e à direita da (t+1)-ésima observação;
# n: número de observações.
def suaviza_sequencia_por_media_movel_simplificada(X_t, q, n=None):
    # Para s = q:
    # Y_t = \frac{1}{2q+1} \sum_{j=-q}^{q}{X_{t+j}}

    # Se a distância temporal for menor que zero:
    if q < 0:
        # Levanta exceção de valor:
        raise ValueError("A distância temporal deve ser um natural não nulo.")
    
    # Se nao passou o número de observações:
    if n is None:
        # Pega o número de observações:
        n = X_t.size

    # Se não há observações:
    if n <= 0:
        # Levanta exceção de valor:
        raise ValueError("O número de observações deve ser um natural não nulo.")

    # Se o número de observações for menor que o tamanho da janela:
    if n < q+q:
        # Levanta exceção de valor:
        raise ValueError("O tamanho da janela deve ser menor que o número de observações.")

    # Cria série Y_t:
    Y_t = []

    # Para todo t:
    for t in range(q, n-q):
        # Inicia acumulador:
        acumulador = 0
        # Para toda observação na janela:
        for x in X_t[t-q:t+q]:
            # Acumula a suavização:
            acumulador += x
        # Salva a observação suavizada:
        Y_t.append(acumulador*(1/(2*q+1)))
    
    # Retorna a sequência suavizada.
    return Y_t

    # {[i for i in range(1, n-q-q+1)], Y, tipo="line",
    # titulo=f"Suavização por Janela [{-q}, {q}]",
    # rotulo_de_x="Tempo", rotulo_de_y="Valor Suavizado",
    # grade=True, cor='blue'}