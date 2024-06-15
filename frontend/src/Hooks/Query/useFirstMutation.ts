import {MutationState} from '@tanstack/react-query';


export const useFirstMutation = <A,B,C>(mutations: MutationState<A, Error, B, C>[]) => {
    if (mutations.length) return mutations[0];
    return null;
}