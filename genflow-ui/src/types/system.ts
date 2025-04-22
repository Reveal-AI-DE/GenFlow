// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

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
