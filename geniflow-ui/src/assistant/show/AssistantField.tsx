// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

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
