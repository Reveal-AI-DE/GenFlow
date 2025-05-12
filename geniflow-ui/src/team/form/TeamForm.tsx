// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import Stack from '@mui/material/Stack';
import { TextInput, required } from 'react-admin';

type TeamFormProps = object;

const TeamForm: FC<TeamFormProps> = () => (
    <Stack spacing={2}>
        <TextInput source='name' variant='outlined' validate={required()} />
        <TextInput source='description' variant='outlined' multiline />
    </Stack>
);

export default TeamForm;
