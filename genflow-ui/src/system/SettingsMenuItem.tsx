// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC, useContext } from 'react';
import SettingsIcon from '@mui/icons-material/Settings';
import { useTranslate, RecordContextProvider } from 'react-admin';

import { GlobalContext, GlobalContextInterface } from '@/context';
import { TeamRole } from '@/types';
import { MenuItemWithDialog, TabsController, TabItems } from '@/common';
import { ProviderList } from '@/provider';
import { MembershipList } from '@/team/membership';
import { Account } from '@/user';

const SettingsMenuItem: FC = () => {
    const translate = useTranslate();
    const { currentMembership, currentTeam } = useContext<GlobalContextInterface>(GlobalContext);
    const tabItems: TabItems = {};

    if (currentMembership && (currentMembership.role === TeamRole.OWNER || currentMembership.role === TeamRole.ADMIN)) {
        tabItems[translate('resources.providers.name', {smart_count: 2})] = <ProviderList key='ai_providers' />;
    }

    if (
        currentMembership && (currentMembership.role === TeamRole.OWNER ||
    currentMembership.role === TeamRole.ADMIN) &&
        currentTeam && !currentTeam.is_personal
    ) {
        tabItems[translate('label.members')] = (
            <RecordContextProvider value={currentTeam}>
                <MembershipList key='members' />
            </RecordContextProvider>
        );
    }

    tabItems[translate('label.account')] = (
        <Account key='account' />
    );

    return (
        <MenuItemWithDialog
            id='settings-menu-item'
            LeftIcon={<SettingsIcon />}
            label='label.settings'
            dialog={{
                id: 'settings-dialog',
                maxWidth: 'md',
                fullWidth: true,
                'aria-labelledby': translate('label.settings'),
                title: translate('label.settings'),
                disableBackdropClick: true,
                ContentProps: {
                    id: 'settings-dialog-content',
                    dividers: true,
                },
                dialogContent: (
                    <TabsController
                        tabLabels={Object.keys(tabItems)}
                        orientation='vertical'
                    >
                        {
                            Object.values(tabItems)
                        }
                    </TabsController>
                ),
            }}
        />
    );
};

export default SettingsMenuItem;
