import { createPrivateStore, iStore } from "@/Utils/Zustand/createPrivate";
import {iActions, iState} from './types';
import dayjs from "dayjs";

export const {
    ContextComponent,
    usePrivateStore
} = createPrivateStore<iStore<iState, iActions>>('lk/orders', (set) => ({
    params: {
        limit: 10,
        offset: 0
    },
    actions: {
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