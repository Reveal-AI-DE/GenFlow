// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

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
    showWelcome: boolean;
};

export const GlobalContext = createContext<GlobalContextInterface>({
    aboutSystem: undefined,
    currentMembership: undefined,
    currentTeam: undefined,
    switchTeam: () => {},
    showWelcome: false,
});
