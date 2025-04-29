// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import { UserIdentity } from 'react-admin';

import { UserDataProvider, RegistrationFormData, ChangePasswordFormData } from '@/types';
import { ResourceURL, fetchJsonWithAuthToken } from '@/utils';

export const userRegister = async (params: RegistrationFormData): Promise<UserIdentity> => {
    const url = ResourceURL(`${process.env.REACT_APP_BACKEND_AUTH_URL}/register`);
    const { json } = await fetchJsonWithAuthToken(url, {
        method: 'POST',
        body: JSON.stringify(params),
    });
    return json;
};

export const changePassword = async (params: ChangePasswordFormData): Promise<UserIdentity> => {
    const url = ResourceURL(`${process.env.REACT_APP_BACKEND_AUTH_URL}/password/change`);
    const { json } = await fetchJsonWithAuthToken(url, {
        method: 'POST',
        body: JSON.stringify(params),
    });
    return json;
};

export const getLoggedInUser = async (): Promise<UserIdentity> => {
    const url = ResourceURL('/users/self');
    const { json } = await fetchJsonWithAuthToken(url);

    return {
        ...json,
        fullName: `${json.first_name} ${json.last_name}`,
    };
};

export default <UserDataProvider> {
    check: async (resource: string, params: any) => {
        const url = ResourceURL(`/${resource}/check`);
        const { status } = await fetchJsonWithAuthToken(url, {
            method: 'POST',
            body: JSON.stringify(params),
        });

        if (status === 200) {
            return true;
        }
        return false;
    },
};
