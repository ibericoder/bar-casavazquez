import type {Wine} from "../website/src/interfaces/vino";

export const tintos: Wine[] = [
    {
        name: 'the guv`nor',
        id: 'r29',
        prices: {
            '0.1l': '4,00€',
            '0.2l': '7,50€',
            'flasche': '25,00€'
        },
        color: 'red',
        grape: '100% Saint Laurent',
        origin: 'Spanien',
        shortDescription: 'Syrah, Tempranillo.',
        longDescription: 'Diese unkomplizierte Cuvée aus Tempranillo und Syrah ist der perfekte Rotwein für den Feierabend oder eine gemütliche Runde mit Freunden. Da auf einen Barrique-Ausbau bewusst verzichtet wurde, kommen die intensiven Fruchtaromen voll zur Geltung, und der ordentliche Restzuckergehalt macht ihn ausgesprochen süffig. Im Glas strahlt er in sattem Kirschrot, im Bouquet entfalten sich Noten dunkler Beeren und Früchte, untermalt von feinen Röstnuancen. Am Gaumen zeigt er einen guten Körper, bleibt dabei sehr ausgewogen und hinterlässt ein rundes, harmonisches Gesamtbild.',
        image: null,
        characteristics: 'Halbtrocken, fruchtig, interessant',
        available: false
    },
    {
        name: 'Cal Y Canto Tinto',
        id: 'r38',
        prices: {
            '0.1l': '4,00€',
            '0.2l': '7,50€',
            'flasche': '24,00€'
        },
        color: 'red',
        grape: 'Tempranillo, Merlot, Syrah',
        origin: 'Kastilien, Spanien',
        shortDescription: 'Brillantes Dunkelrot, würzige Brombeerfrucht und runder Körper.',
        longDescription: 'Cal Y Canto Tinto stammt aus Kastilien und verbindet Tempranillo, Merlot und Syrah zu einem saftig-frischen Literwein. In der Nase zeigen sich würzige, fruchtbetonte Noten von Brombeere, Weißkirsche und weißem Pfeffer. Am Gaumen wirkt die Cuvée weich mit mittlerem Körper, roten Fruchtanklängen und etwas Tabak, bevor ein rundes Finale den unkomplizierten Charakter unterstreicht.',
        image: null,
        characteristics: 'Trocken, fruchtig, Brombeere, Pfeffer, Tabak',
        available: true
    },
    {
        name: 'David Moreno',
        id: 'r2',
        prices: {'0.1l': "4,80€", '0.2l': "8,90€", 'flasche': '€29,50'},
        color: 'red',
        grape: 'Tempranillo',
        origin: 'Rioja DOCa',
        shortDescription:
            'Trocken, kirschrot mit rubinrotem Schimmer – intensiv, elegant, mit reifen Beeren und feinen Röstaromen.',
        longDescription: 'Dieser Rotwein ist trocken und besticht durch eine tief kirschrote Farbe mit einem rubinroten Schimmer. Im Bouquet entfalten sich intensive, elegante Aromen von reifen roten Beeren, ergänzt durch Trockenfrüchte (wie Pfirsich), feine Röstaromen, Vanille und Nuancen von weichem Eichenholz. Am Gaumen präsentiert sich der Wein seidig, würzig, rund und ausgeglichen, mit reifen Tanninen, die in einem lang anhaltenden Abgang münden. Hergestellt aus handverlesenen Trauben, von denen 75 % entrappt wurden, durchläuft er einen 14-monatigen Barriqueausbau – 8 Monate in amerikanischen und 6 Monate in französischen Eichenfässern – gefolgt von weiterer Flaschenreife.',
        image: null,
        characteristics: 'Trocken, elegant, rund',
        available: true
    },
    {
        name: 'Primitivo - DOPPIO PASSO ',
        prices: {'0.1l': "4,50€", '0.2l': "8,00€", 'flasche': '€24,50'},
        id: 'r32',
        color: 'red',
        grape: '100% Primitivo',
        origin: 'Apulien, Italien',
        shortDescription: 'Fruchtig, würzig, samtig mit schwarzen Beeren und Vanille.',
        longDescription: 'Der Doppio Passo Primitivo ist ein Genussgarant aus der berühmten Weinregion Apuliens. Mit seinem warmwürzigen Schmelz und seiner intensiven Frucht verströmt dieser Süditaliener eine heitere Stimmung und mediterrane Lebensfreude. Im Glas funkelt der Wein in tiefem Rubinrot. Seine Aromen klingen an schwarze Beeren, Kakao und Vanille an. Charakteristisch ist eine großartige Fülle und die weichen Tannine, die sich wie Samt über die Zunge legen. Eine feine Spur Restsüße macht ihn sowohl für Trocken-Trinker als auch für Einsteiger höchst attraktiv. Ein Klassiker – egal wer mittrinkt, sie oder er wird diesen Tropfen garantiert ins Herz schließen. Mit 13% Alkoholgehalt und 4 Jahren Lagerfähigkeit.',
        image: null,
        characteristics: 'Halbtrocken, fruchtig, würzig, samtig',
        available: true
    },
    {
        name: 'Viña Albali - Gran Reserva',
        id: 'r31',
        prices: {
            '0.1l': '4,50€',
            '0.2l': '9',
            'flasche': '28,50€'
        },
        color: 'red',
        grape: 'Tempranillo',
        origin: 'Valdepenas, Spanien',
        shortDescription: 'trocken, rauchig, holzig.',
        longDescription: 'Ein Gran Reserva muss insgesamt fünf Jahre reifen, davon mindestens zwei Jahre im Eichenfass. Der Viña Albali Gran Reserva aus dem Jahr erfüllt diese Vorgaben mühelos. Er stammt aus der spanischen Region Valdepeñas in Kastilien-La Mancha und wird ausschließlich aus der Tempranillo-Traube gekeltert. Valdepeñas liegt im Süden der Hochebene Zentralspaniens, geschützt von der Sierra Morena, was zu einem gemäßigten, stark kontinental geprägten Klima führt – im Sommer steigen die Temperaturen oft auf bis zu 40 °C, im Winter können sie bis auf –10 °C fallen. Die Weinberge stehen auf etwa 700 Metern Höhe auf überwiegend kalkhaltigen Böden mit älteren Kreideablagerungen. Der Viña Albali Gran Reserva gehört zur Albali-Linie des Weinguts Félix Solis. Seinen Namen trägt er nach einem Stern im Sternbild des Wassermanns und soll laut Félix Solis die Lebensfreude und Lebendigkeit der Spanier verkörpern.',
        image: null,
        characteristics: 'trocken, rauchig, holzig, Körper',
        available: false
    },
    {
        name: 'Marques de Cáceres',
        id: 3,
        prices: {'flasche': '€37,50'},
        color: 'red',
        grape: 'Tempranillo',
        origin: 'Rioja DOCa',
        shortDescription:
            'Fruchtig-frischer Wein mit dunklen Früchten und würzigem Holz im Geschmack.',
        longDescription: 'Marqués de Cáceres – ein Synonym für herausragende Qualität – präsentiert in diesem Wein eine harmonische Vereinigung der Rebsorten Tempranillo, Garnacha und Graciano. Diese Crianza besticht durch ein Bouquet dunkler Früchte und sonnenreifer Kirschen, untermalt von würzigen Nuancen von Vanille, Nelke und Lakritze, die durch den Einsatz von gewürztem Eichenholz noch intensiviert werden. Am Gaumen zeigt sich der Wein frisch und fruchtig, mit feinen Anklängen von Erdbeeren und Himbeeren, während seine festen Tannine für eine strukturierte Textur sorgen, die hervorragend zu gerösteten Nüssen und mineralischen Noten passt.',
        image: null,
        characteristics: '(NUR FLASCHE) Trocken, würzig',
        available: false
    },
    {
        name: 'Aventura - Vinos del Viento',
        id: 'r30',
        prices: {
            '0.1l': '4,00€',
            '0.2l': '7,50€',
            'flasche': '25,00€'
        },
        color: 'red',
        grape: '60% Grenache, 30% Syrah, 10% Cabernet Sauvignon',
        origin: 'Campo de Borja, Spanien',
        shortDescription: 'trocken, saftig.',
        longDescription: 'Der Aventura präsentiert sich im Glas in tiefem Rubinrot. In der Nase entfalten sich intensive Noten von roten und schwarzen Beeren, ergänzt durch würzige Anklänge von Thymian und schwarzem Pfeffer. Am Gaumen überzeugt er mit weicher, saftiger Textur, reifen Tanninen und einer sehr ausgewogenen Balance. Diese spanische Cuvée vereint drei Rebsorten und ist als Hommage an die nördliche Rhône gedacht. Garnacha und Syrah schenken ihm florale Würze und seinen charakteristischen Pfeffer-Touch, während Cabernet Sauvignon eine reichhaltige, konzentrierte Fülle beisteuert, die die Tannine harmonisch ausgleicht.',
        image: null,
        characteristics: 'trocken, saftig, leicht, sommerlich',
        available: false
    },
    {
        name: 'Barón de Ley Rioja Reserva ',
        id: 17,
        prices: {'flasche': '€39,50'},
        color: 'red',
        grape: 'Tempranillo, Graciano, Maturana',
        origin: 'Spanien, Rioja DOCa',
        shortDescription:
            'Ein klassischer Rioja Reserva mit ausgewogener Fruchtigkeit und eleganter Tanninstruktur – klassisch trocken.',
        longDescription:
            'Der Barón de Ley Rioja Reserva 2019 präsentiert sich in einem tiefen Rubinrot und entfaltet ein komplexes Bouquet aus reifen roten Früchten, feinen Gewürznoten und dezenten Eichenakzenten. Am Gaumen überzeugt er mit einer harmonischen Balance zwischen Fruchtigkeit und strukturierten Tanninen, die in einem langen, eleganten Abgang mündet. Ein Wein, der die Tradition der Rioja DOCa authentisch widerspiegelt.',
        image: null,
        characteristics: 'Trocken, klassisch, elegant, ausgewogen',
        available: true
    },
    {
        name: 'EMBOCADERO',
        id: 1,
        prices: {'flasche': '€39,50'},
        color: 'red',
        grape: '100% Tinto Fino',
        origin: 'Ribera del Duero',
        shortDescription: 'Eleganter, trockener Rotwein mit lebendigen Beeren- und Zedernholznoten.',
        longDescription: 'Embocadero Ribera del Duero 2021 – Dieser trockene Rotwein aus der renommierten Region Ribera del Duero besticht durch eine elegante, feinkörnige Tanninstruktur und animierende Säure. Sein lang anhaltender Abgang ist von Nuancen geprägt, die an Zedernholz erinnern. Im Bouquet entfalten sich lebendige Fruchtnoten von Schlehen, dunklen Beeren und Pflaumen, ergänzt durch subtile Anklänge von Lorbeer, Süßholz und einem Hauch Vanille. Am Gaumen setzt sich der Wein mit einer weichen Holznote in saftige Aromen von Kirsch, Schlehen und Beeren fort – ein harmonischer Wein, der Tiefe und Finesse vereint.',
        image: null,
        characteristics: 'Trocken, vollmundig, tiefrot, ehrlich',
        available: false
    },
    {
        name: 'Borgo Scopeto Chianti Classico Riserva 2017 DOCG',
        id: 16,
        prices: {'flasche': '€45,00'},
        color: 'red',
        grape: 'Sangiovese',
        origin: 'Italien, Toskana',
        shortDescription:
            'Ein kraftvoller Chianti Classico Riserva mit reifen Fruchtnoten, würzigen Akzenten und strukturierten Tanninen – klassisch trocken.',
        longDescription:
            'Der Borgo Scopeto Chianti Classico Riserva 2017 DOCG präsentiert sich in einem tiefen Rubinrot mit einem komplexen Bouquet aus reifen roten Früchten, getrockneten Kräutern und würzigen Noten. Die gut integrierten Tannine und die ausgewogene Säure verleihen ihm eine beeindruckende Struktur und einen langen, eleganten Abgang, der Kenner toskanischer Weine begeistert.',
        image: null,
        characteristics: 'Trocken, kraftvoll, strukturiert, elegant',
        available: false
    },
    {
        name: 'Raineri Zovetto Dogliani 2018',
        id: 15,
        prices: {'flasche': '€32,50'},
        color: 'red',
        grape: 'Barbera | Dolcetto',
        origin: 'Italien, Piemont',
        shortDescription:
            'Ein intensiver Rotwein mit reifen Fruchtaromen und feiner Tanninstruktur – klassisch trocken.',
        longDescription:
            'Der Raineri Zovetto Dogliani 2018 zeigt sich in einem tiefen Rotton mit einem Bouquet aus dunklen Beeren, reifen Kirschen und feinen Gewürznoten. Er ist absolut trocken, mit einer ausgewogenen Säure und samtigen Tanninen, die ihm eine elegante Struktur verleihen – typisch für die Weinregion des Piemont.',
        image: null,
        characteristics: 'Trocken, intensiv, fruchtig, elegant',
        available: false
    },
    {
        name: 'CASTELLO DI BIBBIONE Chianti Classico Riserva 2017',
        id: 14,
        prices: {'flasche': '€39,00'},
        color: 'red',
        grape: 'Sangiovese',
        origin: 'Italien, Toskana',
        shortDescription:
            'Ein traditioneller Chianti Classico Riserva mit komplexen, reifen Fruchtnoten und würzigen Akzenten – klassisch trocken.',
        longDescription:
            'Der Chianti Classico Riserva aus dem Castello di Bibbione Castelli del Grevepesa zeigt sich in einem rubinroten Farbton. Das Bouquet vereint Aromen von reifen Kirschen, getrockneten Kräutern und subtilen Gewürznoten, während die strukturierte Tanninführung und ausgewogene Säure einen langen, eleganten Abgang bieten – ein Wein, der die Tradition der Toskana widerspiegelt.',
        image: null,
        characteristics: 'Trocken, traditionell, komplex, elegant',
        available: true
    },
    {
        name: "1934 CVS Canicatti 2019",
        id: 13,
        prices: {'flasche': '€39,50'},
        color: 'red',
        grape: "Nero d'Avola",
        origin: 'Italien, Sizilien (Canicatti)',
        shortDescription:
            'Ein kraftvoller, vollmundiger Rotwein mit intensiven Fruchtaromen – klassisch trocken.',
        longDescription:
            'Der "1934" CVS Canicatti 2019 präsentiert sich in einem tiefen Rubinrot mit einem Bouquet aus dunklen Kirschen, Pflaumen und einem Hauch Gewürzen. Er ist absolut trocken, mit weichen Tanninen und einer harmonischen Struktur, die das Terroir Siziliens eindrucksvoll widerspiegelt.',
        image: null,
        characteristics: 'Trocken, kraftvoll, vollmundig, elegant',
        available: false
    },
    {
        name: 'Barolo Terre dei Roveri 2020',
        id: 11,
        prices: {'flasche': '€55,00'},
        color: 'red',
        grape: 'Nebbiolo',
        origin: 'Italien, Piemont',
        shortDescription:
            'Ein intensiver Barolo mit komplexem Aromenspektrum und markanten Tanninen – klassisch trocken.',
        longDescription:
            'Der Barolo Terre dei Roveri 2020 besticht durch sein tiefes Rubinrot und ein Bouquet aus reifen roten Früchten, Teer und Gewürzen. Er ist absolut trocken, kraftvoll und elegant, mit intensiven Tanninen, die ihn zu einem anspruchsvollen Wein für Kenner der piemonteschen Weinkultur machen.',
        image: null,
        characteristics: 'Trocken, kraftvoll, elegant, tanninreich',
        available: true
    },
    {
        name: 'Dicatum',
        id: 'w173',
        prices: {
            flasche: '69,00€'
        },
        color: 'red',
        grape: 'Sangiovese',
        origin: 'Italien, Toskana',
        shortDescription:
            'Ein kraftvoll gereifter Sangiovese mit Tiefe und Eleganz aus der toskanischen Fattoria Montellori.',
        longDescription:
            'Der Dicatum 2010 von Fattoria Montellori ist ein reinsortiger Sangiovese aus einem exzellenten Jahrgang. In der Nase zeigt er Aromen von getrockneten Kirschen, Leder, Gewürzen und einem Hauch Tabak. Am Gaumen überzeugt er mit dichter Struktur, feinkörnigem Tannin und einer beeindruckenden Länge. Die Reife verleiht ihm eine komplexe, fast samtige Tiefe. Ein Wein für besondere Anlässe – elegant, charaktervoll und langlebig.',
        image: null,
        characteristics: 'Trocken, gereift, Kirsche, Leder, Tabak',
        available: true
    },
    {
        name: 'Schneider Ursprung',
        id: 'r33',
        prices: {
            'flasche': '34,50€'
        },
        color: 'red',
        grape: 'Cuvée - Cabernet Sauvignon, Merlot, Portugieser',
        origin: 'Pfalz, Deutschland',
        shortDescription: 'Trocken, elegant mit Cassis, Zwetschgen und Paprika.',
        longDescription: 'Mit Markus Schneiders Ursprung hat alles begonnen. 1998 erschien der erste Jahrgang dieses Weins und hat sich gleich einen Platz unter den beliebtesten Rotweinen Deutschlands verdient. Fast schwarz präsentiert sich die Cuvée im Glas. Der Wein duftet nach Cassis und Zwetschgen, Paprika, Zedernholz, Grafit und verströmt zudem einen Hauch von Minze und Pfeffer. Eine Cuvée mit hohem Anspruch für unkomplizierten Genuss. Mit 13,5% Alkoholgehalt ist dieser elegante Qualitätswein trocken und vollmundig.',
        image: null,
        characteristics: 'Trocken, elegant, Cassis, Zwetschgen, Paprika',
        available: true
    },
    {
        name: 'Sirica',
        id: 'r34',
        prices: {
            'flasche': '37,50€'
        },
        color: 'red',
        grape: '100% Sirica',
        origin: 'Kampanien, Italien',
        shortDescription: 'Rubinrot mit intensiven Aromen von roten Früchten und zarten pflanzlichen Noten.',
        longDescription: 'Der Rosso Sirica di Feudi di San Gregorio stammt aus Weinbergen im Herzen der bezaubernden Landschaft von Irpinia. Es wird ausschließlich aus Sirica-Trauben hergestellt, die nur von Hand geerntet und ausgewählt werden. Die Fermentation erfolgt unter Mazeration in Stahltanks für ca. 3 Wochen. Anschließend reift der Wein 12 Monate in mittel gerösteten Barriques aus französischer Eiche und 9 Monate in der Flasche. Die Sirica hat eine rubinrote Farbe. Die Nase öffnet sich mit intensiven Empfindungen von roten Früchten, angereichert mit zarten pflanzlichen Noten. Am Gaumen ist er frisch und weich, mit weichen Tanninen, die einen würzigen und anhaltenden Abgang begleiten. Perfekt zu allen Fleischgerichten.',
        image: null,
        characteristics: 'Trocken, frisch, weich, würzig, Rote Früchte',
        available: true
    },
    {
        name: 'Knipser Kirschgarten GG',
        id: 'r35',
        prices: {
            'flasche': '125,00€'
        },
        color: 'red',
        grape: 'Spätburgunder',
        origin: 'Laumersheim, Pfalz, Deutschland',
        shortDescription: 'Grosses Gewächs mit rauchigem Holz, viel Substanz und eleganter Kirschfrucht.',
        longDescription: 'Der Spätburgunder Kirschgarten 2015 vom Weingut Knipser stammt aus den kalkreichen Parzellen des historischen Kirschgartens in Laumersheim und reifte in Barriques. In der Nase zeigen sich rauchige Röstaromen, Staub von Pfeffer und Gewürzen, am Gaumen viel Saft, Substanz und ein dichtes Tanningerüst, das dennoch Eleganz bewahrt. Mit 13,8 % Vol. und nur 0,5 g Restzucker ist dieses VDP.Große Gewächs knochentrocken, vielschichtig und ideal zu Lamm, Wild oder gegrilltem Rind.',
        image: null,
        characteristics: 'Trocken, elegant, strukturiert, würzig, Kirschfrucht',
        available: true
    },
    {
        name: 'Schneider Steinsatz Cuvée',
        id: 'r36',
        prices: {
            'flasche': '67,50€'
        },
        color: 'red',
        grape: '71% Merlot, 28% Cabernet Franc, 1% Petit Verdot',
        origin: 'Pfalz, Deutschland',
        shortDescription: 'Dunkle Cuvée mit Salz, Feuerstein und kraftvollem Biss.',
        longDescription: 'Der Steinsatz Cuvée 2016 vom Weingut Markus Schneider verbindet 71 % Merlot mit Cabernet Franc und einem Hauch Petit Verdot. Ein Körnchen Salz und etwas Feuerstein prägen die Nase, am Gaumen zeigt sich die Cuvée dicht, dunkel und leicht bissig, bleibt dabei aber saftig und lang. Mit 14 % Alkohol, 1,9 g Restzucker und markanter Struktur passt dieser trockene Pfälzer ideal zu Wild und herzhaften Fleischgerichten.',
        image: null,
        characteristics: 'Trocken, dicht, dunkel, würzig, saftig',
        available: true
    },
    {
        name: 'Campofiorin Rosso del Veronese',
        id: 'r37',
        prices: {
            'flasche': '45,50€'
        },
        color: 'red',
        grape: 'Corvina, Rondinella, Molinara',
        origin: 'Veneto, Italien',
        shortDescription: 'Gut strukturierter, geschmeidiger Veroneser mit weichen Tanninen.',
        longDescription: 'Der Campofiorin Rosso del Veronese Bonacosta 2014 von Masi stammt aus dem hügeligen Valpolicella Classico, wo Corvina, Rondinella und Molinara auf 70 bis 400 Metern Höhe reifen. Nach dem Ausbau im Tonneau zeigt der Wein eine dichte Struktur, komplexe dunkle Frucht und samtene Tannine, weshalb er gerne als kleiner Amarone bezeichnet wird. Weich, rund und dennoch charaktervoll passt er hervorragend zu kräftigen Fleischgerichten oder gereiftem Käse.',
        image: null,
        characteristics: 'Trocken, strukturiert, geschmeidig, komplex',
        available: true
    },
];
