// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import { RaThemeOptions } from 'react-admin';

/** Just for fun */

export const chiptuneTheme: RaThemeOptions = {
    palette: {
        mode: 'dark' as const,
        primary: {
            main: '#0f0',
        },
        background: {
            default: '#111111',
            paper: '#212121',
        },
    },
    typography: {
        fontFamily: '\'Pixelify Sans\', cursive',
    },
    components: {
        MuiAutocomplete: { defaultProps: { fullWidth: true } },
        MuiFormControl: { defaultProps: { fullWidth: true } },
        MuiTextField: { defaultProps: { fullWidth: true } },
        RaSimpleFormIterator: { defaultProps: { fullWidth: true } },
    },
};
