import type {ReactElement} from 'react'
import type {NextPage as NextPageNative} from 'next'
import type {AppProps as AppPropsNative} from 'next/app'
import {DehydratedState} from '@tanstack/react-query';
import {User} from '@/Types';


export type NextPage<P = {}, IP = P> = NextPageNative<P, IP> & {
    getLayout?: (page: ReactElement) => ReactElement;
    Role?: 
        User.Role.Result[] | 
        ((roles: User.Role.ResultValues) => boolean);
}

export type CustomAppProps = {
    dehydratedState?: DehydratedState;
}

export type AppProps = AppPropsNative<CustomAppProps> & {
    Component: NextPage;
}