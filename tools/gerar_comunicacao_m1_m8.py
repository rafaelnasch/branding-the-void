#!/usr/bin/env python3
"""Gera comunicacao-m1-m8.html (sistema Sala Escura v1, The VOID Tattoo Academy).

Os textos moram aqui, como dados; o HTML sai estático (funciona sem JavaScript) e o
script da página só filtra e copia. Para mudar um modelo, edite a lista MODELOS e rode:

    python3 tools/gerar_comunicacao_m1_m8.py

Regras que valem para todo texto daqui (especificação Sala Escura, seções 9, 10, 11 e 12.6):
pt-BR, zero travessão, um CTA por mensagem, nenhum número sem prova, nada de dado interno,
ritos propostos [P 6] fora de qualquer mensagem.
"""
import html
import pathlib
import re

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "comunicacao-m1-m8.html"

# ----------------------------------------------------------------------------- ícones
# Lucide (licença ISC), copiados; traço 1,5 e pontas retas vêm do CSS da página.
LUCIDE = {
    "copy": '<rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>',
    "circle-check": '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
    "circle-x": '<circle cx="12" cy="12" r="10"/><path d="m15 9-6 6"/><path d="m9 9 6 6"/>',
    "circle-dashed": '<path d="M10.1 2.182a10 10 0 0 1 3.8 0"/><path d="M13.9 21.818a10 10 0 0 1-3.8 0"/><path d="M17.609 3.721a10 10 0 0 1 2.69 2.7"/><path d="M2.182 13.9a10 10 0 0 1 0-3.8"/><path d="M20.279 17.609a10 10 0 0 1-2.7 2.69"/><path d="M21.818 10.1a10 10 0 0 1 0 3.8"/><path d="M3.721 6.391a10 10 0 0 1 2.7-2.69"/><path d="M6.391 20.279a10 10 0 0 1-2.69-2.7"/>',
    "mail": '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    "send": '<path d="M14.536 21.686a.5.5 0 0 0 .937-.024l6.5-19a.496.496 0 0 0-.635-.635l-19 6.5a.5.5 0 0 0-.024.937l7.93 3.18a2 2 0 0 1 1.112 1.11z"/><path d="m21.854 2.147-10.94 10.939"/>',
    "play": '<polygon points="6 3 20 12 6 21 6 3"/>',
    "megaphone": '<path d="m3 11 18-5v12L3 14v-3z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/>',
    "message-circle": '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>',
    "calendar-days": '<path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/><path d="M8 14h.01"/><path d="M12 14h.01"/><path d="M16 14h.01"/><path d="M8 18h.01"/><path d="M12 18h.01"/><path d="M16 18h.01"/>',
    "map-pin": '<path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    "user-round": '<circle cx="12" cy="8" r="5"/><path d="M20 21a8 8 0 0 0-16 0"/>',
    "users-round": '<path d="M18 21a8 8 0 0 0-16 0"/><circle cx="10" cy="8" r="5"/><path d="M22 20c0-3.37-2-6.5-4-8a5 5 0 0 0-.45-8.3"/>',
    "arrow-right": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "info": '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/>',
    "triangle-alert": '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
    "lock": '<rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    "route": '<circle cx="6" cy="19" r="3"/><path d="M9 19h8.5a3.5 3.5 0 0 0 0-7h-11a3.5 3.5 0 0 1 0-7H15"/><circle cx="18" cy="5" r="3"/>',
    "flag": '<path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/><line x1="4" x2="4" y1="22" y2="15"/>',
    "list-filter": '<path d="M3 6h18"/><path d="M7 12h10"/><path d="M10 18h4"/>',
    "image": '<rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/>',
    "minus": '<path d="M5 12h14"/>',
    "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    "file-text": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/>',
}
# WhatsApp: glifo monocromático do Simple Icons (CC0), na cor do texto (spec 7.5)
WHATSAPP = '<path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413Z"/>'


def ic(nome, extra=""):
    if nome == "whatsapp":
        return f'<svg class="ic ic-cheio{extra}" viewBox="0 0 24 24" aria-hidden="true" focusable="false">{WHATSAPP}</svg>'
    return f'<svg class="ic{extra}" viewBox="0 0 24 24" aria-hidden="true" focusable="false">{LUCIDE[nome]}</svg>'


def e(t):
    return html.escape(t, quote=True)


def com_variaveis(t):
    """Escapa e destaca {variáveis} e *negrito do WhatsApp* sem mudar o texto."""
    t = e(t)
    t = re.sub(r"\{[a-z_]+\}", lambda m: f'<span class="var">{m.group(0)}</span>', t)
    return t


# ----------------------------------------------------------------------------- dados
CANAIS = {
    "whatsapp": ("WhatsApp", "whatsapp"),
    "email": ("E-mail", "mail"),
    "dm": ("DM do Instagram", "send"),
    "reels": ("Reels e story", "play"),
    "anuncio": ("Anúncio pago", "megaphone"),
    "pesquisa": ("Pesquisa Google", "search"),
}

# Limites de caracteres por campo (conferidos no build; acima do limite, o build para).
# "linha1" conta só a primeira linha: é o que aparece antes do "ver mais" no Feed.
LIMITES = {
    "anuncio": {"Texto principal": ("linha1", 125), "Título": ("tudo", 40), "Descrição": ("tudo", 30)},
    "pesquisa": {"Títulos": ("cada", 30), "Descrições": ("cada", 90), "Caminhos": ("cada", 15)},
}
QUANTIDADE_PESQUISA = {"Títulos": 15, "Descrições": 4, "Caminhos": 2}

PERSONAS = [
    {
        "id": "gabriel", "nome": "Gabriel", "papel": "o jovem sonhador", "produto": "Start",
        "conviccao": "Eu não tenho talento suficiente para viver de tatuagem.",
        "tom": "Coragem e prova social de quem começou do zero.",
        "hero": 'TALENTO É CONSEQUÊNCIA DE <em class="off">treino</em>.',
        "hero_nota": "Hero de teste da especificação, seção 9.5.",
        "status": "decidido",
    },
    {
        "id": "camila", "nome": "Camila", "papel": "a profissional em transição", "produto": "Start, depois Master",
        "conviccao": "Já passei da hora. Quem começa do zero precisa ter começado mais jovem.",
        "tom": "Recomeço, lógica antes da permissão, depoimentos de adultos em transição.",
        "hero": 'SUA EXPERIÊNCIA É UM <em class="off">diferencial</em>, NÃO UM ATRASO.',
        "hero_nota": "Oito palavras: em peça, divida em duas telas para cumprir a L6.",
        "status": "decidido",
    },
    {
        "id": "bruno", "nome": "Bruno", "papel": "o tatuador em evolução", "produto": "Master e Pro",
        "conviccao": "Preciso ser ainda melhor tecnicamente antes de cobrar mais.",
        "tom": "Posicionamento e trajetórias reais de crescimento, sem número de renda.",
        "hero": 'TÉCNICA SEM POSICIONAMENTO É <em class="off">invisível</em>.',
        "hero_nota": "Hero de teste da especificação, seção 9.5.",
        "status": "decidido",
    },
    {
        "id": "sylvia", "nome": "Sylvia", "papel": "subperfil do Pro", "produto": "Pro",
        "conviccao": "Para crescer, preciso tatuar ainda mais.",
        "tom": "Estratégia de carreira e marca, com a agenda e o corpo preservados.",
        "hero": None,
        "hero_frase": "A arte é sua. O plano é nosso.",
        "hero_nota": "Frase de assinatura do Pro (uma por campanha). A convicção acima é formulação da GrowAI a partir da persona da agência; aguarda aprovação.",
        "status": "proposta",
    },
]

# CTA de cada etapa: rótulo exato (spec 10 e biblioteca 12.1). M8 tem um CTA por frente.
ETAPAS = [
    dict(id="m1", nome="Lead", crenca="Isso não é para mim.", atributo="Corajosa", funcao="Atenção",
         recurso="Esfera do Vazio e Palavra Sensível", componente="Gancho do Vazio (Reels e anúncio 9:16), Plano de Abertura",
         cta="Um por porta de entrada (ver as portas)", metrica="Retenção de 3 s; conversão da página",
         guia="O vazio que você sente tem nome, e tem caminho.",
         prova="Uma história real de quem começou do zero, autorizada e com crédito. Uma prova por mensagem.",
         nunca=['"Você vai ganhar R$ X"', '"fácil", "simples assim", "em poucos cliques"', '"mesmo sem talento você consegue"', '"curso barato" como argumento'],
         fora=[]),
    dict(id="m2", nome="Qualificação", crenca="Escola de tatuagem é tudo igual.", atributo="Próxima", funcao="Prova",
         recurso="Crédito de Prova e Fio de Produto", componente="Antes Era (depoimento), Roteiro",
         cta="Agendar minha conversa", metrica="Leads qualificados sobre cadastrados",
         guia="A Void não é um curso. É uma formação com método, estúdio e gente junto.",
         prova="Os três pilares da formação em uma frase e a prática desde o primeiro dia.",
         nunca=["nome de outra escola, nem por insinuação", '"a única escola" ou qualquer exclusividade sem prova', "pergunta de renda ou de dívida por escrito"],
         fora=[]),
    dict(id="m3", nome="Oportunidade", crenca="Lá dentro vou ser só mais um.", atributo="Técnica", funcao="Decisão",
         recurso="Mapa da Trilha", componente="Comparativo de trilhas, Cartão de Turma, visita",
         cta="Receber minha proposta de turma", metrica="Comparecimento: visitas ou conversas realizadas sobre agendadas",
         guia="Veja com seus olhos como se aprende aqui.",
         prova="O estúdio na Vila Madalena, o método no Mapa da Trilha e os professores com nome e trajetória autorizados [P 13].",
         nunca=['"decide hoje que o preço muda amanhã" quando não for verdade', "comparação com outras escolas"],
         fora=[("anuncio", "A decisão acontece na conversa e na visita. Anúncio aqui vira pressão.")]),
    dict(id="m4", nome="Proposta", crenca="É caro. Vou pensar.", atributo="Técnica, com Próxima de apoio", funcao="Decisão para ação",
         recurso="Barra de Turma e Modo Leitura", componente="Ficha da Formação, Perguntas, proposta de uma página",
         cta="Garantir minha vaga na turma de [mês]", metrica="Tempo em decisão: dias entre a proposta e a resposta",
         guia="O que você vai ter, quando começa e como paga. Sem letra miúda.",
         prova="Depoimento de alguém com o mesmo perfil, com crédito; valor total, parcelas e condições iguais ao checkout [P 15].",
         nunca=['"o investimento se paga em X semanas"', '"últimas vagas" sem número real', '"só hoje" que volta toda semana'],
         fora=[("reels", "A proposta é individual. A peça pública de turma é o story Turma Aberta, em M3."),
               ("anuncio", "Anúncio para quem está com proposta aberta vira escassez fabricada."),
               ("dm", "A proposta vai por WhatsApp e e-mail, onde fica por escrito.")]),
    dict(id="m5", nome="Matrícula", crenca="Será que escolhi certo?", atributo="Próxima", funcao="Ação, com acolhida",
         recurso="Selo como Carimbo", componente="E-mail e WhatsApp de boas-vindas, Cartão do Primeiro Dia",
         cta="Confirmar presença no primeiro dia", metrica="Matrículas pagas sobre propostas decididas",
         guia="Você escolheu. Agora a gente cuida do primeiro passo junto com você.",
         prova="O plano do primeiro dia, com horário, endereço e o nome de quem recebe. Clareza é a prova.",
         nunca=['"agora não tem volta"', "condição que não estava na proposta", "várias mensagens no mesmo dia"],
         fora=[("reels", "Quem acabou de se matricular recebe atenção individual, não peça pública."),
               ("anuncio", "Aluno matriculado nunca é público de anúncio.")]),
    dict(id="m6", nome="Ativação", crenca="Minhas mãos não vão obedecer.", atributo="Próxima e Corajosa", funcao="Ação",
         recurso="Esfera no estado vazio, Ritual do Traço", componente="Hoje, Meu Traço",
         cta="Registrar meu primeiro traço", metrica="Ativação no prazo: marcos de M6 cumpridos sobre matrículas pagas",
         guia="Todo mundo começa com um traço. Aqui, ele tem nome, coragem e história.",
         prova="O próprio avanço do aluno. Aqui, a prova de terceiros pesa menos que a evidência de si.",
         nunca=['"relaxa, é fácil"', "correção do erro de um aluno no grupo da turma", "comparação entre alunos"],
         fora=[("dm", "Com aluno, a conversa é no WhatsApp e no portal."),
               ("reels", "Marco de aluno só vira peça pública em M8, com consentimento por escrito."),
               ("anuncio", "Aluno nunca é público de anúncio.")]),
    dict(id="m7", nome="Valor", crenca="Todo mundo evolui mais rápido que eu.", atributo="Técnica (Inspiradora no fecho)", funcao="Prova de si",
         recurso="Anel de Preenchimento, Mapa da Trilha", componente="Minha Trilha, Prática com Feedback, Marco",
         cta="Enviar meu trabalho para feedback", metrica="Conclusão da turma: Formatura com Pele sobre alunos ativados",
         guia="Sua evolução é medida contra você mesmo, não contra os outros.",
         prova="O primeiro traço ao lado do trabalho de hoje, visível só para o aluno.",
         nunca=['"você está atrasado em relação à turma"', "ranking de velocidade", "cobrança financeira na mesma mensagem do feedback"],
         fora=[("dm", "Com aluno, a conversa é no WhatsApp e no portal."),
               ("reels", "A peça pública do marco nasce em M8, com consentimento."),
               ("anuncio", "Aluno nunca é público de anúncio.")]),
    dict(id="m8", nome="Expansão", crenca="Já aprendi o que precisava.", atributo="Inspiradora", funcao="Atenção de novo",
         recurso="Próximo círculo aceso no Mapa da Trilha", componente="Convite Talks, Formatura, próxima formação, indicação",
         cta="Um por mensagem: Conhecer o Master ou Indicar alguém", metrica="Ascensão em 12 meses; indicação consentida",
         guia="Seu próximo capítulo, e o capítulo de quem você trouxer.",
         prova="Trajetória de ex-alunos do Master e do Pro, autorizada; a história do próprio aluno, contada por ele.",
         nunca=['"indique e ganhe dinheiro" como argumento', "benefício de indicação que não exista", '"você ainda não está pronto"', "foto ou depoimento sem consentimento por escrito"],
         fora=[("anuncio", "Lista de ex-alunos não vira público de anúncio sem consentimento.")]),
]

FRENTES_M8 = {
    "proximo": ("Próximo círculo", "Conhecer o Master (ou o Pro)"),
    "indicacao": ("Indicação", "Indicar alguém"),
    "encontro": ("Encontros", "Confirmar presença"),
}
# M1 tem três portas de entrada. Cada mensagem e cada peça pertence a UMA porta e leva o
# CTA dela; a porta é o destino do pedido (L1: um pedido por peça).
FRENTES_M1 = {
    "conversa": ("Conversa", 'Responder "o que te trouxe até aqui?"'),
    "aula": ("Aula experimental", "Garantir minha vaga na aula"),
    "encontro": ("The VOID Talks", "Confirmar presença"),
}
REGRA_PORTAS_M1 = ("Conversa (WhatsApp, e-mail, DM, Reels orgânico e anúncio de conversa): responder "
                   "\"o que te trouxe até aqui?\". Aula experimental (página da aula, anúncio, Reels e régua da aula): "
                   "GARANTIR MINHA VAGA NA AULA. The VOID Talks aberto ao público: CONFIRMAR PRESENÇA. "
                   "Página de formação (Start, Master, Pro) é destino de M2, com o rótulo da própria página.")
FRENTES = {"m1": FRENTES_M1, "m8": FRENTES_M8}

STATUS = {
    "decidido": ("Decidido", "circle-check", "Está na especificação do sistema."),
    "proposta": ("Proposta", "info", "Modelo escrito pela GrowAI. Aguarda aprovação da The VOID."),
    "pendente": ("Pendente", "circle-dashed", "Depende de dado do cliente antes de sair."),
}

# cta: True quando a mensagem carrega o CTA da etapa (ou da frente, em M8);
# None quando é pergunta, lembrete ou cuidado, sem pedido de ação.
MODELOS = [
    # ------------------------------------------------------------------ M1
    dict(id="m1-wa", etapa="m1", frente="conversa", canal="whatsapp", momento="Primeiro contato, até 5 minutos depois do cadastro",
         personas=["todas"], status="proposta", cta=True,
         texto="Oi, {nome}. Aqui é {consultor}, da The VOID.\nVi que você pediu {material}. Já está no seu e-mail.\nAntes de qualquer coisa, me conta:\no que te trouxe até aqui?",
         porque="A primeira resposta vem de uma pessoa com nome. A pergunta abre a conversa e diz ao time qual persona chegou."),
    dict(id="m1-email", etapa="m1", frente="conversa", canal="email", momento="Boas-vindas e entrega do material pedido",
         personas=["todas"], status="proposta", cta=True,
         assunto="{nome}, seu material chegou", pre="E uma pergunta que pouca gente se faz.",
         texto="Oi, {nome}.\n\nAqui está o {material} que você pediu: {link_material}\n\nSe você está se perguntando \"será que eu sou capaz?\", essa dúvida não é um aviso para parar. É o começo do caminho.\n\nResponda este e-mail com uma frase: o que te trouxe até aqui? Quem lê é uma pessoa do time.\n\n{assinatura}",
         porque="Entrega o que foi prometido antes de pedir qualquer coisa. O pedido é uma resposta, não um clique.",
         nota="\"Quem lê é uma pessoa do time\" só fica se for verdade na operação."),
    dict(id="m1-dm", etapa="m1", frente="conversa", canal="dm", momento="Quem comentou ou mandou mensagem no perfil",
         personas=["todas"], status="proposta", cta=True,
         texto="Oi, {nome}. Que bom te ver por aqui.\nMe conta uma coisa:\no que te trouxe até aqui?",
         porque="DM é conversa: uma pergunta, nenhum link, nenhuma oferta."),
    dict(id="m1-reels-gabriel", etapa="m1", frente="conversa", canal="reels", momento="Gancho do Vazio, Reels 9:16 de 20 a 30 s",
         personas=["gabriel"], status="proposta", cta=True,
         telas=[
             ("0 a 2 s", 'TALENTO É CONSEQUÊNCIA DE <em class="off">treino</em>.', "Você acha que não tem talento para tatuar?"),
             ("3 a 14 s", None, "Plano fechado de mão em prática, gravado na escola, com autorização. Legenda: \"Talento é o que aparece depois de muito treino com método.\""),
             ("15 a 22 s", None, "Mão firme no traço. Legenda: \"Na The VOID Tattoo Academy, a formação começa do primeiro traço.\""),
             ("fecho", 'O QUE TE TROUXE ATÉ <em class="off">aqui</em>?', "Me conta na DM."),
         ],
         legenda="Talento não é o ponto de partida. Treino com método é.\nNa The VOID Tattoo Academy, escola de tatuagem na Vila Madalena, em São Paulo, a formação começa do primeiro traço.\nMe conta na DM: o que te trouxe até aqui?",
         porque="Ataca a convicção do Gabriel nos 2 s iniciais e devolve a mesma pergunta das mensagens."),
    dict(id="m1-reels-camila", etapa="m1", frente="conversa", canal="reels", momento="Gancho do Vazio, Reels 9:16 de 20 a 30 s",
         personas=["camila"], status="pendente", pend="15", cta=True,
         telas=[
             ("0 a 2 s", 'SUA EXPERIÊNCIA É UM <em class="off">diferencial</em>.', "Acha que já passou da hora de começar a tatuar?"),
             ("3 a 5 s", "NÃO UM ATRASO.", "Você chega com repertório, disciplina e olhar. Isso conta."),
             ("6 a 22 s", None, "Depoimento real de aluna que entrou vinda de outra carreira, gravado com autorização. Crédito de Prova na tela: \"Depoimento real de [nome], que trabalhava como [ocupação], usado com autorização.\""),
             ("fecho", 'O QUE TE TROUXE ATÉ <em class="off">aqui</em>?', "Me conta na DM."),
         ],
         legenda="Recomeçar não apaga o que você construiu. Soma.\nNa The VOID Tattoo Academy, escola de tatuagem na Vila Madalena, em São Paulo, a formação começa do primeiro traço, em qualquer idade adulta.\nMe conta na DM: o que te trouxe até aqui?\nResultados individuais variam conforme prática e dedicação.",
         porque="O hero tem oito palavras e por isso vira duas telas (L6). Com depoimento, o aviso de resultado vai junto."),
    dict(id="m1-reels-bruno", etapa="m1", frente="conversa", canal="reels", momento="Gancho do Vazio, Reels 9:16 de 20 a 30 s",
         personas=["bruno"], status="proposta", cta=True,
         telas=[
             ("0 a 2 s", 'TÉCNICA SEM POSICIONAMENTO É <em class="off">invisível</em>.', "Você já tatua bem e sente que o seu trabalho não é visto como deveria?"),
             ("3 a 18 s", None, "Mãos de tatuador em sessão, luz lateral. Legenda: \"Antes de buscar mais técnica, olhe para como o seu trabalho é apresentado.\""),
             ("fecho", 'O QUE TE TROUXE ATÉ <em class="off">aqui</em>?', "Me conta na DM."),
         ],
         legenda="Técnica você já tem. O que falta costuma ser posicionamento: como o seu trabalho é visto e apresentado.\nA The VOID Tattoo Academy, escola de tatuagem na Vila Madalena, em São Paulo, trabalha técnica, identidade e carreira.\nMe conta na DM: o que te trouxe até aqui?",
         porque="Fala com quem já tatua sem prometer agenda, seguidor ou preço."),
    dict(id="m1-wa-sem-resposta-d1", etapa="m1", frente="conversa", canal="whatsapp", momento="Sem resposta ao primeiro contato: D+1",
         personas=["todas"], status="proposta", cta=True,
         texto="{nome}, passando só para ver se minha mensagem chegou. Sem pressa.\nQuando quiser, me conta:\no que te trouxe até aqui?",
         porque="Um toque leve no dia seguinte, com a mesma pergunta. Sem link e sem oferta."),
    dict(id="m1-wa-sem-resposta-d3", etapa="m1", frente="conversa", canal="whatsapp", momento="Sem resposta: D+3, uma dúvida comum respondida",
         personas=["gabriel", "camila"], status="proposta", cta=True,
         texto="{nome}, uma dúvida que muita gente tem antes de começar: precisa saber desenhar?\nPara começar na formação Start, não precisa. Tatuar é técnica, e técnica se aprende com método e prática.\nSe quiser conversar, é só responder: o que te trouxe até aqui?",
         porque="Entrega valor antes de pedir de novo. A resposta repete o que o site do Start publica: não é preciso saber desenhar."),
    dict(id="m1-wa-sem-resposta-d7", etapa="m1", frente="conversa", canal="whatsapp", momento="Sem resposta: D+7, último toque da cadência",
         personas=["todas"], status="proposta", cta=None, tipo="Encerramento, porta aberta",
         texto="{nome}, vou parar de te escrever por aqui para não encher sua caixa.\nSe um dia quiser conversar sobre tatuagem, é só responder esta mensagem. Ela fica aberta.",
         porque="Fecha a cadência com respeito. Depois do D+7, o contato só volta com motivo real: nova turma ou nova aula, para quem aceitou receber."),
    dict(id="m1-anuncio", etapa="m1", frente="conversa", canal="anuncio", momento="Anúncio de conversa no WhatsApp, Reels 9:16 e Feed 4:5",
         personas=["gabriel", "camila"], status="proposta", cta=True,
         campos=[
             ("Consciência", "Consciente do problema: quer tatuar e acha que não é para ele.", False),
             ("Tela de abertura (9:16)", 'E SE FOR PARA <em class="off">você</em>?', True),
             ("Texto principal", "Tatuagem não é para quem nasceu pronto. É técnica, e técnica se aprende com método e prática.\nA The VOID Tattoo Academy é uma escola de tatuagem na Vila Madalena, em São Paulo.\nMe conta no WhatsApp: o que te trouxe até aqui?", False),
             ("Título", "Conte o que te trouxe até aqui", False),
             ("Botão da plataforma", "Enviar mensagem", False),
             ("Destino", "Conversa no WhatsApp oficial do Start, com mensagem pré-preenchida.", False),
             ("Mensagem pré-preenchida", "Oi, vim pelo anúncio da The VOID. O que me trouxe até aqui foi:", False),
             ("Público", "Maiores de 18 anos, por interesse em tatuagem e arte, na cidade de São Paulo e arredores. Nunca por renda, dívida ou situação pessoal.", False),
         ],
         nota="O número do WhatsApp oficial de cada formação depende da escola [P 8].",
         porque="O anúncio pede a mesma resposta das mensagens, e a conversa já começa com a origem marcada."),
    dict(id="m1-anuncio-bruno", etapa="m1", frente="conversa", canal="anuncio", momento="Anúncio de conversa para quem já tatua, Reels 9:16 e Feed 4:5",
         personas=["bruno"], status="proposta", cta=True,
         campos=[
             ("Consciência", "Consciente do problema: tatua bem e não é visto como gostaria.", False),
             ("Tela de abertura (9:16)", 'TÉCNICA SEM POSICIONAMENTO É <em class="off">invisível</em>.', True),
             ("Texto principal", "Você já tatua bem e sente que o seu trabalho não é visto como deveria?\nA The VOID Tattoo Academy trabalha técnica, identidade artística e carreira com quem já tatua, na Vila Madalena, em São Paulo.\nMe conta no WhatsApp: o que te trouxe até aqui?", False),
             ("Título", "Conte o que te trouxe até aqui", False),
             ("Botão da plataforma", "Enviar mensagem", False),
             ("Destino", "Conversa no WhatsApp oficial do Master, com mensagem pré-preenchida.", False),
             ("Mensagem pré-preenchida", "Oi, já tatuo e vim pelo anúncio da The VOID. O que me trouxe até aqui foi:", False),
             ("Público", "Maiores de 18 anos, por interesse em tatuagem profissional e equipamento de tatuagem. Sem promessa de agenda, seguidor ou preço.", False),
         ],
         nota="O número do WhatsApp oficial de cada formação depende da escola [P 8].",
         porque="O hero de teste do Bruno abre a peça; a pergunta é a mesma das outras portas de conversa."),
    dict(id="m1-anuncio-sylvia", etapa="m1", frente="conversa", canal="anuncio", momento="Anúncio de conversa sobre carreira, Reels 9:16 e Feed 4:5",
         personas=["sylvia"], status="proposta", cta=True,
         campos=[
             ("Consciência", "Consciente do problema: acha que crescer é só tatuar mais.", False),
             ("Tela de abertura (9:16)", 'CRESCER NÃO É SÓ TATUAR <em class="off">mais</em>.', True),
             ("Texto principal", "Agenda cheia e corpo cansado não são o único caminho para crescer na tatuagem.\nO The VOID Pro é um programa online e ao vivo de marca, conteúdo, vendas e carreira para tatuadores.\nMe conta no WhatsApp: o que te trouxe até aqui?", False),
             ("Título", "Conte o que te trouxe até aqui", False),
             ("Botão da plataforma", "Enviar mensagem", False),
             ("Destino", "Conversa no WhatsApp oficial do Pro, com mensagem pré-preenchida.", False),
             ("Mensagem pré-preenchida", "Oi, sou tatuador e vim pelo anúncio do The VOID Pro. O que me trouxe até aqui foi:", False),
             ("Público", "Maiores de 18 anos, por interesse em tatuagem profissional, em todo o Brasil (o Pro é online). Sem número de faturamento, nem no texto, nem no público.", False),
         ],
         nota="O número do WhatsApp oficial de cada formação depende da escola [P 8].",
         porque="Fala com a convicção da Sylvia sem prometer renda. O formato online abre o público para fora de São Paulo."),
    # porta: aula experimental -------------------------------------------------
    dict(id="m1-anuncio-aula", etapa="m1", frente="aula", canal="anuncio", momento="Anúncio da aula experimental, Reels 9:16 e Feed 4:5",
         personas=["gabriel", "camila"], status="proposta", cta=True,
         campos=[
             ("Consciência", "Consciente do problema: quer saber se tatuagem é para ele antes de investir.", False),
             ("Tela de abertura (9:16)", 'TATUAR NÃO É <em class="off">desenhar</em>.', True),
             ("Texto principal", "Quer saber se tatuagem é para você? Teste numa aula experimental presencial e gratuita.\nNa The VOID Tattoo Academy, na Vila Madalena, em São Paulo. Para maiores de 18 anos, sem pré-requisito.\nGaranta sua vaga pelo link.", False),
             ("Título", "Aula experimental gratuita em SP", False),
             ("Descrição", "Vila Madalena, maiores de 18", False),
             ("Botão da plataforma", "Cadastre-se", False),
             ("Destino", "Página da aula experimental (/aula-experimental/), com formulário de 3 ou 4 campos.", False),
             ("Rótulo na página", "GARANTIR MINHA VAGA NA AULA", False),
             ("Público", "Maiores de 18 anos, por interesse em tatuagem e arte, num raio de deslocamento até a Vila Madalena (a aula é presencial).", False),
         ],
         porque="Mesma promessa e mesmo rótulo da página da aula. Gratuita, presencial, 18 anos e sem pré-requisito estão no site da escola; escassez de vaga só com número real."),
    dict(id="m1-anuncio-aula-carrossel", etapa="m1", frente="aula", canal="anuncio", momento="Carrossel da aula experimental, Feed 4:5, quatro cartões",
         personas=["gabriel", "camila"], status="proposta", cta=True,
         campos=[
             ("Consciência", "Consciente da solução: sabe que existe curso e acha que precisa saber desenhar.", False),
             ("Cartão 1", 'TATUAR NÃO É <em class="off">desenhar</em>.', True),
             ("Cartão 2", 'É TÉCNICA. E TÉCNICA SE <em class="off">treina</em>.', True),
             ("Cartão 3", 'MÁQUINA, AGULHA E <em class="off">profundidade</em>.', True),
             ("Cartão 4", 'TESTE NA AULA <em class="off">experimental</em>.', True),
             ("Texto principal", "Desenhar cria a arte. Tatuar é levar a arte para a pele com controle de máquina, agulha e profundidade.\nA aula experimental da The VOID Tattoo Academy é presencial e gratuita, na Vila Madalena, em São Paulo, para maiores de 18 anos.\nGaranta sua vaga pelo link.", False),
             ("Título", "Teste numa aula experimental", False),
             ("Descrição", "Presencial, na Vila Madalena", False),
             ("Botão da plataforma", "Cadastre-se", False),
             ("Destino", "Página da aula experimental (/aula-experimental/).", False),
             ("Rótulo na página", "GARANTIR MINHA VAGA NA AULA", False),
             ("Público", "Maiores de 18 anos, por interesse em desenho, ilustração e tatuagem, num raio de deslocamento até a Vila Madalena.", False),
         ],
         porque="Responde a objeção principal (\"não sei desenhar\") com a mesma distinção do artigo do guia, um cartão por ideia, até 6 palavras por cartão."),
    dict(id="m1-wa-aula-confirmacao", etapa="m1", frente="aula", canal="whatsapp", momento="Confirmação da inscrição na aula: na hora (D0)",
         personas=["gabriel", "camila"], status="proposta", cta=None, tipo="Confirmação, sem novo pedido",
         texto="{nome}, sua vaga na aula experimental está garantida: *{data_aula}*, às *{horario}*, em *{endereco}*.\nA aula é presencial e gratuita. Não precisa saber desenhar.\nQuem vai te receber sou eu, {consultor}. Qualquer dúvida, é só me chamar aqui.",
         porque="A pessoa recebe na hora a data, o endereço e o nome de quem a recebe. Duração e roteiro da aula só entram depois de confirmados pela escola."),
    dict(id="m1-email-aula", etapa="m1", frente="aula", canal="email", momento="Confirmação da inscrição na aula, por escrito (D0)",
         personas=["gabriel", "camila"], status="proposta", cta=None, tipo="Confirmação, sem novo pedido",
         assunto="Sua vaga na aula experimental", pre="{data_aula}, às {horario}, na Vila Madalena.",
         texto="Oi, {nome}.\n\nSua vaga na aula experimental está garantida.\n\nQuando: {data_aula}, às {horario}.\nOnde: {endereco}.\nComo chegar: {como_chegar}.\n\nA aula é presencial e gratuita, para maiores de 18 anos. Não precisa saber desenhar.\n\nSalvar na agenda: {link_calendario}\nSe não puder vir, responda este e-mail e a gente vê outra data com você.\n\n{assinatura}",
         porque="Tudo o que a pessoa precisa para chegar, num lugar que ela encontra de novo. O link de agenda reduz falta."),
    dict(id="m1-wa-aula-vespera", etapa="m1", frente="aula", canal="whatsapp", momento="Lembrete na véspera da aula (D-1), em horário comercial",
         personas=["gabriel", "camila"], status="proposta", cta=None, tipo="Lembrete, sem pedido",
         texto="{nome}, amanhã é a sua aula experimental: *{data_aula}*, às *{horario}*, em *{endereco}*.\nComo chegar: {como_chegar}.\nSe não puder vir, me avisa por aqui que eu vejo outra data com você.",
         porque="Lembra e já abre a saída para remarcar: quem avisa não vira falta."),
    dict(id="m1-wa-aula-2h", etapa="m1", frente="aula", canal="whatsapp", momento="Duas horas antes da aula (H-2)",
         personas=["gabriel", "camila"], status="proposta", cta=None, tipo="Lembrete, sem pedido",
         texto="{nome}, sua aula começa às *{horario}*. Estou te esperando em *{endereco}*.\nSe não achar a entrada, me chama aqui.",
         porque="Curta, prática e com uma pessoa do outro lado."),
    dict(id="m1-wa-aula-falta", etapa="m1", frente="aula", canal="whatsapp", momento="Falta na aula: no mesmo dia, uma hora depois do início",
         personas=["gabriel", "camila"], status="pendente", pend="16", cta=True,
         texto="{nome}, senti sua falta na aula de hoje. Imprevisto acontece.\nA próxima aula experimental é em *{proxima_data_aula}*, às *{horario}*.\nQuer garantir sua vaga nela?",
         porque="Sem culpa e com a próxima data real na mesma mensagem. Sem calendário de aulas confirmado, a mensagem não sai."),
    dict(id="m1-anuncio-talks", etapa="m1", frente="encontro", canal="anuncio", momento="Anúncio do The VOID Talks aberto ao público, Reels 9:16 e Feed 4:5",
         personas=["todas"], status="pendente", pend="6", cta=True,
         campos=[
             ("Consciência", "Inconsciente ou consciente do problema: gosta de tatuagem e ainda não pensa em tatuar.", False),
             ("Tela de abertura (9:16)", 'DA SALA PRA <em class="off">cena</em>.', True),
             ("Texto principal", "The VOID Talks com {convidado_talk}, em {data_talk}, na Vila Madalena, em São Paulo.\nDa sala pra cena: a Void conecta você com quem vive de tatuagem.\nConfirme sua presença pelo link.", False),
             ("Título", "The VOID Talks em {data_talk}", False),
             ("Descrição", "Na Vila Madalena, em SP", False),
             ("Botão da plataforma", "Cadastre-se", False),
             ("Destino", "Página do Talks (/talks/).", False),
             ("Rótulo na página", "CONFIRMAR PRESENÇA", False),
             ("Público", "Maiores de 18 anos, por interesse em tatuagem e arte, num raio de deslocamento até a Vila Madalena. Lista de ex-alunos só com consentimento.", False),
         ],
         porque="Só sai se o Talks for aberto ao público, com convidado e data confirmados. Gratuidade e frequência não são ditas até a escola confirmar."),
    dict(id="m1-pesquisa-aula", etapa="m1", frente="aula", canal="pesquisa", momento="Anúncio de pesquisa no Google: aula experimental de tatuagem",
         personas=["gabriel", "camila"], status="proposta", cta=True,
         campos=[
             ("Intenção", "Quem busca aula de tatuagem para iniciante, aula gratuita ou aula experimental em São Paulo.", False),
             ("Palavras-chave", "\"aula experimental de tatuagem\", \"aula de tatuagem gratuita\", \"aula de tatuagem sp\", \"aula de tatuagem para iniciantes\" (correspondência de frase). Negativas: online, piercing, emprego, vaga de tatuador.", False),
             ("Títulos", ["Aula experimental de tatuagem", "Aula gratuita e presencial", "Na Vila Madalena, São Paulo", "Para maiores de 18 anos", "Sem pré-requisito", "Não precisa saber desenhar", "The VOID Tattoo Academy", "Tatuar não é desenhar", "Teste antes de decidir", "Garanta sua vaga na aula", "Escola de tatuagem em SP", "Descubra se é para você", "Porta de entrada do Start", "Conheça a The VOID por dentro", "Rua Jericó, 217"], False),
             ("Descrições", ["Aula experimental gratuita e presencial na The VOID Tattoo Academy, na Vila Madalena.", "Para maiores de 18 anos e sem pré-requisito. Não precisa saber desenhar para começar.", "Tatuar não é desenhar. É técnica, e técnica se aprende com método e prática.", "Veja as próximas datas e garanta sua vaga na aula experimental da The VOID."], False),
             ("Caminhos", ["aula", "experimental"], False),
             ("Destino", "Página da aula experimental (/aula-experimental/).", False),
             ("Rótulo na página", "GARANTIR MINHA VAGA NA AULA", False),
             ("Fixar", "Título 1 na posição 1, para a busca sempre ler o que é a página.", False),
         ],
         porque="A busca já diz o que a pessoa quer. Todo título combina sozinho com qualquer outro, sem número sem fonte e sem superlativo."),
    # ------------------------------------------------------------------ M2
    dict(id="m2-wa-1", etapa="m2", canal="whatsapp", momento="Logo depois da resposta da pessoa",
         personas=["todas"], status="proposta", cta=None, tipo="Pergunta de qualificação",
         texto="{nome}, obrigado por contar.\nPara eu te indicar o caminho certo:\nhoje você já tatua ou vai começar do zero?",
         porque="Uma pergunta por vez, de mentor, não de formulário."),
    dict(id="m2-wa-2", etapa="m2", canal="whatsapp", momento="Segunda pergunta, quando a conversa fluiu",
         personas=["todas"], status="proposta", cta=None, tipo="Pergunta de qualificação",
         texto="Mais uma pergunta, e é a última:\nque estilo de tatuagem faz você parar de rolar a tela?",
         porque="Qualifica pelo repertório e já trata a pessoa como artista."),
    dict(id="m2-wa-3", etapa="m2", canal="whatsapp", momento="Convite para a conversa ou a visita",
         personas=["todas"], status="proposta", cta=True,
         texto="Pelo que você contou, o {produto} é o ponto de partida.\nO jeito mais direto de saber se faz sentido é uma conversa de 20 minutos ou uma visita ao estúdio, na Vila Madalena.\nEscolhe o horário aqui: {link_agenda}",
         porque="Conversa ou visita levam ao mesmo destino: a agenda."),
    dict(id="m2-wa-aula-pos", etapa="m2", canal="whatsapp", momento="Depois da aula experimental, no fim do mesmo dia",
         personas=["gabriel", "camila"], status="proposta", cta=True,
         texto="{nome}, foi bom te receber hoje na aula experimental.\nSe você saiu querendo mais, o próximo passo é uma conversa de 20 minutos sobre a formação Start, para ver turma, horário e formato.\nEscolhe o horário aqui: {link_agenda}",
         porque="Quem foi à aula já deu o passo de M1. O pedido seguinte é o de M2: a conversa."),
    dict(id="m2-wa-reativacao", etapa="m2", canal="whatsapp", momento="Abertura da próxima turma, para quem conversou e não fechou",
         personas=["todas"], status="pendente", pend="15", cta=True,
         texto="{nome}, aqui é {consultor}, da The VOID. A gente conversou em {mes_conversa} sobre a formação {produto}.\nAbriu a turma de {mes_turma}, que começa em *{data_turma}*. Quer conversar de novo, sem compromisso?\n{link_agenda}\nSe preferir não receber mais mensagens, responda SAIR.",
         porque="Motivo real para voltar: turma nova com data. Só para quem aceitou receber contato, e com a saída escrita."),
    dict(id="m2-email", etapa="m2", canal="email", momento="Para quem prefere ler antes de conversar",
         personas=["todas"], status="proposta", cta=True,
         assunto="Como funciona a formação por dentro", pre="Três pilares, prática desde o primeiro dia.",
         texto="Oi, {nome}.\n\nA formação {produto} se apoia em três pilares: técnica, identidade artística e carreira. E começa na prática, desde o primeiro dia.\n\nO jeito mais direto de entender se faz sentido para você é conversar com a gente ou visitar o estúdio, na Vila Madalena.\n\n[Agendar minha conversa] {link_agenda}\n\n{assinatura}",
         porque="Responde \"escola é tudo igual\" com estrutura, sem citar ninguém."),
    dict(id="m2-dm", etapa="m2", canal="dm", momento="Quem respondeu pela DM",
         personas=["todas"], status="proposta", cta=True,
         texto="Boa, {nome}. Pelo que você contou, o {produto} é o ponto de partida.\nQuer marcar uma conversa de 20 minutos ou conhecer o estúdio?\n{link_agenda}",
         porque="Mesmo destino do WhatsApp, no canal onde a pessoa já está."),
    dict(id="m2-reels", etapa="m2", canal="reels", momento="Antes Era, Reels 9:16 com depoimento real",
         personas=["gabriel", "camila"], status="pendente", pend="15", cta=True,
         telas=[
             ("0 a 2 s", "ANTES [OCUPAÇÃO]. HOJE, TATUADORA.", "Abertura no rosto ou nas mãos da aluna, preset Terra."),
             ("3 a 25 s", None, "O depoimento em vídeo, com legenda queimada, nome e @ autorizados e Fio de Produto. Na tela: \"Depoimento real de [nome], aluna da formação Start, turma [mês/ano], usado com autorização.\""),
             ("26 a 28 s", None, "Aviso na tela: \"Resultados individuais variam conforme prática e dedicação.\""),
             ("fecho", 'COMO É <em class="off">por dentro</em>?', "Agende sua conversa pelo link do perfil."),
         ],
         legenda="[Nome] trabalhava como [ocupação] quando entrou na formação Start. Hoje tatua.\nDepoimento real, usado com autorização. Resultados individuais variam conforme prática e dedicação.\nPara entender como a formação funciona por dentro, agende sua conversa pelo link do perfil.",
         porque="Prova de alguém parecido com quem assiste. Sem depoimento real e autorizado, a peça não existe."),
    dict(id="m2-anuncio", etapa="m2", canal="anuncio", momento="Anúncio 4:5 para quem já interagiu com o perfil",
         personas=["gabriel", "camila"], status="pendente", pend="15", cta=True,
         campos=[
             ("Consciência", "Consciente da solução: já interagiu e ainda acha que escola é tudo igual.", False),
             ("Peça", "Antes Era (R5): foto do aluno com véu, nome autorizado, Fio de Produto e aviso curto.", False),
             ("Texto principal", "[Nome] trabalhava como [ocupação] quando entrou na formação Start. [Frase real do depoimento, sem edição que mude o sentido.]\nDepoimento real, usado com autorização. Resultados individuais variam conforme prática e dedicação.\nPara entender como a formação funciona por dentro, agende uma conversa.", False),
             ("Título", "Agende sua conversa", False),
             ("Botão da plataforma", "Agendar", False),
             ("Destino", "Agenda de conversas, com a mesma promessa do anúncio.", False),
             ("Público", "Maiores de 18 anos que interagiram com o perfil ou o site nos últimos 30 dias. Exclui quem já tem conversa marcada, proposta aberta ou matrícula. Nunca antes e depois lado a lado.", False),
         ],
         porque="Retoma quem já demonstrou interesse com a prova que responde \"escola é tudo igual\"."),
    dict(id="m2-anuncio-start", etapa="m2", canal="anuncio", momento="Retomada de quem visitou a página do Start ou viu metade da VSL, Feed 4:5 e Reels 9:16",
         personas=["gabriel", "camila"], status="proposta", cta=True,
         campos=[
             ("Consciência", "Consciente do produto: conhece o Start e ainda não pediu a conversa.", False),
             ("Tela de abertura (9:16)", 'DO PRIMEIRO TRAÇO À PRIMEIRA <em class="off">pele</em>.', True),
             ("Texto principal", "Você viu como a formação Start funciona. Falta saber se a turma cabe na sua rotina.\nSão 15 aulas presenciais, 45 horas no total, com 4 tatuagens em pele humana, na Vila Madalena, em São Paulo.\nAgende uma conversa para ver turma, horário e formato.", False),
             ("Título", "Agende sua conversa sobre o Start", False),
             ("Descrição", "15 aulas, 45 horas", False),
             ("Botão da plataforma", "Agendar", False),
             ("Destino", "Página do Start (/trilha/start/).", False),
             ("Rótulo na página", "QUERO CONVERSAR SOBRE MINHA TURMA", False),
             ("Público", "Maiores de 18 anos que visitaram /trilha/start/ ou viram 50% da VSL do Start nos últimos 30 dias. Exclui quem já tem conversa marcada, proposta aberta ou matrícula.", False),
         ],
         porque="Fatos da página do Start (aulas, horas e tatuagens em pele humana), com a mesma promessa e o mesmo pedido da página. Quem já está em M3 ou M4 sai do público: ali a decisão é na conversa."),
    dict(id="m2-anuncio-master", etapa="m2", canal="anuncio", momento="Retomada de quem visitou a página do Master, Feed 4:5 e Reels 9:16",
         personas=["bruno"], status="pendente", pend="15", cta=True,
         campos=[
             ("Consciência", "Consciente do produto: já tatua, conhece o Master e ainda não pediu a conversa.", False),
             ("Tela de abertura (9:16)", 'SEU TRAÇO JÁ EXISTE. FALTA <em class="off">estilo</em>.', True),
             ("Texto principal", "Você já tatua em pele humana. O Master trabalha o que vem depois: técnica avançada e um projeto autoral.\nEspecialização presencial da The VOID, com correção em tempo real, na Vila Madalena, em São Paulo.\nAgende uma conversa sobre a próxima turma.", False),
             ("Título", "Agende sua conversa sobre o Master", False),
             ("Descrição", "Presencial, na Vila Madalena", False),
             ("Botão da plataforma", "Agendar", False),
             ("Destino", "Página do Master (/trilha/master/).", False),
             ("Rótulo na página", "QUERO FALAR SOBRE O MASTER", False),
             ("Público", "Maiores de 18 anos que visitaram /trilha/master/ nos últimos 30 dias. Exclui quem já tem conversa marcada, proposta aberta ou matrícula.", False),
         ],
         porque="O conteúdo do Master vem do site e ainda espera confirmação da escola; tamanho de turma e carga horária só entram depois disso."),
    dict(id="m2-anuncio-pro", etapa="m2", canal="anuncio", momento="Retomada de quem visitou a página do Pro, Feed 4:5 e Reels 9:16",
         personas=["bruno", "sylvia"], status="proposta", cta=True,
         campos=[
             ("Consciência", "Consciente do produto: conhece o Pro e ainda não pediu o diagnóstico.", False),
             ("Tela de abertura (9:16)", 'O PLANO DA SUA <em class="off">carreira</em>.', True),
             ("Texto principal", "Você viu o The VOID Pro: marca, conteúdo, vendas e carreira para tatuadores, online e ao vivo.\nO diagnóstico mostra por onde começar no seu caso, sem promessa de faturamento.\nAgende o seu diagnóstico.", False),
             ("Título", "Agende seu diagnóstico do Pro", False),
             ("Descrição", "Online e ao vivo", False),
             ("Botão da plataforma", "Agendar", False),
             ("Destino", "Página do Pro (/trilha/pro/).", False),
             ("Rótulo na página", "AGENDAR MEU DIAGNÓSTICO", False),
             ("Público", "Maiores de 18 anos que visitaram /trilha/pro/ nos últimos 30 dias, em todo o Brasil. Exclui quem já tem diagnóstico marcado, proposta aberta ou matrícula.", False),
         ],
         porque="O diagnóstico do Pro é a conversa de M2 com o nome da página. Nenhum número de renda, nem no texto, nem na imagem."),
    dict(id="m2-pesquisa-start", etapa="m2", canal="pesquisa", momento="Anúncio de pesquisa no Google: escola e curso de tatuagem em São Paulo",
         personas=["gabriel", "camila"], status="proposta", cta=True,
         campos=[
             ("Intenção", "Quem compara escolas de tatuagem em São Paulo: a crença de M2 (\"escola é tudo igual\") na forma de busca.", False),
             ("Palavras-chave", "\"escola de tatuagem sp\", \"escola de tatuagem em são paulo\", \"curso de tatuagem são paulo\", \"curso de tatuagem presencial\", \"the void tattoo\" (correspondência de frase). Negativas: online, gratuito, grátis, piercing, emprego, vaga de tatuador.", False),
             ("Títulos", ["Escola de tatuagem em SP", "The VOID Tattoo Academy", "Curso de tatuagem presencial", "Na Vila Madalena, São Paulo", "Comece do zero na tatuagem", "Não precisa saber desenhar", "15 aulas presenciais", "45 horas de formação", "4 tatuagens em pele humana", "8 técnicas fundamentais", "Aula de biossegurança", "Formação The VOID Start", "Converse sobre a sua turma", "Método ARTE da The VOID", "Do primeiro traço à pele"], False),
             ("Descrições", ["Para quem nunca tatuou: 15 aulas presenciais, 45 horas e 4 tatuagens em pele humana.", "Não precisa saber desenhar. Tatuar é técnica, e técnica se aprende com método e prática.", "Fundamentos, pele artificial, pele humana e mercado, na Vila Madalena, em São Paulo.", "Converse com a The VOID sobre turma, horário e formato antes de decidir."], False),
             ("Caminhos", ["trilha", "start"], False),
             ("Destino", "Página do Start (/trilha/start/).", False),
             ("Rótulo na página", "QUERO CONVERSAR SOBRE MINHA TURMA", False),
             ("Fixar", "Título 1 na posição 1 e título 2 na posição 2: o que é e quem é.", False),
         ],
         porque="É a busca mais quente da escola. Os números são os da página do Start, com a mesma redação; nenhum título promete renda, emprego ou posição de mercado."),
    # ------------------------------------------------------------------ M3
    dict(id="m3-wa-visita", etapa="m3", canal="whatsapp", momento="Confirmação da visita, logo depois do agendamento",
         personas=["todas"], status="proposta", cta=None, tipo="Lembrete, sem pedido",
         texto="{nome}, sua visita está marcada: *{data}*, às *{horario}*, em *{endereco}*.\nQuem vai te receber sou eu, {consultor}. Pode trazer seus desenhos, se quiser.",
         porque="Nome de quem recebe e endereço do bloco NAP: a visita começa antes de a pessoa chegar."),
    dict(id="m3-wa-visita-falta", etapa="m3", canal="whatsapp", momento="Falta na visita: uma hora depois do horário marcado",
         personas=["todas"], status="proposta", cta=None, tipo="Cuidado, porta aberta",
         texto="{nome}, senti sua falta hoje na visita. Está tudo bem por aí?\nSe quiser, a gente marca outro horário. É só me falar o melhor dia para você.",
         porque="Cuidado antes de pedido. A remarcação fica com a pessoa, sem cobrança."),
    dict(id="m3-wa-pos", etapa="m3", canal="whatsapp", momento="Depois da visita ou da conversa",
         personas=["todas"], status="proposta", cta=True,
         texto="{nome}, foi bom te receber hoje.\nComo você comentou sobre {ponto_citado}, preparei a proposta da turma que mais combina com você.\nPosso te mandar?",
         porque="Devolve algo que a pessoa disse. Prova de escuta é prova técnica."),
    dict(id="m3-email", etapa="m3", canal="email", momento="Resumo da conversa de diagnóstico",
         personas=["todas"], status="proposta", cta=True,
         assunto="O que conversamos hoje", pre="Seu ponto de partida e o próximo passo.",
         texto="Oi, {nome}.\n\nResumo do que ouvi: você {resumo_situacao} e quer {objetivo_declarado}.\n\nPelo seu momento, o caminho é o {produto}, que trabalha {foco_do_produto}.\n\n[Receber minha proposta de turma] {link_proposta}\n\n{assinatura}",
         porque="Escrito, o que foi dito vira compromisso dos dois lados."),
    dict(id="m3-dm", etapa="m3", canal="dm", momento="Quem conversou pela DM",
         personas=["todas"], status="proposta", cta=True,
         texto="{nome}, foi bom conversar com você.\nQuer receber a proposta da turma que combina com o que você contou?",
         porque="A proposta sai do que a pessoa contou, não de uma tabela."),
    dict(id="m3-story", etapa="m3", canal="reels", momento="Turma Aberta, story 9:16 no Campo do Produto",
         personas=["todas"], status="pendente", pend="15", cta=True,
         telas=[
             ("tela única", "TURMA DE [MÊS]", "Campo Start, selo Start no canto superior direito, Barra de Turma ampliada: COMEÇA EM [DATA] · [DIAS] · [HORÁRIO] · [N] VAGAS NO TOTAL."),
             ("rótulo do CTA", None, "Em texto, na área segura entre y = 270 e y = 1500: \"Responda TURMA e receba sua proposta.\""),
         ],
         legenda=None,
         porque="Mesmo dado da Barra de Turma e do Cartão de Turma: uma fonte de verdade. Sem data real, não sai."),
    # ------------------------------------------------------------------ M4
    dict(id="m4-wa-envio", etapa="m4", canal="whatsapp", momento="Envio da proposta",
         personas=["todas"], status="proposta", cta=True,
         texto="{nome}, aqui está sua proposta para a turma de {mes_turma}.\nEstá tudo nela: o que você vai aprender, as datas, o valor total e as formas de pagamento.\nPara garantir sua vaga, é por aqui: {link_proposta}",
         porque="Tudo num lugar só, sem letra miúda, com o link sozinho no fim."),
    dict(id="m4-wa-pensar", etapa="m4", canal="whatsapp", momento="Resposta a \"vou pensar\"",
         personas=["todas"], status="proposta", cta=None, tipo="Pergunta, sem pedido",
         texto="Faz sentido pensar, {nome}. Decisão boa é decisão consciente.\nMe conta: o que pesa mais agora, o valor, o tempo ou a dúvida se você dá conta?",
         porque="Nomeia as três objeções reais e deixa a pessoa escolher qual conversar."),
    dict(id="m4-wa-valor", etapa="m4", canal="whatsapp", momento="Quando a objeção é o valor",
         personas=["gabriel"], status="pendente", pend="15", cta=None, tipo="Pergunta, sem pedido",
         texto="Entendo, {nome}. Dinheiro merece conta feita com calma.\nNa proposta estão o valor total e as parcelas, sem letra miúda: {condicao_pagamento}.\nQuer que eu monte com você a forma de pagamento que cabe no seu mês?",
         porque="Trata o valor com clareza e parcelamento real, sem prometer retorno do investimento."),
    dict(id="m4-wa-tempo", etapa="m4", canal="whatsapp", momento="Quando a objeção é \"e se não der certo\"",
         personas=["camila"], status="pendente", pend="15", cta=None, tipo="Pergunta, sem pedido",
         texto="{nome}, faz sentido pesar o que você já construiu.\nSe ajudar, te mando o depoimento de {nome_depoente}, que entrou na formação vinda de {ocupacao_anterior}. É real, autorizado e mostra o caminho como ele foi.\nPosso te mandar?",
         porque="A Camila precisa de lógica antes da permissão: alguém com o mesmo ponto de partida."),
    dict(id="m4-wa-tecnica", etapa="m4", canal="whatsapp", momento="Quando a objeção é \"preciso de mais técnica antes\"",
         personas=["bruno", "sylvia"], status="proposta", cta=None, tipo="Pergunta, sem pedido",
         texto="{nome}, a técnica você já tem. O {produto} trabalha o que vem depois dela: posicionamento, marca pessoal e como apresentar o valor do seu trabalho.\nQuer ver o roteiro dos módulos antes de decidir?",
         porque="Mostra o conteúdo em vez de prometer resultado."),
    dict(id="m4-wa-prazo", etapa="m4", canal="whatsapp", momento="Lembrete de prazo, só quando a data for real",
         personas=["todas"], status="pendente", pend="15", cta=True,
         texto="{nome}, as matrículas da turma de {mes_turma} fecham em *{data_fechamento}*. Depois disso, a próxima turma começa em *{proxima_turma}*.\nQuer que eu garanta sua vaga?",
         porque="Urgência real: data do calendário e a próxima turma dita junto. Sem data, a mensagem não sai."),
    dict(id="m4-wa-lista-espera", etapa="m4", canal="whatsapp", momento="Turma cheia, com a próxima já no calendário",
         personas=["todas"], status="pendente", pend="15", cta=None, tipo="Pergunta, sem pedido",
         texto="{nome}, as vagas da turma de {mes_turma} terminaram antes da sua decisão.\nA próxima começa em *{proxima_turma}*. Quer que eu guarde seu nome e te avise quando as matrículas dela abrirem?",
         porque="Escassez real dita como fato, com a alternativa concreta na mesma mensagem. Sem turma cheia de verdade, a mensagem não existe."),
    dict(id="m4-email", etapa="m4", canal="email", momento="Proposta por escrito",
         personas=["todas"], status="pendente", pend="15", cta=True,
         assunto="Sua proposta para a turma de {mes_turma}", pre="Tudo por escrito, sem letra miúda.",
         texto="Oi, {nome}.\n\nAqui está o que combinamos:\nFormação: {produto}\nInício: {data_turma}\nInclui: {itens_incluidos}\nInvestimento: {valor_total} ou {parcelamento}\n\nComo a formação termina: {itens_de_encerramento}\n\n[Garantir minha vaga na turma de {mes_turma}] {link_pagamento}\n\nMatrícula feita pela internet, telefone ou WhatsApp pode ser cancelada em até 7 dias a partir da contratação, com devolução integral do valor pago, conforme o artigo 49 do Código de Defesa do Consumidor.\n\n{assinatura}",
         porque="Valor total, parcelas e arrependimento iguais ao checkout. O fim do caminho vem da Ficha da Formação de cada produto, nunca de um texto único para Start, Master e Pro."),
    # ------------------------------------------------------------------ M5
    dict(id="m5-wa", etapa="m5", canal="whatsapp", momento="Confirmação da matrícula, na hora",
         personas=["todas"], status="proposta", cta=True,
         texto="{nome}, matrícula confirmada. Boas-vindas à The VOID.\nSeu primeiro dia é *{data_turma}*, às *{horario}*, em *{endereco}*.\nPode confirmar sua presença?",
         porque="Alívio primeiro, informação prática logo depois."),
    dict(id="m5-wa-vespera", etapa="m5", canal="whatsapp", momento="Véspera do primeiro dia",
         personas=["todas"], status="proposta", cta=True,
         texto="{nome}, amanhã é o seu primeiro dia: *{horario}*, em *{endereco}*.\nO que levar: {o_que_levar}.\nVenha como você é, com as mãos trêmulas e tudo. Aqui, elas ficam firmes.\nMe confirma que você vem?",
         porque="A frase das mãos vem das Personas da The VOID e acolhe o medo de M6 antes de ele chegar."),
    dict(id="m5-email", etapa="m5", canal="email", momento="Boas-vindas com tudo por escrito",
         personas=["todas"], status="proposta", cta=True,
         assunto="Seu primeiro dia na Void", pre="Data, endereço e o que levar.",
         texto="Oi, {nome}.\n\nEstá feito. Agora a gente cuida do primeiro passo junto com você.\n\nSeu primeiro dia: {data_turma}, às {horario}, em {endereco}.\nO que levar: {o_que_levar}.\nQuem te recebe: {nome_recepcao}.\n\nNesse dia acontece o Ritual do Traço. Todo mundo começa com um traço. Aqui, ele tem nome, coragem e história.\n\nSeu acesso ao portal do aluno: {link_portal}\n\n[Confirmar presença no primeiro dia] {link_confirmacao}\n\nA arte que preenche. A carreira que liberta.\n\n{assinatura}",
         porque="Um dos dois e-mails com a tagline (seção 9.6). O Ritual do Traço é anunciado com a frase do próprio rito.",
         nota="O mural do Ritual do Traço só entra no texto depois de confirmado [P 6]."),
    dict(id="m5-dm", etapa="m5", canal="dm", momento="Quando a matrícula veio pela DM",
         personas=["todas"], status="proposta", cta=None, tipo="Aviso, sem pedido",
         texto="{nome}, matrícula confirmada. Te mandei tudo no WhatsApp e no e-mail. Até {data_turma}.",
         porque="Não repete a confirmação: aponta onde ela está."),
    # ------------------------------------------------------------------ M6
    dict(id="m6-wa-ritual", etapa="m6", canal="whatsapp", momento="Depois do Ritual do Traço, no primeiro dia",
         personas=["todas"], status="proposta", cta=True,
         texto="{nome}, hoje você deu seu primeiro traço na The VOID.\nDaqui a alguns meses você vai querer comparar.\nRegistra a foto dele no Meu Traço: {link_portal}",
         porque="O primeiro registro é o ponto de partida de toda comparação de M7."),
    dict(id="m6-wa-pele", etapa="m6", canal="whatsapp", momento="Do professor, depois da Primeira Pele",
         personas=["todas"], status="proposta", cta=True,
         texto="{nome}, aqui é {professor}. Você fez sua primeira pele hoje. Você nunca esquece a primeira.\nUm ponto forte: {ponto_forte}.\nUm ponto para a próxima: {ponto_ajuste}.\nQuando quiser, registra a foto oficial no Meu Traço: {link_portal}",
         porque="Feedback em par, do jeito da Prática com Feedback. A foto só circula com consentimento do aluno e de quem foi tatuado."),
    dict(id="m6-email", etapa="m6", canal="email", momento="Resumo da primeira semana",
         personas=["todas"], status="proposta", cta=True,
         assunto="Sua primeira semana, {nome}", pre="O que você já fez e o que vem agora.",
         texto="Oi, {nome}.\n\nEsta semana você deu seu primeiro traço no Ritual do Traço e começou {modulo_atual}.\nNa próxima: {proxima_pratica}.\n\nSe ainda não registrou, a foto do seu primeiro traço entra no Meu Traço. É o ponto de partida da sua comparação.\n\n[Registrar meu primeiro traço] {link_portal}\n\n{assinatura}",
         porque="Mostra o que já foi feito antes de pedir o próximo passo."),
    # ------------------------------------------------------------------ M7
    dict(id="m7-wa-falta", etapa="m7", canal="whatsapp", momento="Falta em aula prática",
         personas=["todas"], status="proposta", cta=None, tipo="Cuidado, sem pedido",
         texto="{nome}, senti sua falta na prática de hoje. Está tudo bem?\nMe fala como você está, e eu vejo com a coordenação o jeito certo de você não perder esse conteúdo.",
         porque="Cuidado antes de qualquer pedido. Não promete reposição que a escola não tenha confirmado."),
    dict(id="m7-wa-workshop", etapa="m7", canal="whatsapp", momento="Antes do Workshop do Estilo",
         personas=["todas"], status="proposta", cta=True,
         texto="{nome}, o Workshop do Estilo é em *{data_workshop}*. É o espaço para sair do mais do mesmo e testar o que é seu.\nPara chegar com algo na mão, manda um trabalho para {professor} olhar antes: {link_feedback}",
         porque="O rito do meio da formação vira motivo para o pedido da etapa: mostrar um trabalho."),
    dict(id="m7-email", etapa="m7", canal="email", momento="Marco de evolução",
         personas=["todas"], status="proposta", cta=True,
         assunto="Compare você com você", pre="Seu primeiro traço e o trabalho de hoje, lado a lado.",
         texto="Oi, {nome}.\n\nColoquei lado a lado o primeiro traço que você registrou em {data_ritual} e o trabalho que você enviou esta semana.\n\nA distância entre os dois é o que importa. Não a distância para os outros.\n\n[Enviar meu trabalho para feedback] {link_feedback}\n\n{assinatura}",
         porque="A comparação é com a própria pessoa e fica visível só para ela."),
    # ------------------------------------------------------------------ M8
    dict(id="m8-wa-master", etapa="m8", frente="proximo", canal="whatsapp", momento="Alguns dias depois da formatura do Start",
         personas=["gabriel", "camila"], status="proposta", cta=True,
         texto="{nome}, olhando seu portfólio de formatura, o próximo passo natural é o The VOID Master, onde você descobre sua identidade artística.\nQuer conhecer o Master numa conversa de 20 minutos?",
         porque="Parte do que a pessoa já fez. O Master entra com a frase do próprio produto."),
    dict(id="m8-wa-pro", etapa="m8", frente="proximo", canal="whatsapp", momento="Alguns dias depois da formatura do Master",
         personas=["bruno", "sylvia"], status="proposta", cta=True,
         texto="{nome}, olhando seu portfólio de formatura, o próximo passo natural é o The VOID Pro, para quem quer ser estrategista da própria carreira.\nQuer conhecer o Pro numa conversa de 20 minutos?",
         porque="Mesma estrutura do convite ao Master, com a frase de assinatura do Pro."),
    dict(id="m8-email-master", etapa="m8", frente="proximo", canal="email", momento="O próximo círculo no Mapa da Trilha",
         personas=["gabriel", "camila"], status="proposta", cta=True,
         assunto="Seu próximo círculo", pre="O Start foi o primeiro. O Master é o do meio.",
         texto="Oi, {nome}.\n\nNo Mapa da Trilha da The VOID, o Start é o primeiro círculo. Você acabou de preenchê-lo.\n\nO Master é o círculo do meio: o lugar de descobrir sua identidade artística e transformar o seu traço em estilo autoral.\n\n[Conhecer o Master] {link_master}\n\n{assinatura}",
         porque="O Mapa da Trilha com o próximo círculo aceso é o recurso que lidera M8."),
    dict(id="m8-wa-indicacao", etapa="m8", frente="indicacao", canal="whatsapp", momento="Pedido de indicação, com mensagem pronta",
         personas=["todas"], status="proposta", cta=True,
         texto="{nome}, se você conhece alguém que vive dizendo \"um dia eu tatuo\", pode encaminhar esta mensagem:\n\"Fiz minha formação na The VOID Tattoo Academy, na Vila Madalena. Se você quiser conhecer, fala com {consultor}: {link_whatsapp}\"\nSó encaminha se fizer sentido para você.",
         porque="A indicação é um favor, não um negócio. Nada de prêmio que não exista."),
    dict(id="m8-dm-repost", etapa="m8", frente="indicacao", canal="dm", momento="Pedido de autorização para repostar",
         personas=["todas"], status="proposta", cta=None, tipo="Pedido de autorização",
         texto="{nome}, esse trabalho ficou muito forte. Podemos repostar no perfil da The VOID, com seu nome e marcação?\nSe não quiser, tudo bem.",
         porque="Depoimento e repostagem só com sim por escrito. O \"tudo bem\" é parte do pedido."),
    dict(id="m8-wa-talks", etapa="m8", frente="encontro", canal="whatsapp", momento="Convite para o The VOID Talks",
         personas=["todas"], status="proposta", cta=True,
         texto="{nome}, o próximo The VOID Talks é com {convidado_talk}, em *{data_talk}*, às *{horario}*.\nDa sala pra cena.\nQuer que eu guarde seu lugar?",
         porque="A frase do Talks vem da Plataforma de Branding. A frequência dos encontros não é dita até ser confirmada [P 6]."),
    dict(id="m8-email-formatura", etapa="m8", frente="encontro", canal="email", momento="Convite para a Formatura com Pele",
         personas=["todas"], status="proposta", cta=True,
         assunto="Sua Formatura com Pele", pre="{data_formatura}. Traga quem acreditou em você.",
         texto="Oi, {nome}.\n\nVocê não sai apenas com um certificado. Sai com um novo capítulo na pele.\n\nSua Formatura com Pele é em {data_formatura}, às {horario}, em {endereco}. Você pode levar {numero_convidados} convidados.\n\n[Confirmar presença] {link_confirmacao}\n\nA arte que preenche. A carreira que liberta.\n\n{assinatura}",
         porque="Contexto de peso: aceita a tagline (seção 9.6). A frase de abertura é a do próprio rito."),
    dict(id="m8-reels-talks", etapa="m8", frente="encontro", canal="reels", momento="Convocação do Talks, Reels e story 9:16",
         personas=["todas"], status="pendente", pend="6", cta=True,
         telas=[
             ("0 a 2 s", 'DA SALA PRA <em class="off">cena</em>.', "Foto ou vídeo de público, P&B noturno, do próprio evento."),
             ("3 a 12 s", None, "\"CONVOCAÇÃO\" em Crédito; convidado, data e local reais: {convidado_talk} · {data_talk} · Rua Jericó, 217, Vila Madalena."),
             ("pé", None, "Letreiro Corrido: THE VOID TATTOO · ® 2025 · SÃO PAULO · BRAZIL."),
             ("fecho", None, "Confirme presença pelo link do perfil."),
         ],
         legenda="The VOID Talks com {convidado_talk}, em {data_talk}, na Vila Madalena.\nDa sala pra cena. A Void conecta você com quem vive disso.\nConfirme presença pelo link do perfil.",
         porque="Serve ao ex-aluno e a quem ainda não chegou. Dizer \"todo mês\" depende da frequência real [P 6]."),
]

# ----------------------------------------------------------------------------- render
def contar(t, amostra="Camila"):
    return len(re.sub(r"\{nome\}", amostra, re.sub(r"\{[a-z_]+\}", "dd/mm", t)))


def pill_status(m):
    rot, icone, tit = STATUS[m["status"]]
    p = f' [P {m["pend"]}]' if m.get("pend") else ""
    return f'<span class="status" data-status="{m["status"]}" title="{e(tit)}">{ic(icone, " ic-16")}{rot}{p}</span>'


def rotulo_cta(etapa, m=None):
    frentes = FRENTES.get(etapa["id"])
    if frentes and m is not None:
        frente = m["frente"]
        if etapa["id"] == "m8" and frente == "proximo":
            return "Conhecer o Pro" if "Pro" in m["texto"].split("\n")[-1] else "Conhecer o Master"
        return frentes[frente][1]
    return etapa["cta"]


def medir(canal, campo, valor):
    """(texto medido, limite) de cada item com limite de caracteres, ou lista vazia."""
    regra = LIMITES.get(canal, {}).get(campo)
    if not regra:
        return []
    modo, lim = regra
    if modo == "cada":
        return [(v, lim) for v in valor]
    if modo == "linha1":
        return [(valor.split("\n")[0], lim)]
    return [(valor, lim)]


def conta_html(texto, lim, prefixo=""):
    n = contar(texto)
    return f'<span class="conta" data-ok="{str(n <= lim).lower()}">{prefixo}{n} de {lim}</span>'


def personas_tags(m):
    if m["personas"] == ["todas"]:
        return '<span class="tag">Todas as personas</span>'
    nomes = {p["id"]: p["nome"] for p in PERSONAS}
    return "".join(f'<span class="tag tag-persona">{nomes[p]}</span>' for p in m["personas"])


def texto_copia(m):
    if m["canal"] == "email":
        return f'Assunto: {m["assunto"]}\nPré-cabeçalho: {m["pre"]}\n\n{m["texto"]}'
    if "telas" in m:
        linhas = []
        for tempo, tela, fala in m["telas"]:
            t = re.sub(r"<[^>]+>", "", tela).upper() if tela else ""
            linhas.append(f"[{tempo}] " + (f"Tela: {t} " if t else "") + (f"Fala ou cena: {fala}" if fala else ""))
        if m.get("legenda"):
            linhas += ["", "Legenda do post:", m["legenda"]]
        return "\n".join(linhas)
    if "campos" in m:
        linhas = []
        for k, v, tit in m["campos"]:
            if isinstance(v, list):
                linhas.append(f"{k}:")
                linhas += [f"{i}. {x}" for i, x in enumerate(v, 1)]
            else:
                linhas.append(f"{k}: {re.sub(r'<[^>]+>', '', v).upper() if tit else v}")
        return "\n".join(linhas)
    return m["texto"]


def corpo_modelo(m):
    c = m["canal"]
    if c in ("whatsapp", "dm"):
        cls = "balao-zap" if c == "whatsapp" else "balao-dm"
        return f'<div class="balao {cls}"><p class="msg">{com_variaveis(m["texto"])}</p></div>'
    if c == "email":
        na, np_ = contar(m["assunto"]), contar(m["pre"])
        return (
            '<dl class="email-cab">'
            f'<div><dt>Assunto</dt><dd>{com_variaveis(m["assunto"])}<span class="conta" data-ok="{str(na <= 45).lower()}">{na} de 45</span></dd></div>'
            f'<div><dt>Pré-cabeçalho</dt><dd>{com_variaveis(m["pre"])}<span class="conta" data-ok="{str(np_ <= 80).lower()}">{np_} de 80</span></dd></div>'
            '</dl>'
            f'<div class="email-corpo"><p class="msg">{com_variaveis(m["texto"])}</p></div>'
        )
    if "telas" in m:
        itens = []
        for tempo, tela, fala in m["telas"]:
            t = f'<p class="tela-titulo">{tela}</p>' if tela else ""
            f_ = f'<p class="tela-fala">{com_variaveis(fala)}</p>' if fala else ""
            itens.append(f'<li><p class="tela-tempo credito">{e(tempo)}</p><div>{t}{f_}</div></li>')
        leg = ""
        if m.get("legenda"):
            leg = f'<div class="legenda-post"><p class="credito">Legenda do post</p><p class="msg">{com_variaveis(m["legenda"])}</p></div>'
        return f'<ol class="roteiro">{"".join(itens)}</ol>{leg}'
    if "campos" in m:
        linhas = []
        for k, v, tit in m["campos"]:
            medidas = medir(c, k, v)
            if isinstance(v, list):
                itens = "".join(f'<li><span class="msg">{com_variaveis(x)}</span>{conta_html(x, lim)}</li>' for x, lim in medidas)
                dd = f'<ol class="lista-pesquisa">{itens}</ol>'
            elif tit:
                dd = f'<span class="tela-titulo">{v}</span>'
            else:
                pre = "1ª linha: " if LIMITES.get(c, {}).get(k, ("",))[0] == "linha1" else ""
                dd = f'<span class="msg">{com_variaveis(v)}</span>' + "".join(conta_html(x, lim, pre) for x, lim in medidas)
            linhas.append(f'<div><dt>{e(k)}</dt><dd>{dd}</dd></div>')
        return f'<dl class="ficha-anuncio">{"".join(linhas)}</dl>'
    return ""


def cartao_modelo(m, etapa):
    nome_canal, icone = CANAIS[m["canal"]]
    if m["cta"]:
        cta = f'<p class="cta-linha">{ic("arrow-right", " ic-16")}<span>CTA</span><b>{e(rotulo_cta(etapa, m))}</b></p>'
        chave = etapa["id"] + ("-" + m["frente"] if m.get("frente") else "")
        attr_cta = f' data-cta="{chave}" data-cta-rotulo="{e(rotulo_cta(etapa, m) if etapa["id"] != "m8" else FRENTES_M8[m["frente"]][1])}"'
    else:
        cta = f'<p class="cta-linha cta-nenhum">{ic("message-circle", " ic-16")}<span>{e(m.get("tipo", "Sem pedido"))}</span></p>'
        attr_cta = ' data-cta="nenhum"'
    nota = f'<p class="nota-modelo">{ic("triangle-alert", " ic-16")}<span>{e(m["nota"])}</span></p>' if m.get("nota") else ""
    frente = ""
    if m.get("frente"):
        frente = f'<span class="tag tag-frente">{e(FRENTES[m["etapa"]][m["frente"]][0])}</span>'
    return f'''
      <article class="modelo" id="{m["id"]}" data-etapa="{m["etapa"]}" data-canal="{m["canal"]}" data-personas="{" ".join(m["personas"])}"{attr_cta} aria-labelledby="{m["id"]}-t">
        <header class="modelo-cab">
          <p class="modelo-canal credito">{ic(icone)}<span>{e(nome_canal)}</span></p>
          {pill_status(m)}
        </header>
        <h4 class="modelo-titulo" id="{m["id"]}-t">{e(m["momento"])}</h4>
        <p class="modelo-tags">{frente}{personas_tags(m)}</p>
        <div class="modelo-corpo">{corpo_modelo(m)}</div>
        {cta}
        <p class="porque"><b>Por quê:</b> {e(m["porque"])}</p>
        {nota}
        <div class="modelo-acoes">
          <button class="copiar" type="button" data-copiar="{m["id"]}-fonte">{ic("copy")}<span>Copiar mensagem</span></button>
        </div>
        <textarea class="fonte-copia" id="{m["id"]}-fonte" hidden aria-hidden="true" tabindex="-1">{e(texto_copia(m))}</textarea>
      </article>'''


def bloco_etapa(et, idx):
    modelos = [m for m in MODELOS if m["etapa"] == et["id"]]
    cards = "".join(cartao_modelo(m, et) for m in modelos)
    fora = ""
    if et["fora"]:
        itens = "".join(f'<li><b>{e(CANAIS[c][0])}:</b> {e(t)}</li>' for c, t in et["fora"])
        fora = f'<div class="fora" data-etapa-fora="{et["id"]}"><p class="credito">{ic("minus", " ic-16")}Fora desta etapa</p><ul>{itens}</ul></div>'
    nunca = "".join(f"<li>{e(n)}</li>" for n in et["nunca"])
    if et["id"] in FRENTES:
        cta_html = '<div class="frentes">' + "".join(
            f'<p><span class="credito">{e(n)}</span><span class="rotulo-cta">{e(r)}</span></p>' for n, r in FRENTES[et["id"]].values()) + "</div>"
        cta_tit = "Um CTA por mensagem, por porta de entrada" if et["id"] == "m1" else "Um CTA por mensagem, por frente"
    else:
        cta_html = f'<span class="rotulo-cta">{e(et["cta"])}</span>'
        cta_tit = "CTA único da etapa"
    return f'''
    <section class="etapa" id="etapa-{et["id"]}" data-etapa="{et["id"]}" aria-labelledby="etapa-{et["id"]}-t">
      <header class="etapa-cab">
        <p class="etapa-num numeral-prova" aria-hidden="true">{et["id"].upper()}</p>
        <div class="etapa-txt">
          <p class="credito etapa-sobre">{et["id"].upper()} · {e(et["funcao"])} · atributo {e(et["atributo"])}</p>
          <h3 class="etapa-titulo" id="etapa-{et["id"]}-t">{e(et["nome"])}</h3>
          <p class="etapa-crenca">"{e(et["crenca"])}"</p>
          <p class="etapa-guia">{e(et["guia"])}</p>
        </div>
        <div class="etapa-cta"><p class="credito">{cta_tit}</p>{cta_html}</div>
      </header>
      <div class="modelos">{cards}
      </div>
      <p class="vazio-filtro" hidden>{ic("list-filter", " ic-16")}<span>Nenhum modelo desta etapa para esse recorte. Os modelos para todas as personas aparecem com o filtro de canal em Todos.</span></p>
      <div class="etapa-pe">
        {fora}
        <div class="nunca" data-exemplo="proibido"><p class="credito">{ic("circle-x", " ic-16")}Nunca dizer nesta etapa</p><ul>{nunca}</ul></div>
      </div>
    </section>'''


def cartao_matriz(et):
    if et["id"] == "m1":
        cta = "".join(f'<span class="rotulo-cta">{e(r)}</span>' for _, r in list(FRENTES_M1.values())[:2])
        cta_nota = f'<p class="matriz-nota">Um por mensagem, pela porta de entrada. {e(REGRA_PORTAS_M1)}</p>'
    elif et["id"] == "m8":
        cta = "".join(f'<span class="rotulo-cta">{e(r)}</span>' for _, r in list(FRENTES_M8.values())[:2])
        cta_nota = '<p class="matriz-nota">Um por mensagem. Convites para o Talks e a Formatura usam CONFIRMAR PRESENÇA.</p>'
    else:
        cta = f'<span class="rotulo-cta">{e(et["cta"])}</span>'
        cta_nota = ""
    n = sum(1 for m in MODELOS if m["etapa"] == et["id"])
    return f'''
      <article class="matriz-cartao" data-etapa="{et["id"]}" aria-labelledby="mx-{et["id"]}-t">
        <p class="matriz-m numeral-prova" aria-hidden="true">{et["id"].upper()}</p>
        <h3 class="matriz-nome" id="mx-{et["id"]}-t"><span class="so-leitor">{et["id"].upper()} </span>{e(et["nome"])}</h3>
        <p class="matriz-crenca">"{e(et["crenca"])}"</p>
        <dl class="matriz-dl">
          <div><dt>Atributo que sobe</dt><dd>{e(et["atributo"])}</dd></div>
          <div><dt>Função</dt><dd>{e(et["funcao"])}</dd></div>
          <div><dt>Recurso que lidera</dt><dd>{e(et["recurso"])}</dd></div>
          <div><dt>Componente</dt><dd>{e(et["componente"])}</dd></div>
          <div><dt>Métrica</dt><dd>{e(et["metrica"])}</dd></div>
        </dl>
        <div class="matriz-cta"><p class="credito">CTA</p>{cta}{cta_nota}</div>
        <a class="matriz-ir" href="#etapa-{et["id"]}">{ic("arrow-right", " ic-16")}<span>{n} modelos de {et["id"].upper()}</span></a>
      </article>'''


def cartao_persona(p):
    if p["hero"]:
        hero = f'<p class="persona-hero">{p["hero"]}</p>'
    else:
        hero = f'<p class="persona-frase">{e(p["hero_frase"])}</p>'
    st = pill_status(p) if p["status"] != "decidido" else ""
    return f'''
      <article class="persona" data-persona="{p["id"]}" aria-labelledby="pe-{p["id"]}">
        <header><h3 id="pe-{p["id"]}" class="persona-nome">{e(p["nome"])}</h3><p class="credito">{e(p["papel"])} · {e(p["produto"])}</p>{st}<span class="persona-ativa credito" hidden>{ic("list-filter", " ic-16")}Filtro ativo</span></header>
        <p class="persona-conv">"{e(p["conviccao"])}"</p>
        <p class="persona-tom"><b>Tom de conversão:</b> {e(p["tom"])}</p>
        {hero}
        <p class="persona-nota">{e(p["hero_nota"])}</p>
      </article>'''


# Cartões de Conversa (12.6): 1080 por 1350, Sala, selo do produto, título de até 5
# palavras, até 4 linhas de dado em Archivo 500 de 40 u, rodapé-assinatura.
CARTOES = [
    dict(id="cc-turma", nome="Cartão de Turma", etapas=["m3", "m4"], estacao="start", selo="start",
         titulo='TURMA DE <em class="off">[mês]</em>',
         linhas=[("calendar-days", "COMEÇA EM [DATA]"), ("clock", "[DIAS] · [HORÁRIO]"), ("users-round", "[N] VAGAS NO TOTAL"), ("map-pin", "RUA JERICÓ, 217 · VILA MADALENA")],
         nota="Mesmo dado da Barra de Turma: uma fonte de verdade. Datas, horário e vagas dependem do calendário real.",
         pend="15"),
    dict(id="cc-primeiro-dia", nome="Cartão do Primeiro Dia", etapas=["m5"], estacao="start", selo="start",
         titulo='SEU PRIMEIRO <em class="off">dia</em>',
         linhas=[("calendar-days", "[DATA] · [HORÁRIO]"), ("map-pin", "RUA JERICÓ, 217 · VILA MADALENA"), ("file-text", "LEVE: [O QUE LEVAR]"), ("user-round", "QUEM RECEBE: [NOME]")],
         nota="Vai junto da confirmação de matrícula. O que levar e quem recebe saem da coordenação.",
         pend=None),
    dict(id="cc-marco", nome="Cartão de Marco", etapas=["m6", "m7"], estacao="start", selo="start",
         titulo="PRIMEIRA PELE",
         off="Você nunca esquece sua primeira pele.",
         foto=True,
         linhas=[("flag", "[NOME DO ALUNO] · [DATA]")],
         nota="Enviado ao aluno, com pedido de autorização antes de qualquer publicação. A foto segue o protocolo dos ritos e precisa do consentimento de quem foi tatuado.",
         pend="22"),
    dict(id="cc-talks", nome="Convite Talks", etapas=["m8"], estacao="chamado", selo=None,
         titulo='DA SALA PRA <em class="off">cena</em>',
         linhas=[("user-round", "COM [CONVIDADO]"), ("calendar-days", "[DATA] · [HORÁRIO]"), ("map-pin", "RUA JERICÓ, 217 · VILA MADALENA")],
         nota="Co-assinatura: logotipo oficial, fio vertical e TALKS em Archivo 700. Frequência dos encontros a confirmar antes de dizer \"todo mês\" [P 6].",
         pend=None, talks=True),
    dict(id="cc-mapa", nome="Mapa da Trilha", etapas=["m3"], estacao="start", selo="start",
         titulo='É AQUI QUE VOCÊ <em class="off">entra</em>',
         linhas=[],
         mapa=True,
         nota="O produto indicado na conversa fica aceso. Na mensagem, a frase que acompanha é \"é aqui que você entra\".",
         pend=None),
]


def cartao_conversa(c):
    selo = ""
    if c.get("selo"):
        selo = f'<img class="cc-selo" src="assets/brand/svg/selo-completo-{c["selo"]}.svg" alt="Selo The VOID {c["selo"].capitalize()}" width="200" height="200">'
    topo = ""
    if c.get("talks"):
        topo = ('<div class="cc-coass"><img src="assets/brand/svg/void-horizontal-branco.svg" alt="The VOID Tattoo" width="600" height="91">'
                '<span class="cc-coass-fio" aria-hidden="true"></span><span class="cc-coass-nome">TALKS</span></div>')
    else:
        topo = '<p class="cc-marcador"><span data-vforms="marcador-estacao" data-vforms-opts=\'{"tamanho":28}\'></span><span>THE VOID START</span></p>'
    foto = ""
    if c.get("foto"):
        foto = f'<div class="cc-foto" role="img" aria-label="Lugar da foto oficial do rito">{ic("image")}<span>Foto real da escola, com autorização</span></div>'
    mapa = ""
    if c.get("mapa"):
        mapa = '<div class="cc-mapa" data-vforms="mapa-trilha" data-vforms-opts=\'{"ativa":"start","orientacao":"horizontal","frases":false,"voceEstaAqui":true}\'></div>'
    off = f'<p class="cc-off">{e(c["off"])}</p>' if c.get("off") else ""
    linhas = "".join(f'<li>{ic(i)}<span>{e(t)}</span></li>' for i, t in c["linhas"])
    linhas = f'<ul class="cc-linhas">{linhas}</ul>' if linhas else ""
    etapas = " ".join(c["etapas"])
    tags = "".join(f'<span class="tag">{x.upper()}</span>' for x in c["etapas"])
    pend = f'<p class="pendencia" data-p="{c["pend"]}">{ic("circle-dashed", " ic-16")}<span>[P {c["pend"]}] {e(c["nota"])}</span></p>' if c.get("pend") else f'<p class="cc-nota">{e(c["nota"])}</p>'
    return f'''
      <figure class="cc" id="{c["id"]}" data-etapa="{etapas}">
        <div class="peca" data-formato="1080x1350" data-estacao="{c["estacao"]}">
          <div class="peca-tela grao">
            <div class="cc-topo">{topo}{selo}</div>
            {foto}{mapa}
            <div class="cc-meio">
              <p class="cc-titulo">{c["titulo"]}</p>
              {off}
              {linhas}
            </div>
            <p class="cc-rodape" aria-label="TATTOO ACADEMY, ® 2025, SÃO PAULO, BRAZIL, PREENCHA O VAZIO"><span>TATTOO ACADEMY<i>·</i></span><span>® 2025<i>·</i></span><span>SÃO PAULO<i>·</i></span><span>BRAZIL<i>·</i></span><b>PREENCHA O VAZIO</b></p>
          </div>
        </div>
        <figcaption><p class="cc-nome">{e(c["nome"])}</p><p class="modelo-tags">{tags}</p>{pend}</figcaption>
      </figure>'''


VARIAVEIS = [
    ("{nome}", "Primeiro nome da pessoa, como ela escreveu."),
    ("{consultor} · {professor} · {assinatura}", "Pessoa real, com nome e cargo. Nunca \"Equipe The VOID\" sozinha."),
    ("{produto}", "The VOID Start, The VOID Master ou The VOID Pro; no texto corrido, \"formação Start\"."),
    ("{data_turma} · {mes_turma} · {data_fechamento} · {proxima_turma}", "Calendário real de turmas [P 15]. Sem data real, a mensagem não sai."),
    ("{valor_total} · {parcelamento} · {condicao_pagamento} · {itens_incluidos}", "Iguais ao checkout, com valor total e parcelas [P 15]."),
    ("{endereco}", "Bloco NAP canônico: Rua Jericó, 217 · Vila Madalena · São Paulo, SP. Copiar, nunca redigitar."),
    ("{link_whatsapp}", "WhatsApp oficial do produto [P 8]."),
    ("{nome_depoente} · {ocupacao_anterior}", "Depoimento real, autorizado e arquivado. Sem ele, a mensagem não sai."),
    ("{convidado_talk} · {data_talk}", "Convidado confirmado e data marcada do The VOID Talks."),
    ("{data_aula} · {proxima_data_aula} · {como_chegar} · {link_calendario}", "Calendário real das aulas experimentais e instrução de chegada escrita pela recepção. Duração e roteiro da aula ficam fora até a escola confirmar [P 16]."),
    ("{itens_de_encerramento}", "Como a formação termina, copiado da Ficha da Formação do produto. Start: 4 tatuagens em pele humana ao longo do curso e a festa de formatura (página oficial do Start). Master e Pro: a confirmar [P 15]. Certificado só com a frase validada [P 20]."),
    ("{mes_conversa}", "Mês da última conversa registrada no CRM. Reativação só para quem aceitou receber contato."),
]

REGRAS_CANAL = [
    ("whatsapp", "Uma ideia por mensagem, \"você\" direto, contrações naturais, sem caixa alta. Negrito (*assim*) só em data, hora e endereço. A pergunta ou o link sozinho na última linha. Quem abre a conversa se apresenta pelo nome. Nenhum emoji de M1 a M4; no máximo um, no fim, em mensagem de marco (M6 a M8), nunca no lugar de palavra."),
    ("email", "Assunto até 45 caracteres e pré-cabeçalho até 80, sem caixa alta inteira e sem emoji no lugar de palavra. \"Oi, {nome}.\" e a ideia numa frase; até três parágrafos; uma prova no máximo, com crédito. Botão reto com o mesmo link em texto logo abaixo. Pessoa real assina. Tagline só na boas-vindas da matrícula e na Formatura com Pele."),
    ("dm", "Conversa, não vitrine: uma pergunta por mensagem, sem oferta e sem link na primeira resposta. Pedido de repostagem sempre com a saída \"se não quiser, tudo bem\"."),
    ("reels", "Gancho na falsa convicção nos 2 s iniciais, Título de Filme com até 6 palavras por tela, legenda queimada em todo vídeo e transcrição no post. No story, conteúdo entre y = 270 e y = 1500. Número só com Crédito de Prova; depoimento com o aviso de resultado."),
    ("anuncio", "Objetivo e provocador, com a mesma promessa da página ou da conversa de destino. Do anúncio à página: o título da peça repete a promessa da primeira dobra, e o pedido do anúncio é o rótulo do botão da página (campo Rótulo na página). Texto principal com a ideia inteira na primeira linha (até 125 caracteres, o que aparece antes do \"ver mais\"), título até 40, descrição até 30; o build para se passar. Botão da plataforma nunca em inglês. Sem promessa de renda, sem antes e depois lado a lado, sem presumir renda, dívida ou saúde de quem lê. Público de 18 anos ou mais. Quem já tem conversa marcada, proposta aberta ou matrícula sai do público (M3 em diante)."),
    ("pesquisa", "Anúncio responsivo de pesquisa do Google: 15 títulos de até 30 caracteres e 4 descrições de até 90, contados no build. Cada título funciona sozinho e combinado com qualquer outro; número só o que a página de destino publica, com a mesma redação. Nada de superlativo, de selo de órgão público ou de contagem de alunos (lista vetada da seção 33 do manual). Uma página de destino por grupo de anúncios, com o mesmo rótulo de botão. Serve M1 (aula experimental) e M2 (escola e curso)."),
]

RITOS = [
    ("M6 · primeiro dia", "Ritual do Traço", "Todo mundo começa com um traço. Aqui, ele tem nome, coragem e história."),
    ("M6 · a primeira tatuagem", "Primeira Pele", "Você nunca esquece sua primeira pele. Aqui, ela é celebrada."),
    ("M7 · meio da formação", "Workshop do Estilo", "O espaço para sair do mais do mesmo."),
    ("M7 · fim da formação", "Formatura com Pele", "Você não sai apenas com um certificado. Sai com um novo capítulo na pele."),
    ("M8 · comunidade", "The VOID Talks", "Da sala pra cena. A Void conecta você com quem vive disso."),
    ("M8 · comunidade", "Ex-alunos mentores", "Aqui, pertencer é para sempre."),
]
RITOS_PROPOSTOS = ["Pergunta do Vazio", "Primeiro Toque", "Convite ao Traço", "Passagem de Trilha", "padrinho ou madrinha de turma", "Mural do Vazio", "o mural do Ritual do Traço"]


CSS = r'''
:root{--topo-h:64px;--pad-x:var(--e-8);scroll-padding-top:calc(var(--topo-h) + var(--e-4))}
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;text-size-adjust:100%}
body{background:var(--sala);min-height:100vh;overflow-wrap:break-word}
body.grao::after{position:fixed;z-index:0}
::selection{background:var(--areia);color:var(--sala)}
h1,h2,h3,h4,p,figure,ul,ol,dl,dd{margin:0}
ul,ol{padding:0;list-style:none}
button{font:inherit;color:inherit}
b,strong{font-weight:600;color:var(--tela)}
a{color:var(--estacao-destaque);text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:3px}
a:hover{color:var(--tela)}
.so-leitor{position:absolute!important;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}
.pular{position:fixed;left:var(--e-4);top:var(--e-2);z-index:60;padding:var(--e-3) var(--e-4);background:var(--tela);color:var(--sala);transform:translateY(-200%)}
.pular:focus{transform:none}
.ic{width:20px;height:20px;flex:none;fill:none;stroke:currentColor;stroke-width:1.5;stroke-linecap:square;stroke-linejoin:miter}
.ic-16{width:16px;height:16px}
.ic-cheio{fill:currentColor;stroke:none}
.wrap{position:relative;z-index:2;max-width:calc(var(--conteudo) + 2 * var(--pad-x));margin:0 auto;padding:0 var(--pad-x)}

/* topo */
.topo{position:fixed;inset:0 0 auto 0;z-index:40;height:var(--topo-h);display:flex;align-items:center;gap:var(--e-5);padding:0 var(--e-5);background:var(--sala);border-bottom:1px solid var(--fio)}
.topo-marca{display:flex;align-items:center;min-height:var(--alvo-toque)}
.topo-marca img{display:block;width:158px;height:24px}
.topo-nome{padding-left:var(--e-5);border-left:1px solid var(--fio);line-height:24px;color:var(--cal)}
.topo-links{margin-left:auto;display:flex;gap:var(--e-2)}
.topo-links a{display:inline-flex;align-items:center;gap:var(--e-2);min-height:var(--alvo-toque);padding:0 var(--e-3);border:1px solid var(--fio);color:var(--cal);text-decoration:none;font:500 12px/1 var(--font-letreiro);font-variation-settings:"wdth" 125;letter-spacing:.18em;text-transform:uppercase}
.topo-links a:hover{border-color:var(--fumaca);color:var(--tela)}
.topo-links a[data-ativo="sim"]{border-color:var(--areia);color:var(--tela)}

/* abertura */
.abertura{position:relative;overflow:hidden;padding:calc(var(--topo-h) + var(--e-10)) 0 var(--e-9)}
.abertura>.janela-luz{position:absolute;inset:0;z-index:0}
.abertura-grade{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);gap:var(--e-8);align-items:end}
.sobre{display:flex;align-items:center;gap:var(--e-3);margin-bottom:var(--e-6)}
.abertura h1{max-width:12ch}
.apoio{max-width:var(--coluna-leitura);margin-top:var(--e-5);font-size:var(--fs-chamada);line-height:1.5;color:var(--cal)}
.resumo{border-left:2px solid var(--areia);background:var(--bastidor);padding:var(--e-6)}
.resumo ul{display:grid;gap:var(--e-3);margin-top:var(--e-4)}
.resumo li{position:relative;padding-left:var(--e-5);font-size:var(--fs-apoio);line-height:1.5}
.resumo li::before{content:"";position:absolute;left:0;top:.6em;width:8px;height:8px;background:var(--areia)}
.legenda-status{display:flex;flex-wrap:wrap;gap:var(--e-3) var(--e-5);margin-top:var(--e-7);padding-top:var(--e-5);border-top:1px solid var(--fio)}
.legenda-status p{display:flex;align-items:center;gap:var(--e-3);font-size:var(--fs-apoio);color:var(--po)}

/* status e etiquetas */
.status{display:inline-flex;align-items:center;gap:6px;padding:4px 8px;border:1px solid var(--fio);font:500 11px/1.2 var(--font-letreiro);font-variation-settings:"wdth" 125;letter-spacing:.14em;text-transform:uppercase;color:var(--po);white-space:nowrap}
.status[data-status="decidido"]{color:var(--sucesso);border-color:var(--sucesso)}
.status[data-status="proposta"]{color:var(--info);border-color:var(--fumaca)}
.status[data-status="pendente"]{color:var(--atencao);border-color:var(--atencao)}
.tag{display:inline-flex;align-items:center;padding:3px 8px;background:var(--coxia);font:500 11px/1.3 var(--font-letreiro);font-variation-settings:"wdth" 112;letter-spacing:.1em;text-transform:uppercase;color:var(--cal)}
.tag-persona{color:var(--tela)}
.tag-frente{background:transparent;border:1px solid var(--estacao-destaque);color:var(--estacao-destaque)}
.var{color:var(--areia);font-weight:600}

/* filtros */
.filtros{position:relative;z-index:30;background:var(--sala);border-top:1px solid var(--fio);border-bottom:1px solid var(--fio)}
.filtros .wrap{display:grid;grid-template-columns:auto 1fr;gap:var(--e-3) var(--e-5);padding-top:var(--e-4);padding-bottom:var(--e-4);align-items:center}
.filtro-rot{display:flex;align-items:center;gap:var(--e-2);margin:0}
.chips{display:flex;flex-wrap:wrap;gap:var(--e-2)}
.chip{min-height:var(--alvo-toque);min-width:var(--alvo-toque);padding:0 var(--e-4);border:1px solid var(--fio);background:transparent;cursor:pointer;font:600 13px/1 var(--font-letreiro);font-variation-settings:"wdth" 106;letter-spacing:.06em;text-transform:uppercase;color:var(--cal);transition:border-color var(--t-micro) var(--curva-cena),background var(--t-micro) var(--curva-cena)}
.chip:hover{border-color:var(--fumaca);color:var(--tela)}
.chip[aria-pressed="true"]{background:var(--coxia);border-color:var(--areia);color:var(--tela);box-shadow:inset 0 -2px 0 var(--areia)}
.contador{grid-column:2;display:flex;align-items:center;gap:var(--e-3);font-size:var(--fs-apoio);color:var(--po)}
.limpar{min-height:var(--alvo-toque);padding:0 var(--e-3);border:0;background:none;color:var(--areia);cursor:pointer;text-decoration:underline;text-underline-offset:3px}

/* seções */
.parte{position:relative;padding:var(--e-10) 0 0}
.parte-cab{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:var(--e-8);align-items:end;margin-bottom:var(--e-8)}
.parte-n{color:var(--areia);margin-bottom:var(--e-3)}
.parte-cab p.apoio-parte{font-size:var(--fs-apoio);line-height:1.6;color:var(--po);max-width:56ch}

/* matriz */
.matriz{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1px;background:var(--fio);border:1px solid var(--fio)}
.matriz-cartao{display:flex;flex-direction:column;gap:var(--e-4);padding:var(--e-5);background:var(--sala);min-width:0}
.matriz-cartao[hidden]{display:none}
.matriz-m{color:var(--fumaca);font-size:56px}
.matriz-nome{font:700 22px/1.1 var(--font-letreiro);font-variation-settings:"wdth" 100;text-transform:uppercase;letter-spacing:-.005em;color:var(--tela)}
.matriz-crenca{font:600 18px/1.3 var(--font-letreiro);color:var(--cal)}
.matriz-dl{display:grid;gap:var(--e-3)}
.matriz-dl dt{font:500 11px/1.3 var(--font-letreiro);font-variation-settings:"wdth" 125;letter-spacing:.16em;text-transform:uppercase;color:var(--po)}
.matriz-dl dd{font-size:var(--fs-apoio);line-height:1.45;color:var(--cal)}
.matriz-cta{display:grid;gap:var(--e-2);margin-top:auto;padding-top:var(--e-4);border-top:1px solid var(--fio)}
.matriz-nota{font-size:13px;line-height:1.4;color:var(--po)}
.matriz-ir{display:inline-flex;align-items:center;gap:var(--e-2);min-height:var(--alvo-toque);color:var(--areia);font-size:var(--fs-apoio)}
.rotulo-cta{display:inline-flex;align-items:center;min-height:40px;padding:8px 12px;border:1px solid var(--fumaca);font:700 13px/1.25 var(--font-letreiro);font-variation-settings:"wdth" 106;letter-spacing:.06em;text-transform:uppercase;color:var(--tela)}

/* personas */
.personas{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:var(--e-5)}
.persona{display:flex;flex-direction:column;gap:var(--e-4);padding:var(--e-5);background:var(--bastidor);border-top:2px solid var(--fio);transition:background var(--t-ui) var(--curva-cena)}
.persona header{display:grid;gap:var(--e-2);justify-items:start}
.persona-nome{font:700 28px/1 var(--font-letreiro);font-variation-settings:"wdth" 100;text-transform:uppercase;color:var(--tela)}
.persona-conv{font:600 19px/1.3 var(--font-letreiro);color:var(--cal)}
.persona-tom{font-size:var(--fs-apoio);line-height:1.5;color:var(--po)}
.persona-hero{font:800 24px/.98 var(--font-letreiro);font-variation-settings:"wdth" 100;text-transform:uppercase;letter-spacing:-.012em;color:var(--tela);padding-top:var(--e-4);border-top:1px solid var(--fio)}
.persona-frase{font-family:var(--font-off);font-style:italic;font-weight:300;font-variation-settings:"opsz" 72;font-size:28px;line-height:1.1;color:var(--nevoa);padding-top:var(--e-4);border-top:1px solid var(--fio)}
.persona-ativa{display:inline-flex;align-items:center;gap:6px;color:var(--areia)}
.persona-ativa[hidden]{display:none}
.persona-nota{font-size:13px;line-height:1.45;color:var(--po)}
body[data-persona="gabriel"] .persona[data-persona="gabriel"],body[data-persona="camila"] .persona[data-persona="camila"],body[data-persona="bruno"] .persona[data-persona="bruno"],body[data-persona="sylvia"] .persona[data-persona="sylvia"]{border-top-color:var(--areia);background:var(--coxia)}

/* etapas e modelos */
.etapa{padding:var(--e-9) 0 0;border-top:1px solid var(--fio);margin-top:var(--e-9)}
.etapa:first-of-type{margin-top:0}
.etapa[hidden]{display:none}
.etapa-cab{display:grid;grid-template-columns:auto minmax(0,1fr) minmax(0,320px);gap:var(--e-6);align-items:start;margin-bottom:var(--e-7)}
.etapa-num{color:var(--fumaca)}
.etapa-sobre{margin-bottom:var(--e-3)}
.etapa-titulo{font:700 clamp(34px,4.4vw,56px)/.98 var(--font-letreiro);font-variation-settings:"wdth" 100;text-transform:uppercase;letter-spacing:-.012em;color:var(--tela)}
.etapa-crenca{margin-top:var(--e-4);font:600 22px/1.25 var(--font-letreiro);color:var(--cal)}
.etapa-guia{margin-top:var(--e-3);font-size:var(--fs-apoio);line-height:1.55;color:var(--po);max-width:60ch}
.etapa-cta{display:grid;gap:var(--e-3);padding:var(--e-5);background:var(--bastidor);border-left:2px solid var(--areia)}
.frentes{display:grid;gap:var(--e-3)}
.frentes p{display:grid;gap:6px}
.modelos{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,400px),1fr));gap:var(--e-5);align-items:start}
.modelo{display:flex;flex-direction:column;gap:var(--e-4);padding:var(--e-5);background:var(--bastidor);border:1px solid var(--fio);min-width:0}
.modelo[hidden]{display:none}
.modelo-cab{display:flex;justify-content:space-between;align-items:center;gap:var(--e-3);flex-wrap:wrap}
.modelo-canal{display:flex;align-items:center;gap:var(--e-2);color:var(--cal)}
.modelo-titulo{font:600 20px/1.25 var(--font-letreiro);font-variation-settings:"wdth" 100;color:var(--tela)}
.modelo-tags{display:flex;flex-wrap:wrap;gap:6px}
.msg{white-space:pre-wrap;font-size:16px;line-height:1.55;color:var(--cal)}
.balao{padding:var(--e-4);background:var(--coxia);border-left:2px solid var(--fumaca)}
.balao-zap{border-left-color:var(--po)}
.email-cab{display:grid;gap:var(--e-2);padding-bottom:var(--e-3);border-bottom:1px solid var(--fio);margin-bottom:var(--e-3)}
.email-cab div{display:grid;grid-template-columns:110px minmax(0,1fr);gap:var(--e-3)}
.email-cab dt{font:500 11px/1.6 var(--font-letreiro);font-variation-settings:"wdth" 125;letter-spacing:.14em;text-transform:uppercase;color:var(--po)}
.email-cab dd{font-size:15px;line-height:1.45;color:var(--tela)}
.conta{display:inline-block;margin-left:var(--e-2);font-size:12px;color:var(--sucesso)}
.conta[data-ok="false"]{color:var(--erro)}
.email-corpo{padding:var(--e-4);background:var(--coxia)}
.roteiro{display:grid;gap:1px;background:var(--fio)}
.roteiro li{display:grid;grid-template-columns:84px minmax(0,1fr);gap:var(--e-3);padding:var(--e-3) var(--e-4);background:var(--coxia)}
.tela-tempo{padding-top:3px}
.tela-titulo{display:block;font:800 22px/.98 var(--font-letreiro);font-variation-settings:"wdth" 100;text-transform:uppercase;letter-spacing:-.01em;color:var(--tela);margin-bottom:6px}
.tela-fala{font-size:15px;line-height:1.5;color:var(--cal)}
.legenda-post{margin-top:var(--e-3);display:grid;gap:var(--e-2);padding:var(--e-4);border:1px dashed var(--fio)}
.ficha-anuncio{display:grid;gap:1px;background:var(--fio)}
.lista-pesquisa{display:grid;gap:6px;margin:0;padding:0 0 0 1.6em;list-style:decimal;color:var(--po);font-size:14px}
.lista-pesquisa li{padding-left:4px}
.lista-pesquisa .msg{color:var(--tela)}
.ficha-anuncio .conta{white-space:nowrap}
.ficha-anuncio div{display:grid;grid-template-columns:140px minmax(0,1fr);gap:var(--e-3);padding:var(--e-3) var(--e-4);background:var(--coxia)}
.ficha-anuncio dt{font:500 11px/1.5 var(--font-letreiro);font-variation-settings:"wdth" 125;letter-spacing:.14em;text-transform:uppercase;color:var(--po)}
.cta-linha{display:flex;align-items:center;gap:var(--e-2);flex-wrap:wrap;font:500 11px/1.3 var(--font-letreiro);font-variation-settings:"wdth" 125;letter-spacing:.14em;text-transform:uppercase;color:var(--po)}
.cta-linha b{font:700 13px/1.25 var(--font-letreiro);font-variation-settings:"wdth" 106;letter-spacing:.06em;color:var(--areia)}
.cta-nenhum{color:var(--po)}
.porque{font-size:var(--fs-apoio);line-height:1.5;color:var(--po)}
.nota-modelo{display:flex;gap:var(--e-2);align-items:flex-start;font-size:14px;line-height:1.45;color:var(--atencao)}
.modelo-acoes{margin-top:auto;padding-top:var(--e-2)}
.copiar{display:inline-flex;align-items:center;gap:var(--e-2);min-height:var(--alvo-toque);padding:0 var(--e-4);border:1px solid var(--fumaca);background:transparent;cursor:pointer;font:700 13px/1 var(--font-letreiro);font-variation-settings:"wdth" 106;letter-spacing:.06em;text-transform:uppercase;color:var(--tela);transition:border-color var(--t-micro) var(--curva-cena),background var(--t-micro) var(--curva-cena)}
.copiar:hover{border-color:var(--tela);background:var(--coxia)}
.copiar[data-feito="sim"]{border-color:var(--sucesso);color:var(--sucesso)}
.vazio-filtro[hidden]{display:none}
.vazio-filtro{display:flex;align-items:center;gap:var(--e-3);padding:var(--e-5);border:1px dashed var(--fio);font-size:var(--fs-apoio);color:var(--po)}
.etapa-pe{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr));gap:var(--e-5);margin-top:var(--e-5)}
.fora,.nunca{padding:var(--e-5);border:1px solid var(--fio)}
.fora ul,.nunca ul{display:grid;gap:var(--e-2);margin-top:var(--e-3)}
.fora li,.nunca li{font-size:var(--fs-apoio);line-height:1.5}
.fora .credito,.nunca .credito{display:flex;align-items:center;gap:var(--e-2)}
.nunca{border-color:var(--erro)}
.nunca .credito{color:var(--erro)}
.nunca li{color:var(--po)}

/* cartões de conversa */
.cartoes{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,340px),1fr));gap:var(--e-6) var(--e-5)}
.cc[hidden]{display:none}
.cc figcaption{display:grid;gap:var(--e-2);margin-top:var(--e-4)}
.cc-nome{font:600 20px/1.2 var(--font-letreiro);color:var(--tela)}
.cc-nota{font-size:14px;line-height:1.45;color:var(--po)}
.peca{position:relative;container-type:inline-size;aspect-ratio:1080/1350;overflow:hidden;background:var(--sala);border:1px solid var(--fio)}
.peca-tela{--u:calc(100cqw / 1080);position:absolute;inset:0;display:flex;flex-direction:column;padding:calc(var(--u) * 72);background:radial-gradient(110% 75% at 12% 0%,rgb(248 249 244 / .09) 0%,rgb(248 249 244 / 0) 62%),var(--sala)}
.peca-tela>*{position:relative;z-index:2}
.cc-topo{display:flex;justify-content:space-between;align-items:flex-start;gap:calc(var(--u) * 24);min-height:calc(var(--u) * 200)}
.cc-marcador{display:flex;align-items:center;gap:calc(var(--u) * 16);font:500 calc(var(--u) * 26)/1.2 var(--font-letreiro);font-variation-settings:"wdth" 125;letter-spacing:.18em;color:var(--po)}
.cc-marcador svg{width:calc(var(--u) * 28)!important;height:calc(var(--u) * 28)!important}
.cc-selo{width:calc(var(--u) * 200);height:calc(var(--u) * 200);flex:none}
.cc-coass{display:flex;align-items:center;gap:calc(var(--u) * 64)}
.cc-coass img{width:calc(var(--u) * 600);height:auto}
.cc-coass-fio{width:max(1px,calc(var(--u) * 2));height:calc(var(--u) * 87);background:var(--tela)}
.cc-coass-nome{font:700 calc(var(--u) * 42)/1 var(--font-letreiro);font-variation-settings:"wdth" 112;letter-spacing:.04em;color:var(--tela)}
.cc-foto{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:calc(var(--u) * 16);height:calc(var(--u) * 420);margin-top:calc(var(--u) * 24);border:1px dashed var(--fumaca);background:var(--bastidor);color:var(--po);font:500 calc(var(--u) * 26)/1.3 var(--font-letreiro);font-variation-settings:"wdth" 125;letter-spacing:.1em;text-transform:uppercase;text-align:center;padding:0 calc(var(--u) * 48)}
.cc-foto svg{width:calc(var(--u) * 64);height:calc(var(--u) * 64)}
.cc-mapa{margin-top:calc(var(--u) * 24)}
.cc-mapa .vf-mapa{margin:0}
.cc-meio{margin-top:auto;display:grid;gap:calc(var(--u) * 32)}
.cc-titulo{font:800 calc(var(--u) * 112)/.92 var(--font-letreiro);font-variation-settings:"wdth" 100;text-transform:uppercase;letter-spacing:-.02em;color:var(--tela)}
.cc-titulo .off{font-size:1.2em;line-height:.8}
.cc-off{font-family:var(--font-off);font-style:italic;font-weight:300;font-variation-settings:"opsz" 72;font-size:calc(var(--u) * 60);line-height:1.05;color:var(--estacao-destaque)}
.cc-linhas{display:grid;gap:calc(var(--u) * 14);padding-top:calc(var(--u) * 28);border-top:1px solid var(--fio)}
.cc-linhas li{display:flex;align-items:center;gap:calc(var(--u) * 20);font:500 calc(var(--u) * 40)/1.15 var(--font-letreiro);font-variation-settings:"wdth" 100;text-transform:uppercase;color:var(--cal)}
.cc-linhas svg{width:calc(var(--u) * 40);height:calc(var(--u) * 40);color:var(--estacao-destaque)}
.cc-rodape{display:flex;flex-wrap:wrap;row-gap:calc(var(--u) * 10);margin-top:calc(var(--u) * 40);font:500 calc(var(--u) * 26)/1.2 var(--font-letreiro);font-variation-settings:"wdth" 125;letter-spacing:.18em;color:var(--po)}
.cc-rodape>span,.cc-rodape>b{white-space:nowrap}
.cc-rodape i{font-style:normal;margin:0 .9em}
.cc-rodape b{font-weight:700;color:var(--tela)}

/* ritos, regras, variáveis */
.duas{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:var(--e-6)}
.ritos{display:grid;gap:1px;background:var(--fio);border:1px solid var(--fio)}
.ritos li{display:grid;grid-template-columns:180px minmax(0,1fr);gap:var(--e-4);padding:var(--e-4) var(--e-5);background:var(--sala)}
.ritos b{display:block;font:700 18px/1.2 var(--font-letreiro);text-transform:uppercase;letter-spacing:.01em}
.ritos .voz{font-family:var(--font-off);font-style:italic;font-weight:300;font-variation-settings:"opsz" 72;font-size:22px;line-height:1.2;color:var(--areia);margin-top:6px}
.pendencia{display:flex;gap:var(--e-3);align-items:flex-start;padding:var(--e-4);border:1px dashed var(--atencao);font-size:var(--fs-apoio);line-height:1.5;color:var(--cal)}
.pendencia .ic{color:var(--atencao);margin-top:2px}
.propostos{display:grid;grid-template-columns:minmax(0,1fr);gap:var(--e-4);padding:var(--e-5);border:1px dashed var(--atencao);align-content:start;align-self:start}
.propostos>.status{justify-self:start;white-space:normal;max-width:100%}
.propostos ul{display:flex;flex-wrap:wrap;gap:var(--e-2)}
.propostos li{padding:4px 10px;border:1px dashed var(--fumaca);font-size:14px;color:var(--po)}
.regras{display:grid;gap:1px;background:var(--fio);border:1px solid var(--fio)}
.regras li{display:grid;grid-template-columns:200px minmax(0,1fr);gap:var(--e-5);padding:var(--e-5);background:var(--sala)}
.regras .credito{display:flex;align-items:center;gap:var(--e-2);color:var(--cal)}
.regras p{font-size:var(--fs-apoio);line-height:1.6}
.variaveis{display:grid;gap:1px;background:var(--fio);border:1px solid var(--fio)}
.variaveis div{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.3fr);gap:var(--e-4);padding:var(--e-3) var(--e-5);background:var(--sala)}
.variaveis dt{font:600 14px/1.5 ui-monospace,"SF Mono",Menlo,monospace;color:var(--areia);overflow-wrap:anywhere}
.variaveis dd{font-size:var(--fs-apoio);line-height:1.5}

/* fecho */
.fecho{margin-top:var(--e-10);padding:var(--e-9) 0 var(--e-8);border-top:1px solid var(--fio)}
.fecho .vf-termo{white-space:nowrap}
.fecho-links{display:flex;flex-wrap:wrap;gap:var(--e-2) var(--e-5);margin-bottom:var(--e-6)}
.fecho-links a{display:inline-flex;align-items:center;min-height:var(--alvo-toque)}
.fecho .fontes{margin-top:var(--e-6);max-width:80ch;text-transform:none;letter-spacing:.02em;font:400 13px/1.6 var(--font-texto);color:var(--po)}
.aviso-vivo{position:fixed;left:50%;bottom:var(--e-5);z-index:50;transform:translateX(-50%);padding:var(--e-3) var(--e-4);background:var(--tela);color:var(--sala);font:600 14px/1.3 var(--font-letreiro);opacity:0;pointer-events:none;transition:opacity var(--t-ui) var(--curva-cena)}
.aviso-vivo[data-ver="sim"]{opacity:1}

@media (max-width:1100px){
  .matriz{grid-template-columns:repeat(2,minmax(0,1fr))}
  .personas{grid-template-columns:repeat(2,minmax(0,1fr))}
  .etapa-cab{grid-template-columns:auto minmax(0,1fr)}
  .etapa-cta{grid-column:1 / -1}
}
@media (max-width:900px){
  :root{--pad-x:var(--e-6)}
  .abertura-grade,.parte-cab,.duas{grid-template-columns:minmax(0,1fr)}
  .topo-nome{display:none}
}
@media (max-width:640px){
  :root{--pad-x:var(--e-4);--topo-h:56px}
  .topo{padding:0 var(--e-4);gap:var(--e-3)}
  .topo-links a{padding:0 var(--e-2);font-size:11px;letter-spacing:.12em}
  .topo-links a .longo{display:none}
  .abertura{padding:calc(var(--topo-h) + var(--e-8)) 0 var(--e-8)}
  .apoio{font-size:19px}
  .filtros .wrap{grid-template-columns:minmax(0,1fr);gap:var(--e-2)}
  .contador{grid-column:1}
  .matriz,.personas{grid-template-columns:minmax(0,1fr)}
  .etapa-cab{grid-template-columns:minmax(0,1fr);gap:var(--e-4)}
  .etapa-num{font-size:48px}
  .modelo{padding:var(--e-4)}
  .roteiro li,.ficha-anuncio div,.email-cab div,.ritos li,.regras li,.variaveis div{grid-template-columns:minmax(0,1fr);gap:var(--e-2)}
  .parte{padding-top:var(--e-9)}
  .resumo{padding:var(--e-5)}
}
@media (max-width:480px){.topo-links a.so-largo{display:none}}
@media (max-width:360px){.topo{padding:0 var(--e-3);gap:var(--e-2)}.chip{padding:0 var(--e-3)}}
@media print{.topo,.filtros,.copiar,.aviso-vivo{display:none}.abertura{padding-top:var(--e-6)}.modelo,.cc{break-inside:avoid}}
@media (prefers-reduced-motion:reduce){.persona,.chip,.copiar,.aviso-vivo{transition:none}}
'''

JS = r'''
(function(){
  "use strict";
  var corpo=document.body, estado={etapa:"todas",persona:"todas",canal:"todos"};
  var etapas=document.querySelectorAll(".etapa"), modelos=document.querySelectorAll(".modelo"),
      cartoesM=document.querySelectorAll(".matriz-cartao"), cartoesC=document.querySelectorAll(".cc"),
      contador=document.getElementById("contador"), aviso=document.getElementById("aviso-vivo");
  function lerURL(){
    try{var q=new URLSearchParams(location.search);["etapa","persona","canal"].forEach(function(k){var v=q.get(k);if(v)estado[k]=v;});}catch(e){}
  }
  function gravarURL(){
    try{var q=new URLSearchParams();Object.keys(estado).forEach(function(k){if(estado[k]!=="todas"&&estado[k]!=="todos")q.set(k,estado[k]);});
      var s=q.toString();history.replaceState(null,"",location.pathname+(s?"?"+s:"")+location.hash);}catch(e){}
  }
  function aplica(){
    corpo.setAttribute("data-persona",estado.persona);
    document.querySelectorAll("[data-filtro]").forEach(function(b){
      b.setAttribute("aria-pressed",estado[b.getAttribute("data-filtro")]===b.getAttribute("data-valor")?"true":"false");
    });
    document.querySelectorAll(".persona").forEach(function(p){var a=p.querySelector(".persona-ativa");if(a)a.hidden=p.getAttribute("data-persona")!==estado.persona;});
    var vis=0;
    modelos.forEach(function(m){
      var ps=m.getAttribute("data-personas").split(" ");
      var ok=(estado.etapa==="todas"||m.getAttribute("data-etapa")===estado.etapa)&&
             (estado.persona==="todas"||ps.indexOf("todas")>=0||ps.indexOf(estado.persona)>=0)&&
             (estado.canal==="todos"||m.getAttribute("data-canal")===estado.canal);
      m.hidden=!ok; if(ok)vis++;
    });
    etapas.forEach(function(s){
      var id=s.getAttribute("data-etapa");
      s.hidden=!(estado.etapa==="todas"||estado.etapa===id);
      var algum=s.querySelector(".modelo:not([hidden])");
      s.querySelector(".vazio-filtro").hidden=!!algum;
    });
    cartoesM.forEach(function(c){c.hidden=!(estado.etapa==="todas"||c.getAttribute("data-etapa")===estado.etapa);});
    cartoesC.forEach(function(c){c.hidden=!(estado.etapa==="todas"||c.getAttribute("data-etapa").split(" ").indexOf(estado.etapa)>=0);});
    if(contador)contador.textContent="Mostrando "+vis+" de "+modelos.length+" modelos";
    var tf=document.getElementById("topo-filtro-txt");
    if(tf){var partes=[];if(estado.etapa!=="todas")partes.push(estado.etapa.toUpperCase());if(estado.persona!=="todas")partes.push(estado.persona.charAt(0).toUpperCase()+estado.persona.slice(1));
      var nc={whatsapp:"WhatsApp",email:"E-mail",dm:"DM",reels:"Reels",anuncio:"Anúncio",pesquisa:"Pesquisa"};if(estado.canal!=="todos")partes.push(nc[estado.canal]);
      tf.textContent=partes.length?": "+partes.join(" · "):"";var lk=tf.closest("a");if(lk)lk.setAttribute("data-ativo",partes.length?"sim":"nao");}
    gravarURL();
  }
  document.addEventListener("click",function(ev){
    var b=ev.target.closest("[data-filtro]");
    if(b){estado[b.getAttribute("data-filtro")]=b.getAttribute("data-valor");aplica();return;}
    if(ev.target.closest("[data-limpar]")){estado={etapa:"todas",persona:"todas",canal:"todos"};aplica();return;}
    var c=ev.target.closest("[data-copiar]");
    if(c){
      var fonte=document.getElementById(c.getAttribute("data-copiar")); if(!fonte)return;
      var txt=fonte.value, rot=c.querySelector("span");
      var feito=function(){c.setAttribute("data-feito","sim");rot.textContent="Copiado";anuncia("Mensagem copiada.");
        setTimeout(function(){c.removeAttribute("data-feito");rot.textContent="Copiar mensagem";},2000);};
      var reserva=function(){var t=document.createElement("textarea");t.value=txt;t.setAttribute("readonly","");t.style.position="fixed";t.style.left="-9999px";
        document.body.appendChild(t);t.select();try{document.execCommand("copy");feito();}catch(e){anuncia("Não deu certo. Selecione o texto e copie.");}document.body.removeChild(t);};
      if(navigator.clipboard&&window.isSecureContext){navigator.clipboard.writeText(txt).then(feito,reserva);}else{reserva();}
    }
  });
  var tAviso=0;
  function anuncia(t){if(!aviso)return;aviso.textContent=t;aviso.setAttribute("data-ver","sim");clearTimeout(tAviso);tAviso=setTimeout(function(){aviso.removeAttribute("data-ver");},1800);}
  lerURL(); aplica();
  window.ComunicacaoM1M8={estado:estado,aplica:aplica};
})();
'''


def chips(filtro, opcoes):
    return "".join(
        f'<button class="chip" type="button" data-filtro="{filtro}" data-valor="{v}" aria-pressed="false">{e(r)}</button>'
        for v, r in opcoes)


def pagina():
    etapas_html = "".join(bloco_etapa(et, i) for i, et in enumerate(ETAPAS))
    matriz_html = "".join(cartao_matriz(et) for et in ETAPAS)
    personas_html = "".join(cartao_persona(p) for p in PERSONAS)
    cartoes_html = "".join(cartao_conversa(c) for c in CARTOES)
    ritos_html = "".join(f'<li><p class="credito">{e(a)}</p><div><b>{e(b)}</b><p class="voz">{e(c)}</p></div></li>' for a, b, c in RITOS)
    propostos_html = "".join(f"<li>{e(r)}</li>" for r in RITOS_PROPOSTOS)
    regras_html = "".join(f'<li><p class="credito">{ic(CANAIS[c][1])}<span>{e(CANAIS[c][0])}</span></p><p>{com_variaveis(t)}</p></li>' for c, t in REGRAS_CANAL)
    vars_html = "".join(f'<div><dt>{e(a)}</dt><dd>{e(b)}</dd></div>' for a, b in VARIAVEIS)
    n_modelos = len(MODELOS)
    status_leg = "".join(
        f'<p><span class="status" data-status="{k}">{ic(v[1], " ic-16")}{v[0]}</span><span>{e(v[2])}</span></p>' for k, v in STATUS.items())
    chips_etapa = chips("etapa", [("todas", "Todas")] + [(et["id"], et["id"].upper()) for et in ETAPAS])
    chips_persona = chips("persona", [("todas", "Todas")] + [(p["id"], p["nome"]) for p in PERSONAS])
    chips_canal = chips("canal", [("todos", "Todos")] + [(k, v[0]) for k, v in CANAIS.items()])

    return f'''<!DOCTYPE html>
<html lang="pt-BR" data-estacao="chamado">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The VOID · Comunicação M1 a M8</title>
<meta name="description" content="Matriz de comunicação M1 a M8 da The VOID Tattoo Academy (sistema Sala Escura v1): crença, atributo, recurso, CTA e métrica de cada etapa, modelos de WhatsApp, e-mail, DM, Reels e anúncio filtráveis por etapa, persona e canal, e os Cartões de Conversa.">
<meta name="theme-color" content="#181818">
<meta name="color-scheme" content="dark">
<meta name="robots" content="noindex">
<link rel="icon" href="assets/brand/favicon/favicon.svg" type="image/svg+xml">
<link rel="icon" href="assets/brand/favicon/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="assets/brand/favicon/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&family=Newsreader:ital,opsz,wght@1,6..72,300&family=Nunito+Sans:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="tokens.css">
<style>
/* =====================================================================
   THE VOID · COMUNICAÇÃO M1 A M8 (comunicacao-m1-m8.html) · sistema Sala Escura v1
   Gerado por tools/gerar_comunicacao_m1_m8.py: edite os dados lá, não aqui.
   Valores: tokens.css. Regras: especificação Sala Escura, seções 9, 10, 11, 12.5 e 12.6.
   ===================================================================== */
{CSS}
</style>
</head>
<body class="grao" data-persona="todas">
<a class="pular" href="#conteudo">Pular para o conteúdo</a>
<header class="topo">
  <a class="topo-marca" href="index.html" aria-label="The VOID Tattoo Academy, página de entrada do sistema"><img src="assets/brand/svg/void-horizontal-branco.svg" alt="The VOID Tattoo" width="158" height="24"></a>
  <p class="topo-nome credito">Comunicação M1 a M8</p>
  <nav class="topo-links" aria-label="Outros arquivos do sistema">
    <a class="so-largo" href="brand-book.html#s32">{ic("file-text", " ic-16")}<span>Manual<span class="longo">, seção 32</span></span></a>
    <a class="topo-filtro" href="#filtros">{ic("list-filter", " ic-16")}<span>Filtros<span class="longo" id="topo-filtro-txt"></span></span></a>
    <a class="so-largo" href="lockup.html">{ic("copy", " ic-16")}<span>Trechos</span></a>
  </nav>
</header>

<main id="conteudo">
  <section class="abertura" aria-labelledby="titulo">
    <div class="janela-luz" aria-hidden="true"></div>
    <div class="wrap">
      <p class="sobre credito"><span data-vforms="marcador-estacao"></span><span>Régua de comunicação · Bowtie</span></p>
      <div class="abertura-grade">
        <div>
          <h1 id="titulo" class="titulo-filme">Uma crença, <em class="off">um pedido</em></h1>
          <p class="apoio">Do cadastro à indicação, a pessoa passa por oito etapas. Esta página junta o que dizer em cada uma: a crença que pesa, o único pedido, as mensagens prontas por canal e os Cartões de Conversa.</p>
        </div>
        <div class="resumo">
          <p class="credito">Em um minuto</p>
          <ul>
            <li>Filtre por etapa, persona e canal. O endereço da página guarda o filtro, para mandar o recorte para quem vai escrever.</li>
            <li>Cada mensagem tem no máximo um pedido, e todas as mensagens de uma etapa pedem a mesma coisa. Em M1, um pedido por porta de entrada (conversa, aula experimental ou Talks); em M8, um pedido por frente.</li>
            <li>Variáveis entre chaves, como <span class="var">{{nome}}</span>, saem de fonte real. Sem data, preço ou depoimento validado, a mensagem não sai.</li>
            <li>Ritos propostos durante a pesquisa ficam fora de toda mensagem até a aprovação da The VOID [P 6].</li>
          </ul>
        </div>
      </div>
      <div class="legenda-status">{status_leg}</div>
    </div>
  </section>

  <nav class="filtros" id="filtros" aria-label="Filtrar modelos">
    <div class="wrap">
      <p class="filtro-rot credito" id="f-etapa">{ic("list-filter", " ic-16")}Etapa</p>
      <div class="chips" role="group" aria-labelledby="f-etapa">{chips_etapa}</div>
      <p class="filtro-rot credito" id="f-persona">{ic("user-round", " ic-16")}Persona</p>
      <div class="chips" role="group" aria-labelledby="f-persona">{chips_persona}</div>
      <p class="filtro-rot credito" id="f-canal">{ic("message-circle", " ic-16")}Canal</p>
      <div class="chips" role="group" aria-labelledby="f-canal">{chips_canal}</div>
      <p class="contador"><span id="contador" aria-live="polite">Mostrando {n_modelos} de {n_modelos} modelos</span><button class="limpar" type="button" data-limpar>Limpar filtros</button></p>
    </div>
  </nav>

  <section class="parte" id="matriz" aria-labelledby="matriz-t">
    <div class="wrap">
      <header class="parte-cab">
        <div><p class="parte-n credito">01 · A matriz</p><h2 id="matriz-t" class="titulo-secao">Oito etapas, <em class="off">oito pedidos</em></h2></div>
        <p class="apoio-parte">A crença que pesa em cada etapa, o atributo da voz que sobe, o recurso e o componente que lideram, o CTA e a métrica. É a tabela da seção 10 da especificação, em cartões que seguem o filtro de etapa.</p>
      </header>
      <div class="matriz">{matriz_html}
      </div>
    </div>
  </section>

  <section class="parte" id="personas" aria-labelledby="personas-t">
    <div class="wrap">
      <header class="parte-cab">
        <div><p class="parte-n credito">02 · Para quem</p><h2 id="personas-t" class="titulo-secao">Quatro vozes <em class="off">por dentro</em></h2></div>
        <p class="apoio-parte">Toda mensagem declara com quem fala. Gabriel, Camila e Bruno são as personas canônicas; Sylvia cobre o Pro como subperfil. O filtro de persona acende a pessoa aqui e mostra os modelos dela junto dos que servem a todos.</p>
      </header>
      <div class="personas">{personas_html}
      </div>
    </div>
  </section>

  <section class="parte" id="modelos" aria-labelledby="modelos-t">
    <div class="wrap">
      <header class="parte-cab">
        <div><p class="parte-n credito">03 · Modelos</p><h2 id="modelos-t" class="titulo-secao">O que dizer <em class="off">em cada etapa</em></h2></div>
        <p class="apoio-parte">Cada cartão traz o canal, o momento de envio, a persona, o status, o pedido e o porquê. O botão copia o texto inteiro, com assunto e pré-cabeçalho no e-mail e o roteiro completo nos vídeos.</p>
      </header>
      {etapas_html}
    </div>
  </section>

  <section class="parte" id="cartoes" aria-labelledby="cartoes-t">
    <div class="wrap">
      <header class="parte-cab">
        <div><p class="parte-n credito">04 · Cartões de Conversa</p><h2 id="cartoes-t" class="titulo-secao">O dado vira <em class="off">imagem</em></h2></div>
        <p class="apoio-parte">Peças de 1080 por 1350 em Sala para mandar no WhatsApp junto da mensagem: título de até cinco palavras, até quatro linhas de dado, selo do produto e rodapé-assinatura. Os colchetes são preenchidos com o dado real antes do envio.</p>
      </header>
      <div class="cartoes">{cartoes_html}
      </div>
    </div>
  </section>

  <section class="parte" id="ritos" aria-labelledby="ritos-t">
    <div class="wrap">
      <header class="parte-cab">
        <div><p class="parte-n credito">05 · Ritos na régua</p><h2 id="ritos-t" class="titulo-secao">Só o que <em class="off">existe</em></h2></div>
        <p class="apoio-parte">Os ritos que estão nas fontes da The VOID têm lugar fixo na régua e frase própria. Os que foram propostos durante a pesquisa ficam listados como proposta e não aparecem em nenhuma mensagem desta página.</p>
      </header>
      <div class="duas">
        <ul class="ritos" aria-label="Ritos que existem">{ritos_html}</ul>
        <div class="propostos" data-ritos-propostos data-p="6">
          <span class="status" data-status="pendente">{ic("circle-dashed", " ic-16")}Proposta, fora de uso [P 6]</span>
          <p>Estes nomes foram propostos durante a pesquisa e ainda não existem na The VOID. Não entram em mensagem, peça, página ou área de membros antes da aprovação.</p>
          <ul>{propostos_html}</ul>
          <p class="pendencia" data-p="6">{ic("circle-dashed", " ic-16")}<span>[P 6] Também aguardam confirmação: o quinto momento de marca, a existência e o registro do mural do Ritual do Traço e a frequência real do The VOID Talks.</span></p>
        </div>
      </div>
    </div>
  </section>

  <section class="parte" id="regras" aria-labelledby="regras-t">
    <div class="wrap">
      <header class="parte-cab">
        <div><p class="parte-n credito">06 · Regras de escrita</p><h2 id="regras-t" class="titulo-secao">Cada canal, <em class="off">um jeito</em></h2></div>
        <p class="apoio-parte">A voz é a mesma em todos os canais; muda o tom. Antes de mandar qualquer mensagem nova, confira as regras do canal e a lista de variáveis.</p>
      </header>
      <ul class="regras">{regras_html}</ul>
      <h3 class="fala" style="margin:var(--e-8) 0 var(--e-5);font-size:var(--fs-inter)">Variáveis e de onde vêm</h3>
      <dl class="variaveis">{vars_html}</dl>
    </div>
  </section>

  <footer class="fecho">
    <div class="wrap">
      <nav class="fecho-links" aria-label="Outros arquivos do sistema"><a href="index.html">Página de entrada</a><a href="brand-book.html#s32">Manual de marca, seção 32</a><a href="lockup.html">Trechos prontos</a></nav>
      <div data-vforms="rodape"></div>
      <p class="fontes">Fontes: especificação do sistema Sala Escura, 06/10/2026 (seções 3.5, 9, 10, 11, 12.5 e 12.6); pesquisa de comunicação M1 a M8 e área de membros, GrowAI, 06/10/2026; Brand DNA da The VOID, set/2026; Personas, set/2026; Plataforma de Branding, aureadesign, 2025 (experiência atual do aluno, momentos de marca e personas da agência). Mensagens com status Proposta aguardam aprovação da The VOID.</p>
    </div>
  </footer>
</main>
<p class="aviso-vivo" id="aviso-vivo" role="status" aria-live="polite"></p>

<script src="vforms.js"></script>
<script>{JS}</script>
</body>
</html>
'''


def conferir_textos_copiaveis():
    """Reprova o build se algum texto copiável levar marcador interno, travessão, claim vetado
    (spec 11.1) ou termo fora do território (spec 9.2), se um campo de anúncio passar do limite
    de caracteres, se a pesquisa do Google não tiver 15 títulos e 4 descrições, ou se uma mensagem
    de etapa com portas ou frentes não declarar a sua."""
    import sys
    sys.path.insert(0, str(RAIZ / "tools"))
    from verificar import CLAIMS, FORA
    erros = []
    ids = [m["id"] for m in MODELOS]
    for d in sorted({i for i in ids if ids.count(i) > 1}):
        erros.append(f"{d}: id repetido")
    for m in MODELOS:
        if m["etapa"] in FRENTES and m.get("frente") not in FRENTES[m["etapa"]]:
            erros.append(f'{m["id"]}: mensagem de {m["etapa"].upper()} sem porta ou frente válida')
        for k, v, _ in m.get("campos", []):
            for x, lim in medir(m["canal"], k, v):
                if contar(x) > lim:
                    erros.append(f'{m["id"]}: {k} com {contar(x)} caracteres (limite {lim}): {x}')
            if m["canal"] == "pesquisa" and k in QUANTIDADE_PESQUISA and len(v) != QUANTIDADE_PESQUISA[k]:
                erros.append(f'{m["id"]}: {k} com {len(v)} itens (esperado {QUANTIDADE_PESQUISA[k]})')
        t = texto_copia(m)
        for rx, nome in CLAIMS:
            if re.search(rx, t, 0 if nome in ("MEC", "#1") else re.I):
                erros.append(f'{m["id"]}: claim vetado ({nome})')
        for rx in FORA:
            if re.search(rx, t, re.I):
                erros.append(f'{m["id"]}: termo fora do território ({rx})')
        if re.search(r"\[P \d+\]", t):
            erros.append(f'{m["id"]}: código de pendência [P n] no texto copiável')
        if "\u2014" in t or "\u2013" in t:
            erros.append(f'{m["id"]}: travessão no texto copiável')
    if erros:
        raise SystemExit("ERRO no texto copiável:\n  " + "\n  ".join(erros))


if __name__ == "__main__":
    conferir_textos_copiaveis()
    SAIDA.write_text(pagina(), encoding="utf-8")
    print(f"ok: {SAIDA.relative_to(RAIZ)} ({SAIDA.stat().st_size // 1024} KB, {len(MODELOS)} modelos, {len(CARTOES)} cartões)")
