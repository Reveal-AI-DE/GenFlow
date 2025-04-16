// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import { AuthProvider, fetchUtils, UserIdentity } from 'react-admin';

import { ResourceURL } from '@/utils';

const removeItems = (): void => {
    localStorage.removeItem('token');
};

interface FetchJsonOptions {
    user?: {
        authenticated: boolean;
        token: string;
    };
    headers?: Headers;
}

export const createOptions = (url: string): FetchJsonOptions => {
    const token = localStorage.getItem('token');

    if (!token) {
        return {};
    }

    const headers = new Headers({
        Accept: 'application/vnd.genflow+json; version=1.0',
    });

    // parse url for team query parameters
    const urlParams = new URLSearchParams(url.split('?')[1]);
    const teamId = urlParams.get('team');
    if (!teamId && !url.includes('/teams')) {
        // add X-Team header
        const currentTeamId = localStorage.getItem('team');
        if (currentTeamId) {
            headers.set('X-Team', currentTeamId);
        }
    }

    return {
        user: {
            authenticated: true,
            token: `Token ${token}`,
        },
        headers: headers as Headers,
    };
};

export const fetchJsonWithAuthToken = (url: string, options?: object): Promise<any> => (
    fetchUtils.fetchJson(url, Object.assign(createOptions(url), options))
);

const authProvider: AuthProvider = {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    login: async ({ username, password }) => {
        const url = ResourceURL(process.env.REACT_APP_BACKEND_AUTH_URL);
        const request = new Request(url, {
            method: 'POST',
            body: JSON.stringify({ username, password }),
            headers: new Headers({ 'Content-Type': 'application/json' }),
        });
        const response = await fetch(request);
        if (response.ok) {
            const { key } = await response.json();
            localStorage.setItem('token', key);
            return;
        }
        if (response.headers.get('content-type') !== 'application/json') {
            throw new Error(response.statusText);
        }

        const json = await response.json();
        const error = json.non_field_errors;
        throw new Error(error || response.statusText);
    },
    logout: () => {
        removeItems();
        return Promise.resolve();
    },
    checkAuth: () => (localStorage.getItem('token') ? Promise.resolve() : Promise.reject()),
    checkError: ({ status }) => {
        if (status === 401 || status === 403) {
            removeItems();
            return Promise.reject();
        }
        return Promise.resolve();
    },
    getIdentity: () => {
        let userObjString = localStorage.getItem('RaStore.identity');
        userObjString = userObjString === null ? '' : userObjString;

        if (userObjString) {
            const { first_name: firstName, last_name: lastName, user } = JSON.parse(userObjString);
            const fullName = `${firstName} ${lastName}`;

            const identity: UserIdentity = {
                id: user,
                fullName: (fullName !== ' ') ? fullName : user,
            };
            return Promise.resolve(identity);
        }
        return Promise.resolve({ id: '' });
    },
    getPermissions: () => Promise.resolve(),
};

export default authProvider;
