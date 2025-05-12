// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import { ResourceProps } from 'react-admin';

import Message, { MessageSkeleton } from '@/message/Message';

const MessageResourceProps: ResourceProps = {
    name: 'messages',
};

export {
    MessageResourceProps,
    Message, MessageSkeleton,
};
