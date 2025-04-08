// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import { createContext } from 'react';

import {
    AboutSystem, Identity, Team, Membership,
} from '@/types';

export interface GlobalContextInterface {
    aboutSystem: AboutSystem | undefined;
    currentMembership: Membership | undefined;
    currentTeam: Team | undefined;
    currentUser: Identity | undefined;
    switchTeam: (user: Identity, team: Team) => void;
};

export const GlobalContext = createContext<GlobalContextInterface>({
    aboutSystem: undefined,
    currentMembership: undefined,
    currentTeam: undefined,
    currentUser: undefined,
    switchTeam: () => {},
});
