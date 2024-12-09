import tkinter as tk
from tkinter import filedialog, messagebox
import pygame
from PIL import Image, ImageFilter, ImageTk
import random
import os
from screeninfo import get_monitors

c = 0

monitor = get_monitors()[0]

galeriaPuzzle = 'C:/Users/heito/PycharmProjects/quebra_cabeca/galeriaPuzzle'

if not os.path.exists(galeriaPuzzle):
    os.makedirs(galeriaPuzzle)

img_name = 'Nenhuma'

def settings():
    global difficulty, bw, sv, rs, avisoSettings, img_name, ConfigPage
    ConfigPage = tk.Tk()
    ConfigPage.title("Configurações")
    ConfigPage.geometry('500x480')

    difficulty = tk.StringVar(value='hard')
    easy = tk.Radiobutton(ConfigPage, text='Fácil', variable=difficulty, value='easy')
    medium = tk.Radiobutton(ConfigPage, text='Medio', variable=difficulty, value='medium')
    hard = tk.Radiobutton(ConfigPage, text='Difícil', variable=difficulty, value='hard')

    galeria_button = tk.Button(ConfigPage, text='Galeria', command=galeria)

    text = tk.Label(ConfigPage, text='Selecione a dificuldade')

    img = tk.Button(ConfigPage, text="Selecionar Imagem", command=selectImagem)


    avisoSettings = tk.Label(ConfigPage, text=f"Imagem selecionada: {img_name} ", font=('Arial', 10))
    atualizarInterfaceSettings()

    ReadyBotton = tk.Button(ConfigPage, text='Pronto', command=ConfigPage.quit)

    bw = tk.BooleanVar(value=False)
    help = tk.Checkbutton(ConfigPage, text='imagem de ajuda?', variable=bw)

    sv = tk.BooleanVar(value=False)
    save = tk.Checkbutton(ConfigPage, text='Salvar imagem na galeria?', variable=sv)

    rs = tk.BooleanVar(value=True)
    resolution = tk.Checkbutton(ConfigPage, text='Converter a imagem para 1000x700?', variable=rs)


    text.pack(pady=10)
    easy.pack(pady=5)
    medium.pack(pady=5)
    hard.pack(pady=5)
    avisoSettings.pack(pady=10)
    img.pack(pady=20)
    galeria_button.pack(pady=5)
    resolution.pack(pady=10)
    help.pack(pady=5)
    save.pack(pady=5)
    ReadyBotton.pack(pady=20)

    ConfigPage.mainloop()

    sv = sv.get()
    rs = rs.get()
    difficulty = difficulty.get()
    bw = bw.get()
    verificador()

    ConfigPage.destroy()


def galeria():
    global aviso, img_name, avisos, galeria_window
    galeria_window = tk.Toplevel()
    galeria_window.title("Galeria de Imagens")
    galeria_window.geometry('800x600')

    aviso = tk.Label(galeria_window, text=f"Imagem selecionada: {img_name} ", font=('Arial', 10))
    aviso.pack(pady=10)

    # Obtendo uma lista de imagens na pasta
    # Lista de imagens na pasta
    imagens = [img for img in os.listdir(galeriaPuzzle) if
               img.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.jfif'))]

    max_por_linha = 7
    linha_atual = tk.Frame(galeria_window)
    linha_atual.pack()

    for i, imagem in enumerate(imagens):
        # Se já existem 7 imagens na linha, criar um novo Frame para a próxima linha
        if i % max_por_linha == 0 and i != 0:
            linha_atual = tk.Frame(galeria_window)
            linha_atual.pack()

        # Carregar a imagem e criar miniatura
        img_path = os.path.join(galeriaPuzzle, imagem)
        img = Image.open(img_path)
        img.thumbnail((100, 100))  # Redimensiona a imagem para 100x100
        img_tk = ImageTk.PhotoImage(img)

        # Criar o botão da miniatura dentro do Frame da linha atual
        btn = tk.Button(linha_atual, image=img_tk, command=lambda path=img_path: selectImagem(path))
        btn.image = img_tk  # Referência para evitar coleta de lixo
        btn.pack(side=tk.LEFT, padx=5, pady=5)


def atualizarInterfaceSettings():
    global img_name, ConfigPage
    avisoSettings.config(text=f'Imagem selecionada: {img_name}', font=('Arial', 10))
    ConfigPage.after(1000, atualizarInterfaceSettings)


def saveImage():
    global img, img_name
    save_path = 'C:/Users/heito/PycharmProjects/quebra_cabeca/galeriaPuzzle'
    file_name = img_name
    save = os.path.join(save_path, file_name)
    if os.path.exists(save):
        messagebox.showwarning('Aviso', 'Imagem ja salva na galeria')
    else:
        img.save(save)



def verificador():
    global imagem_original

    try:
        print(imagem_original)
    except NameError:
        messagebox.showwarning('Aviso', 'Vc esqueceu de adicionar uma imagem')
        selectImagem()


def selectImagem(imagem=None):
    global imagem_original, img_name, aviso

    if not imagem:
        imagem_original = filedialog.askopenfilename(
            filetypes=[('imagens', '*.png; *.jpg; *.jpeg; *.bmp; *.jfif')]
        )
        img_name = os.path.basename(imagem_original)
    else:
        imagem_original = imagem
        img_name = os.path.basename(imagem_original)
        aviso.config(text=f'imagem selecionada : {img_name}')


def improveAndUpgradeImage():
    global img, sv, rs, bruh, bruh_widht, bruh_height
    oldImg = Image.open(imagem_original)
    largura = oldImg.width
    if rs:
        tamanho = (1000, 700)
        imagem_resized = oldImg.resize(tamanho).convert('RGB')
        img = imagem_resized.filter(ImageFilter.SHARPEN)
    else:
        '''if oldImg.width > monitor.width:
            oldImg = oldImg.resize((1080, oldImg.height)).convert('RGB')
            bruh = True
            bruh_widht = True
        elif oldImg.height > monitor.height:
            oldImg = oldImg.resize((oldImg.width, 1920)).convert('RGB')
            bruh = True
            bruh_height = True'''
        img = oldImg.convert('RGB').filter(ImageFilter.SHARPEN)

    if sv:
        saveImage()


def helpImage():
    global img
    imgNoColor = Image.open(img) if isinstance(img, str) else img
    noColor = imgNoColor.convert("L").convert('RGB')
    noColor_width, noColor_height = noColor.size
    noColor_data = noColor.tobytes()
    noColor = pygame.image.fromstring(noColor_data, (noColor_width, noColor_height), 'RGB')
    return noColor

def splitImagem():
    global img, linhas, colunas, difficulty

    if difficulty == 'easy':
        linhas = 6
        colunas = 8
    elif difficulty == 'medium':
        linhas = 9
        colunas = 12
    elif difficulty == 'hard':
        linhas = 12
        colunas = 16


    largura, altura = img.size
    largura_peca = largura / colunas
    altura_peca = altura / linhas
    pecas = []

    for i in range(linhas):
        for j in range(colunas):
            box = (j * largura_peca, i * altura_peca, (j + 1) * largura_peca, (i + 1) * altura_peca)
            peca = img.crop(box)
            pecas.append(peca)

    return pecas


def game():
    global img, linhas, colunas, bw, difficulty, rs
    pygame.init()

    largura, altura = img.size

    l = 100
    a = 45
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (l, a)

    # Definindo a tela maior de 1920x1060
    if rs:
        tela = pygame.display.set_mode((1920, 1060))
    else:
        tela = pygame.display.set_mode((largura+920, altura+360))

    pygame.display.set_caption("Quebra-Cabeça")

    # Definindo o retângulo central de 1000x700

    if rs:
        largura_retangulo_central = 1000
        altura_retangulo_central = 700
        x_central = (1920 - largura_retangulo_central) // 2
        y_central = (1060 - altura_retangulo_central) // 2
    else:
        largura_retangulo_central = largura
        altura_retangulo_central = altura
        x_central = ((largura + 920) - largura_retangulo_central) // 2
        y_central = ((altura + 360) - altura_retangulo_central) // 2

    retangulo_central = pygame.Rect(x_central, y_central, largura_retangulo_central, altura_retangulo_central)

    pecas = splitImagem()

    pecas_pygame = [pygame.image.fromstring(peca.tobytes(), peca.size, 'RGB') for peca in pecas]

    # Dividindo o retângulo central em quadrados do tamanho das peças
    largura_peca = largura_retangulo_central // colunas
    altura_peca = altura_retangulo_central // linhas

    # Criar uma matriz de posições de encaixe alinhadas ao retângulo central
    posicoes_encaixe = [(x_central + j * largura_peca, y_central + i * altura_peca) for i in range(linhas) for j in
                        range(colunas)]

    # Definindo posições iniciais aleatórias fora do retângulo central
    posicoes_iniciais = []
    espaco_borda = 20  # Espaço para que as peças não se sobreponham
    for i in range(len(pecas_pygame)):
        while True:
            if rs:
                x = random.randint(0, 1920 - largura // colunas)
                y = random.randint(0, 1060 - altura // linhas)
            else:
                x = random.randint(0, (largura + 920) - largura // colunas)
                y = random.randint(0, (altura + 360) - altura // linhas)


            nova_posicao = (x, y)

            # Verificando se a nova posição está fora do retângulo central e sem sobreposição
            peca_rect = pygame.Rect(x, y, largura // colunas, altura // linhas)
            if difficulty == 'hard' and rs == True:
                if not retangulo_central.colliderect(peca_rect): #and all(not peca_rect.colliderect(pygame.Rect(*pos, largura // colunas, altura // linhas)) for pos in posicoes_iniciais):
                    posicoes_iniciais.append(nova_posicao)
                    break
            else:
                if not retangulo_central.colliderect(peca_rect) :
                    posicoes_iniciais.append(nova_posicao)
                    break

    arrastando = False
    peca_atual = None
    offset_x, offset_y = 0, 0

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE):
                rodando = False

            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                rodando = False
                settings()
                improveAndUpgradeImage()
                game()

            # Iniciando o arraste de uma peça
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                for i, posicao in enumerate(posicoes_iniciais):
                    peca_rect = pygame.Rect(*posicao, largura_peca, altura_peca)
                    if peca_rect.colliderect(pygame.Rect(evento.pos[0], evento.pos[1], 1, 1)):
                        arrastando = True
                        peca_atual = i
                        offset_x = posicao[0] - evento.pos[0]
                        offset_y = posicao[1] - evento.pos[1]

            # Soltando a peça
            elif evento.type == pygame.MOUSEBUTTONUP:
                if arrastando and peca_atual is not None:
                    arrastando = False
                    # Verifica se a peça está próxima o suficiente de um ponto de encaixe
                    posicao_atual = (evento.pos[0] + offset_x, evento.pos[1] + offset_y)
                    for encaixe in posicoes_encaixe:
                        if abs(posicao_atual[0] - encaixe[0]) < largura_peca // 2 and abs(
                                posicao_atual[1] - encaixe[1]) < altura_peca // 2:
                            posicoes_iniciais[peca_atual] = encaixe
                            break
                    peca_atual = None

            # Movendo a peça enquanto arrasta
            elif evento.type == pygame.MOUSEMOTION:
                if arrastando and peca_atual is not None:
                    posicoes_iniciais[peca_atual] = (evento.pos[0] + offset_x, evento.pos[1] + offset_y)

        # Desenhando o jogo
        tela.fill((179, 139, 109))  # Cor de fundo branca

        if bw == True :
            noColor = helpImage()
            tela.blit(noColor, (x_central, y_central))
        else:
            pygame.draw.rect(tela, (200, 200, 200), retangulo_central)  # Retângulo central cinza

        # Desenhando os quadrados de encaixe no retângulo central
        for pos in posicoes_encaixe:
            pygame.draw.rect(tela, (150, 150, 150), pygame.Rect(pos[0], pos[1], largura_peca, altura_peca), 3)



        for i, posicao in enumerate(posicoes_iniciais):
            tela.blit(pecas_pygame[i], posicao)

        if arrastando and peca_atual is not None:
            tela.blit(pecas_pygame[peca_atual], posicoes_iniciais[peca_atual])

        pygame.display.flip()

    pygame.quit()


settings()
improveAndUpgradeImage()
game()
