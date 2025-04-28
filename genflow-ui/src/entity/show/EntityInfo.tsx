// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC, ReactNode } from 'react';
import {
    useRecordContext, FunctionField,
    TextField, RecordContextProvider, SimpleShowLayout,
} from 'react-admin';

import { CommonEntity } from '@/types';
import { TruncatedTextField } from '@/common';
import { GroupField } from '@/group';

interface EntityInfoProps {
    additionalFields?: ReactNode;
    children?: ReactNode;
};

const EntityInfo: FC<EntityInfoProps> = ({
    additionalFields,
    children,
}) => {
    const entity = useRecordContext<CommonEntity>();

    if (!entity) {
        return null;
    }

    return (
        <>
            <SimpleShowLayout
                spacing={1}
                sx={{ pl: 0 }}
            >
                <FunctionField
                    source='group.id'
                    render={(record) => (
                        <RecordContextProvider value={record.group}>
                            <GroupField />
                        </RecordContextProvider>
                    )}
                />
                <TextField source='name' />
                <TruncatedTextField source='description' />
                {additionalFields}
            </SimpleShowLayout>
            {children}
        </>
    )
}

export default EntityInfo;
