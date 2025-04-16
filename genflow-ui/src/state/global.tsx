// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, {
    useState, FC, useEffect, ReactNode, useMemo
} from 'react';
import { useAuthState, useRefresh } from 'react-admin';

import { dataProvider } from '@/dataProvider';
import {
    AboutSystem, Membership, Team, Identity,
} from '@/types';
import { GlobalContext } from '@/context';

interface GlobalStateProps {
    children: ReactNode,
};

export const GlobalState: FC<GlobalStateProps> = ({ children }) => {
    const { authenticated } = useAuthState();
    const refresh = useRefresh();

    const [aboutSystem, setAboutSystem] = useState<AboutSystem | undefined>(undefined);
    const [currentMembership, setCurrentMembership] = useState<Membership | undefined>(undefined);
    const [currentTeam, setCurrentTeam] = useState<Team | undefined>(undefined);
    const [currentUser, setCurrentUser] = useState<any>({});

    const switchTeam = async (user: Identity, team: Team): Promise<void> => {
        setCurrentTeam(team);
        localStorage.setItem('team', team.id.toString());
        const { data: memberships } = await dataProvider.getList('memberships', { pagination: { page: 1, perPage: -1 }});
        setCurrentMembership(memberships.find((obj: Membership) => obj.user.id === user.id));
        refresh();
    }

    const fetchStartingData = async (): Promise<void> => {
        const { data: teams } = await dataProvider.getList('teams', { pagination: { page: 1, perPage: -1 } });

        const { user } = await dataProvider.self('users');
        setCurrentUser(user);

        const { data: about } = await dataProvider.getAbout('system', {});
        setAboutSystem(about);

        const savedTeamId = localStorage.getItem('team');
        const team = savedTeamId ? teams.find((obj: Team) => obj.id.toString() === savedTeamId) || teams[0] : teams[0];
        if (team) {
            setCurrentTeam(team);
            localStorage.setItem('team', team.id.toString());
            await switchTeam(user, team);
        }
    };

    useEffect(() => {
        (async () => {
            if (!authenticated) return;
            await fetchStartingData();
        })();
    }, [authenticated]);

    const contextValue = useMemo(() => ({
        aboutSystem,
        currentMembership,
        currentTeam,
        currentUser,
        switchTeam,
    }), [aboutSystem, currentMembership, currentTeam, currentUser]);

    return (
        <GlobalContext.Provider
            value={contextValue}
        >
            {children}
        </GlobalContext.Provider>
    );
};
