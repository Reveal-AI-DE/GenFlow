// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import { UserDataProvider } from '@/types';
import { ResourceURL } from '@/utils';
import { fetchJsonWithAuthToken } from '../auth/authProvider';

export default <UserDataProvider> {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    self: async (resource: string, params: any) => {
        const url = ResourceURL(`/${resource}/self`);
        const { json } = await fetchJsonWithAuthToken(url);

        return {
            user: json,
        };
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
