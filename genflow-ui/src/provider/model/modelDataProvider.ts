// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import { ModelDataProvider } from '@/types';
import { ResourceURL } from '@/utils';
import { fetchJsonWithAuthToken } from '@/auth/authProvider';

export default <ModelDataProvider> {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    getParameterConfig: async (resource: string, params: any) => {
        const url = ResourceURL(`/${resource}/${params.id}/parameter_config?per_page=all`);
        const { json } = await fetchJsonWithAuthToken(url);

        return {
            data: json.results,
            total: json.count,
        };
    }
};
