import qs from 'qs';


export const getQueries = <T>(url: string) => {
    let search: string | undefined = '';
    let buffer = url; 
    if (buffer.indexOf('#') !== -1) {
        //Если есть якорь вырезаем его, он всегда идет после всех квери параметров
        //?test=asd#anchor
        buffer = buffer.split('#')[0];
    }
    if (buffer.indexOf('?') !== -1) {
        search = buffer.split('?')[1];
    }
    return qs.parse(search || '') as unknown as T
}