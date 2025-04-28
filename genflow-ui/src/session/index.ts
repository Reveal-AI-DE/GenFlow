// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import { ResourceProps } from 'react-admin';
import WorkspacesIcon from '@mui/icons-material/Workspaces';

import { SessionCreate } from '@/session/form';
import { SessionList } from '@/session/list';
import { SessionCard, SessionShow, SessionUsageCard } from '@/session/show';

const SessionResourceProps: ResourceProps = {
    name: 'sessions',
    list: SessionList,
    show: SessionShow,
    create: SessionCreate,
    icon: WorkspacesIcon,
};

export {
    SessionResourceProps,
    SessionCreate,
    SessionCard,
    SessionUsageCard,
};
