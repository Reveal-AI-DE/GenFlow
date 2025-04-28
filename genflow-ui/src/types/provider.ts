// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import { RaRecord } from 'react-admin';

import {
    BaseYamlEntityWithIcons, HelpEntity, ConfigurationEntity,
} from '@/types/common';

export interface CommonAIProviderEntity extends RaRecord, BaseYamlEntityWithIcons {
    supported_model_types: string[];
};

export interface AIProviderEntity extends CommonAIProviderEntity {
    background?: string;
    help?: HelpEntity;
    credential_form?: ConfigurationEntity[];
};

export interface SystemConfiguration {
    active: boolean;
};

export interface UserConfiguration extends SystemConfiguration {
    provider: string | null;
};

export interface AIProviderConfiguration extends AIProviderEntity {
    user_configuration?: UserConfiguration;
    system_configuration?: SystemConfiguration;
};

export interface Provider extends RaRecord {
    provider_name: string;
    credentials: object | null;
    is_enabled: boolean;
    last_used: number
}
