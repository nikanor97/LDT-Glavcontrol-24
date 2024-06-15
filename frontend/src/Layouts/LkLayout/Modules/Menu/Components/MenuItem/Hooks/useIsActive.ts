import {usePathname} from 'next/navigation';


export const useIsActive = (link: string, exact: boolean = false) => {
    const pathname = usePathname();
    if (exact) return pathname === link;
    else return pathname.startsWith(link)
}