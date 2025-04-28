// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

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
