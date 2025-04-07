// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, {
    useState, FC, useEffect, ReactNode, useMemo
} from 'react';
import { useAuthState } from 'react-admin';

import { dataProvider } from '@/dataProvider';
import {
    AboutSystem,
} from '@/types';
import { GlobalContext } from '@/context';

interface GlobalStateProps {
    children: ReactNode,
};

export const GlobalState: FC<GlobalStateProps> = ({ children }) => {
    const { authenticated } = useAuthState();

    const [aboutSystem, setAboutSystem] = useState<AboutSystem | undefined>(undefined);

    const fetchStartingData = async (): Promise<void> => {
        const { data: about } = await dataProvider.getAbout('system', {});
        setAboutSystem(about);
    };

    useEffect(() => {
        (async () => {
            if (!authenticated) return;
            await fetchStartingData();
        })();
    }, [authenticated]);

    const contextValue = useMemo(() => ({
        aboutSystem,
    }), []);

    return (
        <GlobalContext.Provider
            value={contextValue}
        >
            {children}
        </GlobalContext.Provider>
    );
};
