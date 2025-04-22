// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC } from 'react';

import { SessionCreate } from '@/session';

type NewChatProps = object;

const NewChat: FC<NewChatProps> = () => (
    <SessionCreate />
);

export default NewChat;
