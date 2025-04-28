// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import { UserDataProvider } from '@/types';
import { ResourceURL } from '@/utils';
import { fetchJsonWithAuthToken, getLoggedInUser } from '@/auth/authProvider';

export default <UserDataProvider> {
    self: async () => {
        const user = await getLoggedInUser();
        return user;
    },
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
