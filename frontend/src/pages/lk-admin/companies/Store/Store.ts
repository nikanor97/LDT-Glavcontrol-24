import { createPrivateStore, iStore } from "@/Utils/Zustand/createPrivate";
import {iActions, iState} from './types';

export const {
    ContextComponent,
    usePrivateStore
} = createPrivateStore<iStore<iState, iActions>>('lk-admin/companies', (set) => ({
    addCompany: {
        visible: false,
        item: null,
    },
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
        },
        closeDrawer: () => {
            set((state) => {
                state.addCompany.visible = false;
                state.addCompany.item = null;
            })
        },
        openDrawer: (item) => {
            set((state) => {
                state.addCompany.visible = true;
                if (item) state.addCompany.item = item;
            })
        }
    }
}))