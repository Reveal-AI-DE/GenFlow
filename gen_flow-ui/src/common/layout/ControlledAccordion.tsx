// Copyright (C) 2024 Reveal AI
//
// SPDX-License-Identifier: MIT

import React, {
    FC, useState, ReactNode, SyntheticEvent
} from 'react';
import Accordion from '@mui/material/Accordion';
import AccordionDetails from '@mui/material/AccordionDetails';
import AccordionSummary from '@mui/material/AccordionSummary';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { styled } from '@mui/material/styles';

export const StyledDialog = styled(Typography, {
    name: 'GFDialog',
    slot: 'root',
})(({ theme }) => ({
    '& .MuiDialogContent-root': {
        padding: theme.spacing(2),
    },
    '& .MuiDialogActions-root': {
        padding: theme.spacing(1),
    },
}));

interface ControlledAccordionProps {
    children: ReactNode | ReactNode[];
    titles: string[];
}

const ControlledAccordion: FC<ControlledAccordionProps> = ({ children, titles}) => {
    const [expanded, setExpanded] = useState<string | false>(false);

    const handleChange = (panel: string) => (event: SyntheticEvent, isExpanded: boolean) => {
        setExpanded(isExpanded ? panel : false);
    };

    return children && (
        <>
            {
                titles.map((title, index) => {
                    const panel = `panel-${index}`;
                    return (
                        <Accordion
                            key={panel}
                            expanded={expanded === panel}
                            onChange={handleChange(panel)}
                        >
                            <AccordionSummary
                                expandIcon={<ExpandMoreIcon />}
                                aria-controls={`${panel}-content`}
                                id={`${panel}-header`}
                            >
                                <Typography sx={{ width: '33%', flexShrink: 0 }}>
                                    {title}
                                </Typography>
                            </AccordionSummary>
                            <AccordionDetails>
                                {Array.isArray(children) ? children[index] : children}
                            </AccordionDetails>
                        </Accordion>
                    )
                })
            }
        </>
    );
};

export default ControlledAccordion;
