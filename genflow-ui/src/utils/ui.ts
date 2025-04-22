// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import { useTheme, useMediaQuery } from '@mui/material';

export const useColsForWidth = (): number => {
    const theme = useTheme();
    const sm = useMediaQuery(theme.breakpoints.up('sm'));
    const md = useMediaQuery(theme.breakpoints.up('md'));
    const lg = useMediaQuery(theme.breakpoints.up('lg'));
    const xl = useMediaQuery(theme.breakpoints.up('xl'));
    // there are all dividers of 24, to have full rows on each page
    if (xl) return 4;
    if (lg) return 3;
    if (md) return 2;
    if (sm) return 1;
    return 1;
};

export const times = (nbChildren: number, fn: (key: number) => any): any => (
    Array.from({ length: nbChildren }, (_, key) => fn(key))
);

export const getCsrfToken = (): string | null => {
    const csrfCookie = document.cookie
        .split('; ')
        .find((row) => row.startsWith('csrftoken='));
    return csrfCookie ? csrfCookie.split('=')[1] : null;
};
