// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

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
