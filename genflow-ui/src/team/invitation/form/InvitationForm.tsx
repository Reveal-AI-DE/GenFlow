// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import EmailIcon from '@mui/icons-material/Email';
import InputAdornment from '@mui/material/InputAdornment';
import Stack from '@mui/material/Stack';
import { TextInput, SelectInput, required } from 'react-admin';

import { TeamRole } from '@/types';
import { getChoicesFromEnum } from '@/utils';

type InvitationFormProps = object;

const InvitationForm: FC<InvitationFormProps> = () => (
    <Stack spacing={2}>
        <TextInput
            source='email'
            type='email'
            variant='outlined'
            slotProps={{
                input: {
                    startAdornment: (
                        <InputAdornment position='start'>
                            <EmailIcon />
                        </InputAdornment>
                    ),
                }
            }}
            validate={required()}
            fullWidth
        />
        <SelectInput
            source='role'
            choices={getChoicesFromEnum(TeamRole)}
            validate={required()}
            variant='outlined'
            fullWidth
        />
    </Stack>
);

export default InvitationForm;
