import {usePrivateStore} from '../../../Store/Store';


export const useIsEdit = () => {
    const item = usePrivateStore((state) => state.addCompany.item);
    return Boolean(item);
}