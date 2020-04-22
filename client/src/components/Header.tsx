import React from 'react';
import { Link } from 'react-router-dom';
import { createStyles, makeStyles, Theme } from '@material-ui/core/styles';
import {
  AppBar,
  Toolbar,
  Typography,
} from '@material-ui/core';

const useStyles = makeStyles((theme: Theme) => 
  createStyles({
    root: {
      width: '100%',
      flexGrow: 1,
      backgroundColor: theme.palette.primary.main,
      padding: theme.spacing(1)
    },
    toolbar: {
      display: 'flex',
      flexDirection: 'row',
      justifyContent: 'space-between'
    },
    title: {
      color: '#fff',
      textDecoration: 'none'
    }
  })
);

export const Header: React.FC = () => {
  const classes = useStyles();

  return (
    <AppBar position="static" className={classes.root}>
      <Toolbar className={classes.toolbar}>
        <Link to='/demo' className={classes.title}>
          <Typography variant="h4">DeepEye</Typography>
        </Link>
      </Toolbar>
    </AppBar>
  );
};
