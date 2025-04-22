// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import { createContext } from 'react';
import { UserIdentity } from 'react-admin';

import {
    AboutSystem, Team, Membership,
} from '@/types';

export interface GlobalContextInterface {
    aboutSystem: AboutSystem | undefined;
    currentMembership: Membership | undefined;
    currentTeam: Team | undefined;
    switchTeam: (team: Team, user: UserIdentity) => void;
};

export const GlobalContext = createContext<GlobalContextInterface>({
    aboutSystem: undefined,
    currentMembership: undefined,
    currentTeam: undefined,
    switchTeam: () => {},
});
