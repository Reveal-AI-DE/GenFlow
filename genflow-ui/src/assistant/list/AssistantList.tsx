// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import {
    ListBase, TextField,
    ReferenceField,
} from 'react-admin';

import { AssistantStatus } from '@/types';
import { ListGridSwitcher } from '@/common';
import { EntityDatagrid, EntityListActions, EntityLisFilters } from '@/entity';
import { GroupField } from '@/group';
import { AssistantCard } from '@/assistant/show';

type AssistantListProps = object

const AssistantList: FC<AssistantListProps> = () => (
    <ListBase perPage={12}>
        <ListGridSwitcher
            actions={EntityListActions}
            filters={
                EntityLisFilters(
                    'assistant-groups',
                    'assistant_status',
                    AssistantStatus,
                )
            }
            ItemComponent={<AssistantCard />}
        >
            <EntityDatagrid>
                <TextField source='name' />
                <ReferenceField
                    source='group.id'
                    reference='assistant-groups'
                    sortBy='group__name'
                >
                    <GroupField />
                </ReferenceField>
                <TextField source='assistant_status' />
            </EntityDatagrid>
        </ListGridSwitcher>
    </ListBase>
);

export default AssistantList;
