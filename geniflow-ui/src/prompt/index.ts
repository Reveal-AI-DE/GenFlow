// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import { ResourceProps } from 'react-admin';
import TerminalIcon from '@mui/icons-material/Terminal';

import { PromptList } from '@/prompt/list';
import { PromptInterface, PromptSelectInput } from '@/prompt/form';
import { PromptCard, PromptInfo, PromptStartingMessage } from '@/prompt/show';

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
    PromptCard,
    PromptInfo,
    PromptStartingMessage,
    PromptSelectInput,
};
