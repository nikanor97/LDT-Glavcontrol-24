


export const getOffsetByPage = (page: number, limit: number) => {
    return (page - 1) * limit;
}