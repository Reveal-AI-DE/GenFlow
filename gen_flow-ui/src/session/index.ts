// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import { ResourceProps } from 'react-admin';
import WorkspacesIcon from '@mui/icons-material/Workspaces';

import { SessionCreate } from '@/session/form';
import { SessionList } from '@/session/list';
import { SessionShow } from '@/session/show';

const SessionResourceProps: ResourceProps = {
    name: 'sessions',
    list: SessionList,
    show: SessionShow,
    icon: WorkspacesIcon,
};

export {
    SessionResourceProps,
    SessionCreate,
};
