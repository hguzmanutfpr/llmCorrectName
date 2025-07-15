**Projeto de Bot que corrige nomes fora do padrão BoCoIn**<br/><br/>
O projeto sera o seguinte, uma ferramenta que identifica nomes fora do padrão e corrige de acordo, no caso sera utilizado um LLM que identificara o nome errado do arquivo e fara a correção automaticamente através de um script<br/><br/>
Para o projeto utilizaremos o LLM Gemini<br/>

* Primeiramente criaremos o virtual environment 
* instalaremos as dependencias necessarias para consumir o modelo GEMINI via API e alem disso o langchain que é uma ferramenta aque facilita o desenvolvimento de aplicações LLM

```python -m venv venv```

* Ativaremos o venv 

```venv\Scripts\activate```

* Instalaremos as dependencias que no caso estão no arquivo requirements.txt

```pip install -r requirements.txt```

* Criaremos um arquivo .env que contera as chaves da API do google 

``` messages = [
        ("system", "ESTA PARTE DEVE SER PREENCHIDA COM O COMPORTAMENTO DESEJADO QUE O MODELO TENHA "),
        ("human", pergunta),
    ]
```

* A partir desta estrutura do Langchain faremos com que o modelo identifique o padrão correto de nomes dados alguns exemplos corretos 

```
messages = [
    ("system", "Você é um assistente que identifica padrões de nomenclatura de arquivos."),
    ("human", "Aqui estão exemplos de nomes de arquivos corretos:\n- relatorio_2025_01.pdf\n- relatorio_2025_02.pdf\n- relatorio_2025_03.pdf\nQual é o padrão de nomenclatura?"),
]
resposta = llm.invoke(messages)
print(resposta.content)
```

* o prompt deve ser preciso a ponto de trazer somente a expressão regex 

```
resposta = llm.invoke(messages)
padrao_detectado = resposta.content
print(resposta.content)

```

* o comportamento e a pergunta feita pelo llm devem ser cuidadosamente feitas a resposta é muito importante para a sequencia 


* A segunda parte devera ser composta por um script que faça a varredura no diretorio buscando nomes errados 



