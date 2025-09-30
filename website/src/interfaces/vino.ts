type Color = 'red' | 'white' | 'rosé';

export interface Wine {
    id: string|number;
    name: string;
    prices: {
        '0.1l'?: string;
        '0.2l'?: string;
        flasche: string;
    };
    color: Color;
    grape: string;
    origin?: string;
    shortDescription?: string;
    longDescription?: string;
    image?: string | null;
    characteristics?: string;
    available: boolean;
}
