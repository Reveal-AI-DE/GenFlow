// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import {
    DataProvider, CreateParams, UpdateParams,
    CreateResult, UpdateResult,
} from 'react-admin';

import { CommonEntity } from '@/types';
import { ResourceURL } from '@/utils';
import defaultDataProvider from '@/dataProvider/defaultDataProvider';
import { fetchJsonWithAuthToken } from '@/auth/authProvider';

export default <DataProvider> {
    create: async (resource: string, params: CreateParams) => {
        const data: CreateResult<CommonEntity> = await defaultDataProvider.create(resource, params);

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
        const data: UpdateResult<CommonEntity> = await defaultDataProvider.update(resource, params);

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
