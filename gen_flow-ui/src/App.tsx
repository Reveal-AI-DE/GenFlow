// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React from 'react';
import {
    Admin, useStore, localStorageStore,
    StoreContextProvider,
} from 'react-admin';
import polyglotI18nProvider from 'ra-i18n-polyglot';

import { dataProvider } from '@/dataProvider';
import authProvider from '@/authProvider';
import englishMessages from '@/i18n/en_US';

import { Layout } from '@/layout';
import { themes, Theme, ThemeName } from '@/themes';

const i18nProvider = polyglotI18nProvider(
    (locale: string) => {
        if (locale === 'de_DE') {
            return import('@/i18n/de_DE').then((messages) => messages.default);
        }

        // Always fallback on english
        return englishMessages;
    },
    'en_US',
    [
        { locale: 'en_US', name: 'English' },
        { locale: 'de_DE', name: 'Deutsche' },
    ],
);

const store = localStorageStore(undefined, 'GenFlow');

const App = (): JSX.Element => {
    const [themeName] = useStore<ThemeName>('themeName', 'soft');
    const lightTheme = themes.find((theme: Theme) => theme.name === themeName)?.light;
    const darkTheme = themes.find((theme: Theme) => theme.name === themeName)?.dark;

    return (
        <Admin
            store={store}
            i18nProvider={i18nProvider}
            layout={Layout}
            lightTheme={lightTheme}
            darkTheme={darkTheme}
            defaultTheme='light'
            dataProvider={dataProvider}
            authProvider={authProvider}
            disableTelemetry
        />
    );
};

const AppWrapper = (): JSX.Element => (
    <StoreContextProvider value={store}>
        <App />
    </StoreContextProvider>
);

export default AppWrapper;
