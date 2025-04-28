// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

const globalConfig = require('../.eslintrc.cjs');
const { join } = require('path');

module.exports = {
    parserOptions: {
        project: './tsconfig.json',
        tsconfigRootDir: __dirname,
    },
    ignorePatterns: [
        'craco.config.js',
        '.eslintrc.cjs',
        'tailwind.config.js',
        'node_modules/**',
        'build/**',
    ],
    extends: ['airbnb', 'airbnb-typescript'],
    rules: {
        ...globalConfig.rules, // need to import rules again because they've been redefined by 'airbnb-typescript'

        'jsx-a11y/control-has-associated-label': 0, // new rule, conflicts with existing code
        'react/no-unused-class-component-methods': 0, // new rule, gives often false positives
        'react/no-unstable-nested-components': 0, // new rule, we have a lot of code conflicting with this
        'react/no-did-update-set-state': 0, // https://github.com/airbnb/javascript/issues/1875
        'react/require-default-props': 'off',
        'react/no-unused-prop-types': 'off',
        'react/no-array-index-key': 'off',
        'react/jsx-props-no-spreading': 0,
        'jsx-quotes': ['error', 'prefer-single'],
        'react/static-property-placement': ['warn', 'static public field'],
        'react/function-component-definition': [2, { 'namedComponents': ['arrow-function', 'function-expression' ] }],
        'import/no-extraneous-dependencies': [
            'error',
            {
                packageDir: [__dirname, join(__dirname, '../')]
            },
        ],
    },
};