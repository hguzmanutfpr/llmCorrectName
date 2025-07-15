import re
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Variavel de ambiente é carregada automaticamente
load_dotenv()

# Escolha do modelo
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001")

# Definição dos prompts (o prompt em si não precisa mudar, pois a correção é na regex)
messages = [
    ("system", "Você é um especialista em padrões de nomes de arquivos. Dada uma lista de nomes de arquivos, seu objetivo é identificar e expressar o padrão geral em uma expressão regular (regex) que capture a estrutura 'data_empresa_equipamentos'."),
    ("human", "Gere uma expressão regular para o seguinte padrão de nomes de arquivos: 'data_empresa_equipamentos'. A seção de 'equipamentos' pode conter um ou mais códigos alfanuméricos, separados por sublinhados (_). Estes códigos devem incluir apenas letras MAIÚSCULAS, números e hífens (-). Os exemplos são: 15072025-0_TORATI_21PH32B66WG-3A, 15072025-0_TRANSPOTECH_21PH28B66WG_21PH32B66WG-3A, 06092023-0_TRANSPOTECH_21PH28B66WG. A saída deve ser apenas a expressão regular.")
]
# Não vamos usar a resposta do LLM diretamente para padrao_detectado
# resposta = llm.invoke(messages)
# padrao_detectado = resposta.content

# Definindo o padrao_detectado manualmente com a regex ajustada
# AGORA APENAS LETRAS MAIÚSCULAS SÃO PERMITIDAS NOS CÓDIGOS DE PRODUTO
padrao_detectado = r"\d{8}-\d+_[A-Z]+(?:_[A-Z0-9-]+)+"
print(f"Padrão usado para validação: {padrao_detectado}")

# Conecta com âncoras de início e fim da string e adiciona a extensão .docx
regex_completa = f"^{padrao_detectado}\\.docx$"
print(f"Expressão Regular Completa: {regex_completa}")

# Diretório a ser analisado (pode ser alterado conforme necessário)
diretorio = "C:\\Users\\olive\\OneDrive\\Documentos\\teste_nomes_arquivos"  # Substitua pelo caminho desejado

# Compila a regex
padrao = re.compile(regex_completa)

# Lista para armazenar arquivos com nomes incorretos
nomes_incorretos = []

# Verifica se o diretório existe
if os.path.isdir(diretorio):
    for nome_arquivo in os.listdir(diretorio):
        if os.path.isfile(os.path.join(diretorio, nome_arquivo)):
            if not padrao.match(nome_arquivo):
                nomes_incorretos.append(nome_arquivo)

    if nomes_incorretos:
        print("\nArquivos com nomes incorretos (ou extensão inválida):")
        for nome in nomes_incorretos:
            print("-", nome)
    else:
        print("\nTodos os arquivos seguem o padrão de nomenclatura e possuem extensão .docx.")
else:
    print(f"O diretório '{diretorio}' não foi encontrado.")