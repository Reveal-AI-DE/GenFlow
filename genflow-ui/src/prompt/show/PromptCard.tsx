// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';

import { EntityCard } from '@/common';
import PromptCardActions from '@/prompt/show/PromptCardActions';
import PromptCardSubHeader from '@/prompt/show/PromptCardSubHeader';

type PromptCardProps = object;

const PromptCard: FC<PromptCardProps> = () => (
    <EntityCard
        subHeader={<PromptCardSubHeader />}
        actions={<PromptCardActions />}
    />
);

export default PromptCard;
