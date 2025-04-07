// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import { DataProvider } from 'react-admin';

import defaultDataProvider from '@/dataProvider/defaultDataProvider';
import { systemDataProvider } from '@/system';

type Providers = {
    [key: string]: DataProvider
};

const providers: Providers = {
    'prompt-groups': defaultDataProvider,
    system: systemDataProvider,
};

type DataProviderMethod = (resource: string, params: any) => any;

const createMethod = (method: string): DataProviderMethod => (resource: string, params: any) => {
    if (providers[resource] && typeof providers[resource][method] === 'function') {
        return providers[resource][method](resource, params);
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
};

export {
    dataProviderWrapper as dataProvider,
};
