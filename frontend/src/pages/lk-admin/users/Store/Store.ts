import { createPrivateStore, iStore } from "@/Utils/Zustand/createPrivate";
import {iActions, iState} from './types';

export const {
    ContextComponent,
    usePrivateStore
} = createPrivateStore<iStore<iState, iActions>>('lk-admin/companies', (set) => ({
    createUser: {
        visible: false,
    },
    actions: {
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