// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';

import { EntityCard } from '@/entity';
import AssistantCardActions from '@/assistant/show/AssistantCardActions';
import AssistantCardSubHeader from '@/assistant/show/AssistantCardSubHeader';

type AssistantCardProps = object;

const AssistantCard: FC<AssistantCardProps> = () => (
    <EntityCard
        subHeader={<AssistantCardSubHeader />}
        actions={<AssistantCardActions />}
    />
);

export default AssistantCard;
