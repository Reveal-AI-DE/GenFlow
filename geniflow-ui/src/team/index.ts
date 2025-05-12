// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

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
