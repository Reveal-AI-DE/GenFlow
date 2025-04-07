// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

export interface MetaParams {
    queryParams?: {
        [key: string]: string;
    }
};

export interface TranslationEntity {
    en_US: string;
    [key: string]: string;
};

export interface HelpEntity {
    title: TranslationEntity;
    url?: TranslationEntity;
};
