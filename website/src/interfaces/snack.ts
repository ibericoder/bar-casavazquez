interface SnackVariant {
    variantName: string;
    price: string;
    short_desc: string;
    long_desc: string;
}

export interface Snack {
    name: string;
    veggie: boolean;
    variants: SnackVariant[];
}