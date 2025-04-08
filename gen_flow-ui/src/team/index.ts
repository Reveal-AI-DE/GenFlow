// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import { ResourceProps } from 'react-admin';
import PeopleOutlineIcon from '@mui/icons-material/PeopleOutline';

import { TeamMenuItem } from '@/team/show';

const TeamResourceProps: ResourceProps = {
    name: 'teams',
    icon: PeopleOutlineIcon,
};

export {
    TeamResourceProps,
    TeamMenuItem,
};
