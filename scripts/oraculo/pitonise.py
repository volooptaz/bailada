import random
from subprocess import Popen, PIPE, STDOUT
import base64

# Para poder usar a wordlist brasileira, ainda é necessário instalar o pacote
# `diceware` manualmente na última versão do repositório.
WORDLIST = 'pt-br'

DADOS = 'x⚀⚁⚂⚃⚄⚅'

FONTES = {
    # Resultados da Mega-Sena
    'megasena': '03 27 39 46 47 60',

    # Resultados do Jogo do Bicho (PT)
    'bicho': '4049 0446 2862 2251 5300',

    # Tor Consensus Shared Random
    'consensus': 'GT4JJxTqQMekVf6hcXlGveEgyBWkb5+oRXc8GrcsiPs=',

    # Resultado do LavaRand na imagem da Lava Lamp
    'lava': 'b682e6ac8ac0d69e4a0ce84a4588ad442664aeec282d49888bac4bee680e636ca2abc8cb0d0f4e67436d60b0a8a4fce414daa2c2f08ac24369010bacab8e29aa2e220acf46d4c6ceb6ae484466c8486ea90f0a288eabed49aacb8dcbe2094d4e4b2b0504cbcbcc694ca4aa8ad4942ece96bce2f4548ca0bcc486c294b272d21e8ca2d6a426da16a0c6de6409ae00e24acfed6fcae56926ee883e828cdcf290e2ccce1886da88ecf6d0d098929aba80c8f4d8ca92b0e2ee6f8f2708eaca4fc208ebcb6c6c8825cf0549264daa4a81aaa86a8d228909e7ab6a2e04ec0c8e8c49af8c03ed442f64028fe32e894f2b4eabefae684a466d4ee9afcac56969a3042dee6eece949e98f89e56e43e82d82684f042baef4beb4b49848a4f48ee2d866a4a8e068f284d0548ae26c8a52d4dab8a2ec8ad6dcbabeb2f890a8c0d04b05a64e6c460a816d2b4e0929eb44dee436a2eeccbe889a968a50e2a04c982e68aaeef6a6',

    # Resultado do LavaRand na imagem do Solo desenhado
    'solo': '8ca01eaec4a480ae34bc1c328a2af8deb4868ebc38feb6848eb4baeade542a463e943ef8de14b89e69c6e7ecc8824d47656d6eef6ea38c8a4a67c96c2c6d01c2b0d084d4b2b88afcb0a212f2c49afeecb0cefab4c682f214e6d0c4dab08c03ef8ae8acc5e3e48d484ba28d8aa2288aab6809e849c84d6e24e98de18bccabc8894b0c8fc88c89086289cd4c0bec686da2eac2ece67872883c92ace012d6054eaee9cf29c7cb0ccc8f6e8c08cfeaef2a890bac8eaf052544e3cb69a86889210de32feb2e02a8cacd6a09c863c90d8eafe032921a1046a6f244d6896fe9460c65cb4badebac6869e64b4d0f07eca1edc9854f6dcc8ce5cfca078dcaee4fc66ce8ede9478aaf2b29e1ab4e2509aa0e212fc8c084b090c0a4c4ce36b2faf2da7acea8c9ac0483af8a9c9cc20beaa2fca0c892be887a72d6e688262094328c4c8ac4cc9af458969c2a8c98e2b0889898f0e8b886ba4cbc34c68490a4e6929abcbea4b6bedc',

    # Bytes de entropia coletados no Random.org
    'random_org': '16 79 0d 1d 6e 5e ba 17 b3 91',

    # Resultado de 5 rolagens de dados
    'dados': '6, 4, 1, 5, 2',
}

BYTES = {}

def megasena_bytes(dados):
    dados = dados.encode('utf-8')
    nums = [n for n in dados.split(b' ') if n != b'']
    return b''.join(bytes(n) for n in nums)

def bicho_bytes(dados):
    dados = dados.encode('utf-8')
    nums = []
    duplas = [n for n in dados.split(b' ') if n != b'']
    for dupla in duplas:
        nums.extend([dupla[:2], dupla[2:]])

    return b''.join(bytes(n) for n in nums)

def consensus_bytes(dados):
    dados = dados.encode('utf-8')
    return base64.b64decode(dados)

def lava_bytes(dados):
    return bytes(bytearray.fromhex(dados))

def solo_bytes(dados):
    return bytes(bytearray.fromhex(dados))

def random_org_bytes(dados):
    return bytes(bytearray.fromhex(dados))

def dados_bytes(dados):
    dados = dados.encode('utf-8')
    return dados


def pegar_diceware(rolagens):
    comando = ['diceware', '-w', WORDLIST, '-n', '1', '-r', 'realdice']
    cli_input = rolagens.encode('utf-8')
    p = Popen(comando, stdout=PIPE, stdin=PIPE, stderr=PIPE)
    stdout_data = p.communicate(input=cli_input)[0][99:-1]
    return stdout_data.decode('utf-8')

if __name__ == '__main__':
    resultado = []

    for nome, dados in FONTES.items():
        nome_func = nome + '_bytes'
        fonte_bytes = locals()[nome_func]
        BYTES[nome] = bytes(fonte_bytes(dados))

    # Para gerar semente com todas as fontes juntas
    # random.seed(b''.join(i for n, i in BYTES.items()))

    for nome, dados in BYTES.items():
        # Para gerar sementes separadas para cada palavra
        random.seed(dados)
        nums = [random.choice(range(1, 7)) for i in range(5)]
        rolagens = ', '.join([str(n) for n in nums])
        rolagens_unicode = ' '.join([DADOS[n] for n in nums])
        # Caso gere uma semente só não faz sentido colocar a fonte aqui
        print(rolagens_unicode + ' ' + pegar_diceware(rolagens) + ' (' + nome + ')')
