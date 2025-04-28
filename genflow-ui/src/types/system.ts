// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import { DataProvider } from 'react-admin';

import { TranslationEntity } from '@/types/common';

export interface AboutSystem {
    name: TranslationEntity;
    description: TranslationEntity;
    license: TranslationEntity;
    version: string;
};

export interface GetAboutResult {
    data: AboutSystem;
};

export interface SystemDataProvider extends DataProvider {
    getSessionTypes: () => Promise<any>;
    getAbout: (resource: string) => Promise<GetAboutResult>;
};
