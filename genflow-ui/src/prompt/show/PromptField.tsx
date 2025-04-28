// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import { useRecordContext } from 'react-admin';

import { Prompt } from '@/types';
import { EntityField, EntityFieldProps, EntityFieldSlot } from '@/entity';

type PromptFieldProps = EntityFieldProps;

const PromptField: FC<PromptFieldProps> = ({
    slots=[EntityFieldSlot.AVATAR, EntityFieldSlot.NAME],
}) => {
    const record = useRecordContext<Prompt>();
    if (!record) {
        return null;
    }

    return (
        <EntityField
            slots={slots}
        />
    );
};

export default PromptField;
