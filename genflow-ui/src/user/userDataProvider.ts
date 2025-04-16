// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import { UserDataProvider } from '@/types';
import { ResourceURL } from '@/utils';
import { fetchJsonWithAuthToken } from '../authProvider';

export default <UserDataProvider> {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    self: async (resource: string, params: any) => {
        const url = ResourceURL(`/${resource}/self`);
        const { json } = await fetchJsonWithAuthToken(url);

        return {
            user: json,
        };
    }
};
