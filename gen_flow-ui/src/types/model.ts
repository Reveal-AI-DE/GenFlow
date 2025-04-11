// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import { RaRecord, DataProvider } from 'react-admin';

import { BaseYamlEntity, ModelType, ConfigurationEntity } from '@/types/common';
import { CommonAIProviderEntity } from '@/types/provider';

export enum Feature {
    TOOL_CALL = 'tool-call',
    MULTI_TOOL_CALL = 'multi-tool-call',
    AGENT_THOUGHT = 'agent-thought',
    VISION = 'vision',
    STREAM_TOOL_CALL = 'stream-tool-call',
};

export enum PropertyKey {
    MODE = 'mode',
    CONTEXT_SIZE = 'context_size',
};

export type ModelProperty = {
    [key in PropertyKey]: any;
};

export interface CommonModelEntity extends RaRecord, BaseYamlEntity {
    type: ModelType;
    features?: Feature[];
    properties: ModelProperty;
    deprecated: boolean;
};

export interface ModelWithProviderEntity extends CommonModelEntity {
    active: boolean;
    provider: CommonAIProviderEntity
}

export interface GetParameterConfig {
    data: ConfigurationEntity[];
    total: number;
};

export interface ModelDataProvider extends DataProvider {
    getParameterConfig: () => Promise<GetParameterConfig>;
};

export interface ModelEntity extends ModelWithProviderEntity {
    parameter_configs?: ConfigurationEntity[];
};

export interface Parameters {
    [key: string]: number | string | boolean;
};

export interface Config {
    parameters: Parameters
};

export interface ModelConfig {
    provider_name: string;
    model_name: string;
    config: Config;
};

export interface ModelConfigWithEntity extends ModelConfig {
    entity: ModelEntity;
};

export type ChatModelSetting = Config;
