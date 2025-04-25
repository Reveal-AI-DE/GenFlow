// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';
import { useRecordContext } from 'react-admin';

import { Assistant } from '@/types';
import { EntityField, EntityFieldProps, EntityFieldSlot } from '@/entity';

type AssistantFieldProps = EntityFieldProps;

const AssistantField: FC<AssistantFieldProps> = ({
    slots=[EntityFieldSlot.AVATAR, EntityFieldSlot.NAME],
}) => {
    const record = useRecordContext<Assistant>();
    if (!record) {
        return null;
    }

    return (
        <EntityField
            slots={slots}
        />
    );
};

export default AssistantField;
