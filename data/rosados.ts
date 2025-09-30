import type {Wine} from "../website/src/interfaces/vino";

export const rosados: Wine[] = [
    {
        name: 'Calalenta ("Kühle Nacht")',
        id: 21,
        prices: {
            '0.1l': '4,00€',
            '0.2l': '7,50€',
            'flasche': '25,00€'
        },
        color: 'rosé',
        grape: '100% Merlot',
        origin: 'Abruzzen, Italien',
        shortDescription: 'Trocken, leichter Rosé aus Merlot-Trauben mit zartem Hellrosa und feinen Fruchtaromen.',
        longDescription: 'Der Calalenta Rosé (auch "Kühle Nacht" genannt) stammt aus den Abruzzen und wird aus 100% Merlot gekeltert. Dank kühler Nachtlese bewahrt er seine frischen Aromen von Erdbeeren, Kirschen und einem Hauch floraler Noten. Ein leichtes, trockenes Geschmacksprofil mit dezenter Säure und einem angenehm fruchtigen Abgang – ideal als Aperitif oder zu leichten Gerichten.',
        image: null,
        characteristics: 'trocken, leicht, hellrosa, rosé, fruchtig, erfrischend',
        available: false
    },
    {
        name: "Knipser 'Rosé 24'",
        id: 822,
        prices: {
            '0.1l': '6,50€',
            '0.2l': '12,50€',
            "flasche": "39,50€"
        },
        color: "rosé",
        grape: "60% Spätburgunder, 20% Dornfelder, 20% Cabernet‑Sorten",
        origin: "Laumersheim, Pfalz, Deutschland",
        shortDescription: "Trocken, frisch‑fruchtiger VDP‑Gutsrosé mit knackigen roten & gelben Fruchtnoten.",
        longDescription: "Ein eleganter Rosé‑Gutswein aus Laumersheim (Pfalz), cuvée aus Spätburgunder, Dornfelder und Cabernet‑Sorten. Feines kupfer‑/antikrosa, Aromen von Beeren, Zitrus und Kräutern. Am Gaumen saftig, harmonisch und rund – ideal pur oder zu Gegrilltem, Salaten und Antipasti.",
        image: null,
        characteristics: 'Trocken, fruchtig, frisch',
        available: true
    },
    {
        name: 'Rosa Dei Frati',
        id: 22,
        prices: {
            '0.1l': '6,00€',
            '0.2l': '11,50€',
            'flasche': '37,50€'
        },
        color: 'rosé',
        grape: 'Gropello, Marzemino, Sangiovese, Barbera',
        origin: 'Lombardia, Italien',
        shortDescription: 'Trocken, komplexer Rosé mit griffiger Struktur und intensiven Fruchtnoten.',
        longDescription: 'Der Rosa Dei Frati ist ein charaktervoller Rosé aus der Lombardei. Durch die Kombination der Rebsorten Gropello, Marzemino, Sangiovese und Barbera entsteht ein komplexes Aroma von roten Beeren, frischen Blüten und feinen Gewürznoten. Eine lebhafte Säure und eine griffige Struktur verleihen ihm eine vielseitige Einsetzbarkeit, ob als Aperitif oder zu Antipasti und leichten Pastagerichten.',
        image: null,
        characteristics: 'Trocken, komplex, griffig, rosé, italienisch, aromatisch',
        available: false
    },
    {
        name: 'Arrogant Frog',
        id: 23,
        prices: {
            '0.1l': '4,80€',
            '0.2l': '8,90€',
            'flasche': '27,50€'
        },
        color: 'rosé',
        grape: 'Syrah',
        origin: 'Coteaux du Languedoc, Frankreich',
        shortDescription: 'Trocken, erfrischender Syrah Rosé mit intensiven Aromen von roten Beeren und Zitrus.',
        longDescription: 'Der Arrogant Frog Syrah Rosé aus dem Languedoc besticht durch seine lebendige Frische und elegante Struktur. Er entfaltet Aromen von roten Beeren, Zitrusfrüchten und floralen Nuancen, was ihm einen einzigartigen Charakter verleiht. Feine Tannine und eine ausgewogene Säure machen ihn zum idealen Begleiter zu leichten Gerichten und sommerlichen Anlässen.',
        image: null,
        characteristics: 'Trocken, knackig, fruchtig, rosé, erfrischend, elegant',
        available: true
    },
    {
        "name": "Guv’nor Rosé",
        "id": 28,
        "prices": {
            "0.1l": "4,50€",
            "0.2l": "8,50€",
            "flasche": "29,00€"
        },
        "color": "rosé",
        "grape": "Blend aus Garnacha, Tempranillo und Bobal",
        "origin": "Spanien",
        "shortDescription": "Pale Rosé mit roten Beeren, frischer Säure und cremigem Finish.",
        "longDescription": "Helles, attraktives Rosé, geprägt von Aromen roter Früchte wie Erdbeere, Himbeere und Johannisbeere. Am Gaumen frisch, mundfüllend mit feiner Säure und weichem, anhaltendem Abgang. Leicht und mehrish, ideal zu Tapas, Meeresfrüchten oder solo. 13 % Vol, Trinktemperatur 8–10 °C.",
        "image": null,
        "characteristics": "trocken, fruchtig, frisch, geschmeidig",
        "available": true
    },
    {
        name: 'El Coto Rosado',
        id: 26,
        prices: {
            '0.1l': '4,00€',
            '0.2l': '7,50€',
            'flasche': '25,00€'
        },
        color: 'rosé',
        grape: '90% Tempranillo, 10% Garnacha',
        origin: 'Spanien, Rioja DOCa',
        shortDescription: 'Frischer, eleganter Rosé mit Aromen von Erdbeeren und roten Johannisbeeren.',
        longDescription: 'Der El Coto Rosado präsentiert sich in einem blassen Lachsrosa und besticht durch ein Bouquet von frischen Erdbeeren und roten Johannisbeeren. Am Gaumen zeigt er sich rund und elegant mit einer lebendigen Frische, die ihn zu einem idealen Begleiter für Salate, Geflügelgerichte und Meeresfrüchte macht. Genießen Sie ihn gut gekühlt.',
        image: null,
        characteristics: 'Trocken, frisch, fruchtig, elegant',
        available: true
    },
    {
        name: 'Minuty Rosé',
        id: 24,
        prices: {'0.1l': '6,50€', '0.2l': '11,50€', 'flasche': '€38,50'},
        color: 'rosé',
        grape: 'Grenache, Cinsault, Syrah',
        origin: 'Frankreich, Côtes de Provence',
        shortDescription: 'Frischer, eleganter Rosé mit zarten Frucht- und Zitrusnoten.',
        longDescription: 'Der M de Minuty Rosé ist ein eleganter Roséwein aus der Provence mit einer zarten, lachsfarbenen Erscheinung. Er verführt mit feinen Aromen von weißen Blüten, Erdbeeren, Johannisbeeren und einem Hauch Zitrus. Leicht, trocken und lebendig am Gaumen – mit einem frischen Abgang und ausgewogener Säure. Ideal zu mediterraner Küche oder als stilvoller Aperitif.',
        image: null,
        characteristics: 'Trocken, frisch, leicht, zitrus, floral',
        available: true
    },
    {
        name: 'PINK St. Laurent Rosé',
        id: 28,
        prices: {
            '0.1l': '4,50€',
            '0.2l': '8,50€',
            'flasche': '27,50€'
        },
        color: 'rosé',
        grape: '100% Saint Laurent',
        origin: 'Pfalz, Deutschland',
        shortDescription: 'Halbtrocken, fruchtig, leicht und aromatisch.',
        longDescription: 'Der PINK St. Laurent Rosé von Tina Pfaffmann aus der Pfalz präsentiert sich halbtrocken mit lebendigen Aromen von Rumtopf, Mon Cheri-Kirsche und wildem Beerenmus. Eine Restsüße von 11,7 g/l sowie eine feine Säurestruktur sorgen für ein ausgewogenes Mundgefühl und erfrischenden Abgang.',
        image: null,
        characteristics: 'Halbtrocken, fruchtig, leicht, aromatisch, rosé, frisch',
        available: false
    },
    {
        name: 'Miraval',
        id: 117,
        prices: {'flasche': '€49,00'},
        color: 'rosé',
        grape: 'Cinsault, Grenache, Syrah, Rolle',
        origin: 'Frankreich, Provence',
        shortDescription: 'Eleganter Rosé mit Frische, Frucht und feiner Mineralität.',
        longDescription: 'Der Miraval Rosé aus der Provence ist ein erfrischender, eleganter Wein mit zarter Lachsfarbe. In der Nase zeigen sich Aromen von frischen Himbeeren, weißen Blüten und einem Hauch Limette. Am Gaumen überzeugt er mit einer lebendigen Frische, feiner Mineralität und einer harmonischen Balance aus Frucht und Säure. Ein stilvoller Rosé, perfekt für warme Tage und mediterrane Speisen.',
        image: null,
        characteristics: 'Trocken, frisch, floral, mineralisch',
        available: true
    }
]