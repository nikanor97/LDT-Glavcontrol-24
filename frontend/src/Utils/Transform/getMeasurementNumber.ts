

export const getMeasurementNumber = (number: number) => {
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
    
    for (const measurement of data) {
        if (digitCount > measurement.count) {
            return {
                number,
                beautified: number / Math.pow(10, measurement.count),
                measurement: measurement.measurement
            }
            break;
        }
    } 
}