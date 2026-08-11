from django.shortcuts import render, get_object_or_404
from .models import webcomic

TRANSLATIONS = {
    "english": {
        "comics_title": "COMICS",
        "main_part": "here, you can read the webcomic! (for free!)",
        "community": "COMMUNITY",
        "discord": "Discord Server!",
        "patreon": "Patreon Profile!",
        "merch": "Merch Website!",
        "twitter": "Twitter/X Profile!",
        "button": "View the webcomic here!",
        "episode": "Episode",
        "ep_1": "DEUS EX MACHINA",
        "ep_2": "THIS WAS THE LAST PLACE MY FATHER WAS SEEN",
        "ep_3": "YOU ONCE LEFT ME WITH THIS",
        "ep_4": "FIGHT OVER",
        "ep_5": "HERE, I'LL TEACH YOU HOW TO COOK",
        "ep_6": "ANYTIME, WHENEVER",
        "ep_7": "CAME HOME TO SEE THE BAD NEWS",
        "ep_8": "DON'T GO",
        "ep_9": "THE BEAUTIFUL SILENCE AFTER THE BANG",
        "owned_by": "maumakanapa is owned by:",
        "assets": (
            "every asset used belongs to <br> labirhin and it's respective"
            " creators"
        ),
        "made_with": "website made with love by:",
        "selector": "/english/comics",
        "index": "/english/",
        "about": "/english/about",
        "about1": "this website as made with the sole purpose of <br> being a 'backup' in case other websites that <br> host Mau Makan Apa randomly go down",
        "about2": "a lot of hard work was put onto this, so i hope that <br> you, the reader, actually enjoys it, <br> as much as i enjoyed making the website it self!",
        "about3": "more stuff will get added here in the future, such as: <br> more languages, more stuff about MMA, and much more!",
        "about4": "thank you to everyone who motivated me to actually <br> make this website!",
        "about5": "-laurah",
        "abouth1": "about this website!",
        "notcomic1": "episode not available...",
        "notcomic2": "what typa episode are you trying to access????",
        "notcomic3": "back to the webcomics",
    },
    "indonesian": {
        "main_part": "di sini, kamu bisa membaca webcomic-nya! (gratis!)",
        "community": "MASYARAKAT",
        "comics_title": "KOMIK",
        "discord": "Server Discord",
        "patreon": "Profil Patreon",
        "merch": "Situs Web Merch",
        "twitter": "Profil Twitter/X",
        "button": "Lihat webkomik di sini!",
        "episode": "Episode",
        "ep_1": "DEUS EX MACHINA",
        "ep_2": "INILAH TEMPAT TERAKHIR AYAHKU TERLIHAT",
        "ep_3": "KAMU JUGA PERNAH NITIPIN AKU INI",
        "ep_4": "FIGHT OVER",
        "ep_5": "SINI AKU AJARIN KAMU MASAK",
        "ep_6": "KAPAN KAPAN ITU BISA KAPAN AJA",
        "ep_7": "PULANG UNTUK MENYAKSIKAN KABAR BURUK",
        "ep_8": "JANGANLAH KAU PERGI",
        "ep_9": "KESUNYIAN YANG INDAH SETELAH KERIBUTAN",
        "owned_by": "maumakanapa dimiliki oleh:",
        "assets": (
            "setiap aset yang digunakan adalah milik <br> labirhin dan"
            " pencipta masing-masing"
        ),
        "made_with": "situs web dibuat dengan cinta oleh:",
        "selector": "/indonesian/comics",
        "index": "/indonesian/",
        "about": "/indonesian/about",
        "about1": "situs web ini dibuat dengan tujuan semata-mata untuk <br>menjadi 'cadangan' jika situs web lain yang <br>menghosting Mau Makan Apa tiba-tiba tidak aktif.",
        "about2": "banyak kerja keras yang dicurahkan untuk ini, jadi saya harap <br>Anda, pembaca, benar-benar menikmatinya, <br>sama seperti saya menikmati pembuatan situs web itu sendiri!",
        "about3": "lebih banyak hal akan ditambahkan di sini di masa mendatang, seperti: <br>lebih banyak bahasa, lebih banyak hal tentang MMA, dan <br>masih banyak lagi!",
        "about4": "terima kasih kepada semua orang yang memotivasi saya untuk <br>benar-benar membuat situs web ini!",
        "about5": "-laurah",
        "abouth1": "tentang situs web ini!",
        "notcomic1": "episode tidak tersedia...",
        "notcomic2": "jenis episode apa yang coba kamu akses????",
        "notcomic3": "kembali ke webcomic",
    },
    "spanish": {
        "comics_title": "COMICS",
        "main_part": "¡aquí puedes leer el webcómic! (¡gratis!)",
        "community": "COMUNIDAD",
        "discord": "Servidor de Discord",
        "patreon": "Perfil de Patreon",
        "merch": "Sitio Web de Merch",
        "twitter": "Perfil de Twitter/X",
        "button": "¡Mira la webcomic aquí!",
        "episode": "Episodio",
        "ep_1": "DEUS EX MACHINA",
        "ep_2": "ESTE ES EL ULTIMO LUGAR DONDE MI PADRE FUE VISTO",
        "ep_3": "UNA VEZ ME DEJASTE CON ESTO",
        "ep_4": "FIGHT OVER",
        "ep_5": "MIRA, TE ENSEÑARE COMO COCINAR",
        "ep_6": "CUANDO Y COMO SEA",
        "ep_7": "LLEGUE A CASA PARA VER MALAS NOTICIAS",
        "ep_8": "NO TE VAYAS",
        "ep_9": "EL HERMOSO SILENCIO DESPUÉS DE LA EXPLOSIÓN",
        "owned_by": "maumakanapa es propiedad de:",
        "assets": (
            "todos los recursos utilizados pertenecen a <br> labirhin y a sus"
            " respectivos creadores"
        ),
        "made_with": "sitio web hecho con amor por:",
        "selector": "/spanish/comics",
        "index": "/spanish/",
        "about": "/spanish/about",
        "about1": "este sitio web fue hecho con el único propósito de <br>ser una 'copia de seguridad' en caso de que otros sitios web que <br>alojan Mau Makan Apa se caigan repentinamente.",
        "about2": "¡se puso mucho esfuerzo en esto, así que espero que <br>tú, el lector, realmente lo disfrutes, <br>tanto como yo disfruté haciendo el sitio web en sí!",
        "about3": "se agregarán más cosas aquí en el futuro, como: <br>más idiomas, más cosas sobre MMA y <br>mucho más!",
        "about4": "¡gracias a todos los que me motivaron a <br>hacer este sitio web!",
        "about5": "-laurah",
        "abouth1": "acerca de este sitio web!",
        "notcomic1": "episodio no disponible...",
        "notcomic2": "¿¿¿¿a qué tipo de episodio intentas acceder????",
        "notcomic3": "volver a los webcómics",
    },
    "portuguese": {
        "comics_title": "QUADRINHOS",
        "main_part": "aqui você pode ler a webcomic! (de graça!)",
        "community": "COMUNIDADE",
        "discord": "Servidor do Discord!",
        "patreon": "Perfil do Patreon!",
        "merch": "Site de Merch!",
        "twitter": "Perfil do Twitter/X",
        "button": "Veja a webcomic aqui!",
        "episode": "Episódio",
        "ep_1": "DEUS EX MACHINA",
        "ep_2": "O ÚLTIMO LUGAR ONDE VIRAM O MEU PAI",
        "ep_3": "FOI ISTO O QUE VOCÊ ME DEIXOU",
        "ep_4": "ULTIMATO",
        "ep_5": "VEM CÁ, VOU TE ENSINAR A COZINHAR",
        "ep_6": "A QUALQUER HORA, EM QUALQUER LUGAR",
        "ep_7": "FINALMENTE EM CASA PARA VER AS MÁS NOTÍCIAS",
        "ep_8": "POR FAVOR, NÃO VÁ!",
        "ep_9": "A CALMARIIA DEPOIS DA TEMPESTADE",
        "owned_by": "maumakanapa pertence a:",
        "assets": (
            "todos os recursos usados pertencem a <br> labirhin e aos seus"
            " respectivos criadores"
        ),
        "made_with": "site feito com amor por:",
        "selector": "/portuguese/comics",
        "index": "/portuguese/",
        "about": "/portuguese/about",
        "about1": "este site foi feito com o objetivo de <br>ser um backup em caso que os sites que <br>tem o comic Mau Makan Apa vão a baixo.",
        "about2": "eu trabalhei muito neste site, então eu espero que <br>tu, o leitor(a), goste do site, como eu gostei de o fazer.",
        "about3": "eu planeio em adicionar mais coisas no futuro, como: <br>mais línguas, mais coisas sobre MMA, e muito mais!",
        "about4": "obrigado a todos por terem me motivado <br>a fazer este site!",
        "about5": "-laurah (sim, sou portuguesa, não brasileira c:)",
        "abouth1": "sobre o site!",
        "notcomic1": "página indisponível..",
        "notcomic2": "que tipo de página é que estás a tentar aceder????",
        "notcomic3": "voltar para a webcomic",
    },
}

def index(request, lang="english"):
  if lang not in TRANSLATIONS:
    lang = "english"

  context = {
      "current_lang": lang,
      "t": TRANSLATIONS[lang],
  }
  return render(request, "comics_app/index.html", context)


def comic_list(request, lang):
  if lang not in TRANSLATIONS:
    lang = "english"

  context = {
      "current_lang": lang,
      "t": TRANSLATIONS[lang],
  }
  return render(request, "comics_app/select.html", context)

def page(request, lang, number):
    if lang not in TRANSLATIONS:
        lang = "english"

    comic = webcomic.objects.filter(language__iexact=lang, ep_number=number).first()

    if comic:
        pages = comic.pages.all()
        
        prev_comic = webcomic.objects.filter(
            language=comic.language,
            ep_number__lt=comic.ep_number
        ).order_by('-ep_number').first()
        next_comic = webcomic.objects.filter(
                language=comic.language,
                ep_number__gt=comic.ep_number
            ).order_by('ep_number').first()
    else:
        pages = []
        prev_comic = None
        next_comic = None
    
    context = {
              "current_lang": lang,
              "t": TRANSLATIONS[lang],
              "comic": comic,
              "pages": pages,
              "prev_comic": prev_comic,
              "next_comic": next_comic,
          }
    
    return render(request, "comics_app/comic.html", context)

def about(request, lang):
  if lang not in TRANSLATIONS:
    lang = "english"

  context = {
      "current_lang": lang,
      "t": TRANSLATIONS[lang],
  }

  return render(request, "comics_app/about.html", context)