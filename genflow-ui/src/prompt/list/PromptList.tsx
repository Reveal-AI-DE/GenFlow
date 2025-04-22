// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC, useContext } from 'react';
import {
    ListBase, Datagrid, TextField,
    ReferenceField, ExportButton, CreateButton,
    BulkDeleteWithConfirmButton, SearchInput,
    SelectInput, BooleanInput,
} from 'react-admin';

import { PromptType, PromptStatus, TeamRole } from '@/types';
import { GlobalContext, GlobalContextInterface } from '@/context';
import { ListGridSwitcher } from '@/common';
import { GroupField, GroupSelectInput } from '@/group';
import { getChoicesFromEnum } from '@/utils';
import { PromptCard } from '@/prompt/show';

const PromptListActions = [
    <CreateButton key='create' />,
    <ExportButton key='export' />,
];

const PromptFilters = [
    <SearchInput
        source='q'
        variant='outlined'
    />,
    <GroupSelectInput
        source='group__id'
        reference='prompt-groups'
        showCreateOption={false}
        validate={undefined}
        variant='outlined'
    />,
    <SelectInput
        source='type'
        choices={getChoicesFromEnum(PromptType)}
        variant='outlined'
    />,
    <SelectInput
        source='status'
        choices={getChoicesFromEnum(PromptStatus)}
        variant='outlined'
    />,
    <BooleanInput
        source='is_pinned'
        variant='outlined'
    />
];

const PromptBulkActionButtons: FC = () => (
    <BulkDeleteWithConfirmButton mutationMode='pessimistic' />
);

type PromptListProps = object

const PromptList: FC<PromptListProps> = () => {
    const { currentMembership } = useContext<GlobalContextInterface>(GlobalContext);
    const isOwnerOrAdmin = currentMembership?.role === TeamRole.OWNER || currentMembership?.role === TeamRole.ADMIN;

    return (
        <ListBase perPage={12}>
            <ListGridSwitcher
                actions={PromptListActions}
                filters={PromptFilters}
                ItemComponent={<PromptCard />}
            >
                <Datagrid
                    bulkActionButtons={
                        isOwnerOrAdmin ? (
                            <PromptBulkActionButtons />
                        ) : false
                    }
                    rowClick={isOwnerOrAdmin ? 'edit' : false}
                >
                    <TextField source='name' />
                    <ReferenceField
                        source='group.id'
                        reference='prompt-groups'
                        sortBy='group__name'
                    >
                        <GroupField />
                    </ReferenceField>
                    <TextField source='type' />
                    <TextField source='status' />
                </Datagrid>
            </ListGridSwitcher>
        </ListBase>
    );
};

export default PromptList;
