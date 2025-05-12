// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';

import { EntityCard } from '@/entity';
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
