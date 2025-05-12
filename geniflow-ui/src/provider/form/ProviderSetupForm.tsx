// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';

import { ConfigurationEntity } from '@/types';
import { ConfigurableInput } from '@/common';

type ProviderSetupFormProps = {
    credentialForm: ConfigurationEntity[];
};

const ProviderSetupForm: FC<ProviderSetupFormProps> = ({
    credentialForm,
}) => (
    credentialForm.map((configurationEntity: ConfigurationEntity) => (
        <ConfigurableInput
            key={configurationEntity.name}
            configurationEntity={
                {
                    ...configurationEntity,
                    name: `credentials.${configurationEntity.name}`
                }
            }
        />
    ))
);

export default ProviderSetupForm;
