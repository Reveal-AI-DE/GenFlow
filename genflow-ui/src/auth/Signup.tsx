// Copyright (C) 2025 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, {
    FC, HtmlHTMLAttributes, ReactNode,
    useRef, useEffect,
} from 'react';
import { styled, SxProps } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import Avatar from '@mui/material/Avatar';
import LockIcon from '@mui/icons-material/Lock';

import { RegistrationForm as DefaultRegistrationForm } from '@/auth/form';
import { LoginButton } from '@/auth/button';

const PREFIX = 'GFSignup';
const SignupClasses = {
    card: `${PREFIX}-card`,
    avatar: `${PREFIX}-avatar`,
    icon: `${PREFIX}-icon`,
};

const Root = styled('div', {
    name: PREFIX,
    slot: 'root',
})(({ theme }) => ({
    display: 'flex',
    flexDirection: 'column',
    minHeight: '100vh',
    height: '1px',
    alignItems: 'center',
    justifyContent: 'flex-start',
    backgroundRepeat: 'no-repeat',
    backgroundSize: 'cover',
    backgroundImage:
        'radial-gradient(circle at 50% 14em, #313264 0%, #00023b 60%, #00023b 100%)',
    [`& .${SignupClasses.card}`]: {
        minWidth: 400,
        marginTop: '6em',
    },
    [`& .${SignupClasses.avatar}`]: {
        margin: '1em',
        display: 'flex',
        justifyContent: 'center',
    },
    [`& .${SignupClasses.icon}`]: {
        backgroundColor: theme.palette.secondary.main,
    },
}));

const Footer = styled(Box,{
    name: 'GFLogin',
    slot: 'toolbar',
})(({ theme }) => ({
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    margin: theme.spacing(1, 2),
}));

const defaultRegistrationForm = <DefaultRegistrationForm />;

const defaultAvatarIcon = <LockIcon />;

export interface SignupProps extends HtmlHTMLAttributes<HTMLDivElement> {
    avatarIcon?: ReactNode;
    backgroundImage?: string;
    children?: ReactNode;
    className?: string;
    sx?: SxProps;
};

const Signup: FC<SignupProps> = ({
    children = defaultRegistrationForm,
    backgroundImage,
    avatarIcon = defaultAvatarIcon,
    ...rest
}) => {
    const containerRef = useRef<HTMLDivElement>(null);
    let backgroundImageLoaded = false;

    const updateBackgroundImage = (): void => {
        if (!backgroundImageLoaded && containerRef.current) {
            containerRef.current.style.backgroundImage = `url(${backgroundImage})`;
            backgroundImageLoaded = true;
        }
    };

    // Load background image asynchronously to speed up time to interactive
    const lazyLoadBackgroundImage = (): void => {
        if (backgroundImage) {
            const img = new Image();
            img.onload = updateBackgroundImage;
            img.src = backgroundImage;
        }
    };

    useEffect(() => {
        if (!backgroundImageLoaded) {
            lazyLoadBackgroundImage();
        }
    });

    return (
        <Root {...rest} ref={containerRef}>
            <Card className={SignupClasses.card}>
                <div className={SignupClasses.avatar}>
                    <Avatar className={SignupClasses.icon}>{avatarIcon}</Avatar>
                </div>
                {children}
                <Footer>
                    <LoginButton />
                </Footer>
            </Card>
        </Root>
    );
};

export default Signup;
