// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import EngineeringIcon from '@mui/icons-material/Engineering';
import { useTranslate } from 'react-admin';

import { PagePlaceholder } from '@/common';

type UnderConstructionProps = object;

const UnderConstruction: FC<UnderConstructionProps> = () => {
    const translate = useTranslate();

    return (
        <PagePlaceholder
            icon={<EngineeringIcon color='disabled' />}
            sx={{
                height: '50%',
            }}
        >
            <Box
                sx={{
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    justifyContent: 'center',
                }}
            >
                <Typography
                    variant='h4'
                    component='p'
                    color='rgba(0, 0, 0, 0.38)'
                    gutterBottom
                >
                    {translate('message.coming_soon')}
                </Typography>
                <Typography
                    variant='body1'
                    component='p'
                    color='rgba(0, 0, 0, 0.38)'
                    gutterBottom
                >
                    {translate('message.under_construction')}
                </Typography>
            </Box>
        </PagePlaceholder>
    );
};

export default UnderConstruction;
