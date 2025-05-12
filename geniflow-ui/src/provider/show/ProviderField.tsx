// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import Chip from '@mui/material/Chip';
import { useLocale } from 'react-admin';

import { CommonAIProviderEntity } from '@/types';
import { MediaURL } from '@/utils';

type ProviderFieldProps = {
    entity: CommonAIProviderEntity;
};

const ProviderField: FC<ProviderFieldProps> = ({
    entity,
}) => {
    const locale = useLocale();
    const avatar = entity.icon_small ? MediaURL(entity.icon_small[locale] ?? entity.icon_small.en_US) : undefined;
    const label = entity.label[locale] ?? entity.label.en_US;

    return (
        <Chip
            avatar={avatar ? (
                <img src={avatar} alt={label} style={{ height: '1rem' }} />
            ) : undefined}
            label={label}
        />
    );
}

export default ProviderField;
