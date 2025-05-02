// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import { fetchUtils } from 'react-admin';

export const ResourceURL = (path: string | undefined, base = process.env.REACT_APP_BACKEND_API_BASE_URL): string => {
    if (path === undefined) return '';
    const parts = [base];
    parts.push(path.replace(/^\//, ''));
    return parts.join('/');
};

export const MediaURL = (path: string | undefined, base = process.env.REACT_APP_BACKEND_BASE_URL): string => (
    ResourceURL(path, base)
);

const getCsrfToken = (): string | null => {
    const csrfCookie = document.cookie
        .split('; ')
        .find((row) => row.startsWith('csrftoken='));
    return csrfCookie ? csrfCookie.split('=')[1] : null;
};

const addTeamHeader = (url: string, headers: Headers): void => {
    // parse url for team query parameters
    const urlParams = new URLSearchParams(url.split('?')[1]);
    const teamId = urlParams.get('team');
    if (!teamId && !url.includes('/teams') && !url.includes('/users/self')) {
        // add X-Team header
        const currentTeamId = localStorage.getItem('team');
        if (currentTeamId) {
            headers.set('X-Team', currentTeamId);
        }
    }
};

export const createFetchOptions = (url: string): fetchUtils.Options => {
    const token = localStorage.getItem('token');

    const headers = new Headers({
        Accept: 'application/vnd.genflow+json; version=1.0',
    });

    // Add the CSRF token to the headers
    const csrfToken = getCsrfToken();
    if (csrfToken) {
        headers.set('X-CSRFToken', csrfToken);
    }

    if (!token) {
        return {
            headers: headers as Headers,
        };
    }

    addTeamHeader(url, headers);

    return {
        user: {
            authenticated: true,
            token: `Token ${token}`,
        },
        headers: headers as Headers,
    };
};

export const fetchJsonWithAuthToken = (url: string, options?: object): Promise<any> => (
    fetchUtils.fetchJson(url, Object.assign(createFetchOptions(url), options))
);
