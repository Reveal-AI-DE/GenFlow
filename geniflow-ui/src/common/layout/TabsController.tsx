// Copyright (C) 2025 Reveal AI
//
// Licensed under the Apache License, Version 2.0 with Additional Commercial Terms.

import React, {
    FC, useState, ReactNode,
} from 'react';
import Box from '@mui/material/Box';
import Tabs, { TabsProps } from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import { styled } from '@mui/material/styles';

export interface TabItems {
    [key: string]: ReactNode;
}

const TabPanelContainer = styled(Box, {
    name: 'GFTabPanel',
    slot: 'root',
})(() => ({
    width: '100%',
    height: '700px',
    overflow: 'scroll',
}));

interface TabPanelProps {
    children?: ReactNode;
    index: number;
    value: number;
}

const TabPanel: FC<TabPanelProps> = (props) => {
    const {
        children, value, index, ...rest
    } = props;

    return (
        <TabPanelContainer
            role='tabpanel'
            hidden={value !== index}
            id={`tabpanel-${index}`}
            aria-labelledby={`tab-${index}`}
            {...rest}
        >
            {value === index && children}
        </TabPanelContainer>
    );
};

function a11yProps(index: number): object {
    return {
        id: `tab-${index}`,
        'aria-controls': `tabpanel-${index}`,
    };
};

interface TabsContainerProps {
    orientation: TabsProps['orientation'];
}

const Root = styled(Box, {
    name: 'GFTabsController',
    slot: 'root',
})<{ ownerState: TabsContainerProps }>(({ ownerState }) => (
    ownerState.orientation === 'vertical' ? {
        display: 'flex',
        flexGrow: 1,
    } : {
        width: '100%',
    }
));

const TabsContainer = styled(Box, {
    name: 'GFTabsController',
    slot: 'tabs',
})<{ ownerState: TabsContainerProps }>(({ ownerState, theme }) => ({
    borderBottom: 1,
    borderColor: 'divider',
    marginBottom: ownerState.orientation === 'vertical' ? theme.spacing(0) : theme.spacing(2),
}));

interface TabsControllerProps extends TabsProps {
    tabLabels: string[];
    children: ReactNode | ReactNode[];
}

const TabsController: FC<TabsControllerProps> = ({
    tabLabels, children, orientation, ...rest
}) => {
    const [value, setValue] = useState(0);

    const handleChange = (event: React.SyntheticEvent, newValue: number): void => {
        event.stopPropagation();
        setValue(newValue);
    };

    return (
        <Root ownerState={{ orientation }}>
            <TabsContainer ownerState={{ orientation }}>
                <Tabs
                    value={value}
                    onChange={handleChange}
                    aria-label='controlled tabs'
                    orientation={orientation}
                    {...rest}
                >

                    {
                        tabLabels.map((label, index) => (
                            <Tab
                                key={index}
                                label={label}
                                {...a11yProps(index)}
                            />
                        ))
                    }
                </Tabs>
            </TabsContainer>
            {
                Array.isArray(children) ? (
                    children.map((child, index) => (
                        <TabPanel key={index} value={value} index={index}>
                            {child}
                        </TabPanel>
                    ))
                ) : (
                    <TabPanel value={value} index={0}>
                        {children}
                    </TabPanel>
                )
            }
        </Root>
    );
};

export default TabsController;
