export interface Notification {
    title: string
    text: string
    image?: string
    roundedImage?: boolean
    createdAt: string | Date
    linkText?: string
    linkTo?: string
}