// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import Stack from '@mui/material/Stack';
import { BooleanInput, SelectInput, required } from 'react-admin';

import { TeamRole } from '@/types';
import { getChoicesFromEnum } from '@/utils';

type MembershipFormProps = object;

const MembershipForm: FC<MembershipFormProps> = () => (
    <Stack spacing={2}>
        <BooleanInput
            source='is_active'
            variant='outlined'
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

export default MembershipForm;
