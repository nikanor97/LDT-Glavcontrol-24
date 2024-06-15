import { createPrivateStore, iStore } from "@/Utils/Zustand/createPrivate";
import {iActions, iState} from './types';

export const {
    ContextComponent,
    usePrivateStore
} = createPrivateStore<iStore<iState, iActions>>('lk-admin/companies', (set) => ({
    addCompany: {
        visible: false,
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
            })
        },
        openDrawer: () => {
            set((state) => {
                state.addCompany.visible = true;
            })
        }
    }
}))