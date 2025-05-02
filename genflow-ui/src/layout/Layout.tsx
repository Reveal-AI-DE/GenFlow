// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React from 'react';
import { Layout as RALayout, LayoutProps } from 'react-admin';

import { GlobalState } from '@/state';
import AppBar from '@/layout/AppBar';
import Menu from '@/layout/Menu';

const Layout = (props: LayoutProps): JSX.Element => (
    <GlobalState
        disableTelemetry={process.env.REACT_APP_TELEMETRY_DISABLED === 'true'}
    >
        <RALayout
            {...props}
            menu={Menu}
            appBar={AppBar}
        />
    </GlobalState>
);

export default Layout;
