import re
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# --- Configuração Inicial ---
# Variáveis de ambiente são carregadas automaticamente
load_dotenv()

# Escolha do modelo
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001")

# Definição do padrão de nomenclatura (a regex mais restritiva)
# Permite apenas letras MAIÚSCULAS, números e hífens nos códigos de produto
padrao_valido_regex_str = r"\d{8}-\d+_[A-Z]+(?:_[A-Z0-9-]+)+"
regex_completa = f"^{padrao_valido_regex_str}\\.docx$"
padrao_regex_compilado = re.compile(regex_completa)

print(f"Padrão de validação: {regex_completa}")

# Diretório a ser analisado
diretorio_alvo = "C:\\Users\\olive\\OneDrive\\Documentos\\teste_nomes_arquivos"

# --- Validação e Identificação de Incorretos ---
nomes_incorretos = []

if os.path.isdir(diretorio_alvo):
    print(f"\nVerificando arquivos em: {diretorio_alvo}")
    for nome_arquivo in os.listdir(diretorio_alvo):
        caminho_completo_arquivo = os.path.join(diretorio_alvo, nome_arquivo)
        if os.path.isfile(caminho_completo_arquivo):
            if not padrao_regex_compilado.match(nome_arquivo):
                nomes_incorretos.append(nome_arquivo)

    if not nomes_incorretos:
        print("Todos os arquivos seguem o padrão de nomenclatura e possuem extensão .docx.")
    else:
        print("\nArquivos com nomes incorretos encontrados:")
        for nome in nomes_incorretos:
            print(f"- {nome}")

        # --- Processamento dos Nomes Incorretos pelo LLM e Renomeação ---
        print("\n--- Iniciando correção e renomeação via LLM ---")
        for i, nome_antigo in enumerate(nomes_incorretos):
            print(f"\nProcessando arquivo {i+1}/{len(nomes_incorretos)}: '{nome_antigo}'")

            # Construção do prompt para a LLM para correção
            # É crucial dar à LLM o padrão esperado para uma boa correção.
            prompt_correcao = [
                ("system", f"Você é um assistente de renomeação de arquivos. Sua tarefa é corrigir nomes de arquivos que não seguem um padrão específico. O padrão esperado é: 'DDMMAAAA-X_EMPRESA_CODIGO-PRODUTO_CODIGO-PRODUTO.docx'. Os códigos de produto devem conter APENAS letras MAIÚSCULAS, números e hífens. Se um nome contém partes como ' - cópia', 'PONTA REDONDA' ou pontos em excesso, você deve removê-las e formatar o resto para se ajustar ao padrão. Mantenha a data (DDMMAAAA), o identificador (X, geralmente '0') e o nome da empresa intactos. Sua saída deve ser APENAS o novo nome completo do arquivo, incluindo a extensão '.docx', sem qualquer outra pontuação ou explicação."),
                ("human", f"Corrija o seguinte nome de arquivo para o padrão correto: '{nome_antigo}'.")
            ]

            try:
                # Chama a LLM para obter a sugestão de novo nome
                print(f"  Enviando para LLM para correção...")
                resposta_llm = llm.invoke(prompt_correcao)
                nome_novo = resposta_llm.content.strip() # .strip() para remover espaços em branco extras

                # Garante que o nome termine com .docx (LLM pode esquecer)
                if not nome_novo.lower().endswith('.docx'):
                    nome_novo += '.docx' # Adiciona se não tiver
                else: # Se já tiver, garante que seja apenas uma vez e na caixa correta
                    nome_novo = nome_novo[:-5] + '.docx'


                print(f"  Sugestão da LLM: '{nome_novo}'")

                # Confirmação do usuário antes de renomear
                confirmacao = input(f"  Renomear '{nome_antigo}' para '{nome_novo}'? (s/n): ").lower()

                if confirmacao == 's':
                    caminho_antigo = os.path.join(diretorio_alvo, nome_antigo)
                    caminho_novo = os.path.join(diretorio_alvo, nome_novo)

                    # Verifica se o novo nome já existe para evitar sobrescrita acidental
                    if os.path.exists(caminho_novo):
                        print(f"    ERRO: O arquivo '{nome_novo}' já existe. Não foi possível renomear '{nome_antigo}'.")
                    else:
                        os.rename(caminho_antigo, caminho_novo)
                        print(f"    SUCESSO: Renomeado para '{nome_novo}'.")
                else:
                    print(f"    Renomeação de '{nome_antigo}' cancelada pelo usuário.")

            except Exception as e:
                print(f"  ERRO ao processar '{nome_antigo}': {e}")
                print(f"  Este arquivo não foi renomeado automaticamente.")
else:
    print(f"O diretório '{diretorio_alvo}' não foi encontrado.")

print("\nProcessamento concluído.")