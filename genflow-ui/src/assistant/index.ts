// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import { ResourceProps } from 'react-admin';
import AssistantIcon from '@mui/icons-material/Assistant';

import { AssistantCreate, AssistantEdit } from '@/assistant/form';
import { AssistantList } from '@/assistant/list';

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
    AssistantResourceProps
};
