import {User, Company} from '@/Types';

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
        password: string;
        telegram_username?: string;
        company_id: Company.ID
    }
    type iSaveUser = Omit<iRegistration, 'password'> & {
        user_id: User.Id
    }
}