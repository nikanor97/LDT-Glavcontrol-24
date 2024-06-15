import React, {createContext, useContext, useRef, useEffect} from 'react';
import {useStore} from 'zustand';
import {StateCreator} from 'zustand/vanilla';
import {createStore, ExtractState} from './create';
export {type iStore} from './create';
//Сквозной каунт для упрощения навигации в devtools
let count = 0;

//Функция, возвращающая хук и контекст для приватного хранилища (изолировано между инстансами одного и того же компонента)
export const createPrivateStore = function<T>(storeName: string, initializer: StateCreator<T, [["zustand/immer", never]], []>) {
    const getStore = () => createStore(initializer, {
        name: `${storeName}_${count}`
    });
    type Store = ReturnType<typeof getStore>;
    const ContextProvider = createContext<null | Store>(null);
    const ContextComponent = (props: React.PropsWithChildren<{}>) => {
        const storeRef = useRef<Store>();
        if (!storeRef.current) {
            count++;
            storeRef.current = getStore();
        }
        useEffect(() => () => {
            if (storeRef.current) {
                //Выполняем сброс состояния на null на всякий случай
                //@ts-ignore
                storeRef.current.setState(null);
            }
        }, []);
        return (
            <ContextProvider.Provider value={storeRef.current}>
                {props.children}
            </ContextProvider.Provider>
        )
    }

    const usePrivateStore = function <U>(selector: (state: ExtractState<ReturnType<typeof getStore>>) => U) {
        const context = useContext(ContextProvider);
        if (!context) throw new Error('Отсутствует контекст для хранилища');
        return useStore(context, selector);
    }
    
    return {
        ContextComponent,
        usePrivateStore
    }
}