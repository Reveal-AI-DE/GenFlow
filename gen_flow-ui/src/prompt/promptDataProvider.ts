// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import {
    DataProvider, CreateParams, UpdateParams,
    CreateResult, UpdateResult,
} from 'react-admin';

import { Prompt } from '@/types';
import { ResourceURL } from '@/utils';
import defaultDataProvider from '@/dataProvider/defaultDataProvider';
import { fetchJsonWithAuthToken } from '@/authProvider';

export default <DataProvider> {
    create: async (resource: string, params: CreateParams) => {
        const data: CreateResult<Prompt> = await defaultDataProvider.create(resource, params);

        if (params.data.avatar && typeof (params.data.avatar) === 'object') {
            const formData = new FormData();
            formData.append('avatar', params.data.avatar.rawFile);

            await fetchJsonWithAuthToken(ResourceURL(`/${resource}/${data.data.id}/upload_avatar`), {
                method: 'POST',
                body: formData,
            });
        }

        return data
    },
    update: async (resource: string, params: UpdateParams) => {
        const data: UpdateResult<Prompt> = await defaultDataProvider.update(resource, params);

        const formData = new FormData();
        if (params.data.avatar && typeof (params.data.avatar) === 'object') {
            formData.append('avatar', params.data.avatar.rawFile);
            await fetchJsonWithAuthToken(ResourceURL(`/${resource}/${data.data.id}/upload_avatar`), {
                method: 'POST',
                body: formData,
            });
        }

        return data;
    },
};
