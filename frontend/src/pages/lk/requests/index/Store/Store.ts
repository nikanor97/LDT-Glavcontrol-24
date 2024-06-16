import { createPrivateStore, iStore } from "@/Utils/Zustand/createPrivate";
import {iActions, iState} from './types';

export const {
    ContextComponent,
    usePrivateStore
} = createPrivateStore<iStore<iState, iActions>>('lk/requests', (set) => ({
    params: {
        limit: 10,
        offset: 0
    },
    deleteModal: {
        visible: false,
        item: null,
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
        openDeleteModal: (item) => {
            set((state) => {
                state.deleteModal.visible = true;
                state.deleteModal.item = item;
            })
        },
        closeDeleteModal: () => {
            set((state) => {
                state.deleteModal.visible = false;
                state.deleteModal.item = null;
            })
        },
    }
}))