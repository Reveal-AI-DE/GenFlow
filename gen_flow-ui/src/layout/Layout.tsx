// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React from 'react';
import { Layout as RALayout, LayoutProps } from 'react-admin';

import { GlobalState } from '@/state';
import AppBar from '@/layout/AppBar';

const Layout = (props: LayoutProps): JSX.Element => (
    <GlobalState>
        <RALayout {...props} appBar={AppBar} />
    </GlobalState>
);

export default Layout;
