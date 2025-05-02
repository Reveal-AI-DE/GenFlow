// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, {
    useState, FC, useEffect, ReactNode, useMemo
} from 'react';
import {
    UserIdentity, useGetIdentity, useRefresh, Loading,
    useLogout, useAuthenticated, Identifier, useNotify, HttpError,
} from 'react-admin';

import { authProvider } from '@/auth';
import { dataProvider } from '@/dataProvider';
import {
    AboutSystem, Membership, Team, GetAboutResult,
} from '@/types';
import { GlobalContext } from '@/context';
import { WelcomeMessage } from '@/system';

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
    const [showWelcome, setShowWelcome] = useState<boolean>(true);

    const getTeamIdFromLocalStorage = (): Identifier | null => (
        localStorage.getItem('team')
    );

    const setTeamIdInLocalStorage = (team: Team): void => (
        localStorage.setItem('team', team.id.toString())
    );

    const setShowWelcomeFromLocalStorage = (): void => {
        const value = localStorage.getItem('showWelcome');
        if (value === null) {
            localStorage.setItem('showWelcome', 'true');
            setShowWelcome(true);
            return;
        }
        setShowWelcome(value === 'true');
    }

    const switchTeam = async (team: Team, user: UserIdentity): Promise<void> => {
        setCurrentTeam(team);
        localStorage.setItem('team', team.id.toString());
        const { data: memberships } = await dataProvider.getList('memberships', { pagination: { page: 1, perPage: -1 }});
        setCurrentMembership(memberships.find((obj: Membership) => obj.user.id === user.id));
        refresh();
    };

    const handleError = async (error: HttpError): Promise<void> => {
        if (error.status) {
            try {
                await authProvider.checkError(error);
            } catch {
                logout();
            }
        }
    };

    const loadSavedTeam = async (teamId: Identifier, user: UserIdentity): Promise<boolean> => (
        dataProvider.getOne('teams', {id: teamId })
            .then(async ({ data: team }) => {
                setCurrentTeam(team);
                setTeamIdInLocalStorage(team);
                await switchTeam(team, user);
                return true;
            }).catch(async (error) => {
                handleError(error)
                return false;
            })
    );

    const loadDefaultTeam = async (user: UserIdentity): Promise<boolean> => (
        dataProvider.getList('teams', { pagination: { page: 1, perPage: -1 } })
            .then(async ({ data: teams }) => {
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
                setTeamIdInLocalStorage(team);
                await switchTeam(team, user);
                return true;
            }).catch(async (error) => {
                handleError(error)
                return false;
            })
    );

    const setupUserTeam = async (user: UserIdentity): Promise<boolean> => {
        const storedTeamId = getTeamIdFromLocalStorage();

        // try loading the saved team
        let teamLoaded = false;
        if (storedTeamId) {
            teamLoaded = await loadSavedTeam(storedTeamId, user);
        }

        // if it fails, load the default team
        if (!teamLoaded) {
            return loadDefaultTeam(user);
        }
        return teamLoaded;
    };

    const fetchStartingData = async (): Promise<void> => (
        dataProvider.getAbout('system', {})
            .then(({ data }: GetAboutResult) => {
                setAboutSystem(data);
            }).catch(async (error: HttpError) => {
                handleError(error);
            })
    );

    useEffect(() => {
        (async () => {
            // Check if the user is authenticated
            if (!authenticated) return;

            if (getIdentityError) logout();
            if (!currentUser) return;

            if (await setupUserTeam(currentUser)) {
                await fetchStartingData();
            }
            setShowWelcomeFromLocalStorage();
            setLoading(false);
        })();
    }, [currentUser]);

    const contextValue = useMemo(() => ({
        aboutSystem,
        currentMembership,
        currentTeam,
        switchTeam,
        showWelcome,
    }), [aboutSystem, currentMembership, currentTeam]);

    return (
        <GlobalContext.Provider
            value={contextValue}
        >
            {
                loading ? (
                    <Loading timeout={100} />
                ) : (
                    <>
                        {children}
                        {aboutSystem && showWelcome && (
                            <WelcomeMessage
                                open={showWelcome}
                                onClose={() => {
                                    setShowWelcome(false);
                                }}
                            />
                        )}
                    </>
                )
            }
        </GlobalContext.Provider>
    );
};
