import {useState, useEffect} from 'react';
import {QueryClient,QueryClientProvider} from '@tanstack/react-query'
import {ReactQueryDevtools} from '@tanstack/react-query-devtools'
import {App} from '@/Types';
import {useRouter} from 'next/router';
import {QueryCategory} from '@/Utils/Query/getQueryKey';

type iReactQueryProvider = {
    children: React.ReactNode;
}

const ReactQueryProvider = (props: iReactQueryProvider) => {
    const [queryClient] = useState(() => new QueryClient({
        defaultOptions: {
            queries: {
                // retry: false
            }
        }
    }));
    const router = useRouter();
    useEffect(() => {
        const handleExit = () => {
            queryClient.removeQueries({
                queryKey: [QueryCategory.PAGE]
            })
        };
        router.events.on("routeChangeComplete", handleExit);
        return () => {
            router.events.off("routeChangeComplete", handleExit);
        };
    }, []);

    return (
        <QueryClientProvider client={queryClient}>
            <ReactQueryDevtools buttonPosition="bottom-right" initialIsOpen={false} />
            {props.children}
        </QueryClientProvider>
    )
}

export default ReactQueryProvider;