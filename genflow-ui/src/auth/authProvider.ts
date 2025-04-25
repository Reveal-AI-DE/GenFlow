// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import { AuthProvider, fetchUtils, UserIdentity } from 'react-admin';

import { RegistrationFormData } from '@/auth/form';
import { ResourceURL, getCsrfToken } from '@/utils';

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

export const createOptions = (url: string): FetchJsonOptions => {
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
    fetchUtils.fetchJson(url, Object.assign(createOptions(url), options))
);

export const getLoggedInUser = async (): Promise<UserIdentity> => {
    const url = ResourceURL('/users/self');
    const { json } = await fetchJsonWithAuthToken(url);

    return {
        ...json,
        fullName: `${json.first_name} ${json.last_name}`,
    };
};

const authProvider: AuthProvider = {
    login: async ({ email, username, password }) => {
        const url = ResourceURL(`${process.env.REACT_APP_BACKEND_AUTH_URL}/login`);
        const data = username ? { username } : { email };
        const {
            status,
            statusText,
            json
        } = await fetchJsonWithAuthToken(url, {
            method: 'POST',
            body: JSON.stringify({ ...data, password }),
        });
        if (status === 200) {
            const { key } = json;
            localStorage.setItem('token', key);
            return;
        }
        throw new Error(statusText);
    },
    logout: async () => {
        removeItems();
    },
    checkAuth: async () => {
        if (!localStorage.getItem('token')) {
            throw new Error();
        }
    },
    checkError: async ({ status }) => {
        if (status === 401) {
            throw new Error();
        }
    },
    getIdentity: async () => {
        let userObjString = localStorage.getItem('RaStoreGenFlow.identity');
        userObjString = userObjString === null ? '' : userObjString;
        if (userObjString) {
            return JSON.parse(userObjString);
        }
        const user = await getLoggedInUser();
        localStorage.setItem('RaStoreGenFlow.identity', JSON.stringify(user));
        return user;
    },
    register: async (params: RegistrationFormData) => {
        const url = ResourceURL(`${process.env.REACT_APP_BACKEND_AUTH_URL}/register`);
        const { json } = await fetchJsonWithAuthToken(url, {
            method: 'POST',
            body: JSON.stringify(params),
        });
        return json;
    },
};

export default authProvider;
