// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, {
    ElementType,
    FocusEvent,
    forwardRef,
    HTMLAttributes,
    KeyboardEvent,
    MouseEvent,
    ReactNode,
    RefAttributes,
    useImperativeHandle,
    useRef,
    useState,
    Ref,
} from 'react';
import Box from '@mui/material/Box';
import Menu, { MenuProps as MuiMenuProps } from '@mui/material/Menu';
import { MenuItemProps as MuiMenuItemProps } from '@mui/material/MenuItem';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';

import IconMenuItem from '@/common/menu/IconMenuItem';

export type NestedMenuItemProps = Omit<MuiMenuItemProps, 'button'> & {
    // parentMenuOpen: boolean;
    component?: ElementType;
    label?: string;
    rightIcon?: ReactNode;
    leftIcon?: ReactNode;
    children?: ReactNode;
    className?: string;
    tabIndex?: number;
    disabled?: boolean;
    ContainerProps?: HTMLAttributes<HTMLElement> & RefAttributes<HTMLElement | null>;
    MenuProps?: Partial<Omit<MuiMenuProps, 'children'>>;
    button?: true | undefined;
    delay?: number;
};

const NestedMenuItem = forwardRef<HTMLLIElement | null, NestedMenuItemProps>((
    props,
    ref
) => {
    const {
        // parentMenuOpen,
        label,
        rightIcon = <ChevronRightIcon />,
        leftIcon = null,
        children,
        className,
        tabIndex: tabIndexProp,
        ContainerProps: ContainerPropsProp = {},
        MenuProps,
        delay = 0,
        onClick,
        ...rest
    } = props;

    const { ref: containerRefProp, ...ContainerProps } = ContainerPropsProp;

    const menuItemRef = useRef<HTMLLIElement | null>(null);
    useImperativeHandle(ref, () => menuItemRef.current!);

    const containerRef = useRef<HTMLDivElement | null>(null);
    useImperativeHandle(containerRefProp as Ref<HTMLElement | null>, () => containerRef.current);

    const menuContainerRef = useRef<HTMLDivElement | null>(null);

    const timeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

    const [isSubMenuOpen, setIsSubMenuOpen] = useState(false);

    const handleMouseEnter = (e: MouseEvent<HTMLElement>): void => {
        timeoutRef.current = setTimeout(() => {
            if (!props.disabled) {
                setIsSubMenuOpen(true);
            }

            if (ContainerProps.onMouseEnter) {
                ContainerProps.onMouseEnter(e);
            }
        }, delay);
    };

    const handleMouseLeave = (e: MouseEvent<HTMLElement>): void => {
        if (timeoutRef.current) {
            clearTimeout(timeoutRef.current);
        }

        setIsSubMenuOpen(false);

        if (ContainerProps.onMouseLeave) {
            ContainerProps.onMouseLeave(e);
        }
    };

    // Check if any immediate children are active
    const isSubmenuFocused = (): boolean => {
        const active = containerRef.current?.ownerDocument.activeElement ?? null;
        if(menuContainerRef.current == null) {
            return false;
        }
        for (const child of menuContainerRef.current.children) {
            if (child === active) {
                return true;
            }
        }

        return false;
    };

    const handleFocus = (e: FocusEvent<HTMLElement>): void => {
        if (e.target === containerRef.current && !props.disabled) {
            setIsSubMenuOpen(true);
        }

        if (ContainerProps.onFocus) {
            ContainerProps.onFocus(e);
        }
    };

    const handleKeyDown = (e: KeyboardEvent): void => {
        if (e.key === 'Escape') {
            return;
        }

        if (isSubmenuFocused()) {
            e.stopPropagation();
        }

        const active = containerRef.current?.ownerDocument.activeElement;

        if (e.key === 'ArrowLeft' && isSubmenuFocused()) {
            containerRef.current?.focus();
        }

        if (e.key === 'ArrowRight' && e.target === containerRef.current && e.target === active) {
            const firstChild = menuContainerRef.current?.children[0] as HTMLDivElement;
            firstChild?.focus();
        }
    };

    const open = isSubMenuOpen;

    // Root element must have a `tabIndex` attribute for keyboard navigation
    let tabIndex;
    if (!props.disabled) {
        tabIndex = tabIndexProp !== undefined ? tabIndexProp : -1;
    }

    return (
        <Box
            {...ContainerProps}
            ref={containerRef}
            onFocus={handleFocus}
            tabIndex={tabIndex}
            onMouseEnter={handleMouseEnter}
            onMouseLeave={handleMouseLeave}
            onKeyDown={handleKeyDown}
        >
            <IconMenuItem
                className={className}
                label={label}
                leftIcon={leftIcon}
                ref={menuItemRef}
                rightIcon={rightIcon}
                onClick={(event: any) => {
                    if (onClick) {
                        onClick(event);
                    }
                }}
                {...rest}
            />

            <Menu
                // Set pointer events to 'none' to prevent the invisible Popover div
                // from capturing events for clicks and hovers
                style={{ pointerEvents: 'none' }}
                anchorEl={menuItemRef.current}
                anchorOrigin={{
                    horizontal: 'left',
                    vertical: 'top',
                }}
                transformOrigin={{
                    horizontal: 'right',
                    vertical: 'top',
                }}
                open={open}
                autoFocus={false}
                disableAutoFocus
                disableEnforceFocus
                onClose={() => {
                    setIsSubMenuOpen(false);
                }}
                {...MenuProps}
            >
                <Box ref={menuContainerRef} style={{ pointerEvents: 'auto' }}>
                    {children}
                </Box>
            </Menu>
        </Box>
    );
});

NestedMenuItem.displayName = 'NestedMenuItem';
export default NestedMenuItem;
