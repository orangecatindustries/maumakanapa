from django.shortcuts import render
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
        "wiki": "Official Wiki!",
        "youtube": "Youtube Channel!",
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
        "about1": "this website was made with the sole purpose of <br> being a 'backup' in case other websites that <br> host Mau Makan Apa randomly go down",
        "about2": "a lot of hard work was put onto this, so i hope that <br> you, the reader, actually enjoys it, <br> as much as i enjoyed making the website it self!",
        "about3": "more stuff will get added here in the future, such as: <br> more languages, more stuff about MMA, and much more!",
        "about4": "thank you to everyone who motivated me to actually <br> make this website!",
        "about5": "-laurah",
        "abouth1": "about this website!",
        "notcomic1": "episode not available...",
        "notcomic2": "what typa episode are you trying to access????",
        "notcomic3": "back to the webcomics",
        "aboutme": "about me!",
        "aboutme1": "my name is laurah, i'm the person who made <br> this website, and i'm just your typical web developer!",
        "aboutme2": "i'm also a youtuber, so if you want to go <br> check out my channel, you can do so here: ",
        "aboutme3": "fun fact: this website is actually open-sourced <br> on github! you can go check it out here:  ",
        "aboutme4": "thank you!!!",
        "languages": "view more languages here!",
        "missilecity": "MISSILE CITY",
        "missilecityinfo": "Missile City is currently an upcoming webcomic & animated series, it is planned to be released after the final animation of Mau Makan Apa (in this case, episode 9). The series is going to feature characters from MMA, but also have it's own unique ones such as: Weewee, Lobi Kalobi & Supernova. According to the current information that we have, the animation will be based in Pemucik, and the story is going to be about both Weewee and Lobi, who at some point get handcuffed to each other, searching for the location of the evil supreme leader, Supernova. <br> (Official animation isn't out yet, so here's the music video!)",
        "rar": "REVISION AFTER REVISION",
        "rarinfo": "Revision After Revision is a short film that tells a story about Sorbitol, who currently works at Jaya Studios, which is an animation studio for Jaya TV. In the short-film, he tells about his feelings, and how much he is sick of revisions given by his CEO. He also meets Kontol Diamond, which was a love interest for him, which implies that they lived their lives together in the end.",
        "tsrf": "THE STARS ARE FALLING",
        "tsrfinfo": "In The Stars Are Falling, school friends Poteto and Oktana are forced apart when Poteto contracts scabies. During isolation, Poteto tragically cuts off his ears and receives metal prosthetics, only to be struck by lightning and resurrected with superpowers after speaking with an angel. Upon returning, Poteto finds Oktana with a woman named Bombax, though Oktana claims he'd rather be with him. Angered by Oktana teasing his prosthetic ears as 'goofy' Poteto uses his new powers to rain falling stars down on Lawu City and publicly blames Oktana for the chaos.",
        "tbtl": "THE BIG TEMPE LIE",
        "tbtlinfo": "In The Big Tempe Lie, the media falsely claims that a new strain of tempe caused by volcanic ash turns people into mind-controlling fungus monsters, leading the government to quarantine Boyolali. A person named Dino sneaks into the quarantined zone to find his friend Rizo, only to discover the entire epidemic was a hoax; the 'monsters' are actually just people wearing promotional tempe costumes. Motivated by Rizo to save their cultural food, Dino records video evidence and escapes to reveal the truth online, successfully lifting the quarantine and restoring normalcy two months later.",
        "button2": "view the content!",
        "titlerar": "Revision After Revision",
        "subtitlerar": "Mmm.. Yes, Sorbitol.",
        "titletsrf": "The Stars Are Falling",
        "subtitletsrf": "Poteto & his goofy ears.",
        "titlemc": "Missile City",
        "subtitlemc": "Lobi, why are you handcuffed?!",
        "titletbtl": "The Big Tempe Lie",
        "subtitletbtl": "Mmm.. Yes, Sorbitol.",
        "buttonmc": "/english/mc",
        "buttontsrf": "/english/tsrf",
        "buttontbtl": "/english/tbtl",
        "buttonrar": "/english/rar",
    },
    "indonesian": {
        "main_part": "di sini, kamu bisa membaca webcomic-nya! (gratis!)",
        "community": "MASYARAKAT",
        "comics_title": "KOMIK",
        "discord": "Server Discord",
        "patreon": "Profil Patreon",
        "merch": "Situs Web Merch",
        "twitter": "Profil Twitter/X",
        "wiki": "Wiki Resmi!",
        "youtube": "Saluran Youtube!",
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
        "aboutme": "tentang saya!",
        "aboutme1": "nama saya laurah, akulah orang yang membuat <br> situs web ini, dan aku hanyalah pengembang web biasa!",
        "aboutme2": "aku juga seorang youtuber, jadi jika kamu ingin <br> memeriksa saluranku, kamu bisa melakukannya di sini: ",
        "aboutme3": "fakta menarik: situs web ini sebenarnya bersumber terbuka <br> di github! kamu bisa memeriksanya di sini:",
        "aboutme4": "terima kasih!!!",
        "languages": "lihat bahasa lainnya di sini!",
        "missilecity": "KOTA MISIL",
        "missilecityinfo": "Kota Misil saat ini adalah sebuah webcomic & serial animasi mendatang, yang rencananya akan dirilis setelah animasi terakhir Mau Makan Apa (dalam hal ini, episode 9). Serial ini akan menampilkan karakter dari MMA, tetapi juga memiliki karakter uniknya sendiri seperti: Weewee, Lobi Kalobi & Supernova. Menurut informasi saat ini, animasi ini akan berlatar di Pemucik, dan ceritanya tentang Weewee dan Lobi yang pada suatu titik diborgol bersama, mencari lokasi pemimpin tertinggi yang jahat, Supernova. <br> (Animasi resminya belum keluar, jadi ini video musiknya!)",
        "rar": "REVISI DEMI REVISI",
        "rarinfo": "Revisi Demi Revisi adalah sebuah film pendek yang menceritakan tentang Sorbitol, yang saat ini bekerja di Jaya Studios, sebuah studio animasi untuk Jaya TV. Dalam film pendek tersebut, ia menceritakan tentang perasaannya dan betapa ia muak dengan revisi yang diberikan oleh CEO-nya. Ia juga bertemu dengan Kontol Diamond, yang merupakan kekasihnya, yang menyiratkan bahwa mereka menjalani hidup bersama pada akhirnya.",
        "tsrf": "BINTANG-BINTANG BERJATUHAN",
        "tsrfinfo": "Dalam Bintang-Bintang Berjatuhan, teman sekolah Poteto dan Oktana terpaksa berpisah ketika Poteto terkena skabies. Selama isolasi, Poteto secara tragis memotong telinganya dan menerima prostetik logam, hanya untuk disambar petir dan dibangkitkan dengan kekuatan super setelah berbicara dengan seorang malaikat. Sekembalinya, Poteto menemukan Oktana bersama seorang wanita bernama Bombax, meskipun Oktana mengklaim dia lebih suka bersamanya. Marah karena Oktana menggoda telinga prostetiknya sebagai 'konyol', Poteto menggunakan kekuatan barunya untuk menurunkan hujan bintang jatuh ke Kota Lawu dan secara terbuka menyalahkan Oktana atas kekacauan tersebut.",
        "tbtl": "KEBOHONGAN TEMPE BESAR",
        "tbtlinfo": "Dalam Kebohongan Tempe Besar, media secara keliru mengklaim bahwa jenis tempe baru yang disebabkan oleh abu vulkanik mengubah orang menjadi monster jamur pengendali pikiran, yang membuat pemerintah mengarantina Boyolali. Seseorang bernama Dino menyelinap ke zona karantina untuk menemukan temannya Rizo, hanya untuk menemukan bahwa seluruh epidemi tersebut adalah tipuan; para 'monster' sebenarnya hanya orang-orang yang mengenakan kostum tempe promosi. Didorong oleh Rizo untuk menyelamatkan makanan budaya mereka, Dino merekam bukti video dan melarikan diri untuk mengungkapkan kebenaran secara online, berhasil mencatat karantina dan mengembalikan kenormalan dua bulan kemudian.",
        "button2": "lihat kontennya!",
        "titlerar": "Revisi Demi Revisi",
        "subtitlerar": "Mmm.. Ya, Sorbitol.",
        "titletsrf": "Bintang-Bintang Berjatuhan",
        "subtitletsrf": "Poteto & telinga konyolnya.",
        "titlemc": "Kota Misil",
        "subtitlemc": "Lobi, kenapa kamu diborgol?!",
        "titletbtl": "Kebohongan Besar Tempe",
        "subtitletbtl": "Mmm.. Ya, Sorbitol.",
        "buttonmc": "/indonesian/mc",
        "buttontsrf": "/indonesian/tsrf",
        "buttontbtl": "/indonesian/tbtl",
        "buttonrar": "/indonesian/rar",
    },
    "spanish": {
        "comics_title": "COMICS",
        "main_part": "¡aquí puedes leer el webcómic! (¡gratis!)",
        "community": "COMUNIDAD",
        "discord": "Servidor de Discord",
        "patreon": "Perfil de Patreon",
        "merch": "Sitio Web de Merch",
        "twitter": "Perfil de Twitter/X",
        "wiki": "¡Wiki Oficial!",
        "youtube": "¡Canal de Youtube!",
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
        "aboutme": "¡sobre mí!",
        "aboutme1": "¡mi nombre es laurah, soy la persona que hizo <br> este sitio web y soy una desarrolladora web típica!",
        "aboutme2": "también soy youtuber, así que si quieres <br> visitar mi canal, puedes hacerlo aquí: ",
        "aboutme3": "dato curioso: ¡este sitio web es de código abierto <br> en github! puedes consultarlo aquí:",
        "aboutme4": "¡¡¡muchas gracias!!!",
        "languages": "ver más idiomas aqui!",
        "missilecity": "CIUDAD MISIL",
        "missilecityinfo": "Ciudad Misil es actualmente un webcomic y serie animada próxima, planeada para estrenarse después de la última animación de Mau Makan Apa (en este caso, el episodio 9). La serie contará con personajes de MMA, pero también tendrá otros únicos como: Weewee, Lobi Kalobi y Supernova. Según la información actual, la animación se basará en Pemucik, y la historia tratará sobre Weewee y Lobi, quienes en algún punto son esposados juntos, buscando la ubicación del malvado líder supremo, Supernova. <br> (¡La animación oficial aún no sale, así que aquí está el video musical!)",
        "rar": "REVISIÓN TRAS REVISIÓN",
        "rarinfo": "Revisión tras Revisión es un cortometraje que cuenta la historia de Sorbitol, quien actualmente trabaja en Jaya Studios, un estudio de animación para Jaya TV. En el cortometraje, cuenta sobre sus sentimientos y lohartto que está de las revisiones dadas por su CEO. También conoce a Kontol Diamond, quien fue un interés amoroso para él, lo que implica que vivieron sus vidas juntos al final.",
        "tsrf": "LAS ESTRELLAS ESTÁN CAYENDO",
        "tsrfinfo": "En Las Estrellas Están Cayendo, los amigos escolares Poteto y Oktana se ven separados cuando Poteto contrae sarna. Durante el aislamiento, Poteto trágicamente se corta las orejas y recibe prótesis de metal, solo para ser alcanzado por un rayo y resucitado con superpoderes después de hablar con un ángel. Al regresar, Poteto encuentra a Oktana con una mujer llamada Bombax, aunque Oktana afirma que preferiría estar con él. Enojado porque Oktana se burla de sus orejas protésicas llamándolas 'tontas', Poteto usa sus nuevos poderes para hacer llover estrellas sobre Ciudad Lawu y culpa públicamente a Oktana por el caos.",
        "tbtl": "LA GRAN MENTIRA DEL TEMPE",
        "tbtlinfo": "En La Gran Mentira del Tempe, los medios afirman falsamente que una nueva cepa de tempe causada por ceniza volcánica convierte a la gente en monstruos de hongos controladores Mentes, lo que lleva al gobierno a poner en cuarentena a Boyolali. Una persona llamada Dino se cuela en la zona de cuarentena para encontrar a su amigo Rizo, solo para descubrir que toda la epidemia fue un engaño; los 'monstruos' son en realidad personas usando disfraces promocionales de tempe. Motivado por Rizo para salvar su comida cultural, Dino graba evidencia en video y escapa para revelar la verdad en línea, levantando con éxito la cuarentena y restaurando la normalidad dos meses después.",
        "button2": "¡ver el contenido!",
        "titlerar": "Revisión tras Revisión",
        "subtitlerar": "Mmm.. Sí, Sorbitol.",
        "titletsrf": "Las Estrellas Están Cayendo",
        "subtitletsrf": "Poteto y sus orejas graciosas.",
        "titlemc": "Ciudad Misil",
        "subtitlemc": "¡Lobi, por qué estás esposado?!",
        "titletbtl": "La Gran Mentira de Tempe",
        "subtitletbtl": "Mmm.. Sí, Sorbitol.",
        "buttonmc": "/spanish/mc",
        "buttontsrf": "/spanish/tsrf",
        "buttontbtl": "/spanish/tbtl",
        "buttonrar": "/spanish/rar",
    },
    "portuguese": {
        "comics_title": "QUADRINHOS",
        "main_part": "aqui você pode ler a webcomic! (de graça!)",
        "community": "COMUNIDADE",
        "discord": "Servidor do Discord!",
        "patreon": "Perfil do Patreon!",
        "merch": "Site de Merch!",
        "twitter": "Perfil do Twitter/X",
        "wiki": "Wiki Oficial!",
        "youtube": "Canal do Youtube!",
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
        "about4": "obrigada a todos por terem me motivado <br>a fazer este site!",
        "about5": "-laurah (sim, sou portuguesa, não brasileira c:)",
        "abouth1": "sobre o site!",
        "notcomic1": "página indisponível..",
        "notcomic2": "que tipo de página é que estás a tentar aceder????",
        "notcomic3": "voltar para a webcomic",
        "aboutme": "sobre mim!",
        "aboutme1": "o meu nome é laurah, eu sou a pessoa que fez <br> este site, e sou a tua típica programadora de Web",
        "aboutme2": "eu também sou uma youtuber, então se quiseres ir dar <br> uma olhada, podes ir ver aqui: ",
        "aboutme3": "fun fact: este site é de código aberto <br> no github! tu podes ir ver aqui: ",
        "aboutme4": "obrigada!!!!!!!",
        "languages": "veja mais idiomas aqui!",
        "missilecity": "CIDADE MÍSSIL",
        "missilecityinfo": "Cidade Míssil é atualmente um webcomic e série animada futura, planejada para ser lançada após a última animação de Mau Makan Apa (neste caso, o episódio 9). A série contará com personagens de MMA, mas também terá os seus próprios únicos, tais como: Weewee, Lobi Kalobi & Supernova. De acordo com as informações atuais, a animação será baseada em Pemucik, and a história será sobre Weewee e Lobi, que em algum ponto são algemados um ao outro, procurando pela localização do líder supremo do mal, Supernova. <br> (A animação oficial ainda não saiu, então aqui está o videoclipe!)",
        "rar": "REVISÃO APÓS REVISÃO",
        "rarinfo": "Revisão Após Revisão é um curta-metragem que conta a história de Sorbitol, que atualmente trabalha na Jaya Studios, um estúdio de animação para a Jaya TV. No curta, ele fala sobre seus sentimentos e o quanto está enjooado das revisões dadas por seu CEO. Ele também conhece Kontol Diamond, que foi um interesse amoroso para ele, o que implica que eles viveram suas vidas juntos no fim.",
        "tsrf": "AS ESTRELAS ESTÃO CAINDO",
        "tsrfinfo": "Em As Estrelas Estão Caindo, os amigos de escola Poteto e Oktana são forçados a se separar quando Poteto contrai sarna. Durante o isolamento, Poteto tragicamente corta suas orelhas e recebe próteses de metal, apenas para ser atingido por um raio e ressuscitado com superpoderes após falar com um anjo. Ao retornar, Poteto encontra Oktana com uma mulher chamada Bombax, embora Oktana afirme que preferiría estar com ele. Irritado porque Oktana zoa suas orelhas protéticas chamando-as de 'bobas', Poteto usa seus novos poderes para fazer chover estrelas cadentes sobre a Cidade de Lawu e culpa publicamente Oktana pelo caos.",
        "tbtl": "A GRANDE MENTIRA DO TEMPE",
        "tbtlinfo": "Em A Grande Mentira do Tempe, a mídia afirma falsamente que uma nova cepa de tempe causada por cinzas vulcânicas transforma pessoas em monstros de fungos controladores de mente, levando o governo a colocar Boyolali em quarentena. Uma pessoa chamada Dino entra furtivamente na zona de quarentena para encontrar seu amigo Rizo, apenas para descobrir que toda a epidemia foi uma farsa; os 'monstros' são na verdade apenas pessoas usando fantasias promocionais de tempe. Motivado por Rizo para salvar sua comida cultural, Dino grava evidências em vídeo e foge para revelar a verdade online, levantando com sucesso a quarentena e restaurando a normalidade dois meses depois.",
        "button2": "ver o conteúdo!",
        "titlerar": "Revisão Após Revisão",
        "subtitlerar": "Mmm.. Sim, Sorbitol.",
        "titletsrf": "As Estrelas Estão Caindo",
        "subtitletsrf": "Poteto e suas orelhas bobas.",
        "titlemc": "Cidade Míssil",
        "subtitlemc": "Lobi, por que você está algemado?!",
        "titletbtl": "A Grande Mentira de Tempe",
        "subtitletbtl": "Mmm.. Sim, Sorbitol.",
        "buttonmc": "/portuguese/mc",
        "buttontsrf": "/portuguese/tsrf",
        "buttontbtl": "/portuguese/tbtl",
        "buttonrar": "/portuguese/rar",
    },
    "russian": {
        "comics_title": "КОМИКСЫ",
        "main_part": "здесь вы можете почитать веб-комикс! (бесплатно!)",
        "community": "СООБЩЕСТВО",
        "discord": "Сервер Discord!",
        "patreon": "Профиль Patreon!",
        "merch": "Сайт с мерчем!",
        "twitter": "Профиль Twitter/X!",
        "wiki": "Официальная Вики!",
        "youtube": "Ютуб Канал!",
        "button": "Смотреть веб-комикс здесь!",
        "episode": "Эпизод",
        "ep_1": "Деус Экс Макина",
        "ep_2": "Где-то Там В Последний Раз Видели Моего Отца",
        "ep_3": "Ты Мне Тогда Вручил Это",
        "ep_4": "Конфликт",
        "ep_5": "Давай, Я Научу Тебя Готовить",
        "ep_6": "Навсегда, Никогда",
        "ep_7": "Как Бы Ты Не Старался",
        "ep_8": "Отпусти",
        "ep_9": "Долгожданная Тишина",
        "owned_by": "владелец maumakanapa:",
        "assets": "все использованные материалы принадлежат <br> labirhin и их соответствующим создателям",
        "made_with": "сайт создан с любовью:",
        "selector": "/russian/comics",
        "index": "/russian/",
        "about": "/russian/about",
        "about1": "этот сайт был создан с единственной целью <br> быть 'резервной копией' на случай, если другие сайты, <br> где размещен Mau Makan Apa, внезапно перестанут работать",
        "about2": "в это было вложено много труда, поэтому я надеюсь, что <br> вам, читатель, это действительно понравится <br> так же сильно, как мне понравилось создавать сам сайт!",
        "about3": "в будущем сюда добавится больше нового, например: <br> больше языков, больше материалов о MMA и многое другое!",
        "about4": "спасибо всем, кто мотивировал меня <br> сделать этот сайт!",
        "about5": "-лора",
        "abouth1": "об этом сайте!",
        "notcomic1": "эпизод недоступен...",
        "notcomic2": "что за эпизод вы пытаетесь открыть????",
        "notcomic3": "вернуться к веб-комиксам",
        "aboutme": "о обо мне!",
        "aboutme1": "моё имя лора, я тот человек, который создал <br> этот сайт, и я просто типичный веб-разработчик!",
        "aboutme2": "я также ютубер, так что если вы хотите <br> заглянуть на мой канал, вы можете сделать это здесь:",
        "aboutme3": "интересный факт: этот сайт на самом деле с открытым исходным кодом <br> на github! вы можете посмотреть его здесь:",
        "aboutme4": "спасибо вам!!!",
        "languages": "посмотреть другие языки здесь!",
        "missilecity": "ГОРОД РАКЕТ",
        "missilecityinfo": "Город Ракет — это предстоящий веб-комикс и анимационный сериал, релиз которого запланирован после финальной анимации Mau Makan Apa (в данном случае, 9-го эпизода). В сериале будут участвовать персонажи из MMA, а также появятся свои собственные уникальные, такие как: Уиви, Лоби Калоби и Супернова. Согласно текущей информации, действие анимации будет происходить в Пемуцике, а сюжет расскажет о Уиви и Лоби, которые в какой-то момент оказываются скованы друг с другом наручниками и ищут местонахождение злого верховного лидера, Суперновы. <br> (Официальная анимация еще не вышла, так что вот музыкальный клип!)",
        "rar": "ПЕРЕСМОТР ЗА ПЕРЕСМОТРОМ",
        "rarinfo": "Пересмотр за пересмотром — это короткометражный фильм, рассказывающий историю Сорбитола, который в настоящее время работает в Jaya Studios, анимационной студии для Jaya TV. В короткометражке он рассказывает о своих чувствах и о том, как ему надоели правки, даваемые его генеральным директором. Он также встречает Контол Даймонд, которая была его любовным интересом, что подразумевает, что в конце они прожили свою жизнь вместе.",
        "tsrf": "ЗВЕЗДЫ ПАДАЮТ",
        "tsrfinfo": "В фильме «Звезды падают» школьные друзья Потето и Октана вынуждены расстаться, когда Потето заболевает чесоткой. Во время изоляции Потето трагически отрезает себе уши и получает металлические протезы, после чего в него попадает молния, и он воскресает со сверхспособностями после разговора с ангелом. Вернувшись, Потето находит Октану с женщиной по имени Бомбакс, хотя Октана утверждает, что предпочел бы быть с ним. Разозлившись на то, что Октана дразнит его протезы ушей называя их «дурацкими», Потето использует свои новые силы, чтобы обрушить падающие звезды на город Лаву и публично обвиняет Октану в хаосе.",
        "tbtl": "БОЛЬШАЯ ЛОЖЬ О ТЕМПЕ",
        "tbtlinfo": "В фильме «Большая ложь о темпе» СМИ ложно заявляют, что новый штамм темпе, вызванный вулканическим пеплом, превращает людей в монстров-грибов, управляющих сознанием, что побуждает правительство ввести карантин в Бойолали. Человек по имени Дино проникает в карантинную зону, чтобы найти своего друга Ризо, но обнаруживает, что вся эпидемия была обманом; «монстры» на самом деле просто люди в рекламных костюмах темпе. Мотивированный Ризо спасти свою культурную еду, Дино записывает видеодоказательства и сбегает, чтобы раскрыть правду в интернете, успешно сняв карантин и восстановив нормальную жизнь два месяца спустя.",
        "button2": "посмотреть контент!",
        "titlerar": "Пересмотр за пересмотром",
        "subtitlerar": "Мм.. Да, Сорбитол.",
        "titletsrf": "Звезды падают",
        "subtitletsrf": "Потето и его глупые ушки.",
        "titlemc": "Город Ракет",
        "subtitlemc": "Лоби, почему ты в наручниках?!",
        "titletbtl": "Большая ложь Темпе",
        "subtitletbtl": "Мм.. Да, Сорбитол.",
        "buttonmc": "/russian/mc",
        "buttontsrf": "/russian/tsrf",
        "buttontbtl": "/russian/tbtl",
        "buttonrar": "/russian/rar",
    },
    "chinese": {
        "comics_title": "漫画",
        "main_part": "在这里，你可以阅读网络漫画！（免费！）",
        "community": "社群",
        "discord": "Discord 服务器！",
        "patreon": "Patreon 主页！",
        "merch": "周边网站！",
        "twitter": "Twitter/X 主页！",
        "wiki": "官方Wiki!",
        "youtube": "Youtube频道!",
        "button": "在此处查看网络漫画!",
        "episode": "话",
        "ep_1": "机械降神的驾驶员",
        "ep_2": "这是我父亲最后被见到的地方",
        "ep_3": "曾与之物",
        "ep_4": "决斗争胜",
        "ep_5": "来，我教你做饭",
        "ep_6": "时空不定",
        "ep_7": "归家见噩耗",
        "ep_8": "不要离去",
        "ep_9": "爆炸之后，万籁俱静",
        "owned_by": "maumakanapa 归属于：",
        "assets": "使用所有素材均属于 <br> labirhin 及其各自的创作者",
        "made_with": "网站由以下人员倾心制作：",
        "selector": "/chinese/comics",
        "index": "/chinese/",
        "about": "/chinese/about",
        "about1": "创建本网站的唯一目的就是 <br> 作为“备份”，以防托管 Mau Makan Apa 的其他网站 <br> 随机瘫痪",
        "about2": "这其中倾注了许多心血，所以我希望 <br> 作为读者的你能够真正喜欢它， <br> 就像我享受制作这个网站的过程一样!",
        "about3": "未来这里还会添加更多内容，例如： <br> 更多语言、更多关于 MMA 的内容等等!",
        "about4": "感谢所有激励我 <br> 制作这个网站的人!",
        "about5": "-laurah",
        "abouth1": "关于本网站!",
        "notcomic1": "章节不可用...",
        "notcomic2": "你到底在尝试访问什么类型的章节????",
        "notcomic3": "返回网络漫画",
        "aboutme": "关于我!",
        "aboutme1": "我叫拉拉（laurah），我是制作 <br> 这个网站的人，我只是一个普通的网页开发者!",
        "aboutme2": "我同时也是一名油管（YouTube）博主，如果你想去 <br> 看看我的频道，可以在这里找到：",
        "aboutme3": "趣事：这个网站其实在 <br> GitHub上是开源的! 你可以在这里查看：",
        "aboutme4": "非常感谢！！！",
        "languages": "在此查看更多语言!",
        "missilecity": "导弹之城",
        "missilecityinfo": "《导弹之城》目前是一部即将推出的网络漫画和动画系列，计划在《Mau Makan Apa》的最终动画（本例中为第9集）之后发布。该系列将包含来自MMA的角色，同时也有其独特的角色，例如：Weewee、Lobi Kalobi 和 Supernova。根据目前的信息，该动画将以Pemucik为背景，故事讲述了Weewee和Lobi在某个时刻被手铐铐在一起，寻找邪恶最高领袖Supernova的下落。<br>（官方动画尚未上映，所以这里是音乐视频！）",
        "rar": "一次又一次的修改",
        "rarinfo": "《一次又一次的修改》是一部短片，讲述了Sorbitol的故事，他目前在Jaya TV的动画工作室Jaya Studios工作。在短片中，他讲述了自己的感受，以及对首席执行官提出的修改意见感到的厌烦。他还遇到了Kontol Diamond，这是他的心上人，暗示他们最终一起生活。",
        "tsrf": "繁星坠落",
        "tsrfinfo": "在《繁星坠落》中，学校朋友Poteto和Oktana在Poteto感染疥疮时被迫分开。在隔离期间，Poteto悲惨地割掉了耳朵并接受了金属假肢，却在与天使交谈后被闪电击中并带着超能力复活。回来后，Poteto发现Oktana和一个名叫Bombax的女人在一起，尽管Oktana声称他宁愿和Poteto在一起。由于Oktana取笑他的假肢耳朵“滑稽”而生气，Poteto利用他的新超能力将坠落的星辰洒向拉武市（Lawu City），并公开将混乱归咎于Oktana。",
        "tbtl": "巨型豆饼谎言",
        "tbtlinfo": "在《巨型豆饼谎言》中，媒体错误地声称由火山灰引起的一种新型豆饼（Tempe）会把人变成控制心灵的真菌怪物，导致政府对博约拉利（Boyolali）实施隔离。一个名叫Dino的人潜入隔离区寻找他的朋友Rizo，却发现整场疫情只是一场骗局；所谓的“怪物”其实只是穿着促销豆饼服装的人。在Rizo的激励下为了拯救他们的传统文化食物，Dino录下了视频证据并逃脱，在网上揭露了真相，两个月后成功解除了隔离并恢复了正常。",
        "button2": "查看内容！",
        "titlerar": "一次又一次的修改",
        "subtitlerar": "嗯……是的，山梨醇。",
        "titletsrf": "繁星坠落",
        "subtitletsrf": "波特托和他的滑稽耳朵。",
        "titlemc": "导弹城",
        "subtitlemc": "洛比，你为什么被手铐铐住了？！",
        "titletbtl": "坦佩大谎言",
        "subtitletbtl": "嗯……是的，山梨醇。",
        "buttonmc": "/chinese/mc",
        "buttontsrf": "/chinese/tsrf",
        "buttontbtl": "/chinese/tbtl",
        "buttonrar": "/chinese/rar",
    },
    "filipino": {
        "comics_title": "MGA KOMIKS",
        "main_part": "dito, maaari kang magbasa ng webcomic! (nang libre!)",
        "community": "KOMUNIDAD",
        "discord": "Discord Server!",
        "patreon": "Patreon Profile!",
        "merch": "Merch Website!",
        "twitter": "Twitter/X Profile!",
        "wiki": "Opisyal na Wiki!",
        "youtube": "Channel sa Youtube!",
        "button": "Tingnan ang webcomic dito!",
        "episode": "Episode",
        "ep_1": "DEUS EX MACHINA",
        "ep_2": "ITO ANG HULING LUGAR KUNG SAAN NAKITA ANG AKING AMA",
        "ep_3": "MINSAN MO AKONG INIWAN NG NITO",
        "ep_4": "TAPOS NA ANG LABAN",
        "ep_5": "HALIKA, ITUTURO KO SA IYONG MAGLUTO",
        "ep_6": "KAILANMAN, ANUMANG ORAS",
        "ep_7": "UMUWI PARA MAKITA ANG MASAMANG BALITA",
        "ep_8": "HUWAG KANG UMALIS",
        "ep_9": "ANG MAGANDANG TAHIMIK PAGKATAPOS NG PUTOK",
        "owned_by": "ang maumakanapa ay pagmamay-ari ni:",
        "assets": "ang bawat asset na ginamit ay pagmamay-ari ng <br> labirhin at ng kani-kanilang mga creator",
        "made_with": "ang website na ito ay ginawa nang may pagmamahal ni:",
        "selector": "/filipino/comics",
        "index": "/filipino/",
        "about": "/filipino/about",
        "about1": "ang website na ito ay ginawa para sa tanging layunin na <br> maging 'backup' kung sakaling biglang bumagsak ang ibang mga website <br> na nagho-host ng Mau Makan Apa",
        "about2": "maraming hirap ang ibinuhos dito, kaya umaasa ako na <br> ikaw, ang mambabasa, ay talagang mag-enjoy dito, <br> tulad ng pag-enjoy ko sa paggawa ng website mismo!",
        "about3": "mas maraming bagay ang idadagdag dito sa hinaharap, tulad ng: <br> mas maraming wika, mas maraming bagay tungkol sa MMA, at marami pang iba!",
        "about4": "salamat sa lahat ng nag-udyok sa akin na <br> gawin talaga ang website na ito!",
        "about5": "-laurah",
        "abouth1": "tungkol sa website na ito!",
        "notcomic1": "hindi available ang episode...",
        "notcomic2": "anong klaseng episode ba ang sinusubukan mong puntahan????",
        "notcomic3": "bumalik sa mga webcomic",
        "aboutme": "tungkol sa akin!",
        "aboutme1": "ang pangalan ko ay laurah, ako ang gumawa <br> ng website na ito, at isa lang akong tipikal na web developer!",
        "aboutme2": "isa rin akong youtuber, kaya kung gusto mong <br> bisitahin ang aking channel, maaari mo itong gawin dito:",
        "aboutme3": "fun fact: ang website na ito ay open-source <br> sa github! maaari mo itong tignan dito: ",
        "aboutme4": "maraming salamat!!!",
        "languages": "tingnan ang iba pang mga wika dito!",
        "missilecity": "LUNGSOD NG MISIL",
        "missilecityinfo": "Ang Lungsod Ng Misil ay kasalukuyang isang paparating na webcomic & animated series, na planong ipalabas pagkatapos ng huling animation ng Mau Makan Apa (sa kasong ito, episode 9). Itantampok sa serye ang mga karakter mula sa MMA, ngunit magkakaroon din ito ng sariling mga natatanging karakter tulad nina: Weewee, Lobi Kalobi & Supernova. Ayon sa kasalukuyang impormasyon, ang animation ay magaganap sa Pemucik, at ang kuwento ay tungkol kina Weewee at Lobi, na sa ilang punto ay pinosasan sa isa't isa, hinahanap ang lokasyon ng masamang pinuno, si Supernova. <br> (Wala pa ang opisyal na animation, kaya narito ang music video!)",
        "rar": "REBISYON PAGKATAPOS NG REBISYON",
        "rarinfo": "Ang Rebisyon Pacgkatapos Ng Rebisyon ay isang maikling pelikula na nagtękuwento tungkol kay Sorbitol, na kasalukuyang nagtatrabaho sa Jaya Studios, isang animation studio para sa Jaya TV. Sa maikling pelikula, ikinukuwento niya ang kanyang mga nararamdaman, at kung gaano na siya nagsasawa sa mga rebisyong ibinibigay ng kanyang CEO. Nakilala rin niya si Kontol Diamond, na naging love interest niya, na nagpapahiwatig na namuhay sila nang magkasama sa huli.",
        "tsrf": "HULOG NG MGA BITUIN",
        "tsrfinfo": "Sa Hulog Ng Mga Bituin, ang magkaibigan sa eskwela na sina Poteto at Oktana ay pinilit na maghiwalay nang magka-scabies si Poteto. Sa panahon ng pagka-isolate, tragikong pinutol ni Poteto ang kanyang mga tainga at tumanggap ng metal prosthetics, hanggang sa tinamaan ng kidlat at nabuhay na muli na may mga superpower pagkatapos makausap ang isang anghel. Pagbalik, nakita ni Poteto si Oktana kasama ang isang babaeng nagngangalang Bombax, bagama't iginiit ni Oktana na mas gusto niyang makasama siya. Nagalit dahil tinukso ni Oktana ang kanyang prosthetics na tainga bilang 'katawa-tawa', ginamit ni Poteto ang kanyang mga bagong kapangyarihan para magpaulan ng mga bituin sa Lawu City at hayagang sinisi si Oktana sa kaguluhan.",
        "tbtl": "ANG MALAKING KASINUNGALINGAN SA TEMPE",
        "tbtlinfo": "Sa Ang Malaking Kasinungaligan Sa Tempe, maling ibinalita ng media na ang isang bagong uri ng tempe na dulot ng abo ng bulkan ay nagiging mga mind-controlling fungus monsters ang mga tao, kaya ipinailalim ng pamahalaan sa quarantine ang Boyolali. Ang isang taong nagngangalang Dino ay palihim na pumasok sa quarantined zone para hanapin ang kanyang kaibigang si Rizo, ngunit natuklasan niyang ang buong epidemya ay isang panlilinlang lamang; ang mga 'halimaw' ay mga tao lamang na nakasuot ng promotional tempe costumes. Hinihimok ni Rizo na iligtas ang kanilang pangkulturang pagkain, nag-record si Dino ng ebidensya sa video at tumakas upang ibunyag ang katotohanan online, na matagumpay na nag-alis ng quarantine at nagbalik sa normalidad makalipas ang dalawang buwan.",
        "button2": "tingnan ang nilalaman!",
        "titlerar": "Rebisyon Pagkatapos ng Rebisyon",
        "subtitlerar": "Mmm.. Oo, Sorbitol.",
        "titletsrf": "Hulog ng mga Bituin",
        "subtitletsrf": "Si Poteto at ang kanyang mga nakakatawang tainga.",
        "titlemc": "Lungsod ng Misil",
        "subtitlemc": "Lobi, bakit ka naka-posas?!",
        "titletbtl": "Ang Malaking Kasinungalingan ng Tempe",
        "subtitletbtl": "Mmm.. Oo, Sorbitol.",
        "buttonmc": "/filipino/mc",
        "buttontsrf": "/filipino/tsrf",
        "buttontbtl": "/filipino/tbtl",
        "buttonrar": "/filipino/rar",
    },
    "italiano": {
        "comics_title": "FUMETTI",
        "main_part": "qui puoi leggere il webcomic! (gratuitamente!)",
        "community": "COMMUNITY",
        "discord": "Server Discord!",
        "patreon": "Profilo Patreon!",
        "merch": "Sito di Merch!",
        "twitter": "Profilo Twitter/X!",
        "wiki": "Wiki Ufficiale!",
        "youtube": "Canale Youtube!",
        "button": "Guarda il webcomic qui!",
        "episode": "Episodio",
        "ep_1": "DEUS EX MACHINA",
        "ep_2": "L'ULTIMO POSTO OVE FU VISTO MIO PADRE",
        "ep_3": "MI LASCIASTI CON QUESTO",
        "ep_4": "FIGHT OVER",
        "ep_5": "VIENI, TI INSEGNO A CUCINARE",
        "ep_6": "OGNIDDOVE, OGNIQUANDO",
        "ep_7": "ARRIVAI A CASA, ALLA BRUTTA NOTIZIA",
        "ep_8": "NON ANDARE",
        "ep_9": "LO STUPENDO SILENZIO DOPO L'ESPLOSIONE",
        "owned_by": "maumakanapa è di proprietà di:",
        "assets": "ogni risorsa utilizzata appartiene a <br> labirhin e ai rispettivi creatori",
        "made_with": "sito web realizzato con amore da:",
        "selector": "/italiano/comics",
        "index": "/italiano/",
        "about": "/italiano/about",
        "about1": "questo sito web è stato realizzato con l'unico scopo di <br> essere un 'backup' nel caso in cui altri siti web che <br> ospitano Mau Makan Apa dovessero smettere di funzionare",
        "about2": "ci è stato messo molto impegno, quindi spero che <br> tu, lettore, possa davvero apprezzarlo, <br> tanto quanto mi è piaciuto creare il sito stesso!",
        "about3": "altre cose verranno aggiunte qui in futuro, come ad esempio: <br> più lingue, più contenuti su MMA e molto altro!",
        "about4": "grazie a tutti coloro che mi hanno motivato a <br> fare davvero questo sito web!",
        "about5": "-laurah",
        "abouth1": "informazioni su questo sito!",
        "notcomic1": "episodio non disponibile...",
        "notcomic2": "che tipo di episodio stai cercando di raggiungere????",
        "notcomic3": "torna ai webcomic",
        "aboutme": "su di me!",
        "aboutme1": "mi chiamo laurah, sono la persona che ha creato <br> questo sito web e sono una normale sviluppatrice web!",
        "aboutme2": "sono anche una youtuber, quindi se vuoi <br> dare un'occhiata al mio canale, puoi farlo qui",
        "aboutme3": "curiosità: questo sito web è open-source <br> su github! puoi darci un'occhiata qui: ",
        "aboutme4": "grazie mille!!!",
        "languages": "visualizza altre lingue qui!",
        "missilecity": "CITTÀ MISSILE",
        "missilecityinfo": "Città Missile è attualmente un webcomic e una serie animata in arrivo, il cui rilascio è previsto dopo l'animazione finale di Mau Makan Apa (in questo caso, l'episodio 9). La serie presenterà personaggi di MMA, ma avrà anche dei propri personaggi unici come: Weewee, Lobi Kalobi e Supernova. Secondo le informazioni attuali, l'animazione sarà basata a Pemucik, e la storia riguarderà Weewee e Lobi, che a un certo punto vengono ammanettati insieme alla ricerca della posizione del malvagio leader supremo, Supernova. <br> (L'animazione ufficiale non è ancora uscita, quindi ecco il video musicale!)",
        "rar": "REVISIONE DOPO REVISIONE",
        "rarinfo": "Revisione Dopo Revisione è un cortometraggio che racconta la storia di Sorbitol, che attualmente lavora presso i Jaya Studios, uno studio di animazione per Jaya TV. Nel cortometraggio, racconta i suoi sentimenti e quanto sia stufo delle revisioni fornite dal suo CEO. Incontra anche Kontol Diamond, che è stato un interesse amoroso per lui, il che implica che alla fine hanno vissuto le loro vite insieme.",
        "tsrf": "LE STELLE STANO CADENDO",
        "tsrfinfo": "In Le Stelle Stando Cadeno, gli amici di scuola Poteto e Oktana sono costretti a separarsi quando Poteto contrae la scabbia. Durante l'isolamento, Poteto si taglia tragicamente le orecchie e riceve protesi di metallo, solo per essere colpito da un fulmine e risuscitato con superpoteri dopo aver parlato con un angelo. Al suo ritorno, Poteto trova Oktana con una donna di nome Bombax, sebbene Oktana sostenga di preferire stare con lui. Arrabbiato perché Oktana prende in giro le sue orecchie protesiche definendole 'sciocche', Poteto usa i suoi nuovi poteri per far piovere stelle cadenti sulla città di Lawu e incolpa pubblicamente Oktana per il caos.",
        "tbtl": "LA GRANDE BUGIA DEL TEMPE",
        "tbtlinfo": "In La grande Bugia Del Tempe, i media affermano falsamente che un nuovo ceppo di tempe causato dalla cenere vulcanica trasforma le persone in mostri di funghi controlla-menti, spingendo il governo a mettere in quarantena Boyolali. Una persona di nome Dino si introduce clandestinamente nella zona di quarantena per trovare il suo amico Rizo, solo per scoprire che l'intera epidemia era una bufala; i 'mostri' sono in realtà solo persone che indossano costumi promozionali da tempe. Spinto da Rizo a salvare il loro cibo culturale, Dino registra prove video e fugge per rivelare la verità online, revocando con successo la quarantena e ripristinando la normalità due mesi dopo.",
        "button2": "visualizza il contenuto!",
        "titlerar": "Revisione Dopo Revisione",
        "subtitlerar": "Mmm.. Sì, Sorbitol.",
        "titletsrf": "Le Stelle Stanno Cadendo",
        "subtitletsrf": "Poteto e le sue orecchie buffe.",
        "titlemc": "Città Missile",
        "subtitlemc": "Lobi, perché sei ammanettato?!",
        "titletbtl": "La Grande Bugia di Tempe",
        "subtitletbtl": "Mmm.. Sì, Sorbitol.",
        "buttonmc": "/italian/mc",
        "buttontsrf": "/italian/tsrf",
        "buttontbtl": "/italian/tbtl",
        "buttonrar": "/italian/rar",
    }
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

    custom_fonts = {
       "russian": "russianlabi, sans-serif",
    }

    fonts = custom_fonts.get(lang, "Labirhin, sans-serif")

    context = {
        "current_lang": lang,
        "t": TRANSLATIONS[lang],
        "fonts": fonts,
    }

    return render(request, "comics_app/about.html", context)

def revindex(request, lang):
    if lang not in TRANSLATIONS:
        lang = "english"

    custom_fonts = {
       "russian": "russianlabi, sans-serif",
    }

    fonts = custom_fonts.get(lang, "Labirhin, sans-serif")

    context = {
       "current_lang": lang,
       "t": TRANSLATIONS[lang],
       "fonts": fonts,
    }

    return render(request, "comics_app/revindex.html", context)

def mcindex(request, lang):
    if lang not in TRANSLATIONS:
        lang = "english"

    custom_fonts = {
       "russian": "russianlabi, sans-serif",
    }

    fonts = custom_fonts.get(lang, "Labirhin, sans-serif")

    context = {
       "current_lang": lang,
       "t": TRANSLATIONS[lang],
       "fonts": fonts,
    }

    return render(request, "comics_app/mcindex.html", context)

def tsrfindex(request, lang):
    if lang not in TRANSLATIONS:
        lang = "english"

    custom_fonts = {
       "russian": "russianlabi, sans-serif",
    }

    fonts = custom_fonts.get(lang, "Labirhin, sans-serif")

    context = {
       "current_lang": lang,
       "t": TRANSLATIONS[lang],
       "fonts": fonts,
    }

    return render(request, "comics_app/tsrfindex.html", context)

def tbtlindex(request, lang):
    if lang not in TRANSLATIONS:
        lang = "english"

    custom_fonts = {
       "russian": "russianlabi, sans-serif",
    }

    fonts = custom_fonts.get(lang, "Labirhin, sans-serif")

    context = {
       "current_lang": lang,
       "t": TRANSLATIONS[lang],
       "fonts": fonts,
    }

    return render(request, "comics_app/tbtlindex.html", context)