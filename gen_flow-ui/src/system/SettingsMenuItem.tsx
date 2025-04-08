// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, { FC, useContext } from 'react';
import SettingsIcon from '@mui/icons-material/Settings';
import { useTranslate } from 'react-admin'; // RecordContextProvider

import { GlobalContext, GlobalContextInterface } from '@/context';
import { TeamRole } from '@/types';
import { MenuItemWithDialog, TabsController, TabItems } from '@/common';
import { ProviderList } from '@/provider';
// import { MembershipList } from '@/team/membership';

const SettingsMenuItem: FC = () => {
    const translate = useTranslate();
    const { currentMembership } = useContext<GlobalContextInterface>(GlobalContext); // currentTeam
    const tabItems: TabItems = {};

    if (currentMembership && (currentMembership.role === TeamRole.OWNER || currentMembership.role === TeamRole.ADMIN)) {
        tabItems[translate('resources.providers.name', {smart_count: 2})] = <ProviderList key='model_providers' />;
    }

    // if (
    //     currentMembership && (currentMembership.role === TeamRole.OWNER ||
    // currentMembership.role === TeamRole.ADMIN) &&
    //     currentTeam && !currentTeam.is_personal
    // ) {
    //     tabItems['label.members'] = (
    //         <RecordContextProvider value={currentTeam}>
    //             <MembershipList key='members' />
    //         </RecordContextProvider>
    //     );
    // }

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
