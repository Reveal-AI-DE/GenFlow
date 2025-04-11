// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import { RaRecord } from 'react-admin';

export interface MetaParams {
    queryParams?: {
        [key: string]: string;
    }
};

export interface TranslationEntity {
    en_US: string;
    [key: string]: string;
}

export interface BaseYamlEntity {
    label: TranslationEntity;
    description?: TranslationEntity;
};

export interface BaseYamlEntityWithIcons extends BaseYamlEntity {
    icon_small?: TranslationEntity;
    icon_large?: TranslationEntity;
};

export interface HelpEntity {
    title: TranslationEntity;
    url?: TranslationEntity;
};

export enum ConfigurationType {
    FLOAT = 'float',
    INT = 'int',
    STRING = 'string',
    BOOLEAN = 'boolean',
    TEXT = 'text',
    OBJECT = 'object',
    SECRET = 'secret',
};

export interface CommonConfigurationEntity {
    name: string;
    label: TranslationEntity;
    type: ConfigurationType;
    required?: boolean;
    disabled?: boolean;
    advanced?: boolean;
};

export interface ConfigurationEntity extends CommonConfigurationEntity {
    help?: TranslationEntity;
    placeholder?: TranslationEntity;
    default?: any;
};

export interface NumberConfigurationEntity extends ConfigurationEntity {
    min?: number;
    max?: number;
    precision?: number;
};

export interface StringConfigurationEntity extends ConfigurationEntity {
    options?: ConfigurationEntity[];
};

export type BooleanConfigurationEntity = ConfigurationEntity;

export type TextConfigurationEntity = ConfigurationEntity;

export interface ObjectConfigurationEntity extends ConfigurationEntity {
    parameters?: ConfigurationEntity[];
};

export enum ModelType {
    LLM = 'llm',
};

export interface Group extends RaRecord {
    name: string;
    description: string;
    color: string;
};

export interface FileEntity {
    id: string;
    path: string;
};
