// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import { SystemDataProvider } from '@/types';
import { ResourceURL } from '@/utils';
import { fetchJsonWithAuthToken } from '@/auth/authProvider';

export default <SystemDataProvider> {
    getAbout: async (resource: string) => {
        const url = ResourceURL(`/${resource}/about`);
        const { json } = await fetchJsonWithAuthToken(url);
        return {
            data: json,
        };
    }
};
