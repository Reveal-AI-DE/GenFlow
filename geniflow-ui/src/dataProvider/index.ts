// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import { DataProvider } from 'react-admin';

import defaultDataProvider from '@/dataProvider/defaultDataProvider';
import { entityDataProvider } from '@/entity';
import { fileDataProvider } from '@/file';
import { modelDataProvider } from '@/provider/model';
import { systemDataProvider } from '@/system';
import { userDataProvider } from '@/user';

type Providers = {
    [key: string]: DataProvider
};

const providers: Providers = {
    assistants: {
        ...defaultDataProvider,
        ...entityDataProvider,
    },
    'assistant-groups': defaultDataProvider,
    invitations: defaultDataProvider,
    files: fileDataProvider,
    memberships: defaultDataProvider,
    messages: defaultDataProvider,
    models: {
        ...defaultDataProvider,
        ...modelDataProvider
    },
    prompts: {
        ...defaultDataProvider,
        ...entityDataProvider
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
    // system
    getAbout: createMethod('getAbout'),
    // users
    check: createMethod('check'),
    // models
    getParameterConfig: createMethod('getParameterConfig'),
    // files
    getFiles: createMethod('getFiles'),
    deleteFile: createMethod('deleteFile'),
};

export {
    dataProviderWrapper as dataProvider,
};
