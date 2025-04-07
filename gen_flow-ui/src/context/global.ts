// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import { createContext } from 'react';

import {
    AboutSystem
} from '@/types';

export interface GlobalContextInterface {
    aboutSystem: AboutSystem | undefined;
};

export const GlobalContext = createContext<GlobalContextInterface>({
    aboutSystem: undefined,
});
