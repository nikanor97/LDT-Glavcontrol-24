


export const getPageByOffset = (offset: number, limit: number) => {
    return Math.floor(offset / limit) + 1
}