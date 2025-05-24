export interface Game {
    appid: string,
    name: string,
    releaseDate: string,
    detailedDescription: string,
    shortDescription: string,
    headerImage: string,
    developer: string,
    publisher: string,
    screenshots: string[],
    tags: string[],
    recommendationScore: number
}