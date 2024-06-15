

export type iState = {
    orders: {
        year: number;
        quarter: number;
    }
    remains: {
        year: number;
        quarter: number;
    }
}

export type iActions = {
    setOrderDates: (year: number, quarter: number) => any
    setRemainsDates: (year: number, quarter: number) => any
}