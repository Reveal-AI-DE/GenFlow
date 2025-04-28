// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React from 'react';
import {
    Admin, useStore, localStorageStore,
    StoreContextProvider, Resource, CustomRoutes,
} from 'react-admin';
import polyglotI18nProvider from 'ra-i18n-polyglot';

import { dataProvider } from '@/dataProvider';
import { authProvider, Login } from '@/auth';
import englishMessages from '@/i18n/en_US';

import { Layout } from '@/layout';
import { Dashboard } from '@/dashboard';
import { themes, Theme, ThemeName } from '@/themes';

// Resources
import { AssistantGroupResourceProps, AssistantResourceProps } from '@/assistant';
import { CollectionResourceProps } from '@/collection';
import { FileResourceProps } from '@/file';
import { InvitationResourceProps } from '@/team/invitation';
import { MembershipResourceProps } from '@/team/membership';
import { MessageResourceProps } from '@/message';
import { ModelResourceProps } from '@/provider/model';
import { PromptGroupResourceProps, PromptResourceProps } from '@/prompt';
import { ProviderResourceProps } from '@/provider';
import { TeamResourceProps } from '@/team';
import { SessionResourceProps } from '@/session';

// Custom routes
import { layoutCustomRoutes, noLayoutCustomRoutes } from '@/customRoutes';

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
            theme={lightTheme}
            darkTheme={darkTheme}
            defaultTheme='light'
            dataProvider={dataProvider}
            authProvider={authProvider}
            loginPage={Login}
            dashboard={Dashboard}
            requireAuth
            disableTelemetry
        >
            <Resource
                {...AssistantGroupResourceProps}
            />
            <Resource
                {...AssistantResourceProps}
            />
            <Resource
                {...CollectionResourceProps}
            />
            <Resource
                {...FileResourceProps}
            />
            <Resource
                {...InvitationResourceProps}
            />
            <Resource
                {...MembershipResourceProps}
            />
            <Resource
                {...MessageResourceProps}
            />
            <Resource
                {...ModelResourceProps}
            />
            <Resource
                {...PromptGroupResourceProps}
            />
            <Resource
                {...PromptResourceProps}
            />
            <Resource
                {...ProviderResourceProps}
            />
            <Resource
                {...SessionResourceProps}
            />
            <Resource
                {...TeamResourceProps}
            />
            <CustomRoutes>
                {layoutCustomRoutes}
            </CustomRoutes>
            <CustomRoutes noLayout>
                {noLayoutCustomRoutes}
            </CustomRoutes>
        </Admin>
    );
};

const AppWrapper = (): JSX.Element => (
    <StoreContextProvider value={store}>
        <App />
    </StoreContextProvider>
);

export default AppWrapper;
