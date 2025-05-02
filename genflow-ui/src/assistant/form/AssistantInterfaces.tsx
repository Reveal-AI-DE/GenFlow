// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import { CreateBase, EditBase } from 'react-admin';

import { AssistantState } from '@/state';
import { FormMode } from '@/types';
import AssistantForm from '@/assistant/form/AssistantForm';

const AssistantCreate: FC = () => (
    <CreateBase
        mutationMode='pessimistic'
    >
        <AssistantState
            formMode={FormMode.CREATE}
        >
            <AssistantForm />
        </AssistantState>
    </CreateBase>
)

const AssistantEdit: FC = () => (
    <EditBase
        mutationMode='pessimistic'
    >
        <AssistantState
            formMode={FormMode.EDIT}
        >
            <AssistantForm />
        </AssistantState>
    </EditBase>
)

export {
    AssistantCreate,
    AssistantEdit,
};
