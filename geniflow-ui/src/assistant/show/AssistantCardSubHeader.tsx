// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import Tooltip from '@mui/material/Tooltip';
import DraftsIcon from '@mui/icons-material/Drafts';
import PublishedWithChangesIcon from '@mui/icons-material/PublishedWithChanges';
import { useRecordContext, ReferenceField } from 'react-admin';

import {
    Assistant, AssistantStatus,
} from '@/types';
import { GroupField, GroupFieldSlot } from '@/group';
import { EntityCardSubHeader } from '@/entity';

type AssistantCardSubHeaderProps = object;

const AssistantCardSubHeader: FC<AssistantCardSubHeaderProps> = () => {
    const assistant = useRecordContext<Assistant>();
    if (!assistant) {
        return null;
    }

    const renderStatus = (assistant_status: string): JSX.Element => (
        <Tooltip title={assistant_status.toUpperCase()}>
            { assistant_status === AssistantStatus.DRAFTED ? (
                <DraftsIcon color='warning' />
            ) : (
                <PublishedWithChangesIcon color='success' />
            )}
        </Tooltip>
    );

    return (
        <EntityCardSubHeader
            statusSource='assistant_status'
            renderStatus={renderStatus}
        >
            <ReferenceField
                source='group.id'
                reference='assistant-groups'
            >
                <GroupField
                    slots={[GroupFieldSlot.COLOR]}
                />
            </ReferenceField>
        </EntityCardSubHeader>
    );
};

export default AssistantCardSubHeader;
