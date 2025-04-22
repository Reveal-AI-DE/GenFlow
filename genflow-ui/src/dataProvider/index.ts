// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import { DataProvider } from 'react-admin';

import defaultDataProvider from '@/dataProvider/defaultDataProvider';
import { modelDataProvider } from '@/provider/model';
import { promptDataProvider } from '@/prompt';
import { systemDataProvider } from '@/system';
import { userDataProvider } from '@/user';

type Providers = {
    [key: string]: DataProvider
};

const providers: Providers = {
    invitations: defaultDataProvider,
    memberships: defaultDataProvider,
    messages: defaultDataProvider,
    models: {
        ...defaultDataProvider,
        ...modelDataProvider
    },
    prompts: {
        ...defaultDataProvider,
        ...promptDataProvider
    },
    'prompt-groups': defaultDataProvider,
    providers: defaultDataProvider,
    sessions: defaultDataProvider,
    system: systemDataProvider,
    teams: defaultDataProvider,
    users: userDataProvider,
};

type DataProviderMethod = (resource: string, params: any) => any;

const createMethod = (method: string): DataProviderMethod => (resource: string, params: any) => {
    if (providers[resource] && typeof providers[resource][method] === 'function') {
        // if the resource has the pattern prefix-resource
        // then we need to convert it to prefix/resource
        const convertResource = resource.includes('-') ? resource.replace('-', '/') : resource;
        return providers[resource][method](convertResource, params);
    }
    throw new Error(`Method ${method} not found on provider for resource ${resource}`);
};

const dataProviderWrapper: DataProvider = {
    getList: createMethod('getList'),
    getOne: createMethod('getOne'),
    getMany: createMethod('getMany'),
    getManyReference: createMethod('getManyReference'),
    create: createMethod('create'),
    update: createMethod('update'),
    updateMany: createMethod('updateMany'),
    delete: createMethod('delete'),
    deleteMany: createMethod('deleteMany'),
    // Add any additional methods here
    getAbout: createMethod('getAbout'),
    self: createMethod('self'),
    check: createMethod('check'),
    getParameterConfig: createMethod('getParameterConfig'),
};

export {
    dataProviderWrapper as dataProvider,
};
