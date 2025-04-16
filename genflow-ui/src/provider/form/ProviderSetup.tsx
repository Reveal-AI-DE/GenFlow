// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import Stack from '@mui/material/Stack';
import Box from '@mui/material/Box';
import RadioButtonCheckedIcon from '@mui/icons-material/RadioButtonChecked';
import RadioButtonUncheckedIcon from '@mui/icons-material/RadioButtonUnchecked';
import Tooltip from '@mui/material/Tooltip';
import Typography from '@mui/material/Typography';
import { useRecordContext, useTranslate } from 'react-admin';

import { AIProviderConfiguration } from '@/types';
import ProviderSetupButton from '@/provider/form/ProviderSetupButton';

type ProviderHelpProps = object;

const ProviderSetup: FC<ProviderHelpProps> = () => {
    const aiProviderConfiguration = useRecordContext<AIProviderConfiguration>();
    const translate = useTranslate();

    if (!aiProviderConfiguration) return null;

    return (
        <Box display='flex' flexDirection='column' p={1} alignItems='center'>
            <Stack direction='row' spacing={1}>
                <Typography variant='caption' component='span'>
                    {translate('label.credentials')}
                </Typography>
                {
                    aiProviderConfiguration.user_configuration?.active ? (
                        <Tooltip title={translate('label.enabled')}>
                            <RadioButtonCheckedIcon
                                color='success'
                                fontSize='small'
                            />
                        </Tooltip>
                    ) : (
                        <Tooltip title={translate('label.disabled')}>
                            <RadioButtonUncheckedIcon
                                color='error'
                                fontSize='small'
                            />
                        </Tooltip>
                    )
                }
            </Stack>
            <ProviderSetupButton />
        </Box>
    );
};

export default ProviderSetup;
