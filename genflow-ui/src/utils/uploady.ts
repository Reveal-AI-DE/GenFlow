// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import { Destination } from '@rpldy/uploady';
import { Identifier } from 'react-admin';

import { ResourceURL, createFetchOptions } from '@/utils/dataProvider';

export const createUploadyDestination = (
    resource: string,
    recordId: Identifier,
): Destination | null => {
    const url = ResourceURL(`${resource}/${recordId}/upload_file`);

    const options = createFetchOptions(url);
    if (!options.user || !options.user.token || !options.headers) {
        return null;
    }

    const requestHeaders = options.headers as Headers;
    requestHeaders.set('authorization', options.user.token);

    const headersRecord: Record<string, string> = {};
    requestHeaders.forEach((value, key) => {
        headersRecord[key] = value;
    });

    return {
        url,
        headers: headersRecord,
    }
};
