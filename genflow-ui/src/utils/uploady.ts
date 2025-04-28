// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import { Destination } from '@rpldy/uploady';
import { Identifier } from 'react-admin';

import { ResourceURL } from '@/utils/dataProvider';
import { createOptions } from '@/auth/authProvider';

export const createUploadyDestination = (
    resource: string,
    recordId: Identifier,
): Destination | null => {
    const url = ResourceURL(`${resource}/${recordId}/upload_file`);

    const options = createOptions(url);
    if (!options.user || !options.headers) {
        return null;
    }

    options.headers.set('authorization', options.user.token);
    const headersRecord: Record<string, string> = {};
    options.headers.forEach((value, key) => {
        headersRecord[key] = value;
    });

    return {
        url,
        headers: headersRecord,
    }
};
