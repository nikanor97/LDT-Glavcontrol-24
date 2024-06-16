import dayjs from "dayjs"



export const getDateValue = (format: string = 'YYYY-MM-DD') => (value: string) => {
    return { 
        value: value && dayjs(value, {format}) 
    }
}

export const getNormalizedValue = (format: string = 'YYYY-MM-DD') => (value: string) => {
    return value && dayjs(value).format(format)
} 