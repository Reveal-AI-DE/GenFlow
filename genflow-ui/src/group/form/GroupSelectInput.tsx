// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC, useCallback } from 'react';
import {
    useTranslate, useGetResourceLabel, RecordContextProvider,
    ReferenceInput, required, SelectInput,ReferenceInputProps,
    CreateBase, useCreateSuggestionContext, ResourceContextProvider,
    useResourceContext,
} from 'react-admin'

import { EntityGroup } from '@/types';
import GroupFormDialog from '@/group/form/GroupFormDialog';
import { GroupField } from '@/group/show';

const CreateOption: FC = () => {
    const { onCancel, onCreate } = useCreateSuggestionContext();
    const resource = useResourceContext();

    return (
        <CreateBase
            resource={resource}
            redirect={false}
            mutationOptions={{
                onSuccess: (data) => onCreate(data),
            }}
        >
            <GroupFormDialog
                open
                onClose={onCancel}
            />
        </CreateBase>
    );
}

interface GroupSelectInputProps extends ReferenceInputProps {
    showCreateOption?: boolean;
}

const GroupSelectInput: FC<GroupSelectInputProps> = ({
    source='group_id',
    reference,
    showCreateOption=true,
    ...props
}) => {
    const getResourceLabel = useGetResourceLabel();
    const translate = useTranslate();

    const renderOptionText = useCallback((choice: EntityGroup) => (
        <RecordContextProvider value={choice}>
            <GroupField key={choice.id} />
        </RecordContextProvider>
    ), []);

    const renderCreate = showCreateOption ? (
        <ResourceContextProvider value={reference}>
            <CreateOption />
        </ResourceContextProvider>
    ): undefined;

    return (
        <ReferenceInput
            source={source}
            reference={reference}
            {...props}
        >
            <SelectInput
                variant='standard'
                validate={required()}
                optionText={renderOptionText}
                create={renderCreate}
                margin='none'
                createLabel={translate('action.add_new', {name: getResourceLabel(reference, 1)})}
            />
        </ReferenceInput>
    );
};

export default GroupSelectInput;
