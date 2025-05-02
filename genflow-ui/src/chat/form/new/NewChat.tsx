// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';

import { SessionCreate } from '@/session';

type NewChatProps = object;

const NewChat: FC<NewChatProps> = () => (
    <SessionCreate />
);

export default NewChat;
