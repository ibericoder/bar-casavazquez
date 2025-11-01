type Color = 'red' | 'white' | 'rosé';

export interface Wine {
    id: string|number;
    name: string;
    price_bottle: number | null;
    price_glass_01: number | null;
    price_glass_02: number | null;
    color: Color;
    grape: string;
    origin?: string;
    short_description?: string;
    long_description?: string;
    image?: string | null;
    characteristics?: string;
    available: boolean;
}
