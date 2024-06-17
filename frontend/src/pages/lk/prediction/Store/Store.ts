import { createPrivateStore, iStore } from "@/Utils/Zustand/createPrivate";
import {iActions, iState} from './types';
import dayjs from "dayjs";

export const {
    ContextComponent,
    usePrivateStore
} = createPrivateStore<iStore<iState, iActions>>('lk/predictions', (set) => ({
    params: {
        limit: 10,
        offset: 0,
        quarter: 1,
        year: 2023
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