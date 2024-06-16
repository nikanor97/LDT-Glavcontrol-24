import { createPrivateStore, iStore } from "@/Utils/Zustand/createPrivate";
import {iActions, iState} from './types';
import dayjs from "dayjs";

export const {
    ContextComponent,
    usePrivateStore
} = createPrivateStore<iStore<iState, iActions>>('lk/orders', (set) => ({
    params: {
        limit: 20,
        offset: 0
    },
    selected: [],
    actions: {
        setSelected: (items) => {
            set((state) => {
                state.selected = items;
            })
        },
        changeParams: (params) => {
            set((state) => {
                state.params = {
                    ...state.params,
                    ...params
                }
            })
        }
    }
}))