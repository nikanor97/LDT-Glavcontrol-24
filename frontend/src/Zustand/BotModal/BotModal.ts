import { create, iStore } from "@/Utils/Zustand/create";
import {iActions, iState} from './types';

export const useBotStore = create<iStore<iState, iActions>>((set) => ({
    visible: false,
    actions: {
        openModal: () => {
            set((state) => {
                state.visible = true;
            })
        },
        closeModal: () => {
            set((state) => {
                state.visible = false;
            })
        }
    }
}))