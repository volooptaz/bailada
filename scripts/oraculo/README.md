# Oráculo dadoware

Através destes scripts,  com a coleta de 7 fontes diferentes de aleatoriedade / entropia e a partir de uma lista de palavras do Dadoware, é gerado um Oráculo.

Cada fonte gera uma quantidades de bytes aleatórios que é usada como semente (*seed*) para o módulo `random` do Python, que então simula a rolagem de dados e consulta a lista Dadoware para produzir uma palavra. O Oráculo é a concatenação destas palavras, em ordem de tiragem, a ser interpretado da forma que se preferir.

## Exemplo

Execução do programa a partir dos dados presentes em `pitonise.py`, tirados a partir da Bailada Nervosa da Criptofunk 2020:

```bash
$ python3 pitonise.py
megasena: Golfinho
bicho: Captei
consensus: Classista
lava: Expugnar
solo: Esmaga
random_org: Leal
dados: Desengano
```

## Requisitos

- Python2 para o script `lava.py`, que gera bytes de entropia a partir de imagens baseado no algoritmo LavaRand [implementado em modo alpha por Anthony Briggs](https://gist.github.com/AnthonyBriggs/8396607)

- Python3 para o script `pitonise.py`

- Módulo python [dadoware](https://github.com/ulif/dadoware/), com acesso ao programa `dadoware` para gerar senhas.
	- Para usar a [wordlist em português](https://github.com/ulif/dadoware/blob/master/dadoware/wordlists/wordlist_pt-br.txt) pode ser necessário instalar o módulo a partir do código-fonte.

## Passos

- Tirar fotografia da Lava Lamp e screenshot do Solo, colocando-as em `lavalamp.png` e `solo.png` respectivamente.

- Executar `python2 lava.py` e coletar as sequências de caracteres de cada uma das fontes

- Lançar 5 dados para coletar os valores em ordem

- Coletar os resultados das fontes de entropia restantes nas suas respectivas fontes. Sugestões:
	- [Mega Sena](http://loterias.caixa.gov.br/wps/portal/loterias/landing/megasena/)
	- [Jogo do Bicho](https://www.ojogodobicho.com/deu_no_poste.htm)
	- [Tor Consensus Shared Random](https://consensus-health.torproject.org/consensus-health.html)
	- [Random.org bytes](https://www.random.org/bytes/)

- Preencher variáveis de `FONTES` em `pitonise.py` com os respectivos valores coletados

- Executar `python3 pitonise.py` para gerar o oráculo.

