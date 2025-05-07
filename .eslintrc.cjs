// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

module.exports = {
    root: true,
    env: {
        node: true,
        browser: true,
        es2020: true,
    },
    parserOptions: {
        sourceType: 'module',
        parser: '@typescript-eslint/parser',
    },
    ignorePatterns: [
        '.eslintrc.cjs',
        'lint-staged.config.js',
        '.*/',
        'node_modules/',
        'build/',
        'data/',
        'keys/',
        'logs/',
        'statics/',
        'templates/',
        'site/themes/**'
    ],
    plugins: ['@typescript-eslint', 'security', 'no-unsanitized', 'import'],
    extends: [
        'eslint:recommended', 'plugin:security/recommended-legacy', 'plugin:no-unsanitized/recommended-legacy',
        'airbnb-base', 'plugin:import/errors', 'plugin:import/warnings',
        'plugin:import/typescript', 'plugin:@typescript-eslint/recommended', 'airbnb-typescript/base',
    ],
    rules: {
        'no-plusplus': 0,
        'no-continue': 0,
        'no-console': 0,
        'no-param-reassign': ['error', { 'props': false }],
        'no-restricted-syntax': [0, { selector: 'ForOfStatement' }],
        'no-await-in-loop': 0,
        'indent': ['error', 4, { 'SwitchCase': 1 }],
        'max-len': ['error', { code: 120, ignoreStrings: true }],
        'func-names': 0,
        'valid-typeof': 0,
        'no-useless-constructor': 0, // sometimes constructor is necessary to generate right documentation
        'quotes': ['error', 'single', { 'avoidEscape': true }],
        'lines-between-class-members': 0,
        'class-methods-use-this': 0,
        'no-underscore-dangle': ['error', { allowAfterThis: true }],
        'max-classes-per-file': 0,
        'operator-linebreak': ['error', 'after'],
        'newline-per-chained-call': 0,
        'global-require': 0,
        'arrow-parens': ['error', 'always'],
        'security/detect-object-injection': 0, // the rule is relevant for user input data on the node.js environment
        'import/order': ['error', { 'groups': ['builtin', 'external', 'internal'] }],
        'import/prefer-default-export': 0, // works incorrect with interfaces

        'react/jsx-indent-props': 0, // new rule, breaks current styling
        'react/jsx-indent': 0, // new rule, conflicts with eslint@typescript-eslint/indent eslint@indent, breaks current styling
        'function-paren-newline': 0, // new rule, breaks current styling
        '@typescript-eslint/default-param-last': 0, // does not really work with redux reducers
        '@typescript-eslint/ban-ts-comment': 0,
        '@typescript-eslint/no-explicit-any': 0,
        '@typescript-eslint/indent': ['error', 4],
        '@typescript-eslint/lines-between-class-members': 0,
        '@typescript-eslint/explicit-function-return-type': ['warn', { allowExpressions: true }],
        '@typescript-eslint/explicit-module-boundary-types': 'off',
        '@typescript-eslint/ban-types': [
            'error',
            {
                types: {
                    '{}': false, // TODO: try to fix with Record<string, unknown>
                    object: false, // TODO: try to fix with Record<string, unknown>
                    Function: false, // TODO: try to fix somehow
                },
            },
        ],

        'import/extensions': [
            2,
            {
                'js': 'never',
                'mjs': 'never',
                'jsx': 'never',
                'ts': 'never',
                'tsx': 'never'
            }
        ],

        // deprecated rules
        '@typescript-eslint/indent': 'off',
        '@typescript-eslint/ban-types': 'off',
        '@typescript-eslint/brace-style': 'off',
        '@typescript-eslint/comma-dangle': 'off',
        '@typescript-eslint/comma-spacing': 'off',
        '@typescript-eslint/func-call-spacing': 'off',
        '@typescript-eslint/keyword-spacing': 'off',
        '@typescript-eslint/no-extra-semi': 'off',
        '@typescript-eslint/space-before-blocks': 'off',
        '@typescript-eslint/no-throw-literal': 'off',
        '@typescript-eslint/quotes': 'off',
        '@typescript-eslint/semi': 'off',
        '@typescript-eslint/space-before-function-paren': 'off',
        '@typescript-eslint/space-infix-ops': 'off',
        '@typescript-eslint/object-curly-spacing': 'off',
    },
};
