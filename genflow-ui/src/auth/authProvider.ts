// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import {
    AuthProvider,
} from 'react-admin';

import { getLoggedInUser } from '@/user';
import { ResourceURL, MediaURL, fetchJsonWithAuthToken } from '@/utils';

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
        localStorage.removeItem('token');
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
            const user = JSON.parse(userObjString);
            if (user.avatar) {
                user.avatar = MediaURL(user.avatar);
            }
            return user;
        }
        const user = await getLoggedInUser();
        localStorage.setItem('RaStoreGenFlow.identity', JSON.stringify(user));
        return user;
    },
};

export default authProvider;
