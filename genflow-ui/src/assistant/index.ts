// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import { ResourceProps } from 'react-admin';
import AssistantIcon from '@mui/icons-material/Assistant';

import { AssistantCreate, AssistantEdit, AssistantSelectInput } from '@/assistant/form';
import { AssistantList } from '@/assistant/list';
import { AssistantCard, AssistantInfo, AssistantStartingMessage } from '@/assistant/show';

const AssistantGroupResourceProps: ResourceProps = {
    name: 'assistant-groups',
};

const AssistantResourceProps: ResourceProps = {
    name: 'assistants',
    list: AssistantList,
    create: AssistantCreate,
    edit: AssistantEdit,
    icon: AssistantIcon,
};

export {
    AssistantGroupResourceProps,
    AssistantResourceProps,
    AssistantCard,
    AssistantInfo,
    AssistantSelectInput,
    AssistantStartingMessage,
};
