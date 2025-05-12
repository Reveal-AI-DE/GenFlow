// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import {
    RaThemeOptions,
    defaultLightTheme,
    defaultDarkTheme,
    nanoDarkTheme,
    nanoLightTheme,
    radiantDarkTheme,
    radiantLightTheme,
    houseDarkTheme,
    houseLightTheme,
    bwLightTheme,
    bwDarkTheme,
} from 'react-admin';

import { softDarkTheme, softLightTheme } from './softTheme';
import { chiptuneTheme } from './chiptuneTheme';

export type ThemeName =
    | 'soft'
    | 'B&W'
    | 'default'
    | 'nano'
    | 'radiant'
    | 'house'
    | 'chiptune';

export interface Theme {
    name: ThemeName;
    light: RaThemeOptions;
    dark?: RaThemeOptions;
}

const BW_SIDEBAR_OVERRIDE = {
    styleOverrides: {
        root: {
            '& .SubMenu .MuiMenuItem-root': {
                paddingLeft: 24,
            },
            '& .RaMenu-closed .SubMenu .MuiMenuItem-root': {
                paddingLeft: 8,
            },
        },
    },
};

const TABS_OVERRIDE = {
    styleOverrides: {
        root: {
            height: 'auto',
        },
    },
};

const HOUSE_TAB_OVERRIDE = {
    styleOverrides: {
        root: {
            '&.Mui-selected, &.Mui-selected:hover': {
                color: 'inherit',
            }
        },
    },
};

export const themes: Theme[] = [
    { name: 'soft', light: softLightTheme, dark: softDarkTheme },
    { name: 'default', light: defaultLightTheme, dark: defaultDarkTheme },
    {
        name: 'B&W',
        light: {
            ...bwLightTheme,
            components: {
                ...bwLightTheme.components,
                RaSidebar: BW_SIDEBAR_OVERRIDE,
                MuiTabs: TABS_OVERRIDE,
            },
        },
        dark: {
            ...bwDarkTheme,
            components: {
                ...bwDarkTheme.components,
                RaSidebar: BW_SIDEBAR_OVERRIDE,
                MuiTabs: TABS_OVERRIDE,
            },
        },
    },
    { name: 'nano', light: nanoLightTheme, dark: nanoDarkTheme },
    { name: 'radiant', light: radiantLightTheme, dark: radiantDarkTheme },
    {
        name: 'house',
        light: {
            ...houseLightTheme,
            components: {
                ...houseLightTheme.components,
                MuiTab: HOUSE_TAB_OVERRIDE,
                MuiTabs: TABS_OVERRIDE,
            },
        },
        dark: {
            ...houseDarkTheme,
            components: {
                ...houseDarkTheme.components,
                MuiTabs: TABS_OVERRIDE,
            },
        },
    },
    { name: 'chiptune', light: chiptuneTheme },
];
