import React from 'react';
import { createStyles, makeStyles, Theme } from '@material-ui/core/styles';

const useStyles = makeStyles((theme: Theme) => 
  createStyles({
    root: {
      backgroundColor: theme.palette.primary.light,
      height: '100vh',
    },
  })
);

export const App: React.FC = () => {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      hello world
    </div>
  );
};
