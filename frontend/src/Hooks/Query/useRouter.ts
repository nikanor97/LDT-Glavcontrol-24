import {useRouter as useNextRouter, NextRouter} from 'next/router';


export const useRouter = <T>() => {
    const nextRouter = useNextRouter() as NextRouter & {
        query: T

    }
    return nextRouter;
}