

export const getMeasurementNumber = (number: number, parseLessItem: boolean = true) => {
    //Получили количество разрядов
    const digitCount = number.toString().length;
    const data = [
        {
            count: 12,
            measurement: 'трлн.'
        },
        {
            count: 9,
            measurement: 'млрд.'
        },
        {
            count: 6,
            measurement: 'млн.'
        },
        {
            count: 3,
            measurement: 'тыс.'
        }
    ];
    for (let index = 0; index < data.length; index = index + 1) {
        const item = data[index];
        if (digitCount > item.count) {
            return {
                number,
                beautified: number / Math.pow(10, item.count),
                measurement: item.measurement
            }
        }
    }
    //Если число очень маленькое
    const lastItem = data[data.length - 1];
    if (parseLessItem) {
        //Если включена опция парсинга мелкий чисел
        return {
            number,
            beautified: number / Math.pow(10, lastItem.count),
            measurement: lastItem.measurement
        }
    } else {
        return {
            number,
            beautified: number,
            measurement: null
        }
    }

}