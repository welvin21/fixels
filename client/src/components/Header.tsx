import React from 'react';
import { createStyles, makeStyles, Theme } from '@material-ui/core/styles';
import { AppBar, Box, Toolbar, Typography } from '@material-ui/core';

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    root: {
      width: '100%',
      flexGrow: 1,
      backgroundColor: theme.palette.primary.main,
      padding: theme.spacing(1),
    },
    toolbar: {
      display: 'flex',
      flexDirection: 'row',
      justifyContent: 'space-between',
    },
    title: {
      color: '#fff',
      textDecoration: 'none',
      '&:hover': {
        cursor: 'pointer',
      },
    },
  })
);

export const Header: React.FC = () => {
  const classes = useStyles();

  return (
    <AppBar position="static" className={classes.root}>
      <Toolbar className={classes.toolbar}>
        <Box onClick={() => window.location.reload()} className={classes.title}>
          <Typography variant="h4">Fixels</Typography>
        </Box>
      </Toolbar>
    </AppBar>
  );
};
