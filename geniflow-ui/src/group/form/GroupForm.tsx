// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import { TextInput, required } from 'react-admin';

import { ColorInput } from '@/common';

type GroupInputsProps = object;

const GroupInputs: FC<GroupInputsProps> = () => (
    <>
        <TextInput
            source='name'
            validate={required()}
            variant='outlined'
        />
        <TextInput
            source='description'
            validate={required()}
            variant='outlined'
            multiline
        />
        <ColorInput
            source='color'
            validate={required()}
            format='hex8'
            fullWidth
        />
    </>
);

export default GroupInputs;
