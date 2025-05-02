// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import { SystemDataProvider } from '@/types';
import { ResourceURL, fetchJsonWithAuthToken } from '@/utils';

export default <SystemDataProvider> {
    getAbout: async (resource: string) => {
        const url = ResourceURL(`/${resource}/about`);
        const { json } = await fetchJsonWithAuthToken(url);
        return {
            data: json,
        };
    }
};
