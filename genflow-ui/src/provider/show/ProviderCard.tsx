// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import Card from '@mui/material/Card';
import CardHeader from '@mui/material/CardHeader';
import CardContent from '@mui/material/CardContent';
import Chip from '@mui/material/Chip';
import { styled } from '@mui/material/styles';
import { useLocale, useRecordContext } from 'react-admin';

import { AIProviderConfiguration } from '@/types';
import { MediaURL } from '@/utils';
import { ProviderSetup } from '@/provider/form';

const StyledImg = styled('img', {
    name: 'GFProviderCard',
    slot: 'img',
})(() => ({
    height: '1.5rem'
}));

type ProviderCardProps = object;

const ProviderCard: FC<ProviderCardProps> = () => {
    const locale = useLocale();
    const record = useRecordContext<AIProviderConfiguration>();

    if (!record) {
        return null;
    }

    // sx={{ backgroundColor: record.background ? record.background : 'transparent' }}
    return (
        <Card>
            <CardHeader
                title={
                    record.icon_large ? (
                        <StyledImg
                            src={MediaURL(record.icon_large[locale] ?? record.icon_large.en_US)}
                            alt={record.label[locale] ?? record.label.en_US}
                        />
                    ) : (
                        record.label[locale] ?? record.label.en_US
                    )
                }
                subheader={record.description ? record.description[locale] ?? record.description.en_US : ''}
                action={(
                    <ProviderSetup />
                )}
            />
            <CardContent>
                {
                    record.supported_model_types.map((modelType: string) => (
                        <Chip key={modelType} label={modelType.toUpperCase()} />
                    ))
                }
            </CardContent>
        </Card>
    );
};

export default ProviderCard;
