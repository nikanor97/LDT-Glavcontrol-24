import { createPrivateStore, iStore } from "@/Utils/Zustand/createPrivate";
import {iActions, iState} from './types';
import dayjs from "dayjs";

export const {
    ContextComponent,
    usePrivateStore
} = createPrivateStore<iStore<iState, iActions>>('lk/main', (set) => ({
    orders: {
        quarter: 4,
        year:  2022,
    },
    remains: {
        quarter: 4,
        year:  2022,
    },
    actions: {
        setOrderDates: (year, quarter) => {
            set((state) => {
                state.orders.quarter = quarter;
                state.orders.year = year;
            })
        },
        setRemainsDates: (year, quarter) => {
            set((state) => {
                state.remains.quarter = quarter;
                state.remains.year = year;
            })
        }
    }
}))