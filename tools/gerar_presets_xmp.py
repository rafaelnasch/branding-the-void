#!/usr/bin/env python3
"""Gera as predefinições .xmp de Lightroom e Camera Raw do sistema Sala Escura.

Saídas em assets/foto/:
  void-ritual.xmp   VOID P&B 01 "Ritual" (padrão)
  void-vazio.xmp    VOID P&B 02 "Vazio" (capa e topo de funil)
  void-terra.xmp    VOID COR 01 "Terra" (depoimento e comunidade)

Os valores são a receita de Lightroom de assets/foto/receitas.md (pesquisa 07, seção 1.9),
a mesma família de números da especificação 8.3: a curva do Ritual (0>8 em 0 a 255) é o
0,00>0,03 da LUT, e o grão nunca vai dentro da LUT, mas vai dentro da predefinição.

O que a predefinição não grava, de propósito:
  - Exposição: a receita diz "0 a -0,3"; é ajuste de cada foto.
  - Temperatura do Terra ("150 K acima da neutra"): é relativa ao balanço de cada foto.
  - Perfil (Adobe Monochrome ou Adobe Color): fica o perfil da foto; o Ritual e o Vazio
    convertem para preto e branco pela mistura de canais.
Os duotons de produto continuam só em .cube (peça de produto, não fotografia de acervo).

Uso:
  python3 tools/gerar_presets_xmp.py            gera os três arquivos
  python3 tools/gerar_presets_xmp.py --testar   gera, relê o XML e confere os valores da receita
"""
import sys
import uuid
import xml.etree.ElementTree as ET
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DESTINO = RAIZ / "assets" / "foto"
GRUPO = "The VOID · Sala Escura"
DONO = "The VOID Tattoo Academy"
NS_CRS = "http://ns.adobe.com/camera-raw-settings/1.0/"
NS_RDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"

RITUAL = {
    "nome": "VOID P&B 01 Ritual",
    "arquivo": "void-ritual.xmp",
    "descricao": "P&B padrão da The VOID. Grão já incluído (28/20/55). Confira o perfil Adobe Monochrome e ajuste a exposição entre 0 e -0,3.",
    "cinza": True,
    "valores": {
        "Contrast2012": 25, "Highlights2012": -40, "Shadows2012": 10, "Whites2012": 15, "Blacks2012": -35,
        "GrayMixerRed": 10, "GrayMixerOrange": 15, "GrayMixerYellow": 0, "GrayMixerGreen": -20,
        "GrayMixerAqua": 0, "GrayMixerBlue": -25, "GrayMixerPurple": 0, "GrayMixerMagenta": 0,
        "Texture": 15, "Clarity2012": 12, "Dehaze": 0,
        "Sharpness": 50, "SharpenRadius": 0.8, "SharpenDetail": 30, "SharpenEdgeMasking": 60,
        "LuminanceSmoothing": 10,
        "GrainAmount": 28, "GrainSize": 20, "GrainFrequency": 55,
        "PostCropVignetteAmount": -12, "PostCropVignetteMidpoint": 40, "PostCropVignetteRoundness": 0,
        "PostCropVignetteFeather": 80, "PostCropVignetteStyle": 1, "PostCropVignetteHighlightContrast": 0,
    },
    "curva": [(0, 8), (40, 30), (128, 128), (200, 212), (255, 245)],
}

VAZIO = {
    "nome": "VOID P&B 02 Vazio",
    "arquivo": "void-vazio.xmp",
    "descricao": "P&B de capa e topo de funil. Parte do Ritual com mais contraste, pretos mais fundos e grão 40/25/60.",
    "cinza": True,
    "valores": dict(RITUAL["valores"], Contrast2012=40, Blacks2012=-55, GrainAmount=40, GrainSize=25,
                    GrainFrequency=60, PostCropVignetteAmount=-25),
    "curva": [(0, 0), (60, 35), (128, 120), (255, 250)],
}

TERRA = {
    "nome": "VOID COR 01 Terra",
    "arquivo": "void-terra.xmp",
    "descricao": "Cor contida para depoimento e comunidade. Confira o perfil Adobe Color e suba a temperatura cerca de 150 K acima da neutra em cada foto.",
    "cinza": False,
    "valores": {
        "Contrast2012": 15, "Highlights2012": -35, "Shadows2012": 5, "Blacks2012": -30,
        "Vibrance": -15, "Saturation": -20,
        "HueAdjustmentOrange": -5, "SaturationAdjustmentOrange": -10, "LuminanceAdjustmentOrange": 5,
        "SaturationAdjustmentRed": -15,
        "SaturationAdjustmentGreen": -60, "LuminanceAdjustmentGreen": -20,
        "SaturationAdjustmentBlue": -70,
        "SaturationAdjustmentPurple": -80, "SaturationAdjustmentMagenta": -80,
        "SplitToningShadowHue": 25, "SplitToningShadowSaturation": 12,
        "ColorGradeMidtoneHue": 35, "ColorGradeMidtoneSat": 6,
        "SplitToningHighlightHue": 45, "SplitToningHighlightSaturation": 8,
        "ColorGradeBlending": 60, "SplitToningBalance": -10,
        "GrainAmount": 20, "GrainSize": 20, "GrainFrequency": 50,
    },
    "curva": None,
}

PRESETS = [RITUAL, VAZIO, TERRA]

# Campos em que o Camera Raw grava o sinal de mais (ajustes de -100 a +100).
COM_SINAL = {"Contrast2012", "Highlights2012", "Shadows2012", "Whites2012", "Blacks2012", "Texture",
             "Clarity2012", "Dehaze", "Vibrance", "Saturation", "SharpenRadius", "PostCropVignetteAmount",
             "PostCropVignetteRoundness", "SplitToningBalance"}
COM_SINAL_PREFIXOS = ("GrayMixer", "HueAdjustment", "SaturationAdjustment", "LuminanceAdjustment")


def formatar(campo, valor):
    if isinstance(valor, float):
        texto = ("%.1f" % valor).rstrip("0").rstrip(".")
    else:
        texto = str(valor)
    sinal = campo in COM_SINAL or campo.startswith(COM_SINAL_PREFIXOS)
    if sinal and not texto.startswith("-") and valor != 0:
        texto = "+" + texto
    return texto


def xml_attr(texto):
    return texto.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")


def alt(tag, texto):
    return ('   <crs:%s>\n    <rdf:Alt>\n     <rdf:li xml:lang="x-default">%s</rdf:li>\n'
            '    </rdf:Alt>\n   </crs:%s>\n') % (tag, xml_attr(texto), tag)


def seq(tag, pontos):
    itens = "".join("     <rdf:li>%d, %d</rdf:li>\n" % p for p in pontos)
    return "   <crs:%s>\n    <rdf:Seq>\n%s    </rdf:Seq>\n   </crs:%s>\n" % (tag, itens, tag)


def gerar(p):
    ident = uuid.uuid5(uuid.NAMESPACE_URL, "the-void/sala-escura/" + p["arquivo"]).hex.upper()
    attrs = [
        ("PresetType", "Normal"), ("Cluster", ""), ("UUID", ident), ("SupportsAmount", "False"),
        ("SupportsColor", "True"), ("SupportsMonochrome", "True"), ("SupportsHighDynamicRange", "True"),
        ("SupportsNormalDynamicRange", "True"), ("SupportsSceneReferred", "True"),
        ("SupportsOutputReferred", "True"), ("CameraModelRestriction", ""), ("Copyright", DONO),
        ("ContactInfo", ""), ("Version", "15.0"), ("ProcessVersion", "11.0"),
    ]
    attrs += [(k, formatar(k, v)) for k, v in p["valores"].items()]
    if p["cinza"]:
        attrs.append(("ConvertToGrayscale", "True"))
    if p["curva"]:
        attrs.append(("ToneCurveName2012", "Custom"))
    attrs.append(("HasSettings", "True"))
    linhas = "".join('   crs:%s="%s"\n' % (k, xml_attr(v)) for k, v in attrs)
    corpo = alt("Name", p["nome"]) + alt("ShortName", p["nome"]) + alt("SortName", p["nome"])
    corpo += alt("Group", GRUPO) + alt("Description", p["descricao"])
    if p["curva"]:
        linear = [(0, 0), (255, 255)]
        corpo += seq("ToneCurvePV2012", p["curva"])
        for canal in ("Red", "Green", "Blue"):
            corpo += seq("ToneCurvePV2012" + canal, linear)
    return (
        '<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 7.0">\n'
        ' <rdf:RDF xmlns:rdf="%s">\n'
        '  <rdf:Description rdf:about=""\n'
        '    xmlns:crs="%s"\n%s'
        '   >\n%s'
        '  </rdf:Description>\n'
        ' </rdf:RDF>\n'
        '</x:xmpmeta>\n'
    ) % (NS_RDF, NS_CRS, linhas.rstrip("\n").rstrip() + "\n", corpo)


def testar(p, caminho):
    raiz = ET.parse(caminho).getroot()
    desc = raiz.find(".//{%s}Description" % NS_RDF)
    erros = []
    for k, v in p["valores"].items():
        lido = desc.get("{%s}%s" % (NS_CRS, k))
        if lido is None or float(lido) != float(v):
            erros.append("%s: esperado %s, lido %s" % (k, v, lido))
    if (desc.get("{%s}ConvertToGrayscale" % NS_CRS) == "True") != p["cinza"]:
        erros.append("ConvertToGrayscale divergente")
    if p["curva"]:
        itens = [li.text for li in desc.find("{%s}ToneCurvePV2012" % NS_CRS).iter("{%s}li" % NS_RDF)]
        if itens != ["%d, %d" % c for c in p["curva"]]:
            erros.append("curva divergente: %s" % itens)
    nome = desc.find("{%s}Name" % NS_CRS).find(".//{%s}li" % NS_RDF).text
    if nome != p["nome"]:
        erros.append("nome divergente: %s" % nome)
    texto = caminho.read_text(encoding="utf-8")
    if chr(0x2014) in texto or chr(0x2013) in texto:
        erros.append("travessão no arquivo")
    return erros


def main():
    DESTINO.mkdir(parents=True, exist_ok=True)
    falhas = 0
    for p in PRESETS:
        caminho = DESTINO / p["arquivo"]
        caminho.write_text(gerar(p), encoding="utf-8")
        if "--testar" in sys.argv:
            erros = testar(p, caminho)
            falhas += len(erros)
            print("%-16s %s" % (p["arquivo"], "ok" if not erros else "; ".join(erros)))
        else:
            print("gerado", caminho.relative_to(RAIZ))
    sys.exit(1 if falhas else 0)


if __name__ == "__main__":
    main()
