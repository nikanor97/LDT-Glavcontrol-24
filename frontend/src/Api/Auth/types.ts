import {User} from '@/Types';

export declare namespace iApi {
    type iLogin = {
        username: string;
        password: string;
    }
    type oLogin = User.Token;
    type iRegistration = {
        name: string;
        email: string;
        permission_read_stat: boolean;
        permission_create_order: boolean;
        // is_deleted: true,
        password: string;
    }
}