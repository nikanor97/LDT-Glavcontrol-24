import { isServer } from '@/Utils/Server/isServer';
import {create as createNative, createStore as createStoreNative} from 'zustand';
import {devtools, DevtoolsOptions} from 'zustand/middleware';
import {immer} from 'zustand/middleware/immer'
import {StateCreator} from 'zustand/vanilla';

export type ExtractState<S> = S extends {
    getState: () => infer T;
} ? T : never;


export type iStore<S, A = null> = A extends Object ? S & {actions: A} : S;



export const create = <T>(initializer: StateCreator<T, [["zustand/immer", never]], []>, options?: DevtoolsOptions) => 
    createNative<T>()(devtools(immer<T>(initializer), {
        ...options,
        enabled: process.env.NODE_ENV === 'development' && !isServer,
    }));

export const createStore = <T>(initializer: StateCreator<T, [["zustand/immer", never]], []>, options?: DevtoolsOptions) => 
    createStoreNative<T>()(devtools(immer<T>(initializer), {
        ...options,
        enabled: process.env.NODE_ENV === 'development' && !isServer,
    }))


