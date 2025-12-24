import scheibelImage from "../assets/images/scheibel_marille.png";
import silvesterImage from "../assets/images/silvester.png";
import roseImage from "../assets/images/riscal_rose.png";
import giftCardImage from "../assets/images/gutschein.jpg";

export interface FeaturedPromo {
  id: string;
  title: string;
  description: string;
  image?: string;
}

export const featuredPromos: FeaturedPromo[] = [
  {
    id: "scheibel",
    title: "Der perfekte Abschluss",
    description: "Hochwertige Brände von Scheibel, um den Abend abzurunden. Jetzt probieren!",
    image: scheibelImage,
  },
  {
    id: "silvester",
      title: "Silvester-Tickets",
    
    description: "Jetzt erhältlich - 49€ inklusive Aperitif, kaltem Buffet, und Prosecco um Mitternacht",
    image: silvesterImage
  },
  {
    id: "limited-rose",
    title: "Limited Winter Rosé",
    description: " Unsere Winter Rosé von Marqués de Riscal und Baron de Ley  – 34,50€ solange der Vorrat reicht",
    image: roseImage
  },
  {
    id: "gift-card",
    title: "Geschenkgutschein",
    description: "Verschenke Abende mit leckeren Drinks und Tapas - vor Ort erhältlich",
    image: giftCardImage
  }
];
