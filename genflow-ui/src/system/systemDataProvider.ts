// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import { SystemDataProvider } from '@/types';
import { ResourceURL } from '@/utils';
import { fetchJsonWithAuthToken } from '@/auth/authProvider';

export default <SystemDataProvider> {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    getAbout: async (resource: string, params: any) => {
        const url = ResourceURL(`/${resource}/about`);
        const { json } = await fetchJsonWithAuthToken(url);
        return {
            data: json,
        };
    }
};
