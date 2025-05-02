// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, { FC } from 'react';
import IconButton from '@mui/material/IconButton';
import GoogleIcon from '@mui/icons-material/Google';
import { useGoogleLogin } from '@react-oauth/google';
import { useTranslate } from 'react-admin';

import { WithTooltip } from '@/common';
import { ResourceURL } from '@/utils';

type GoogleLoginButtonProps = object;

const GoogleLoginButton: FC<GoogleLoginButtonProps> = () => {
    const translate = useTranslate();
    const googleLogin = useGoogleLogin({
        flow: 'auth-code',
        onSuccess: async (codeResponse) => {
            const data = {
                code: codeResponse.code,
            };
            try {
                const url = ResourceURL(process.env.REACT_APP_BACKEND_GOOGLE_AUTH_URL);
                const request = new Request(url, {
                    method: 'POST',
                    body: JSON.stringify(data),
                    headers: new Headers({ 'Content-Type': 'application/json' }),
                });
                const response = await fetch(request);
                console.log('response', response);
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
            } catch (error) {
                console.error(error);
            }
        },
        onError: (errorResponse) => console.log(errorResponse),
    });

    return (
        <WithTooltip
            title={translate('action.google_login')}
            trigger={(
                <span>
                    <IconButton
                        edge='start'
                        aria-label={translate('action.google_login')}
                        onClick={() => googleLogin()}
                        size='small'
                        color='primary'
                    >
                        <GoogleIcon
                            fontSize='medium'
                            sx={{
                                color: '#e74133',
                            }}
                        />
                    </IconButton>
                </span>
            )}
            arrow
        />
    );
};

export default GoogleLoginButton;
