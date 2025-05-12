// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

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
