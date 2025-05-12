// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

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
