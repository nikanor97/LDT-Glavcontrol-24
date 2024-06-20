export const numberFormatter = (value?:string|number, splitter = ' ') => `${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, splitter);

export default numberFormatter;