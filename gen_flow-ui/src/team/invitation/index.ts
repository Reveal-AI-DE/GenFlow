// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import { ResourceProps } from 'react-admin';
import BadgeIcon from '@mui/icons-material/Badge';

import { InvitationCreateButton } from '@/team/invitation/form';

const InvitationResourceProps: ResourceProps = {
    name: 'invitations',
    icon: BadgeIcon,
};

export {
    InvitationResourceProps,
    InvitationCreateButton,
};
