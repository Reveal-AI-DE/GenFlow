// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import { ResourceProps } from 'react-admin';

import Message, { MessageSkeleton } from '@/message/Message';

const MessageResourceProps: ResourceProps = {
    name: 'messages',
};

export {
    MessageResourceProps,
    Message, MessageSkeleton,
};
