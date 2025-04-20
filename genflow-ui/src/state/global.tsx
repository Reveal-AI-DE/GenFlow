// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, {
    useState, FC, useEffect, ReactNode, useMemo
} from 'react';
import {
    UserIdentity, useGetIdentity, useRefresh, Loading,
    useLogout, useAuthenticated, Identifier, useNotify,
} from 'react-admin';

import { dataProvider } from '@/dataProvider';
import {
    AboutSystem, Membership, Team,
} from '@/types';
import { GlobalContext } from '@/context';

interface GlobalStateProps {
    children: ReactNode,
};

export const GlobalState: FC<GlobalStateProps> = ({ children }) => {
    const { authenticated } = useAuthenticated();
    const { data: currentUser, error: getIdentityError } = useGetIdentity();

    const logout = useLogout();
    const refresh = useRefresh();
    const notify = useNotify();

    const [loading, setLoading] = useState<boolean>(true);
    const [aboutSystem, setAboutSystem] = useState<AboutSystem | undefined>(undefined);
    const [currentMembership, setCurrentMembership] = useState<Membership | undefined>(undefined);
    const [currentTeam, setCurrentTeam] = useState<Team | undefined>(undefined);

    const getTeamIdFromLocalStorage = (): Identifier | null => (
        localStorage.getItem('team')
    );

    const setTeamIdFromLocalStorage = (team: Team): void => (
        localStorage.setItem('team', team.id.toString())
    );

    const switchTeam = async (team: Team, user: UserIdentity): Promise<void> => {
        setCurrentTeam(team);
        localStorage.setItem('team', team.id.toString());
        const { data: memberships } = await dataProvider.getList('memberships', { pagination: { page: 1, perPage: -1 }});
        setCurrentMembership(memberships.find((obj: Membership) => obj.user.id === user.id));
        refresh();
    };

    const loadSavedTeam = async (teamId: Identifier): Promise<boolean> => (
        dataProvider.getOne('teams', {id: teamId })
            .then(({ data: team }) => {
                setCurrentTeam(team);
                setTeamIdFromLocalStorage(team);
                return true;
            }
            ).catch(() => (false))
    );

    const loadDefaultTeam = async (user: UserIdentity): Promise<boolean> => {
        const { data: teams } = await dataProvider.getList('teams', { pagination: { page: 1, perPage: -1 } });

        // Check if the user has any teams
        if (!teams || teams.length === 0) {
            notify('message.no_teams', { type: 'error'});
            logout();
            return false;
        }

        // Currently, we are just taking the first team
        // TODO: add default team selector
        const team = teams[0];
        setCurrentTeam(team);
        setTeamIdFromLocalStorage(team);
        await switchTeam(team, user);
        return true;
    }

    const setupUserTeam = async (user: UserIdentity): Promise<boolean> => {
        const storedTeamId = getTeamIdFromLocalStorage();

        // try loading the saved team
        let teamLoaded = false;
        if (storedTeamId) {
            teamLoaded = await loadSavedTeam(storedTeamId);
        }

        // if it fails, load the default team
        if (!teamLoaded) {
            teamLoaded = await loadDefaultTeam(user);
        }
        return teamLoaded;
    };

    const fetchStartingData = async (): Promise<void> => {
        const { data: about } = await dataProvider.getAbout('system', {});
        setAboutSystem(about);
    };

    useEffect(() => {
        (async () => {
            // Check if the user is authenticated
            if (!authenticated) return;

            if (getIdentityError) logout();
            if (!currentUser) return;

            if (await setupUserTeam(currentUser)) {
                await fetchStartingData();
                setLoading(false);
            }
        })();
    }, [currentUser]);

    const contextValue = useMemo(() => ({
        aboutSystem,
        currentMembership,
        currentTeam,
        switchTeam,
    }), [aboutSystem, currentMembership, currentTeam]);

    return (
        <GlobalContext.Provider
            value={contextValue}
        >
            {
                loading ? (
                    <Loading />
                ) : (
                    children
                )
            }
        </GlobalContext.Provider>
    );
};
