// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { ReactElement } from 'react';
import {
    SearchInput, SelectInput, BooleanInput,
} from 'react-admin';

import { GroupSelectInput } from '@/group';
import { getChoicesFromEnum } from '@/utils';

const EntityLisFilters = (
    groupReference: string,
    statusSource: string,
    statusEnum: object,
): ReactElement[] => (
    [
        <SearchInput
            source='q'
            variant='outlined'
        />,
        <GroupSelectInput
            source='group__id'
            reference={groupReference}
            showCreateOption={false}
            validate={undefined}
            variant='outlined'
        />,
        <SelectInput
            source={statusSource}
            choices={getChoicesFromEnum(statusEnum)}
            variant='outlined'
        />,
        <BooleanInput
            source='is_pinned'
            variant='outlined'
        />
    ]
);

export default EntityLisFilters;
