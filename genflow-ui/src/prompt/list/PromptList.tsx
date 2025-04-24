// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import {
    ListBase, TextField,
    ReferenceField, SelectInput,
} from 'react-admin';

import { PromptType, PromptStatus } from '@/types';
import {
    ListGridSwitcher, EntityDatagrid,
    EntityListActions, EntityLisFilters,
} from '@/common';
import { GroupField } from '@/group';
import { getChoicesFromEnum } from '@/utils';
import { PromptCard } from '@/prompt/show';

const PromptFilters = [
    ...EntityLisFilters(
        'prompt-groups',
        'prompt_status',
        PromptStatus,
    ),
    <SelectInput
        source='prompt_type'
        choices={getChoicesFromEnum(PromptType)}
        variant='outlined'
    />,
];

type PromptListProps = object

const PromptList: FC<PromptListProps> = () => (
    <ListBase perPage={12}>
        <ListGridSwitcher
            actions={EntityListActions}
            filters={PromptFilters}
            ItemComponent={<PromptCard />}
        >
            <EntityDatagrid>
                <TextField source='name' />
                <ReferenceField
                    source='group.id'
                    reference='prompt-groups'
                    sortBy='group__name'
                >
                    <GroupField />
                </ReferenceField>
                <TextField source='prompt_type' />
                <TextField source='prompt_status' />
            </EntityDatagrid>
        </ListGridSwitcher>
    </ListBase>
);

export default PromptList;
