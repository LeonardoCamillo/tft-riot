import requests

nickname = input("Digite seu nick: ")
    ## PEGAR PUUID PELO NOME ##
puuidPorNome = requests.get(f'https://br1.api.riotgames.com/tft/summoner/v1/summoners/by-name/{nickname}?api_key=RGAPI-edd3adc4-d6b2-4e26-a6b5-4c8a7256e400')
while puuidPorNome.status_code == 404:
    print("Digite um nick válido")
    nickname = input("Digite seu nick: ")
    puuidPorNome = requests.get(f'https://br1.api.riotgames.com/tft/summoner/v1/summoners/by-name/{nickname}?api_key=RGAPI-edd3adc4-d6b2-4e26-a6b5-4c8a7256e400')
puuidPorNome = puuidPorNome.json()

while True:
    ## PEGAR LISTA DE PARTIDAS PELO PUUID ##
    listaPartidas = requests.get(f'https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuidPorNome["puuid"]}/ids?start=0&count=20&api_key=RGAPI-edd3adc4-d6b2-4e26-a6b5-4c8a7256e400')
    listaPartidas = listaPartidas.json()
    listaPartidas = listaPartidas[:5]
    for n, p in enumerate(listaPartidas):
        print(f'{n} - ID da Partida: {p}')
    numero_partida = int(input("Escolha qual partida deseja ver: "))
    while numero_partida > len(listaPartidas) - 1 or numero_partida < 0:
        print("Numero inválido")
        numero_partida = int(input("Escolha qual partida deseja ver: "))

    ## PEGAR POSIÇÃO NA PARTIDA ##
    partida = requests.get(f'https://americas.api.riotgames.com/tft/match/v1/matches/{listaPartidas[numero_partida]}?api_key=RGAPI-edd3adc4-d6b2-4e26-a6b5-4c8a7256e400')
    partida = partida.json()
    participantes = []
    for i in partida['info']['participants']:
        pegar_nome = requests.get(f'https://br1.api.riotgames.com/tft/summoner/v1/summoners/by-puuid/{i["puuid"]}?api_key=RGAPI-edd3adc4-d6b2-4e26-a6b5-4c8a7256e400')
        pegar_nome = pegar_nome.json()
        participantes.append((f'{i["placement"]}: {pegar_nome["name"]}'))

    ## MOSTRAR POSIÇÔES NA PARTIDA ##
    print('~~'* 10)
    print(' ' * 5,'RANKING')
    print('~~' * 10)
    for participante in sorted(participantes):
        print(participante)
    print('~~' * 10)
    print('~~' * 10)
    desejaContinuar = input("Deseja continuar? [S/N]").lower()
    while desejaContinuar != 's' and desejaContinuar != 'n':
        print("Resposta inválida")
        desejaContinuar = input("Deseja continuar: ").lower()
    if desejaContinuar == 'n':
        break
