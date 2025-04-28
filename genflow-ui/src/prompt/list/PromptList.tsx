// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import {
    ListBase, TextField,
    ReferenceField, SelectInput,
} from 'react-admin';

import { PromptType, PromptStatus } from '@/types';
import { ListGridSwitcher } from '@/common';
import {
    EntityDatagrid, EntityListActions, EntityLisFilters
} from '@/entity';
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
