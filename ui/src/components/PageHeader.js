import React from "react";
import AppBar from '@mui/material/AppBar';
import {Toolbar} from '@mui/material';
import Typography from '@mui/material/Typography';
import CssBaseline from '@mui/material/CssBaseline';

const PageHeader = () => {
    return (
        <React.Fragment>
            <CssBaseline />
            <AppBar position="static" color="primary">
                <Toolbar>
                    <Typography variant='h6' color='inherit' noWrap>
                        MapAider
                    </Typography>
                </Toolbar>
            </AppBar>
        </React.Fragment>
    )
}

export default PageHeader
