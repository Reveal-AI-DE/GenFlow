// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import { ResourceProps } from 'react-admin';
import BadgeIcon from '@mui/icons-material/Badge';

import { MembershipList } from '@/team/membership/list';

const MembershipResourceProps: ResourceProps = {
    name: 'memberships',
    icon: BadgeIcon,
};

export {
    MembershipResourceProps,
    MembershipList,
};
