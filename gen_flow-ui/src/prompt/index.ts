// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import { ResourceProps } from 'react-admin';
import TerminalIcon from '@mui/icons-material/Terminal';

import promptDataProvider from '@/prompt/promptDataProvider';
import { PromptList } from '@/prompt/list';
import { PromptInterface } from '@/prompt/form';

const PromptGroupResourceProps: ResourceProps = {
    name: 'prompt-groups',
};

const PromptResourceProps: ResourceProps = {
    name: 'prompts',
    list: PromptList,
    create: PromptInterface,
    edit: PromptInterface,
    icon: TerminalIcon,
};

export {
    PromptGroupResourceProps,
    PromptResourceProps,
    promptDataProvider,
};
