import { createPrivateStore, iStore } from "@/Utils/Zustand/createPrivate";
import {iActions, iState} from './types';

export const {
    ContextComponent,
    usePrivateStore
} = createPrivateStore<iStore<iState, iActions>>('lk-admin/companies', (set) => ({
    createUser: {
        visible: false,
    },
    usersListParams: {
        limit: 100,
        offset: 0,
    },
    actions: {
        changeParams: (params) => {
            set((state) => {
                state.usersListParams = {
                    ...state.usersListParams,
                    ...params
                }
            })
        },
        openDrawer: () => {
            set((state) => {
                state.createUser.visible = true;
            })
        },
        closeDrawer: () => {
            set((state) => {
                state.createUser.visible = false;
            })
        }
    }
}))