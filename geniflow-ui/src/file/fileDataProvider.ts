// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import { DataProvider } from 'react-admin';

import { ResourceURL, fetchJsonWithAuthToken } from '@/utils';
import { GetFilesParams, DeleteFileParams, DeleteFilesParams } from '@/types';

export default <DataProvider> {
    getList: async (resource: string, params: GetFilesParams) => {
        const url = ResourceURL(`/${params.meta.resource}/${params.meta.recordId}/${resource}`);
        const { json } = await fetchJsonWithAuthToken(url);
        return {
            data: json.results,
            total: json.count,
        };
    },
    delete: async (resource: string, params: DeleteFileParams) => {
        const url = ResourceURL(`/${params.meta.resource}/${params.id}/${resource}/${params.meta.fileId}`);
        const { json } = await fetchJsonWithAuthToken(url, { method: 'DELETE' });
        return { data: json };
    },
    deleteMany: (resource: string, params: DeleteFilesParams) => Promise.all(
        params.ids.map((id) => (
            fetchJsonWithAuthToken(
                ResourceURL(`/${params.meta.resource}/${params.meta.recordId}/${resource}/${id}`), {
                    method: 'DELETE',
                }))),
    ).then(() => ({ data: [] })),
};
