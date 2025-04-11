// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import { ResourceProps } from 'react-admin';
import PeopleOutlineIcon from '@mui/icons-material/PeopleOutline';

import { TeamList } from '@/team/list';
import { TeamMenuItem } from '@/team/show';

const TeamResourceProps: ResourceProps = {
    name: 'teams',
    list: TeamList,
    icon: PeopleOutlineIcon,
};

export {
    TeamResourceProps,
    TeamMenuItem,
};
